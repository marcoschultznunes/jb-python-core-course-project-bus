import json
from BusStops import BusStops


def main():
    json_input = input()
    bs = BusStops(json.loads(json_input))
    bs.print_stops_by_bus()


main()
