import io
import os
import subprocess
from fs.tempfs import TempFS
from fs.errors import ResourceNotFound

class RcloneFile(io.IOBase):
    
    def __init__(self, parentfs, path, mode):
        super().__init__()
        self.parentfs = parentfs
        self.rclone = parentfs.rclone
        self.temp_fs = parentfs.temp_fs
        
        self.path = path
        self.internal_path = f"{os.path.basename(path)}"        
        self.internal_root = f"{self.temp_fs.getsyspath('/')}"
        self.mode = mode

        if self.parentfs.exists(path):
            # here, we should not use the parentfs.download() method
            # becasue that expects an open file object as the second argument.
            # Instead, we'll use the rclone function directly because it will
            # take a system path to our temp location.
            self.rclone.copyto(self.parentfs._path(path), self.temp_fs.getsyspath(self.internal_path))

        # After the file has been downloaded to our temp storage we can open it.
        self.file = self.temp_fs.openbin(self.internal_path, mode)

        self.file.seek(0,os.SEEK_END)
        self.file_length = self.tell()
        self.file.seek(0,os.SEEK_SET)
        self.position = 0

        self._closed = False

    
    def _length(self):
        prev = self.tell()
        self.seek(0, os.SEEK_END)
        end = self.tell()
        self.seek(prev, os.SEEK_SET)
        return end
        
    def read(self, size=-1):
        return self.file.read(size)

    def readable(self):
        return True

    def write(self, data):
        length_written = self.file.write(data)
        if self.tell() > self.file_length:
            self.file_length = self.tell()
        return length_written

    def truncate(self):
        self.file_length = self.tell()
        return self.file.truncate()
        
    def writable(self):
        return True
        
    def seek(self, offset, whence=io.SEEK_SET):
        return self.file.seek(offset, whence)

    def seekable(self):
        return True
        
    def tell(self):
        return self.file.tell()

    def close(self):
        self.flush()
        if self.file and not self._closed:
            self.file.close()
            self._closed = True
            if 'w' in self.mode or '+' in self.mode:
                self._upload()
                
    def _upload(self):
        f = self.temp_fs.openbin(self.path, 'r')
        opened_length = f.seek(0,os.SEEK_END)
        expected_length = self.file_length
        
        self.parentfs.upload(self.path, f)
        f.close()
