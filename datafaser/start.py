from datafaser.data import Data
from datafaser.run import Runner


class Start:
    """
    Builds first run plan to load files given as arguments.
    """

    def __init__(self, args):
        """
        :param args: list of paths to files or directories to load as data
        """
        self.args = args
        self.data = self._get_start_data()
        self.runner = Runner(self.data)
        self.phase_number = 0

    def load_and_run_all_plans(self):
        """
        Runs plans as long as any are available at `datafaser.run.plan`.
        """

        while len(self.data.dig('datafaser.run.plan')) > 0:
            self.phase_number += 1
            run = self.data.dig('datafaser.run')
            phase = run['plan'].pop()
            if isinstance(phase, dict) and len(phase) == 1:
                run['phase'] = phase
                for phase_name, operations in phase.items():
                    print('Running phase #%d: "%s"' % (self.phase_number, phase_name))
                    self.runner.run(operations)
                run['done'].append(phase)
                del run['phase']
            else:
                raise ValueError('Phase #%d in plan does not map one name to operations: %s' % (self.phase_number, str(phase)))

    def _get_start_data(self):
        return Data({
            'datafaser': {
                'run': {
                    'arguments': self.args,
                    'plan': [self._get_start_plan()],
                    'done': []
                }
            }
        })

    def _get_start_plan(self):
        return {'start': [{
            'load': {
                'from': [{
                    'files': self.args
                }]
            }
        }]}
