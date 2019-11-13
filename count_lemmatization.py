import glob
import os.path
import csv
from collections import defaultdict

OCR_PATH = "/home/thibault/dev/dh-meier/output/transkribus/lemmatized/boudams"
LEMMA_PATH = "/home/thibault/dev/LiSeinConfessorPandora/data/lemmatises"

files = {
	"29_Wau_Leg-C_Co_Ev_Vie_Martin.decolumnized.txt": "jns915.jns1856.ciham-fro1__Pandora.tsv",
	"30_Wau_Leg-C_Co_Ev_Tra_Martin2.decolumnized.txt": "jns915.jns1856.ciham-fro1__Pandora.tsv",
	"31_Wau_Leg-C_Co_Ev_Dia_Martin3.decolumnized.txt": "jns915.jns2117.ciham-fro1__Pandora.tsv",
	"32_Wau_Leg-C_Co_Ev_Vie_Brice.decolumnized.txt": "jns915.jns1743.ciham-fro1__Pandora.tsv",
	"33_Wau_Leg-C_Co_Er_Vie_Gilles.decolumnized.txt": "jns915.jns2000.ciham-fro1__Pandora.tsv",
	"34_Wau_Leg-C_Co_Ev_Vie_Martial.decolumnized.txt": "jns915.jns1761.ciham-fro1__Pandora.tsv",
	"35_Wau_Leg-C_Co_Ev_Vie_Nicolas.decolumnized.txt": "jns915.jns2114.ciham-fro1__Pandora.tsv",
	"36_Wau_Leg-C_Co_Ev_Mir_Nicolas2.decolumnized.txt": "jns915.jns2114.ciham-fro1__Pandora.tsv",
	"37_Wau_Leg-C_Co_Ev_Tra_Nicolas3.decolumnized.txt": "jns915.jns2114.ciham-fro1__Pandora.tsv",
	"38_Wau_Leg-C_Co_Ev_Vie_Jerome.decolumnized.txt": "jns915.jns1742.ciham-fro1__Pandora.tsv",
	"39_Wau_Leg-C_Co_Ev_Vie_Benoit.decolumnized.txt": "jns915.jns1744.ciham-fro1__Pandora.tsv",
	"40_Wau_Leg-C_Co_Er_Vie_Alexis.decolumnized.txt": "jns915.jns1994.ciham-fro1__Pandora.tsv",
}

titles = {
	"29_Wau_Leg-C_Co_Ev_Vie_Martin.decolumnized.txt": "Vie_Martin",
	"30_Wau_Leg-C_Co_Ev_Tra_Martin2.decolumnized.txt": "Vie_Martin",
	"31_Wau_Leg-C_Co_Ev_Dia_Martin3.decolumnized.txt": "Dia_Martin",
	"32_Wau_Leg-C_Co_Ev_Vie_Brice.decolumnized.txt": "Vie_Brice",
	"33_Wau_Leg-C_Co_Er_Vie_Gilles.decolumnized.txt": "Vie_Gilles",
	"34_Wau_Leg-C_Co_Ev_Vie_Martial.decolumnized.txt": "Vie_Martial",
	"35_Wau_Leg-C_Co_Ev_Vie_Nicolas.decolumnized.txt": "Vie_Nicolas",
	"36_Wau_Leg-C_Co_Ev_Mir_Nicolas2.decolumnized.txt": "Vie_Nicolas",
	"37_Wau_Leg-C_Co_Ev_Tra_Nicolas3.decolumnized.txt": "Vie_Nicolas",
	"38_Wau_Leg-C_Co_Ev_Vie_Jerome.decolumnized.txt": "Vie_Jerome",
	"39_Wau_Leg-C_Co_Ev_Vie_Benoit.decolumnized.txt": "Vie_Benoit",
	"40_Wau_Leg-C_Co_Er_Vie_Alexis.decolumnized.txt": "Vie_Alexis",
}


def maker_reader(f):
	reader = csv.DictReader(f, delimiter="\t")
	return reader

POS = {
	"Vie_Martin": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Martin": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Dia_Martin": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Brice": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Gilles": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Martial": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Nicolas": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Nicolas": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Nicolas": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Jerome": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Benoit": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Alexis": defaultdict(lambda : {"ocr": 0, "truth": 0}),
}
lemma = {
	"Vie_Martin": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Martin": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Dia_Martin": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Brice": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Gilles": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Martial": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Nicolas": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Nicolas": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Nicolas": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Jerome": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Benoit": defaultdict(lambda : {"ocr": 0, "truth": 0}),
	"Vie_Alexis": defaultdict(lambda : {"ocr": 0, "truth": 0}),
}

