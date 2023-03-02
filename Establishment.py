import string


class Establishment:
    def __init__(self,id : int, district: string, county: string, parish: string, address: string, latitude: float, longitude: float, inspecDuration : int, inspecUtility : int, openingHours : list) :
        self.id = id
        self.district = district
        self.county = county
        self.parish = parish
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.inspecDuration = inspecDuration
        self.inspecUtility = inspecUtility
        self.openingHours = openingHours