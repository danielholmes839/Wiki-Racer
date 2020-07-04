"""
Downloads a pre-trained glove model from gensim (98MB)
"""
import joblib
import gensim.downloader as api

print('downloading glove...')
glove = api.load('glove-wiki-gigaword-50')
print('saving...')
joblib.dump(glove.wv, 'model.joblib')
