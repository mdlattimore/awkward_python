from nameparser import HumanName
from simple_name_parser import parse_name
import time
from statistics import mean


name = "Charles Emerson Winchester, III"


all_times1 = []
for n in range(1000):
    start1 = time.perf_counter()
    name1 = HumanName(name)
    end1 = time.perf_counter()
    all_times1.append(end1 - start1)

all_times2 = []
for n in range(1000):
    start2 = time.perf_counter()
    name2 = parse_name(name)
    end2 = time.perf_counter()
    all_times2.append(end2 - start2)

name1_1 = HumanName(name)
name2_1 = parse_name(name)

print("nameparser.HumanName")
print(name1_1.__repr__())
print(f"{mean(all_times1)}")
print()
print()
print("parse_name")
print(name2_1)
print(f"{mean(all_times2)}")
