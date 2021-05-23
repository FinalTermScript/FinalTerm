class Major():

    def __init__(self,major,salary,employment, department,job,subject_name):
        self.major = major
        self.salary = salary
        self.employment = employment
        self.department = department
        self.job = job
        self.subject_name = subject_name


    def getMajor(self):
        return self.major

    def getSalary(self):
        return self.salary

    def getEmployment(self):
        return self.employment

    def getDepartment(self):
        return self.department

    def getJob(self):
        return self.job

    def getSubjectName(self):
        return self.subject_name


    #성비 등 계속 추가 필요