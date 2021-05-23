class University():

    def __init__(self,school_name,campus_name,major_name,area, school_URL):
        self.school_name = school_name
        self.campus_name =campus_name
        self.major_name = major_name
        self.area = area
        self.school_URL = school_URL

    def getSchoolName(self):
        return self.school_name

    def getCampusName(self):
        return self.campus_name

    def getMajorName(self):
        return self.major_name

    def getArea(self):
        return self.area

    def getSchoolURL(self):
        return self.school_URL