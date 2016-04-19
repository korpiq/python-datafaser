import io
import os
import sys
import unittest
import datafaser
import datafaser.start


class InitTest(unittest.TestCase):

    args = []

    def setUp(self):
        self.original = datafaser.start.create_runner_to_load
        self.original_stderr = sys.stderr

    def tearDown(self):
        datafaser.start.create_runner_to_load = self.original
        sys.stderr = self.original_stderr

    def test_run_ok(self):
        self.got_files = None
        self.runner_called = 0
        datafaser.start.create_runner_to_load = self._mock_create
        datafaser.run(self.args)
        self.assertIs(self.got_files, self.args, 'run passes list of files on')
        self.assertEqual(self.runner_called, 1, 'run calls runner once')

    def test_run_failing_prints_error(self):
        self._run_failing()
        self._assert_correct_error_output()

    def test_run_failure_passed_on_when_debugging(self):
        os.environ['datafaser_debug'] = '1'
        exception = None
        try:
            self._run_failing()
        except Exception as e:
            exception = e
        self.assertIsInstance(exception, Exception, 'datafaser.run lets error through in debug mode')
        self._assert_correct_error_output()

    def _run_failing(self):
        datafaser.start.create_runner_to_load = None
        sys.stderr = io.StringIO()
        datafaser.run(self.args)

    def _assert_correct_error_output(self):
        self.assertRegexpMatches(
                sys.stderr.getvalue(),
                '^Datafaser run failed on \w+: ',
                'datafaser.run reports error'
        )

    def _mock_create(self, files):
        self.got_files = files
        return InitTest.MockRunner(self._mock_runner)

    def _mock_runner(self):
        self.runner_called += 1

    class MockRunner:
        def __init__(self, callback):
            self.callback = callback

        def load_and_run_all_plans(self):
            return self.callback()
