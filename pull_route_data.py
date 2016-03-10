#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs

# Get all routes from mobile site
#curl -X POST http://www.dublinbus.ie/modules/MobilePack/DBMobileFindStops.aspx/FindRouteSearchAutocomplete -H 'Content-Type: application/json; charset=UTF-8' --data '{"searchTerm":""}'

# Get all routes from desktop site
# curl -X POST http://www.dublinbus.ie/Templates/public/RoutePlannerService/RTPIWebServiceProxy.asmx/GetRoutesViaService -H 'Content-Type: application/json; charset=UTF-8' --data '{"context":{"Text":"","NumberOfItems":0,"Filter":"","MinStringLength":2}}'
# where the NumberOfItems attribute increases from 0 by jumps of 50 and indicates start position of next set of data.
# The returned data has an attribute 'EndOfItems' which indicates whether more rows can be returned (by incrementing NumberOfItems as above).
# I have seen the second call to this location fail sporadically with 'GetRoutesViaService Web Service method name is not valid.'

# Route info
# curl -X GET 'http://www.dublinbus.ie/DublinBus-Mobile/RTPI-Stops/?routeNumber=13&Towards=Grange%20Castle&From=Harristown&Direction=I'
# alternatively, Direction=O
# From and Towards parameters are required

# Stop info
# GET
# http://www.dublinbus.ie/DublinBus-Mobile/Real-Time-Info/?RTPISearch=stops&stopnumber=7229


# Get all bus routes and stops
# all_routes will be a dict of the form {route_number: {from:<>,to:<>,outbound_stops:[],inbound_stops:[]}}
# all_stops will be a dict of the form {stop_number: {name:<>, latitude:<>, longitude:<>, routes:[(num, outbound/inbound)]}}
all_routes = {}
all_stops = {}
all_routes_request = requests.post('http://www.dublinbus.ie/modules/MobilePack/DBMobileFindStops.aspx/FindRouteSearchAutocomplete',
                                   headers={'Content-Type':'application/json; charset=UTF-8'},
                                   data='{"searchTerm":""}')
all_routes_soup = BeautifulSoup(all_routes_request.json()['d'],'lxml')
for hyperlink in all_routes_soup.find_all('asp:hyperlink',onclick=True):
    m = re.search('\'(.*)\|(.*)\|(.*)\|\'',re.sub('\\\\\'','\'',hyperlink['onclick']))
    route_number = m.group(1)
    route_from = m.group(2)
    route_to = m.group(3)
    all_routes[route_number] = {'from':route_from,'to':route_to,'outbound_stops':[],'inbound_stops':[]}
    print("Route {} from {} to {}".format(route_number,route_from,route_to))
    # Find all stops by traversing the outbound and inbound routes
    outbound_stops_request = requests.get('http://www.dublinbus.ie/DublinBus-Mobile/RTPI-Stops/',
                                          params={'routeNumber':route_number,'Towards':route_to,'From':route_from,'Direction':'O'})
    outbound_stops_soup = BeautifulSoup(outbound_stops_request.text,'lxml')
    for stop in outbound_stops_soup.find_all('span',id=re.compile('ctl00_BodyContents_rptStops_ctl[0-9]+_lblStopNumber')):
        stop_number = stop.string
        stop_name = outbound_stops_soup.find('span',id=re.sub('Number','Name',stop['id'])).string
        all_routes[route_number]['outbound_stops'].append(stop_number)
        if not stop_number in all_stops:
            # Get real time info for stop, as well as GPS coordinates (from map link)
            stop_details_request = requests.get('http://www.dublinbus.ie/DublinBus-Mobile/Real-Time-Info/',
                                                params={'RTPISearch':'stop','stopnumber':stop_number})
            stop_details_soup = BeautifulSoup(stop_details_request.text,'lxml')
            stop_details = parse_qs(urlparse(stop_details_soup.find(href=re.compile('RTPI-Map-Details'))['href'])[4])
            stop_latitude = stop_details['stopLat'][0]
            stop_longitude = stop_details['stopLng'][0]
            all_stops[stop_number] = {'name':stop_name,'latitude':stop_latitude,'longitude':stop_longitude,'routes':[]}
            print("First instance of stop {} ({}) found, latitude {}, longitude {}.".format(stop_number,stop_name, stop_latitude, stop_longitude))
        all_stops[stop_number]['routes'].append((route_number,'O'))

    inbound_stops_request = requests.get('http://www.dublinbus.ie/DublinBus-Mobile/RTPI-Stops/',
                                         params={'routeNumber':route_number,'Towards':route_to,'From':route_from,'Direction':'I'})
    inbound_stops_soup = BeautifulSoup(inbound_stops_request.text,'lxml')
    for stop in inbound_stops_soup.find_all('span',id=re.compile('ctl00_BodyContents_rptStops_ctl[0-9]+_lblStopNumber')):
        stop_number = stop.string
        stop_name = inbound_stops_soup.find('span',id=re.sub('Number','Name',stop['id'])).string
        all_routes[route_number]['inbound_stops'].append(stop_number)
        if not stop_number in all_stops:
            # Get real time info for stop, as well as GPS coordinates (from map link)
            stop_details_request = requests.get('http://www.dublinbus.ie/DublinBus-Mobile/Real-Time-Info/',
                                                params={'RTPISearch':'stop','stopnumber':stop_number})
            stop_details_soup = BeautifulSoup(stop_details_request.text,'lxml')
            stop_details = parse_qs(urlparse(stop_details_soup.find(href=re.compile('RTPI-Map-Details'))['href'])[4])
            stop_latitude = stop_details['stopLat'][0]
            stop_longitude = stop_details['stopLng'][0]
            all_stops[stop_number] = {'name':stop_name,'latitude':stop_latitude,'longitude':stop_longitude,'routes':[]}
            print("First instance of stop {} ({}) found, latitude {}, longitude {}.".format(stop_number,stop_name, stop_latitude, stop_longitude))
        all_stops[stop_number]['routes'].append((route_number,'I'))