# amarillo-stops

Carpool stop import library with shared code for Amarillo GTFS-generator and Enhancer. Provides stop import functions in multiple formats and the StopsStore class with a couple of function to manage and query the stops.

## Supported import formats

Import stops from:

### .csv:
Example format:

```csv filename="stops.csv"
stop_id;stop_code;stop_lat;stop_lon;stop_name
mfdz:x;x;52.11901;14.2;Stop x
mfdz:y;y;53.1;14.01;Stop y
mfdz:z;z;54.11;14.0;Stop z
mfdz:Ang001;Ang001;53.11901;14.015776;Mitfahrbank Biesenbrow
```

### GeoJSON:
Example format:
```json filename="stops.json"
{
  "data": {
    "pointsOfInterest": [
      {
        "id": "14622",
        "externalId": "bbnavi:12073:0001",
        "name": "Parkbank",
        "description": "Parkbank",
        "dataProvider": {
          "id": "1",
          "name": "Administrator"
        },
        "addresses": [
          {
            "street": "Hauptstrasse",
            "city": "Wittenberge",
            "zip": "12345",
            "geoLocation": {
              "latitude": 52.9932971109789,
              "longitude": 11.767383582547
            }
          }
        ],
        "openStreetMap": {
          "capacity": 112,
          "capacityCharging": "2",
          "capacityDisabled": "",
          "fee": "No",
          "lit": "Yes",
          "parking": "",
          "shelter": "No",
          "surface": "",
          "utilization": "",
          "website": ""
        }
      }
    ]
  }
}
```

### Overpass
    
Makes a request to `https://overpass-api.de/api/interpreter` with the query below and imports the result:
```
[out:csv(::"type", ::"id", ::"lat", ::"lon", name,parking,park_ride,operator,access,lit,fee,capacity,"capacity:disabled",supervised,surface,covered,maxstay,opening_hours)][timeout:60];
area{area_selector}->.a;
nwr(area.a)[park_ride][park_ride!=no][access!=customers];
out center;
```

<!-- ## Usage TODO -->
        
###  GTFS
Opens stops.txt inside the zip file and imports it as .csv

## StopsStore class

Constructor parameters:
- `stop_sources`: array of stop source urls. Can point to local or remote resources. `vicinity` controls how far from the trip path they can still be associated with a trip. Example:
```python 
[
    {"url": "https://datahub.bbnavi.de/export/rideshare_points.geojson", "vicinity": 50},
    {"url": "https://data.mfdz.de/mfdz/stops/stops_zhv.csv", "vicinity": 50},
    {"url": "https://data.mfdz.de/mfdz/stops/parkings_osm.csv", "vicinity": 500}
]
```
- `internal_projection`: optionally override the used projection. Default value is `EPSG:32632`.

`load_stop_sources(self)`:
Imports stops from  stop_sources and registers them with
the distance they are still associated with a trip.
E.g. bus stops should be registered with a distance of e.g. 30m,
while larger carpool parkings might be registered with e.g. 500m.

Subsequent calls of load_stop_sources will reload all stop_sources
but replace the current stops only if all stops could be loaded successfully.

`find_additional_stops_around(self, line, stops)`:
Returns a GeoDataFrame with all stops in vicinity of the
given line, sorted by distance from origin of the line.
Note: for internal projection/distance calculations, the
lat/lon geometries of line and stops are converted to

<!-- coverted to ... ? or converted too?-->

`find_closest_stop(self, carpool_stop, max_search_distance)`:
Returns the closest stop to the given carpool stop, searching within the max_search_distance

<!-- what is the carpool_stop data structure? distance unit? (m?) -->

