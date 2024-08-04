import subprocess
import json
import os

class Rclone:
    def __init__(self, rclone_path="rclone", config_file=None):
        self.rclone_path = rclone_path
        self.config_file = config_file

    def _run_command(self, args, flags=None):
        command = [self.rclone_path]
        if self.config_file:
            command.extend(["--config", self.config_file])
        command.extend(args)
        if flags:
            command.extend(flags)
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"RClone command failed: {result.stderr}")
        return result.stdout

    def list_remotes(self, flags=None):
        return self._run_command(["listremotes"], flags).splitlines()

    def list_files(self, remote_path, flags=None):
        output = self._run_command(["lsjson", remote_path], flags)
        return json.loads(output)

    def copy(self, source, destination, flags=None):
        self._run_command(["copy", source, destination], flags)

    def copyto(self, source, destination, flags=None):
        self._run_command(["copyto", source, destination], flags)

    def move(self, source, destination, flags=None):
        self._run_command(["move", source, destination], flags)

    def sync(self, source, destination, flags=None):
        self._run_command(["sync", source, destination], flags)

    def delete(self, path, flags=None):
        self._run_command(["delete", path], flags)

    def deletefile(self, path, flags=None):
        self._run_command(["deletefile", path], flags)

    def mkdir(self, path, flags=None):
        self._run_command(["mkdir", path], flags)

    def rmdir(self, path, flags=None):
        self._run_command(["rmdir", path], flags)

    def purge(self, path, flags=None):
        self._run_command(["purge", path], flags)

    def check(self, source, destination, flags=None):
        return self._run_command(["check", source, destination], flags)

    def version(self, flags=None):
        return self._run_command(["version"], flags).strip()

    def set_config_file(self, config_file):
        self.config_file = config_file

    def get_config_file(self):
        return self.config_file

    def get_remote_info(self, remote: str, flags=None) -> dict:
        try:
            output = self._run_command(["about", remote, "--json"], flags)
            return json.loads(output)
        except Exception as e:
            return {}