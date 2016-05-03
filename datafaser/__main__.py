import os
import sys
import logging
import logging.config

# Let submodules use full name even when run without installing
base_dir = os.path.dirname(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)


if __name__ == '__main__':
    logging.basicConfig(level='WARN', format='Unconfigured %(name)s %(levelname)s: %(message)s')
    try:
        from datafaser.main import Main
        Main(sys.argv).run_with_command_line()
    except Exception as e:
        logging.getLogger(sys.argv[0]).fatal(
                '%s: %s\n' % (e.__class__.__name__, str(e)),
                exc_info=os.environ.get('DATAFASER_STACKTRACE', 0))
        sys.exit(2)
