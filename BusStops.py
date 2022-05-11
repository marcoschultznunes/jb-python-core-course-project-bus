import re
import itertools


class BusStops:
    STOP_NAME_TEMPLATE = r"([A-Z][a-z]+)( \w+)?( Road| Avenue| Boulevard| Street)$"
    STOP_TYPE_TEMPLATE = "[SOF]{1}$|$"
    TIME_TEMPLATE = r"([0-1]\d|2[0-3]):([0-5]\d)$"

    errors = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}

    def __init__(self, stops):
        self.stops = stops

    def validate(self):
        for element in self.stops:
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

    # returns all stops as arrays containing the bus lines they are part of
    def get_stops_by_name(self):
        def stops_group(stop):
            return stop['stop_name']

        stops = sorted(self.stops, key=stops_group)
        return itertools.groupby(stops, key=stops_group)

    # returns all stops grouped by each bus line
    def get_stops_by_bus(self):
        def bus_group(stop):
            return stop['bus_id']

        stops = sorted(self.stops, key=bus_group)
        return itertools.groupby(stops, key=bus_group)

    def print_stops_by_bus(self):
        print("Line names and number of stops:")

        for key, bus in self.get_stops_by_bus():
            bus = list(bus)
            print(f"bus_id: {bus[0]['bus_id']}, stops: {len(bus)}")

    # verifies if bus lines have 1 start and 1 ending point
    def verify_bus_lines(self):
        for key, bus in self.get_stops_by_bus():
            bus = list(bus)
            start_stops = len(list(filter(lambda s: s['stop_type'] == 'S', bus)))
            final_stops = len(list(filter(lambda s: s['stop_type'] == 'F', bus)))
            if not start_stops == 1 or not final_stops == 1:
                print(f"There is no start or end stop for the line: {bus[0]['bus_id']}.")
                return False
        return True

    # determines if the stop intersects 2+ bus lines
    @staticmethod
    def stop_is_transfer(stop):  # Requires a list with all the stop's bus lines (get_stops_by_name)
        return len(set(map(lambda s: s['bus_id'], stop))) > 1

    # https://stackoverflow.com/questions/21289315/itertools-groupby-returns-empty-list-items-when-populated-with-operator-itemget
    def print_stops(self):  # t_stops => 2+ bus lines
        s_stops, f_stops, t_stops = set(), set(), set()
        for k, stop in self.get_stops_by_name():
            stop = list(stop)
            for b in stop:
                if b['stop_type'] == "S":
                    s_stops.add(b['stop_name'])
                if b['stop_type'] == "F":
                    f_stops.add(b['stop_name'])
            if BusStops.stop_is_transfer(stop):
                t_stops.add(stop[0]['stop_name'])
        print(f"Start stops: {len(s_stops)} {sorted(list(s_stops))}")
        print(f"Transfer stops: {len(t_stops)} {sorted(list(t_stops))}")
        print(f"Finish stops: {len(f_stops)} {sorted(list(f_stops))}")

    def verify_time(self):
        wrong_stations = []

        for k, bus in self.get_stops_by_bus():
            bus = list(bus)

            first_stop = list(filter(lambda fs: fs['stop_type'] == 'S', bus))[0]  # Gets the starting stop

            curr_stop = first_stop
            while curr_stop['next_stop'] != 0:  # Iterate stops in order
                next_stop = list(filter(lambda ns: ns['stop_id'] == curr_stop['next_stop'], bus))[0]

                if next_stop['a_time'] < curr_stop['a_time']:
                    s = {"bus_id": first_stop['bus_id'], "stop": next_stop['stop_name']}
                    wrong_stations.append(s)
                    break  # Only one error needed per bus line

                curr_stop = next_stop

        print("Arrival time test:")
        if len(wrong_stations) == 0:
            print("OK")
        else:
            for s in wrong_stations:
                print(f"bus_id line {s['bus_id']}: wrong time on station {s['stop']}")

    # ondemand stops: not type F, S or transfer
    def verify_ondemand_stops(self):
        ondemand_stops = []
        wrong_stops = []

        for k, stop in self.get_stops_by_name():
            stop = list(stop)
            if list(filter(lambda s: s['stop_type'] == 'O', stop)):  # Adds all O stops to the array
                ondemand_stops.append(stop)

        for stop in ondemand_stops:
            print(stop)
            if list(filter(lambda s: s['stop_type'] in ('F', 'S'), stop)):
                wrong_stops.append(stop[0]['stop_name'])
            elif BusStops.stop_is_transfer(stop):
                wrong_stops.append(stop[0]['stop_name'])

        print("On demand stops test:")
        if wrong_stops:
            print(f"Wrong stop type: {wrong_stops}")
        else:
            print("OK")
