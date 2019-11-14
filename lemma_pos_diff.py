import csv
import collections
import math
import statistics
from pprint import pprint

def geomean(xs):
    return math.exp(math.fsum(math.log(x) for x in xs) / len(xs))

counts = collections.defaultdict(lambda: {"ocr": [], "gt": []})


with open("pos.csv") as f:
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

	decompte = {
		title: {"ocr": 0, "gt": 0}
		for title in titles
	}
	decompte["total"] = {"ocr": 0, "gt": 0}

	nb_lemma = {
		title: {"ocr": 0, "gt": 0}
		for title in titles
	}
	nb_lemma["total"] = {"ocr": 0, "gt": 0}

	diff_moy_by_title_hors_apaxes_de_type = {
		title: []
		for title in titles
	}
	diff_moy_by_title_hors_apaxes_de_type["total"] = []

	# On repasse pour les vrais décomptes
	f.seek(0)
	for num, line in enumerate(reader):
		if num == 0:
			titles = line[1:]
		elif num == 1:
			types = line[1:]
		else:
			by_types = zip(titles, types, line[1:])

			here = {title: {"ocr": 0, "gt": 0} for title in titles}
			here["total"] = {"ocr": 0, "gt": 0}


			for title, type_name, cnt in by_types:
				totals[type_name] += int(cnt)

				here[title][type_name] += int(cnt)
				here["total"][type_name] += int(cnt)

			# Diff relative générale
			for title in here:
				freqs = {
					key: val/totals[key] 
					for key, val in here[title].items()
				}
				maximum_freq = max(list(freqs.values()))

				if maximum_freq > 0.:
					rel = abs(freqs["gt"] - freqs["ocr"]) / maximum_freq

					# If 1.0, apaxe de type (présent que dans OCR ou que dans GT)
					if rel != 1.0:
						diff_moy_by_title_hors_apaxes_de_type[title].append(rel)
					

					nb_lemma[title]["ocr"] += int(freqs["ocr"] > 0)
					nb_lemma[title]["gt"] += int(freqs["gt"] > 0)

					decompte[title]["ocr"] += int(maximum_freq == freqs["ocr"] and rel == 1.0)
					decompte[title]["gt"] += int(maximum_freq == freqs["gt"] and rel == 1.0)
					

					diff_moy_by_title[title].append(rel)


			# Decompte des apaxes pour le total
			for key in ["gt", "ocr"]:
				if here["total"][key] == 1:
					apaxes[key] += 1

			# Decompte des apaxes retrouvés dans les deux documents
			if here["total"]["gt"] == here["total"]["ocr"]:
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

	pprint(decompte)
	for key in decompte:
		decompte[key] = {
			ocr_or_gt: specs/nb_lemma[key][ocr_or_gt]
			for ocr_or_gt, specs in decompte[key].items()
		}

print("======")
print("Apaxes")	
print(apaxes) # {'ocr': 2353, 'gt': 1052, 'same': 871}
print("======")
print("Diff moy out of apaxes")
pprint(diff_moy_by_title_hors_apaxes_de_type)
print("======")
print("Diff moy ")
pprint(diff_moy_by_title)
import json
pprint(decompte)


for num, (title, values) in enumerate(diff_moy_by_title_hors_apaxes_de_type.items()):
	if num == 0:
		keys = list(values.keys())
		print("|"+"|".join(["Corpus"]+keys)+"|")
	print("|"+"|".join([title]+[str(round(value*100, 2)) for value in values.values()])+"|")


for num, (title, values) in enumerate(decompte.items()):
	if num == 0:
		keys = list(values.keys())
		print("|"+"|".join(["Corpus"]+keys)+"|")
	print("|"+"|".join([title]+[str(round(value*100, 2)) for value in values.values()])+"|")
