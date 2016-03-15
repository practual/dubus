from django.db import models
#from datetime import datetime

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

# Could be useful to cache the arrival data rather than send requests straight through to
# dublinbus.ie. Depends how many requests are arriving for the same stop in the same minute,
# since anything less frequent would still need an update from the source to avoid stale data.
#class StopArrival(models.Model):
#    route_stop = models.ForeignKey(RouteStop, on_delete=models.CASCADE)
#    data_retrieved_time = models.DateTimeField()
#    arrival_time = models.DateTimeField()
#
#    def __str__(self):
#        return "Bus on route {} {} arriving at stop {} in {} minutes".format(self.route_stop.route.number,
#                                                                             {'O':'outbound','I':'inbound'}[self.route_stop.direction],
#                                                                             self.route_stop.stop.number,
#                                                                             int((arrival_time - datetime.utcnow()).total_seconds() / 60))