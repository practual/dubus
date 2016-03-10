from django.db import models

class Stop(models.Model):
    number = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)

    def __str__(self):
        return "{} ({})".format(self.number,self.name)

class Route(models.Model):
    number = models.CharField(max_length=4,primary_key=True)
    from_stop = models.CharField(max_length=200)
    to_stop = models.CharField(max_length=200)
    stops = models.ManyToManyField(Stop,through='RouteStop')

    def __str__(self):
        return "{} from {} to {}".format(self.number,self.from_stop,self.to_stop)

class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    direction = models.CharField(max_length=1)
    stop_number = models.PositiveIntegerField()

    def __str__(self):
        return "Route {} {}, stop {} ({} - {})".format(self.route.number,{'O':'outbound','I':'inbound'}[self.direction],self.stop_number,self.stop.number,self.stop.name)
