import sys
import os
import glob
import csv
from collections import defaultdict

# Should definitely use SKlearn but would like to not install dependencies


def cleaner(fp):
    item = os.path.split(fp)[-1]
    return item.split(".")[0]


def F(dic):
    f = defaultdict(lambda: 0)

    for fpath in dic:
        for key in dic[fpath]:
            f[key] += dic[fpath][key]

    dic["F"] = f
    return dic


if __name__ == "__main__":
    args = sys.argv
    if len(args) >= 3:
        prefix = sys.argv[1]
        paths = glob.glob(os.path.join(sys.argv[2], "lemmatized", "boudams", "*.txt"))

        pos = {cleaner(path): defaultdict(lambda: 0) for path in paths}
        pos_keys = set()

        lemmas = {cleaner(path): defaultdict(lambda: 0) for path in paths}
        lemma_keys = set()

        # Generate pos 3
        for inp_fp in paths:
            key = cleaner(inp_fp)
            with open(inp_fp) as inp:
                reader = csv.DictReader(inp, delimiter="\t", quotechar="¥")

                last_pos = []

                for line in reader:
                    lemmas[key][line["lemma"]] += 1
                    last_pos.append(line["POS"])

                    if len(last_pos) > 3:
                        last_pos = last_pos[1:]
                    if len(last_pos) == 3:
                        pos[key][" ".join(last_pos)] += 1

                lemma_keys.update(set(lemmas[key].keys()))
                pos_keys.update(set(pos[key].keys()))

        # Compute F
        F(pos)
        F(lemmas)

        with open(os.path.join("data", prefix+"_lemmas.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=["lemma", "F"] + list(map(cleaner, paths)), delimiter=";")
            writer.writeheader()
            for lemma in lemmas["F"]:
                writer.writerow(dict(lemma=lemma, **{
                    filepath: lemmas[filepath][lemma]
                    for filepath in lemmas
                }))

        with open(os.path.join("data", prefix + "_pos3-gr.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=["pos", "F"] + list(map(cleaner, paths)), delimiter=";")
            writer.writeheader()
            for val in pos["F"]:
                writer.writerow(dict(pos=val, **{
                    filepath: pos[filepath][val]
                    for filepath in pos
                }))


    else:
        print("python generate_lemma_pos.py prefix path")
