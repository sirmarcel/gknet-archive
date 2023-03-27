import pathlib
import shutil


class Tempdir:
    def makedir(self):
        self.tempdir = (
            pathlib.Path(__file__) / ".."
        ).resolve() / f"tmp_{self.__class__.__name__}"
        self.tempdir.mkdir(exist_ok=True)

    def cleanup(self):
        shutil.rmtree(self.tempdir)

    def reset_tempdir(self):
        self.cleanup()
        self.makedir()

    def setUp(self):
        self.makedir()        

        if hasattr(self, "_setUp"):
            self._setUp()

    def tearDown(self):
        self.cleanup()

        if hasattr(self, "_tearDown"):
            self._tearDown()
