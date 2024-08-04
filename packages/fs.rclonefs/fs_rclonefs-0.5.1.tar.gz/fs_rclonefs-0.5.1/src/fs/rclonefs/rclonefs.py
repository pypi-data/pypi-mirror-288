from fs.base import FS
from fs.info import Info
from fs.permissions import Permissions
from fs.enums import ResourceType
from fs.errors import DirectoryExists, ResourceNotFound, DirectoryNotEmpty
from fs.errors import DirectoryExpected, RemoveRootError
from fs.errors import FileExpected
from fs.path import split, normpath
from datetime import datetime
import json
from typing import List, Union, Optional
from fs.tempfs import TempFS

if __name__ == '__main__':
    from rclone import Rclone
    from file import RcloneFile
else:
    from .rclone import Rclone
    from .file import RcloneFile
    
class RcloneFS(FS):
    def __init__(self, remote: str, rclone: Optional[Rclone] = None, config_file: Optional[str] = None):
        super().__init__()
        self.remote = remote.rstrip(':')
        if rclone is None:
            self.rclone = Rclone(config_file=config_file)
        else:
            self.rclone = rclone
            if config_file:
                self.rclone.set_config_file(config_file)
        self.temp_fs = TempFS()

    def close(self):
        super().close()
        self.temp_fs.close()

    def _path(self, path: str) -> str:
        return f"{self.remote}:{normpath(path).lstrip('/')}"
    

    def getinfo(self, path: str, namespaces=None) -> Info:
        path = normpath(path)
        if path == '/':
            return self._root_info(namespaces)
        
        parent_dir, name = split(path)
        try:
            parent_path = self._path(parent_dir)
            files = self.rclone.list_files(parent_path)
            for file_info in files:
                if file_info['Name'] == name:
                    return self._make_info(path, file_info, namespaces)
            raise ResourceNotFound(path)
        except Exception as e:
            raise ResourceNotFound(path)

    def _root_info(self, namespaces=None) -> Info:
        try:
            # Attempt to get remote info
            remote_info = self.rclone.get_remote_info(self.remote+':')
            
            raw_info = {
                "basic": {
                    "name": "",
                    "is_dir": True
                }
            }

            if namespaces and 'details' in namespaces:
                raw_info["details"] = {
                    "type": int(ResourceType.directory),
                    "size": remote_info.get('total', 0),  # Total space if available
                    "used": remote_info.get('used', 0),  # Used space if available
                    "free": remote_info.get('free', 0),  # Free space if available
                }
            
            
                if 'modified' in remote_info:
                    raw_info['details']['modified'] = self._parse_time(remote_info['modified'])

            return Info(raw_info)
        except Exception:
            # If we can't get remote info, return minimal info
            return Info({
                "basic": {
                    "name": "",
                    "is_dir": True
                }
            })

    def _make_info(self, path: str, file_info: dict, namespaces: Optional[list]=None) -> Info:
        raw_info = {
            "basic": {
                "name": file_info['Name'],
                "is_dir": file_info['IsDir']
            }
        }

        if namespaces and 'details' in namespaces:
            raw_info["details"] = {
                "type": int(ResourceType.directory) if file_info['IsDir'] else int(ResourceType.file),
                "size": file_info['Size'],
                "modified": self._parse_time(file_info['ModTime'])
            }
        
            if 'Mode' in file_info:
                raw_info['access'] = {
                    "permissions": Permissions(mode=int(file_info['Mode'], 8)).dump()
                }

        if namespaces and 'rclone' in namespaces:
            raw_info["rclone"] = file_info
                        
        if namespaces and 'storage' in namespaces:

            if file_info['IsDir']:
                cumulative_size = self._calculate_dir_size(path)
            else:
                cumulative_size = file_info['Size']
            
            if 'storage' not in raw_info:
                raw_info['storage'] = {}
            raw_info['storage']['size'] = cumulative_size
        
        return Info(raw_info)

    def _calculate_dir_size(self, dir_path: str) -> int:
        cumulative_size = 0
        try:
            files = self.rclone.list_files(self._path(dir_path),
                                           flags=['--recursive',
                                                  '--files-only'
                                                 ])
            for file_info in files:
                cumulative_size += file_info.get('Size', 0)
        except Exception:
            # If there's an error, we'll just return 0 as the size
            raise
        return cumulative_size
    
    def _parse_time(self, time_str: str) -> datetime:
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",  # Dropbox format
            "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 with microseconds
            "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 with timezone
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                # Convert to UTC if timezone-aware
                if dt.tzinfo is not None:
                    dt = dt.astimezone(timezone.utc)
                return dt.timestamp()
            except ValueError:
                continue
        raise ValueError(f"Time '{time_str}' doesn't match any known format")

    def listdir(self, path: str) -> List[str]:
        path = normpath(path)
        try:
            files = self.rclone.list_files(self._path(path))
            return [file['Name'] for file in files]
        except Exception as e:
            raise ResourceNotFound(path)

    def makedir(self, path: str, permissions=None, recreate=False):
        path = normpath(path)
        try:
            self.rclone.mkdir(self._path(path))
        except Exception as e:
            if not recreate:
                raise DirectoryExists(path)

    def remove(self, path: str):
        path = normpath(path)
        if self.isdir(path):
            raise FileExpected(path)
        try:
            self.rclone.deletefile(self._path(path))
        except Exception as e:
            if 'not found' in str(e):
                raise ResourceNotFound(path)
            raise

    def removedir(self, path: str):
        path = normpath(path)
        if path == '/':
            raise RemoveRootError(path)
        try:
            self.rclone.rmdir(self._path(path))
        except Exception as e:
            msg = str(e)
            if 'directory not empty' in msg:
                raise DirectoryNotEmpty(path)
            if 'directory not found' in msg:
                raise ResourceNotFound(path)
            if 'not a directory' in msg:
                raise DirectoryExpected(path)
            # fallback
            raise

    def removetree(self, path: str):
        path = normpath(path)
        if not self.exists(path):
            raise ResourceNotFound(path)
        if not self.isdir(path):
            raise DirectoryExpected(path)
        try:
            self.rclone.purge(self._path(path))
        except Exception as e:
            msg = str(e)
            if 'not found' in msg:
                raise ResourceNotFound(path)
            # fallback
            raise

    def setinfo(self, path: str, info):
        path = normpath(path)
        # RClone doesn't provide a direct way to set file info
        # You might need to implement this differently based on your needs
        # raise NotImplementedError("setinfo is not implemented for RcloneFS")
        pass
        # not implemented with rclone
    
    def openbin(self, path: str, mode="r", buffering=-1, **options):
        path = normpath(path)
        # return self.temp_fs.openbin(path, mode, buffering, **options)
        return RcloneFile(self, path, mode)

    def upload(self, path: str, file, chunk_size=None, **options):
        path = normpath(path)
        parent_dir, name = split(path)
        local_path = str(file.name, encoding='utf-8')

        if not parent_dir == '' and not self.exists(parent_dir):
            raise ResourceNotFound(parent_dir)

        self.rclone.copyto(local_path, self._path(path))
        

    def download(self, path: str, file, chunk_size=None, **options):
        path = normpath(path)
        local_path = file.name
        self.rclone.copyto(self._path(path), str(local_path, encoding='utf-8'))
        