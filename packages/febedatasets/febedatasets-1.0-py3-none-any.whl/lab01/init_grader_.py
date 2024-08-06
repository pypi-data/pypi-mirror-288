import otter
import os

def init_grader():
    # Determine the path to the tests directory within the package
    tests_dir = os.path.join(os.path.dirname(__file__), '../tests')
    # Initialize Otter
    grader = otter.Notebook(tests_dir=tests_dir)
    return grader
