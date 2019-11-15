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
	hapaxs = {"ocr": 0, "gt": 0, "same": 0}
	nb_tokens = {"ocr": 0, "gt": 0}
	nb_tokens_ocr = collections.defaultdict(lambda: 0)

	# On tourne une première fois pour avoir le décompte total
	# C'est pas beau; mais ça fait le café
	for num, line in enumerate(reader):
		if num == 0:
			titles = line[1:]
		elif num == 1:
			types = line[1:]
		else:
			by_types = zip(titles, types, line[1:])

			for title, type_name, cnt in by_types:
				nb_tokens[type_name] += int(cnt)
				if type_name == "ocr":
					nb_tokens_ocr[title] += int(cnt)

	# Distance relative des fréquences relatives
	diff_moy_by_title = { title: [] for title in titles }
	diff_moy_by_title["total"] = []

	# Somme des distances absolues divisées par la somme des fréquences OCR
	deltas = {title: [] for title in titles }
	deltas["total"] = []

	# Distance relative des fréquences relatives hors hapax d'OCR ou de GT (Comptés ci-desous)
	diff_moy_by_title_hors_hapaxs_de_type = { title: [] for title in titles}
	diff_moy_by_title_hors_hapaxs_de_type["total"] = []

	# Compte des lemmes spécifiques d'un corpus (OCR ou GT) et non des fréquences
	decompte = {title: {"ocr": 0, "gt": 0} for title in titles}
	decompte["total"] = {"ocr": 0, "gt": 0}

	# Nombres de lemmes présent / texte au total
	nb_lemma = { title: {"ocr": 0, "gt": 0} for title in titles }
	nb_lemma["total"] = {"ocr": 0, "gt": 0}


	# On repasse pour les vrais décomptes
	f.seek(0)
	for num, line in enumerate(reader):
		if num <= 1:
			continue
		else:
			by_types = zip(titles, types, line[1:])

			# Création d'un dictionaire local de fréquences absolues
			here = {title: {"ocr": 0, "gt": 0} for title in titles}
			here["total"] = {"ocr": 0, "gt": 0}

			# On compte les localement les valeurs
			for title, type_name, cnt in by_types:
				here[title][type_name] += int(cnt)
				here["total"][type_name] += int(cnt)

			# On calcule pour chacun des titres et le total 
			for title in here:

				# Key = OCR ou GT, évite de hardcoder le décompte
				# On calcule ici la fréquence relative à partir de leur fréquence absolue
				freqs_relatives = { ocr_or_gt: freq_absolue/nb_tokens[ocr_or_gt]  for ocr_or_gt, freq_absolue in here[title].items()}
				maximum_freq = max(list(freqs_relatives.values()))

				# Calcul de la distance absolue entre OCR et GT
				deltas[title].append(abs(here[title]["ocr"]-here[title]["gt"]))

				if maximum_freq > 0.:
					# On calcule la distance relative de fréquences relatives
					dist_rel_freq_rel = abs(freqs_relatives["gt"] - freqs_relatives["ocr"]) / maximum_freq

					
					# Si 1.0, hapax de type (présent que dans OCR ou que dans GT)
					if dist_rel_freq_rel == 1.0:
						decompte[title]["ocr"] += int(maximum_freq == freqs_relatives["ocr"])
						decompte[title]["gt"] += int(maximum_freq == freqs_relatives["gt"])
					# Du coup chiffre qui nous intéresse pour les calculs hors hapax
					else:
						diff_moy_by_title_hors_hapaxs_de_type[title].append(dist_rel_freq_rel)
					
					# Si la fréquence relative est supérieure à 0
					# le lemme est présent dans le titre
					nb_lemma[title]["ocr"] += int(freqs_relatives["ocr"] > 0)
					nb_lemma[title]["gt"] += int(freqs_relatives["gt"] > 0)

					# Ajout de cette distance relative en prenant en compte les hapax
					diff_moy_by_title[title].append(dist_rel_freq_rel)

			# Decompte des hapaxs absolus  pour le total
			for key in ["gt", "ocr"]:
				if here["total"][key] == 1:
					hapaxs[key] += 1

			# Decompte des hapaxs absolus retrouvés dans les deux documents
			if here["total"]["gt"] == here["total"]["ocr"]:
				hapaxs["same"] += 1


# Calcul des moyennes
for key in diff_moy_by_title:
	if diff_moy_by_title[key]:
		diff_moy_by_title[key] = {
			"arith_mean": sum(diff_moy_by_title[key]) / len(diff_moy_by_title[key]),
			"geo_mean" : geomean(diff_moy_by_title[key]),
			"median": statistics.median(diff_moy_by_title[key])
		}

for key in diff_moy_by_title_hors_hapaxs_de_type:
	if diff_moy_by_title_hors_hapaxs_de_type[key]:
		diff_moy_by_title_hors_hapaxs_de_type[key] = {
			"arith_mean": sum(diff_moy_by_title_hors_hapaxs_de_type[key]) / len(diff_moy_by_title_hors_hapaxs_de_type[key]),
			"geo_mean" : geomean(diff_moy_by_title_hors_hapaxs_de_type[key]),
			"median": statistics.median(diff_moy_by_title_hors_hapaxs_de_type[key])
		}


# Avant le calcul des deltas, calcul du nombres de tokens total
nb_tokens_ocr["total"] = sum(list(nb_tokens_ocr.values()))

# Calcul des deltas
for title in deltas:
	deltas[title] = {"delta": sum(deltas[title])/nb_tokens_ocr[title]}

# Calcul des % de termes spécifiques à chaque corpora (nb d'individus uniques)
for key in decompte:
	decompte[key] = {
		ocr_or_gt: specs/nb_lemma[key][ocr_or_gt]
		for ocr_or_gt, specs in decompte[key].items()
	}

print("======")
print("hapaxs")	
print(hapaxs) # {'ocr': 2353, 'gt': 1052, 'same': 871}
print("======")

def print_table_moy(dico, title, reformat=lambda x: str(round(x*100, 2))):
	print("======")
	print(title)
	print("---------")
	for num, (title, values) in enumerate(dico.items()):
		if num == 0:
			keys = list(values.keys())
			print("|"+"|".join(["Corpus"]+keys)+"|")
		print("|"+"|".join([title]+[reformat(value) for value in values.values()])+"|")
	print("=========")


print_table_moy(deltas, "Deltas", lambda x: str(x))
print_table_moy(diff_moy_by_title, "Distances relatives des fréquences relatives")
print_table_moy(diff_moy_by_title_hors_hapaxs_de_type, "Distances relatives des fréquences relatives, hors termes spécifiques à un corpus")
print_table_moy(deltas, "Deltas")

for num, (title, values) in enumerate(decompte.items()):
	if num == 0:
		keys = list(values.keys())
		print("|"+"|".join(["Corpus"]+keys)+"|")
	print("|"+"|".join([title]+[str(round(value*100, 2)) for value in values.values()])+"|")
