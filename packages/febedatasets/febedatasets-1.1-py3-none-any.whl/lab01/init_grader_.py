import otter
import os

def init_grader():
   
    # Determine the base directory of the package
    base_dir = os.path.dirname(__file__)
    tests_dir = os.path.join(base_dir, 'tests')
    
    # Ensure the tests directory exists
    if not os.path.isdir(tests_dir):
        raise ValueError(f"Tests directory {tests_dir} does not exist")
    
    # Initialize Otter
    grader = otter.Notebook(tests_dir=tests_dir)
    return grader
