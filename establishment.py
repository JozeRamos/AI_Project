import string


class Establishment:
    def __init__(self, id: int, district: string, county: string,
                 parish: string, address: string, latitude: float,
                 longitude: float, inspec_utility: float, inspec_duration: int, opening_hours: list):
        self.id = id
        self.district = district
        self.county = county
        self.parish = parish
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.inspec_duration = inspec_duration * 60 #transform to seconds
        self.inspec_utility = inspec_utility
        self.opening_hours = opening_hours
        self.visited = False

    #inspec duration + travel time + getWaitingTime()
