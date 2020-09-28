# Wauchier_stylo


Stylometric analysis of Old French _légendiers_.

N.B.: the `data` folder contains data generated with `stylo` from the raw text data.
If you need to generate new data, you will need to run the (commented-out) commands using stylo, 
and then use `write.csv` to save them / `read.csv` to load them.

## Generate analysis data

To generate the analysis, you need to clone: https://github.com/PonteIneptique/dh-meier-data

### Generate lemma and pos data

Use `generate_lemma_pos.py`:

```shell
python3 generate_lemma_pos.py [PrefixNameOfTheOutput] [Path to the directory containing texts]
```

For example, `python3 generate_lemma_pos.py transkribus ../dh-meier-data/output/transkribus/lemmatized/ocr/` will produce 
`./data/transkribus_lemmas.csv` and `./data/transkribus_pos3.csv`.

### Generate the Character 3-Grams 

Done with the Rmd files in the first few cells

### Generate the comparison between Gold and output data

ToDo
