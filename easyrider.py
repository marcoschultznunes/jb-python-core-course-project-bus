import json
from BusStops import BusStops


def main():
    json_input = input()
    bs = BusStops(json.loads(json_input))

    if bs.verify_stops():
        bs.print_stops()


main()
