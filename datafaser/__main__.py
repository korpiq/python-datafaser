import os
import sys

this_path = os.path.dirname(os.path.dirname(__file__))
if this_path not in sys.path:
    sys.path.append(this_path)  # tests and other misusers can override by putting their path first


if __name__ == '__main__':
    from datafaser.start import Start

    try:
        Start(sys.argv[1:]).load_and_run_all_plans()
    except Exception as e:
        sys.stderr.write('Datafaser run failed on %s: %s' % (e.__class__.__name__, str(e)))
        if 'datafaser_debug' in os.environ:
            raise e
