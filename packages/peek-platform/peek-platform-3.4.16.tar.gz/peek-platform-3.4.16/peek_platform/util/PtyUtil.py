import logging
import os
import subprocess
import sys

from typing import Optional

from vortex.DeferUtil import deferToThreadWrapWithLogger

from peek_platform.WindowsPatch import isWindows

logger = logging.getLogger(__name__)


class SpawnOsCommandException(subprocess.CalledProcessError):
    """Spawn OS Command Exception

    This exception is raised when an OS command fails or returns a non-zero exit code

    """

    def __init__(
        self,
        returncode: int,
        cmd: str,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
        message: Optional[str] = None,
    ):
        """Constructor

        :param returncode: The code returned by the process.
        :param cmd: A string representing the command and args executed by bash.
        :param stdout: The output from the process.
        :param stderr: The error from the process.
        :param message: An additional message that can be used to emulate the message
        method of standard exceptions
        """

        subprocess.CalledProcessError.__init__(
            self, returncode, cmd, stdout, stderr
        )
        self.message = message

    def __str__(self):
        return "%s\nCommand '%s' returned non-zero exit status %d" % (
            self.message,
            self.cmd,
            self.returncode,
        )


class PtyOutParser:
    """PTY Out Parser

    The node tools require a tty, so we run it with

        parser = _PtyOutParser()
        import pty
        pty.spawn(\*args, parser.read)

    The only problem being that the output is sent to stdout, to solve this we intercept
    the output, return a . (dot) for every read, which it sends to stdout, and then only log
    the summary at the end of the webpack build.

    """

    def __init__(self, loggingStartMarker=None):
        """Constructor

        :param loggingStartMarker: If this is set, logging will not start until a line
        is starts with this marker.

        """
        self.data = ""
        self.startLogging = (
            False  # Ignore all the stuff before the final summary
        )
        self.allData = ""
        self.loggingStartMarker = loggingStartMarker

    def read(self, fd, size: Optional[int] = 1024):
        data = os.read(fd, size)
        self.data += data.decode(errors="ignore")
        self.allData += data.decode(errors="ignore")
        self.splitData()

        # Silence all the output
        if len(data):
            return b"."

        # If there is no output, return the EOF data
        return data

    def splitData(self):
        lines = self.data.splitlines(True)
        lines.reverse()
        while lines:
            line = lines.pop()
            if not line.endswith(os.linesep):
                self.data = line
                break
            self.logData(line.strip(os.linesep))

    def logData(self, line):
        self.startLogging = self.startLogging or (
            self.loggingStartMarker and line.startswith(self.loggingStartMarker)
        )

        if not (line and self.startLogging):
            return

        logger.debug(line)


def spawnPty(
    cmdAndArgs: str,
    parser: PtyOutParser = PtyOutParser(),
    env: Optional[dict] = None,
) -> None:
    """Spawn PTY

    This function spawns a PTY in Linux and falls back to using subprocess on windows.

    The commands are run via bash on both windows and posix compliant OSs. GitBash is
    recommended for windows.

    :param cmdAndArgs: A string containing the command and arguments to pass to bash.

    :param parser: An instance of c{PtyOutParser} that intercepts the PTY output.

    :returns: None, This either succeeds or raises an exception.

    :raises: c{CalledProcessError}
    """

    # If this is a posix compliant environment, then use pty
    if not isWindows:
        __reallySpawnSubprocess(cmdAndArgs, parser, env=env)
        return

    # Else, use subprocess
    spawnSubprocess(cmdAndArgs, env=env)


def __reallySpawnSubprocess(
    cmdAndArgs: str,
    parser: PtyOutParser = PtyOutParser(),
    env: Optional[dict] = None,
) -> None:
    from peek_platform import PeekPlatformConfig

    bashExec = PeekPlatformConfig.config.bashLocation

    logger.debug("Using interpreter : %s", bashExec)

    path, _, command = cmdAndArgs.partition("&&")
    path = path.strip("cd").strip()
    command = command.strip()

    import pexpect

    bashArgs = ["-l", "-c", command]

    logger.debug(
        f"Running command via pexpect : '{bashExec} {' '.join(bashArgs)}' in"
        f" folder '{path}'"
    )

    child = pexpect.spawn(
        bashExec,
        bashArgs,
        cwd=path,
        env=env,
        maxread=10000,  # a bigger value prints fewer dots
        use_poll=True,  # set to True when your `ulimit` is high
        encoding="utf-8",
    )

    class DotMaskedPtyLogFileWriter:
        def write(self, data):
            print(".", end="")

        def flush(self):
            sys.stdout.flush()

        def close(self):
            print("", flush=True)

    logfile = DotMaskedPtyLogFileWriter()
    child.logfile = logfile
    # alternate to show pty outputs
    # child.logfile = sys.stdout

    child.expect(pexpect.EOF, timeout=None)
    child.wait()
    logfile.close()
    child.close()

    logger.debug(f"subprocess returned status code {child.exitstatus}")
    if child.exitstatus:
        raise SpawnOsCommandException(
            child.exitstatus, cmdAndArgs, stdout="", stderr=parser.allData
        )


def spawnSubprocess(
    cmdAndArgs: str,
    parser: Optional[PtyOutParser] = None,
    env: Optional[dict] = None,
) -> None:
    """Spawn Subprocess

    This method calls an OS command using the subprocess package and bash as the
    interpreter.

    :param cmdAndArgs: A string containing the command and arguments to pass to bash.
    :param parser: The parser for the command output.

    :returns: None, This either succeeds or raises an exception.

    :raises: c{CalledProcessError}

    """
    from peek_platform import PeekPlatformConfig

    bashExec = PeekPlatformConfig.config.bashLocation

    logger.debug("Using interpreter : %s", bashExec)
    logger.debug("Running command via subprocess : %s", cmdAndArgs)

    commandComplete = subprocess.run(
        [cmdAndArgs],
        executable=bashExec,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        env=env,
    )

    if parser:
        parser.read(commandComplete.stdout, size=None)
        parser.read(commandComplete.stderr, size=None)

    if commandComplete.returncode:
        raise SpawnOsCommandException(
            commandComplete.returncode,
            cmdAndArgs,
            stdout=commandComplete.stdout.decode(),
            stderr=commandComplete.stderr.decode(),
        )

    return commandComplete


def logSpawnException(exception: Exception) -> None:
    """Log Exception

    This method logs the stderr / stdout data from an exception to the logger.

    :param exception: The exception to log the data from.
    """

    logger.exception(exception)

    if hasattr(exception, "message"):
        logger.error(exception.message)

    if hasattr(exception, "stderr"):
        [logger.error(l) for l in exception.stderr.splitlines()]

    if hasattr(exception, "stderr"):
        [logger.error(l) for l in exception.stderr.splitlines()]
