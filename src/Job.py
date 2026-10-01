from job_tests.test_manager import get_tests_paths

class Job:
    
    def __init__(self, id=None, status=None):
        self.job_examples = get_tests_paths()