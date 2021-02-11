#Tension and Compression member determiner
import math
import csv

horizontal_length = 2.64
diagonal_length = 4.545
vertical_length = 3.7

member_types = {
    "HSS 51 X 51 X 6.4": {"Area": 1030, "r": 17.6},
    "HSS 76 X 51 X 6.5": {"Area": 1350, "r": 26.1},
    "HSS 76 X 51 X 8.0": {"Area": 1600, "r": 25.1},
    "HSS 89 X 64 X 8.0": {"Area": 2010, "r": 30.5},
    "HSS 102 X 102 X 6.4": {"Area": 2320, "r": 38.4},
    "HSS 102 X 76 X 8.0": {"Area": 2410, "r": 35.8},
    "HSS 102 X 76 X 9.5": {"Area": 2790, "r": 35.0},
    "HSS 127 X 64 X 9.5": {"Area": 3030, "r": 41.7},
    "HSS 127 X 76 X 9.5": {"Area": 3280, "r": 43.2},
    "HSS 152 X 102 X 8.0": {"Area": 3620, "r": 54.8},
    "HSS 152 X 102 X 9.5": {"Area": 4240, "r": 54.0},
    "HSS 152 X 102 X 11": {"Area": 4840, "r": 53.1},
    "HSS 203 X 102 X 9.5": {"Area": 5210, "r": 70.3},
    "HSS 203 X 102 X 11": {"Area": 5870, "r": 69.3},
    "HSS 203 X 102 X 13": {"Area": 6680, "r": 68.4},
    "HSS 203 X 152 X 9.5": {"Area": 6180, "r": 75.1},
    "HSS 203 X 152 X 11": {"Area": 7100, "r": 74.2},
    "HSS 254 X 254 X 8.0": {"Area": 7660, "r": 99.9},
    "HSS 254 X 254 X 9.5": {"Area": 9090, "r": 99.1},
    "HSS 254 X 254 X 13": {"Area": 11800, "r": 97.6},
    "HSS 203 X 152 X 13": {"Area": 7970, "r": 73.4},
    "HSS 254 X 152 X 11": {"Area": 8230, "r": 91.0},
    "HSS 254 X 152 X 13": {"Area": 9260, "r": 90.1},
    "HSS 305 X 305 X 8.0": {"Area": 9280, "r": 121},
    "HSS 305 X 203 X 9.5": {"Area": 9090, "r": 113},
    "HSS 305 X 203 X 11": {"Area": 10500, "r": 112},
    "HSS 305 X 203 X 13": {"Area": 11800, "r": 111},
    "HSS 305 X 305 X 11": {"Area": 12800, "r": 119},
    "HSS 305 X 305 X 13": {"Area": 14400, "r": 118},
}

with open ("./members.csv") as f:
    members = [{k: v for k, v in row.items ()}
        for row in csv.DictReader(f, skipinitialspace=True)]

def find_compression_member_type (direction, force):
    if direction == "H":
        length = horizontal_length
    elif direction == "D":
        length = diagonal_length
    elif direction == "V":
        length = vertical_length

    resistances = {}
    for member_type in member_types:
        area = float (member_types[member_type]["Area"])
        r = float (member_types[member_type]["r"])

        slenderness_ratio = (1 * length / (r /  1000))
        sigma_e =  ((math.pi ** 2) * (200000000000)) / (slenderness_ratio) ** 2
        lamda = (370000000 / sigma_e) ** (1 / 2)
        f = 1 / ((1 + (lamda) ** (2 * 1.34)) ** (1/1.34))
        compressive_resistance = 0.9 * f * 370000000 * (area / (1000*1000))
        compressive_resistance = compressive_resistance / 1000

        resistances[member_type] = compressive_resistance

    differences = {}
    for resistance in resistances:
        difference = resistances[resistance] - float (force)
        if difference > 0:
            differences[resistance] = difference

    member_type = min (differences, key=differences.get)
    return member_type

def find_tension_member_type (force):
    resistances = {}
    for member_type in member_types:
        area = float (member_types[member_type]["Area"])
        r = float (member_types[member_type]["r"])

        tensile_resistance = 0.9 * (370 * 1000) * (area / 1000)

        resistances[member_type] = tensile_resistance

    differences = {}
    for resistance in resistances:
        difference = resistances[resistance] - float (force)
        if difference > 0:
            differences[resistance] = difference

    member_type = min (differences, key=differences.get)
    return member_type

print ("Returning member types")
for member in members:
    if member["Type"] == "C":
        member_type = find_compression_member_type (member["Direction"], member["Force"])

    elif member["Type"] == "T":
        member_type = find_tension_member_type (member["Force"])

    print (member["Member"], "-", member_type)
