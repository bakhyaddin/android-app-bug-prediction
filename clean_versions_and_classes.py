import pandas as pd
import csv
from itertools import repeat

csv_file_name = "cleaned_versions_and_locations.csv"

df = pd.read_csv("versions_and_classes.csv", sep=';')


def convert_to_list(np_array):
    new_list = []
    for value in np_array.tolist():
        new_list.append(value[0])
    return new_list


versions_column = convert_to_list(df[["Version"]].to_numpy())
location_column = convert_to_list(df[["Location"]].to_numpy())


headers = ["Location"]
for x in versions_column:
    if x in headers:
        continue
    else:
        headers.append(x)

csv_file = open(csv_file_name, 'w')
csv_out = csv.writer(csv_file)
csv_out.writerow(headers)

set_of_location_version = set()

for location_array in location_column:
    for location in location_array.split(","):
        if location.split(".")[1] != "java":
            continue
        set_of_location_version.add((location, versions_column[location_column.index(location_array)]))

for loc_ver in list(set_of_location_version):
    data = [loc_ver[0]]
    data = data + list(repeat(0, len(headers) - 1))
    data[headers.index(loc_ver[1])] = 1
    csv_out.writerow(data)