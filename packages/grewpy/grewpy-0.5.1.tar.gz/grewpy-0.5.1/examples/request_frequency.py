from grewpy import Request, Corpus

# Suppose that the folder UD_Hebrew-IAHLTwiki is available locally
corpus = Corpus("UD_Hebrew-IAHLTwiki")

# build a dictionary which gives the frequency of each lemma in the corpus
lemma_frequences = (corpus.count(Request.parse("pattern { X[lemma] }"), ["X.lemma"]))

request = Request.parse ("pattern { X[upos=NOUN, Definite=Cons] }")

all_occurrences = corpus.search (request, ["X.lemma"])
hapax_occurences = { lemma: all_occurrences[lemma] for lemma in all_occurrences if lemma_frequences[lemma] == 1}

print (f"Total Number of occurrences: {len(all_occurrences)}")
print (f"Hapax occurrences: {len(hapax_occurences)}")

for hapax_lemma in hapax_occurences:
   print(hapax_lemma)
