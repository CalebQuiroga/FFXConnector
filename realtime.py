import requests
from google.transit import gtfs_realtime_pb2
import time

def fetch_vehicle_feed():
    VEHICLES_URL = "https://www.fairfaxcounty.gov/gtfsrt/vehicles"
    API_KEY = "vBg3jyUZpetWjpeDRiJSVCMTP"
    HEADERS = {"x-api-key": API_KEY}
    feed = gtfs_realtime_pb2.FeedMessage()
    r = requests.get(VEHICLES_URL, headers=HEADERS)
    feed.ParseFromString(r.content)
    return feed

def fetch_trip_feed():
    TRIPS_URL = "https://www.fairfaxcounty.gov/gtfsrt/trips"
    API_KEY = "vBg3jyUZpetWjpeDRiJSVCMTP"
    HEADERS = {"x-api-key": API_KEY}
    feed = gtfs_realtime_pb2.FeedMessage()
    r = requests.get(TRIPS_URL, headers=HEADERS)
    feed.ParseFromString(r.content)
    return feed

def parse_vehicle_positions(feed):
    vehicles = []
    for entity in feed.entity:
        if entity.HasField("vehicle"):
            v = entity.vehicle
            vehicles.append({
                "id": v.vehicle.id,
                "lat": v.position.latitude,
                "lon": v.position.longitude,
                "timestamp": v.timestamp,
                "trip_id": v.trip.trip_id if v.trip else None,
                "route_id": v.trip.route_id if v.trip else None
            })
    return vehicles

def parse_trip_updates(feed):
    trip_updates = {}
    current_time = int(time.time())
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            tu = entity.trip_update
            trip_id = tu.trip.trip_id
            next_stop = None
            last_stop = None
            arrival_time = None
            next_stop_seq = None
            last_stop_seq = -1

            for stu in tu.stop_time_update:
                if stu.arrival and stu.arrival.time > current_time:
                    next_stop = stu.stop_id
                    arrival_time = stu.arrival.time
                    next_stop_seq = stu.stop_sequence
                    break

            for stu in tu.stop_time_update:
                if next_stop_seq is not None and stu.stop_sequence < next_stop_seq and stu.stop_sequence > last_stop_seq:
                    last_stop = stu.stop_id
                    last_stop_seq = stu.stop_sequence

            trip_updates[trip_id] = {
                "next_stop": next_stop,
                "last_stop": last_stop,
                "arrival_time": arrival_time
            }
    return trip_updates
