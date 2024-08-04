import sys, os, json

sys.path.insert(0, os.path.abspath(os.path.join( os.path.dirname(__file__), "../"))) # Use local grew lib

# from grewpy import Graph, CorpusDraft, Request, Corpus, GRS, request_counter
from grewpy import Request


r = Request("pattern { X[!lemma] }")
r = Request("pattern { X-[^comp]->Y }")
r = Request("pattern { X-[comp|aux]->Y}")
r = Request("pattern { X-[1=comp]->*}")
r = Request('pattern { X[lemma <> re"er"] }')
r = Request('pattern { X[lemma <> /re"er"/] }')
