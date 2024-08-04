from grewpy import Request
r = Request("pattern { e: N -[1=subj]-> M; N[upos=VERB] }").without("M[upos=NOUN]")
print (r.named_entities())
