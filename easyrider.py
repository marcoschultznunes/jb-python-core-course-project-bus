import json
import re
errors = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}
stop_name_template = r"([A-Z][a-z]+)( \w+)?( Road| Avenue| Boulevard| Street)$"
stop_type_template = "[SOF]{1}$|$"
time_template = r"([0-1]\d|2[0-3]):([0-5]\d)$"
json_input = input()
db = json.loads(json_input)

for element in db:
    # print(element['a_time'])
    # print(re.match(time_template, element['a_time']))
    if not isinstance(element["bus_id"], int):
        errors["bus_id"] += 1
    if not isinstance(element["stop_id"], int):
        errors["stop_id"] += 1
    if not re.match(stop_name_template, element["stop_name"]):
        errors["stop_name"] += 1
    if not isinstance(element["next_stop"], int):
        errors["next_stop"] += 1
    if not re.match(stop_type_template, element["stop_type"]):
        errors["stop_type"] += 1
    if not re.match(time_template, element['a_time']):
        errors["a_time"] += 1

print(f"Format validation: {sum(errors.values())} errors")
for key, v in errors.items():
    if key == "stop_name" or key == "stop_type" or key == "a_time":
    # if v > 0:
        print(key + ":", errors[key])
