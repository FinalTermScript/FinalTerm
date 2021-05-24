class Major():

    def __init__(self,major,salary,employment, department,job,main_subject,male_percent): #리스트는 미리 만들어서 리스트로 넘겨줘야함 (employment,department 등 )
        self.major = major
        self.salary = salary
        self.employment = employment
        self.department = department[0:8] #최대 8개만
        self.job = job[0:5] #최대 5개만
        self.main_subject = main_subject
        self.male_percent = male_percent

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

    def getMalePercent(self):
        return self.male_percent


    #성비 등 계속 추가 필요