import glob
import collections

with open("training full.txt") as f:
	chars = collections.Counter(f.read().strip())

del chars["\n"]

import pprint
pprint.pprint(chars)

print(sum(list(chars.values())))
print(len(chars))

print(len([x for x in chars.values() if x < 10]))

import csv
with open("chars.csv", "w") as f:
	w = csv.writer(f)
	w.writerow(["char", "occs"])
	for char in chars:
		w.writerow([char, chars[char]])