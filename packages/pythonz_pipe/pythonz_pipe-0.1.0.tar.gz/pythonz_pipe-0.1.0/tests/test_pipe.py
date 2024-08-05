from unittest import TestCase

from pythonz_pipe import pipe


class TestPipe(TestCase):
    def test_pipe_unwrap(self):
        a = pipe(5).unwrap()
        b = 5
        self.assertEqual(a, b)

    def test_pipe_methods(self):
        a = pipe(5).and_then(range).then_finally(list)
        b = [0, 1, 2, 3, 4]
        self.assertListEqual(a, b)

    def test_pipe_operators(self):
        a = pipe(5) / range // list
        b = [0, 1, 2, 3, 4]
        self.assertListEqual(a, b)

    def test_pipe_call_methods(self):
        f = pipe().and_then(range).and_then(list)
        a = 5
        b = [0, 1, 2, 3, 4]
        self.assertListEqual(f.call(a), b)

    def test_pipe_call_operators(self):
        f = pipe() / range / list
        a = 5
        b = [0, 1, 2, 3, 4]
        self.assertListEqual(f(a), b)

