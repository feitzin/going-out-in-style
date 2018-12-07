import numpy as np
import pickle

from embeddings import load_w2v, save_w2v, load_glove, train_w2v, find_top_k
from align import gw, align_map
from preprocess import compile_shakespeare

print 'getting models.'

sentences = compile_shakespeare()
shakespeare_model = train_w2v(sentences)
shakespeare_model.save('../models/shakespeare.model')

#shakespeare_model = load_w2v('../models/shakespeare.model')
shakespeare_model = shakespeare_model.wv

english_model = load_w2v('../../../waypoint/GoogleNews-vectors-negative300.bin', binary=True)

print 'models done.'

swords, svectors, sc = find_top_k(shakespeare_model, 10000)
ewords, evectors, ec = find_top_k(english_model, 10000)

sc = np.array(sc)
ec = np.array(ec)

sc = sc / np.sum(sc)
ec = ec / np.sum(ec)

print 'trimming done.'

G, P = gw(evectors, svectors, ec, sc)

print 'alignment done.'

pickle.dump(G, open('gamma.pkl', 'w'))
pickle.dump(P, open('P.pkl', 'w'))

print 'saved.'

print align_map('hello', shakespeare_model, G, P)