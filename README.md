# Dubus: static data API for Dublin bus routes #
## Usage ##

Unless noted otherwise, all requests should be HTTP GET without body or URL query string.

### All route details ###
    api/route/
Returns a list of JSON objects with attributes:
- `routeNumber`: Bus route number,
- `fromLocation`: Description of starting location for the route's outbound journey,
- `toLocation`: Description of final location for the route's outbound journey.

Note, the `fromLocation` and `toLocation` do not explicitly refer to the first and last bus stops of the route.

### Single route details ###
    api/route/[route number]/
where `[route number]` is a valid value as in `routeNumber` above. Returns the details for a single bus route, with the same format and attributes as above.

### Stops in journey ###
    api/route/[route number]/[outbound|inbound]/
Returns a list of bus stops in the given bus route's `outbound` (i.e. starting at `fromLocation` and finishing at `toLocation`) or `inbound` journey. Each item in the list is a JSON object with attributes:
- `stopNumber`: Unique stop number as displayed on bus stop signs,
- `stopName`: Description of stop,
- `stopSequenceNum`:The position of the stop along the route, represented as an integer counted consecutively from 0.

### Single stop details ###
    api/stop/[stop number]/
where `[stop number]` is a valid value as in `stopNumber` above. Returns the details for a single bus route, as a JSON object with the following attributes:
- `stopNumber`: as above,
- `stopName`: as above,
- `latitude`: GPS latitude given as a decimal degree to six decimal places of precision,
- `longitude`: GPS longitude given as a decimal degree to six decimal places of precision,
- `routes`: a list summarising the bus routes using the stop, where each item is a JSON object with attributes:
    - `routeNumber`: as above,
    - `direction`: either 'O' for outbound or 'I' for inbound,
    - `towards`: either the `toLocation` or the `fromLocation` of the route, depending on `direction`. 

### Arrival times ###
    api/stop/[stop number]/arrivals/
where `[stop number]` is interpreted as above. Returns the most imminent arrivals at the given stop, as a JSON object with the following attributes:
- `arrivalsRetrievedTime`: time at which data was retrieved, in the format HH:MM,
- `arrivingBuses`: a list of the most imminent arrivals, where each item is a JSON object with attributes:
    - `routeNumber`: as above,
    - `waitTime`: integer number of minutes until arrival of the bus (relative to `arrivalsRetrievedTime`), rounded down, in the format 'X mins'. If less than one minute, 'Due' is returned instead.