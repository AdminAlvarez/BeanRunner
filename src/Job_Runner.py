from job_tests.test_manager import get_tests_paths

class Job_Runner:
    def __init__(self, id=None, status=None):
        
        self.job_examples = get_tests_paths()
        
        self.id = None
        self.status = None
        
A = Job_Runner()
print(A.job_examples)