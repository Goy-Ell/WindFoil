
class Station():
    def __init__(self,id,name,latitude,longitude) -> None:
        self.id=id
        self.name=name
        self.latitude=latitude
        self.longitude=longitude

    def __str__(self) -> str:
        return f"{self.id}, {self.name}"


class Measure():
    def __init__(self,date, station,wind_heading,wind_speed_avg,wind_speed_max,wind_speed_min) -> None:
        self.date=date
        self.station=station
        self.wind_heading=wind_heading
        self.wind_speed_avg=wind_speed_avg
        self.wind_speed_max=wind_speed_max
        self.wind_speed_min=wind_speed_min

    def __str__(self) -> str:
        return f"{self.station}, {self.date}, wind heading : {self.wind_heading}, wind_speed_avg :  {self.wind_speed_avg} , wind_speed_max : {self.wind_speed_max} , wind_speed_min : {self.wind_speed_min} "





