import numpy as np
import random
import time
import csv

data = []
max_days = 100
max_samples = max_days * 24 * 4

random.seed(time.time())
cur_hour = 0.0
for i in range(max_samples):
    row = []
    row.append(0)
    row.append(0)
    row.append(0)
    row.append(0)
    room_to_activate = random.randint(0,2)
    # print(room_to_activate)
    row[room_to_activate] = 1
    row[3] = cur_hour
    cur_hour += 0.25
    data.append(row)
    # print(row)
print(len(data))
print(len(data[0]))
with open('test.csv', 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(data)