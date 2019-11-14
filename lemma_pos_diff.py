import csv
import collections
import math
import statistics

def geomean(xs):
    return math.exp(math.fsum(math.log(x) for x in xs) / len(xs))

counts = collections.defaultdict(lambda: {"ocr": 0, "raw": 0})


with open("lemma.csv") as f:
	reader = csv.reader(f)

	titles = []
	types = []

	apaxes = {"ocr": 0, "gt": 0, "same": 0}
	totals = {"ocr": 0, "gt": 0}

	# On tourne une première fois pour avoir le décompte total
	# C'est pas beau; mais ça fait le café
	for num, line in enumerate(reader):
		if num == 0:
			titles = line[1:]
		elif num == 1:
			types = line[1:]
		else:
			by_types = zip(types, line[1:])

			here = {"ocr": 0, "gt": 0}

			for type_name, cnt in by_types:
				totals[type_name] += int(cnt)

	# Set-up stuff based on title
	diff_moy_by_title = {
		title: []
		for title in titles
	}
	diff_moy_by_title["total"] = []

	diff_moy_by_title_hors_apaxes_de_type = {
		title: []
		for title in titles
	}
	diff_moy_by_title_hors_apaxes_de_type["total"] = []

	# On repasse pour les vrais décomptes
	f.seek(0)
	for num, line in enumerate(reader):
		if num == 0:
			titles = ["lemma"] + line[1:]
		elif num == 1:
			types = line[1:]
		else:
			by_types = zip(types, line[1:])

			here = {"ocr": 0, "gt": 0}

			for type_name, cnt in by_types:
				totals[type_name] += int(cnt)
				here[type_name] += int(cnt)

			# Diff relative générale
			freqs = {key: val/totals[key] for key, val in here.items()}
			rel = abs(freqs["gt"] - freqs["ocr"]) / max(list(freqs.values()))

			if rel == 1.0:
				print(list(zip(types, line[1:])))

			# If 1.0, apaxe de type (présent que dans OCR ou que dans GT)
			if rel != 1.0:
				diff_moy_by_title_hors_apaxes_de_type["total"].append(rel)

			diff_moy_by_title["total"].append(rel)


			# Decompte des apaxes pour le total
			for key in ["gt", "ocr"]:
				if here[key] == 1:
					apaxes[key] += 1

			# Decompte des apaxes retrouvés dans les deux documents
			if here["gt"] == here["ocr"]:
				apaxes["same"] += 1

	for key in diff_moy_by_title:
		if diff_moy_by_title[key]:
			#print(diff_moy_by_title[key])
			diff_moy_by_title[key] = {
				"arith_mean": sum(diff_moy_by_title[key]) / len(diff_moy_by_title[key]),
				"geo_mean" : geomean(diff_moy_by_title[key]),
				"median": statistics.median(diff_moy_by_title[key])
			}

	for key in diff_moy_by_title_hors_apaxes_de_type:
		if diff_moy_by_title_hors_apaxes_de_type[key]:
			diff_moy_by_title_hors_apaxes_de_type[key] = {
				"arith_mean": sum(diff_moy_by_title_hors_apaxes_de_type[key]) / len(diff_moy_by_title_hors_apaxes_de_type[key]),
				"geo_mean" : geomean(diff_moy_by_title_hors_apaxes_de_type[key]),
				"median": statistics.median(diff_moy_by_title_hors_apaxes_de_type[key])
			}
	print(apaxes) # {'ocr': 2353, 'gt': 1052, 'same': 871}
	print(diff_moy_by_title_hors_apaxes_de_type)