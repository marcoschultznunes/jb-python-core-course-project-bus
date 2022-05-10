import re
import itertools


class BusStops:
    STOP_NAME_TEMPLATE = r"([A-Z][a-z]+)( \w+)?( Road| Avenue| Boulevard| Street)$"
    STOP_TYPE_TEMPLATE = "[SOF]{1}$|$"
    TIME_TEMPLATE = r"([0-1]\d|2[0-3]):([0-5]\d)$"

    errors = {
        "bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0,
        "stop_type": 0, "a_time": 0
    }

    def __init__(self, stops):
        self.stops = stops

    def validate(self):
        for element in self.stops:
            # print(element['a_time'])
            # print(re.match(BusStops.TIME_TEMPLATE, element['a_time']))
            if not isinstance(element["bus_id"], int):
                self.errors["bus_id"] += 1
            if not isinstance(element["stop_id"], int):
                self.errors["stop_id"] += 1
            if not re.match(BusStops.STOP_NAME_TEMPLATE, element["stop_name"]):
                self.errors["stop_name"] += 1
            if not isinstance(element["next_stop"], int):
                self.errors["next_stop"] += 1
            if not re.match(BusStops.STOP_TYPE_TEMPLATE, element["stop_type"]):
                self.errors["stop_type"] += 1
            if not re.match(BusStops.TIME_TEMPLATE, element['a_time']):
                self.errors["a_time"] += 1

    def print_validation(self):
        self.validate()
        print(f"Format validation: {sum(self.errors.values())} errors")
        for key, v in self.errors.items():
            if key == "stop_name" or key == "stop_type" or key == "a_time":
                # if v > 0:
                print(key + ":", self.errors[key])

    def print_stops_by_bus(self):
        def bus_group(stop):
            return stop['bus_id']

        print("Line names and number of stops:")

        stops = sorted(self.stops, key=bus_group)
        for key, bus in itertools.groupby(stops, key=bus_group):
            bus = list(bus)
            print(f"bus_id: {bus[0]['bus_id']}, stops: {len(bus)}")
