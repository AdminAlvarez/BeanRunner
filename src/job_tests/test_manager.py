def get_tests_paths ():
    path = 'src/job_tests/'
    with open(path+"job_names.txt", "r") as file:
        names = [path+line.strip() for line in file.readlines()]
    return names