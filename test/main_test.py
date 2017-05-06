import os
import sys
import unittest
import runpy
from datafaser import operations
from datafaser.main import Main
from getopt import GetoptError
import logging
import logging.config
from io import StringIO


class OutputBlocker:

    _not_set = []

    def block_output(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        self.original_exit = sys.exit
        sys.exit = self._exit_called
        self.exit_status = self._not_set

    def unblock_output(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        sys.exit = self.original_exit

    def _exit_called(self, status):
        self.exit_status = status


class MetaMainModuleTest(unittest.TestCase, OutputBlocker):

    _schema_path_required_for_validation = 'schema.properties.datafaser.properties.run.properties.options.properties'

    def setUp(self):
        self.original_argv = sys.argv
        self.original_path = sys.path
        self.original_operations_provider = operations.get_default_operations_map
        self.got_files = []
        self.block_output()

    def tearDown(self):
        sys.argv = self.original_argv
        sys.path = self.original_path
        operations.get_default_operations_map = self.original_operations_provider
        self.unblock_output()

    def test_starts_ok(self):
        self._run_main()
        self.assertRegexpMatches(self.got_files[0], '.*/datafaser/data$', '__main__ loads datafaser schema')
        self.assertEqual(sys.argv[1:], self.got_files[1:], '__main__ runs with command-line arguments without program name')

    def test_unrecognized_option_fails(self):
        self._run_main(['datafaser', '--bad-option'])
        self.assertEquals(self.exit_status, 2, '__main__ exits with status 2 on unrecognized option')

    def test_fixes_path_ok(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path = list(filter(lambda part: part != base_dir, sys.path))
        self._run_main()
        self.assertIn(base_dir, sys.path, 'main adds datafaser to path')

    def _run_main(self, args=None):
        operations.get_default_operations_map = self._mock_operations_map
        sys.argv = args or ['some', 'strings']
        runpy.run_module('datafaser', run_name='__main__')

    def _mock_operations_map(self, _):
        return {'load': self._mock_load}

    def _mock_load(self, data_tree, directives):
        self.got_files.append(directives['from']['file'])
        self._create_schema_required_for_validation(data_tree)

    def _create_schema_required_for_validation(self, data_tree):
        data_tree.reach(self._schema_path_required_for_validation, create_containers=True)


class MainObjectTest(unittest.TestCase, OutputBlocker):

    def setUp(self):
        self.original_dictConfig = logging.config.dictConfig
        logging.config.dictConfig = self._config_called
        self.config = self._not_set
        self.block_output()

    def tearDown(self):
        logging.config.dictConfig = self.original_dictConfig
        self.unblock_output()

    def test_help_ok(self):
        Main(['datafaser', '--help']).run_with_command_line()
        self.assertEquals(self.exit_status, 1, 'Option --help exits with status 1')

    def test_no_logging_ok(self):
        Main(['datafaser']).run_with_command_line()
        self.assertIs(self.exit_status, self._not_set, 'Datafaser without options does not call exit')
        self.assertIsInstance(self.config, dict, 'Datafaser without options configures logging')
        self.assertIs(
                self.config.get('handlers', {}).get('syslog', self._not_set),
                self._not_set,
                'Datafaser without options does not configure syslog'
        )
        self.assertIs(
                self.config.get('handlers', {}).get('file', self._not_set),
                self._not_set,
                'Datafaser without options does not configure log file'
        )

    def test_unrecognized_option_fails(self):
        exception = None
        try:
            Main(['datafaser', '--unrecognized-option']).run_with_command_line()
        except GetoptError as e:
            exception = e
        self.assertIsNotNone(exception, 'Unrecognized option raises exception')

    def test_log_file_option_ok(self):
        Main(['datafaser', '--log-file', '-']).run_with_command_line()
        self.assertIsInstance(self.config, dict, 'Option --log-file configures logging')
        self.assertEquals(
                self.config.get('handlers', {}).get('file', {}).get('filename'),
                '-',
                'Option --log-file sets log filename'
        )
        self.assertIs(
                self.config.get('handlers', {}).get('syslog', self._not_set),
                self._not_set,
                'Option --log-file not configure syslog'
        )

    def test_syslog_option_ok(self):
        Main(['datafaser', '--syslog']).run_with_command_line()
        self.assertIsInstance(self.config, dict, 'Option --syslog configures logging')
        self.assertEquals(
                self.config.get('handlers', {}).get('syslog', {}).get('()'),
                'logging.handlers.SysLogHandler',
                'Option --syslog defines syslog handler'
        )
        self.assertIs(
                self.config.get('handlers', {}).get('file', self._not_set),
                self._not_set,
                'Option --syslog does not configure log file'
        )

    def _config_called(self, config):
        self.config = config
