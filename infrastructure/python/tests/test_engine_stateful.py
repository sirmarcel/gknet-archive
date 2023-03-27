from unittest import TestCase

from gknet.engine import Stateful

from tempdir import Tempdir


class Dummy(Stateful):
    kind = "test_dummy"

    def __init__(self, a=2):
        self.a = a

        self.state = "great"

    def _get_config(self):
        return {"a": self.a}

    def _get_state(self):
        return {"state": self.state}

    def _restore(self, payload):
        self.state = payload["state"]

    def work(self):
        self.state = "tired"


class TestStateful(Tempdir, TestCase):
    def test_rountrip(self):
        import gknet

        gknet.components.append(Dummy)

        dummy = Dummy(a=1)
        dummy.work()
        dummy.save(self.tempdir / "dummy")
        dummy2 = gknet.load(self.tempdir / "dummy")

        self.assertEqual(dummy2.state, dummy.state)
        self.assertEqual(dummy2.a, dummy.a)
