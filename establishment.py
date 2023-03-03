import string


class Establishment:
    def __init__(self, id: int, district: string, county: string,
                 parish: string, address: string, latitude: float,
                 longitude: float, inspec_duration: int, inspec_utility: int, opening_hours: list):
        self.id = id
        self.district = district
        self.county = county
        self.parish = parish
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.inspec_duration = inspec_duration
        self.inspec_utility = inspec_utility
        self.opening_hours = opening_hours
