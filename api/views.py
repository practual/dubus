from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Route, Stop, RouteStop

def route(request, route_num=None):
    if route_num:
        route = get_object_or_404(Route,pk=route_num)
        route_dict = {'routeNumber':route.number,
                      'fromLocation':route.from_stop,
                      'toLocation':route.to_stop}
        return JsonResponse(route_dict)
    else:
        routes = get_list_or_404(Route)
        routes_list = []
        for route in routes:
            routes_list.append({'routeNumber':route.number,
                                'fromLocation':route.from_stop,
                                'toLocation':route.to_stop})
        # safe=False flag allows lists to be serialised as JSONs.
        return JsonResponse(routes_list,safe=False)

def route_stops(request, route_num, direction):
    route = get_object_or_404(Route,pk=route_num)
    route_stops = get_list_or_404(RouteStop,route=route,direction={'outbound':'O','inbound':'I'}[direction])
    route_stops_list = []
    for route_stop in route_stops:
        route_stops_list.append({'stopSequenceNum':route_stop.stop_number,
                                 'stopNumber':route_stop.stop.number,
                                 'stopName':route_stop.stop.name})
    # safe=False flag allows lists to be serialised as JSONs.
    return JsonResponse(route_stops_list,safe=False)

def stop(request, stop_num):
    stop = get_object_or_404(Stop,pk=stop_num)
    stop_routes = RouteStop.objects.filter(stop=stop)
    stop_routes_list = []
    for stop_route in stop_routes:
        if stop_route.direction == 'O':
            towards = stop_route.route.to_stop
        else:
            towards = stop_route.route.from_stop
        stop_routes_list.append({'routeNumber':stop_route.route.number,
                                 'direction':stop_route.direction,
                                 'towards':towards})
    stop_dict = {'stopNumber':stop.number,
                 'stopName':stop.name,
                 'latitude':stop.latitude,
                 'longitude':stop.longitude,
                 'routes':stop_routes_list}
    return JsonResponse(stop_dict)