treated = []
lemma_keys, pos_keys = [], []

# Count stuff
for file in files:
	filepath = os.path.join(OCR_PATH, file)
	canonical_name = titles[file]

	# Treat OCR output
	with open(filepath) as f:
		reader = maker_reader(f)

		# Treat POS
		last_three = []
		for line in reader:
			last_three.append(line["pos"])
			if len(last_three) == 3:
				POS[canonical_name]["->".join(last_three)]["ocr"] += 1
				last_three = last_three[1:]

			# Treat Lemma
			lemma[canonical_name][line["lemma"]]["ocr"] += 1

	# Treat Original output
	# Because not a 1-1 pairing, we ensure we do not treat the GT twice
	if canonical_name not in treated:
		with open(os.path.join(LEMMA_PATH, files[file])) as f:
			reader = maker_reader(f)

			# Treat POS
			last_three = []
			for line in reader:
				last_three.append(line["POS"])
				if len(last_three) == 3:
					POS[canonical_name]["->".join(last_three)]["truth"] += 1
					last_three = last_three[1:]

				# Treat Lemma
				lemma[canonical_name][line["lemma"]]["truth"] += 1
		treated.append(canonical_name)

	pos_keys.extend(list(POS[canonical_name].keys()))
	lemma_keys.extend(list(lemma[canonical_name].keys()))

# Write stuff
pos_keys = sorted(list(set(pos_keys)))
lemma_keys = sorted(list(set(lemma_keys)))
			
############ Scheme
#
# corpus->Vie_martin->Vie_martin->Dia_martin->Dia_martin
# lemma->ocr->gt->ocr->gt
# lemme1->0->5->7->9	
# lemme2->0->5->7->9
# lemme3->0->5->7->9
#

with open("lemma.csv", mode="w") as f:
	writer = csv.writer(f)
	writer.writerow(["Title", 
		"Vie_Martin", "Vie_Martin",
		"Dia_Martin", "Dia_Martin",
		"Vie_Brice", "Vie_Brice",
		"Vie_Gilles", "Vie_Gilles",
		"Vie_Martial", "Vie_Martial",
		"Vie_Nicolas", "Vie_Nicolas",
		"Vie_Jerome", "Vie_Jerome",
		"Vie_Benoit", "Vie_Benoit",
		"Vie_Alexis", "Vie_Alexis"
		])
	writer.writerow(["Corpus"] + ["ocr", "gt"] * 9)
	for lemma_key in lemma_keys:
		line = [lemma_key]
		for corpus in ["Vie_Martin", "Dia_Martin", "Vie_Brice", "Vie_Gilles", "Vie_Martial", "Vie_Nicolas", "Vie_Jerome", "Vie_Benoit", "Vie_Alexis"]:
			numbers = lemma[corpus].get(lemma_key, {"ocr": 0, "truth": 0})
			line.extend([numbers["ocr"], numbers["truth"]])
		writer.writerow(line)


with open("pos.csv", mode="w") as f:
	writer = csv.writer(f)
	writer.writerow(["Title", 
		"Vie_Martin", "Vie_Martin",
		"Dia_Martin", "Dia_Martin",
		"Vie_Brice", "Vie_Brice",
		"Vie_Gilles", "Vie_Gilles",
		"Vie_Martial", "Vie_Martial",
		"Vie_Nicolas", "Vie_Nicolas",
		"Vie_Jerome", "Vie_Jerome",
		"Vie_Benoit", "Vie_Benoit",
		"Vie_Alexis", "Vie_Alexis"
		])
	writer.writerow(["Corpus"] + ["ocr", "gt"] * 9)
	for pos_key in pos_keys:
		line = [pos_key]
		for corpus in ["Vie_Martin", "Dia_Martin", "Vie_Brice", "Vie_Gilles", "Vie_Martial", "Vie_Nicolas", "Vie_Jerome", "Vie_Benoit", "Vie_Alexis"]:
			numbers = POS[corpus].get(pos_key, {"ocr": 0, "truth": 0})
			line.extend([numbers["ocr"], numbers["truth"]])
		writer.writerow(line)
