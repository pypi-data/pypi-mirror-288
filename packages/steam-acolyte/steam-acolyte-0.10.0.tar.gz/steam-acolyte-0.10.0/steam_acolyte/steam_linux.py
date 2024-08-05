from .util import (
    read_file, write_file, join_args, subkey_lookup, Tracer,
    realpath, find_exe, samefile,
)

import vdf
from PyQt5.QtCore import QThread, pyqtSignal

import fcntl
import os
from time import sleep
import logging


trace = Tracer(__name__)

# I tested this script on an ubuntu and archlinux machine, where I found
# the steam config and program files in different locations. In both cases
# there was also a path/symlink that pointed to the correct location:
#
#             common name           ubuntu            archlinux
#   config    ~/.steam/steam@   ->  ~/.steam/steam    ~/.local/share/Steam
#   data      ~/.steam/root@    ->  ~/.steam          ~/.local/share/Steam
CONFIGS = {
    'DEFAULT': {
        'exe': 'steam',
        'prefix': '~/.steam',
        'root': '~/.steam/steam',
    },
    'NATIVE': {
        'exe': 'steam-native',
        'prefix': '~/.steam',
        'root': '~/.steam/steam',
    },
    'FLATPACK': {
        'exe': 'com.valvesoftware.Steam',
        'prefix': '~/.var/app/com.valvesoftware.Steam/.steam',
        'root': '~/.var/app/com.valvesoftware.Steam/steam',
    },
}


