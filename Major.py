class Major():

    def __init__(self,major,salary,employment, department,job,main_subject): #리스트는 미리 만들어서 리스트로 넘겨줘야함 (employment,department 등 )
        self.major = major
        self.salary = salary
        self.employment = employment
        self.department = department
        self.job = job
        self.main_subject = main_subject

        print(self.major)
        print(self.salary)
        print(self.employment)
        print(self.department)
        print(self.job)
        print(self.main_subject)


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

    def getMainSubject(self):
        return self.main_subject


    #성비 등 계속 추가 필요