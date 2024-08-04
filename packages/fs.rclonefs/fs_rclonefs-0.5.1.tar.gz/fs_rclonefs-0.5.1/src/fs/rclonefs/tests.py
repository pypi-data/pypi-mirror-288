import unittest

from fs.test import FSTestCases

from rclonefs import RcloneFS

class TestMyFS(FSTestCases, unittest.TestCase):
    
    def make_fs(self):
        return RcloneFS("dropbox:")

    def destroy_fs(self, fs):
        self.fs.close()