class SteamLinux:

    """Linux specific methods for the interaction with steam. This implements
    the SteamBase interface and is used as a mixin for Steam."""

    def __init__(self, prefix=None, root=None, exe=None):
        super().__init__()
        self.prefix = realpath(prefix or self.find_prefix(root, exe))
        self.root = realpath(root or self.find_root(self.prefix))
        self.exe = find_exe(exe or self.find_exe(self.prefix))
        self.steam_config = os.path.join(self.root, 'config')
        self.acolyte_data = os.path.join(self.root, 'acolyte')
        self.reg_file = os.path.join(self.prefix, 'registry.vdf')
        self.pid_file = os.path.join(self.prefix, 'steam.pid')
        self.pipe_file = os.path.join(self.prefix, 'steam.pipe')
        if not self.exe:
            raise RuntimeError(
                "Unable to find steam executable! If your steam installation "
                "is feeling special, verify that you have passed '--exe' "
                "correctly!")

    @classmethod
    def find_prefix(cls, root, exe):
        if root:
            logging.getLogger(__name__).warning(
                "Please pass '--prefix' in addition to, or instead of, "
                "'--root'. There is no reliable way to determine PREFIX from "
                "ROOT.")
            # Try anyway…
            root = os.path.expanduser(root)
            prefixes = [
                # <prefix>/steam@ -> <root>
                os.path.normpath(os.path.join(root, '..')),
                # <prefix>/steam = <root>
                os.path.realpath(os.path.join(root, '..')),
                # <prefix>/steam@ -> <root> = <prefix>/../.local/share/Steam
                os.path.normpath(os.path.join(root, '../../../.steam')),
            ]
            for prefix in prefixes:
                if cls._prefix_exists(prefix):
                    return prefix

        elif exe:
            exe = find_exe(exe)
            for cfg in CONFIGS.values():
                if samefile(exe, find_exe(cfg['exe'])):
                    prefix = os.path.expanduser(cfg['prefix'])
                    if cls._prefix_exists(prefix):
                        return prefix

        else:
            for cfg in CONFIGS.values():
                exe = find_exe(cfg['exe'])
                if exe:
                    prefix = os.path.expanduser(cfg['prefix'])
                    if cls._prefix_exists(prefix):
                        return prefix

        raise RuntimeError(
            "Unable to find steam user path! Please pass --prefix pointing "
            "to the folder containing the registry.vdf file.")

    @classmethod
    def _prefix_exists(cls, prefix):
        return os.path.exists(os.path.join(prefix, 'registry.vdf'))

    @classmethod
    def find_root(cls, prefix):
        root = os.path.join(prefix, 'steam')
        conf = os.path.join(root, 'config', 'config.vdf')
        if not os.path.isfile(conf):
            raise RuntimeError("""Unable to find steam user path!""")
        return root

    @classmethod
    def find_exe(cls, prefix):
        if not prefix:
            raise RuntimeError("Unable to find steam user path!")

        for cfg in CONFIGS.values():
            if samefile(prefix, cfg['prefix']):
                exe = find_exe(cfg['exe'])
                if exe:
                    return exe

        # TODO: we could also check <prefix>/bin/steam

        raise RuntimeError("Unable to find steam executable!")

    def get_last_user(self):
        reg_data = vdf.loads(read_file(self.reg_file))
        steam_config = subkey_lookup(
            reg_data, r'Registry\HKCU\Software\Valve\Steam')
        return steam_config.get('AutoLoginUser', '')

    @trace.method
    def set_last_user(self, username):
        reg_data = vdf.loads(read_file(self.reg_file))
        steam_config = subkey_lookup(
            reg_data, r'Registry\HKCU\Software\Valve\Steam')
        steam_config['AutoLoginUser'] = username
        steam_config['RememberPassword'] = '1'
        reg_data = vdf.dumps(reg_data, pretty=True)
        with open(self.reg_file, 'wt') as f:
            f.write(reg_data)

    def _is_steam_pid_valid(self):
        """Check if the steam.pid file designates a running process."""
        return is_process_running(self._read_steam_pid())

    def _read_steam_pid(self):
        pidfile = os.path.expanduser(self.pid_file)
        pidtext = read_file(pidfile)
        if not pidtext:
            return False
        return int(pidtext)

    @trace.method
    def _set_steam_pid(self):
        pidfile = os.path.expanduser(self.pid_file)
        pidtext = str(os.getpid())
        write_file(pidfile, pidtext)

    @trace.method
    def _unset_steam_pid(self):
        pidfile = os.path.expanduser(self.pid_file)
        write_file(pidfile, '')

    _lock_fd = -1
    _pipe_fd = -1
    _thread = None

    @trace.method
    def _connect(self):
        self._pipe_fd = self._open_pipe_for_writing(self.pipe_file)
        return self._pipe_fd != -1

    @trace.method
    def _listen(self):
        self._has_steam_lock = True
        self._pipe_fd = self._open_pipe_for_reading(self.pipe_file)
        self._thread = FileReaderThread(self._pipe_fd)
        self._thread.line_received.connect(self.command_received.emit)
        self._thread.start()
        return True

    @trace.method
    def _send(self, args):
        text = join_args(args) + '\n'
        os.write(self._pipe_fd, text.encode('utf-8'))

    @trace.method
    def unlock(self):
        if self._thread is not None:
            self._thread.stop()
            self._thread = None
        if self._pipe_fd != -1:
            self._unset_steam_pid()
            os.close(self._pipe_fd)
            self._pipe_fd = -1
            self._has_steam_lock = False

    @trace.method
    def ensure_single_acolyte_instance(self):
        """Ensure that we are the only acolyte instance. Return true if we are
        the first instance, false if another acolyte instance is running."""
        if self._lock_fd != -1:
            return True
        pid_file = os.path.join(self.acolyte_data, 'acolyte.lock')
        os.makedirs(os.path.dirname(pid_file), exist_ok=True)
        self._lock_fd = os.open(pid_file, os.O_WRONLY | os.O_CREAT, 0o644)
        try:
            fcntl.lockf(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._has_acolyte_lock = True
            return True
        except IOError:
            self.release_acolyte_instance_lock()
            return False

    @trace.method
    def release_acolyte_instance_lock(self):
        if self._lock_fd != -1:
            os.close(self._lock_fd)
            self._lock_fd = -1
            self._has_acolyte_lock = False

    @trace.method
    def wait_for_steam_exit(self):
        """Wait until steam is closed."""
        # Unfortunately, we have to poll here because we can't os.wait() for
        # non-child processes, and the alternatives using the ptrace, inotifyd
        # or netlink interfaces are much more involved.
        pid = self._read_steam_pid()
        while pid and is_process_running(pid):
            sleep(0.010)

    @trace.method
    def _open_pipe_for_writing(self, name):
        """Open steam.pipe as a writer (client)."""
        mode = os.O_WRONLY | os.O_NONBLOCK
        path = os.path.expanduser(name)
        try:
            return os.open(path, mode)
        except OSError:
            return -1

    @trace.method
    def _open_pipe_for_reading(self, name):
        """Open steam.pipe as a reader (server)."""
        path = os.path.expanduser(name)
        dirname = os.path.dirname(path)
        os.makedirs(dirname, 0o755, exist_ok=True)
        try:
            os.mkfifo(path, 0o644)
        except FileExistsError:
            pass
        # You may think O_RDWR is awkward here, but it seems to be the only
        # way to have a nonblocking open() combined with blocking read()!
        # With mode=O_RDONLY, the open call would block, waiting for a
        # writer. It can be made nonblocking using mode=O_RDONLY|O_NONBLOCK,
        # but then the pipe would be always ready to read, returning empty
        # strings upon read()-ing (even if fcntl()-ing away O_NONBLOCK).
        # See also: https://stackoverflow.com/a/580057/650222.
        # Additionally, this makes it possible for us to send data into the
        # pipe to wake up the reader thread!
        return os.open(path, os.O_RDWR)


class FileReaderThread(QThread):

    """Read a file asynchronously. Emit signal whenever a new line becomes
    available."""

    line_received = pyqtSignal(str)

    def __init__(self, fd):
        super().__init__()
        self._fd = fd
        self._exit = False

    def run(self):
        # `dup()`-ing the file descriptor serves two purposes here:
        # - leave the `self._fd` open when `f` reaches its end of life
        # - allow writing to `self._fd` without blocking from the main thread
        with os.fdopen(os.dup(self._fd)) as f:
            for line in f:
                line = line.rstrip('\n')
                if line:
                    self.line_received.emit(line)
                elif self._exit:
                    return

    def stop(self):
        self._exit = True
        # We have to wake up the reader thread by sending an empty line. I
        # first tried to close the file directly, but it turns out this blocks
        # the main thread and does not wake up the reader thread. Note that
        # this operation would block if we hadn't dup()-ed the file descriptor
        # for the reader thread:
        os.write(self._fd, b"\n")
        self.wait()


def is_process_running(pid):
    """Check if a process with the given PID is currently running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
