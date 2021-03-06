#Shuo Huang (sh2443)
#Xinyu Ma (xm99)
#Yiran Zheng (yz2353)
#CS5740 
#Project1 Part1

# coding: utf-8

# In[125]:

from collections import defaultdict
import operator
import random
import numpy as np

#read file and generate corpus
def get_corpus(file):
    corpus = []
    f = open(file, 'r')
    for line in f:
        # append start word
        new_line = ['<s>']
        for word in line.split():
            new_line.append(word.lower())
        # append stop word
        new_line.append('</s>')
        corpus.append(new_line)
    return corpus

# the frequency of each word in the corpus, eg P(word = A)
def get_unigram_freqs(corpus):
    w_count = defaultdict(float)
    total_count = 0
    for line in corpus:
        for word in line:
            w_count[word.lower()] += 1
            total_count += 1
    for key in w_count:
        w_count[key] /= (1.0 * total_count)  
    return w_count

# the frequency of each bigram in the corpus, eg P(B = key[1] | A = key[0])
def get_bigram_freqs(corpus, unigram_freqs):
    bi_count = defaultdict(float)
    total_count = 0
    for line in corpus:
        for i in range(len(line) - 1):
            bi_count[(line[i].lower(), line[i + 1].lower())] += 1
            total_count += 1
            
    for key in bi_count:
        bi_count[key] = (bi_count[key] * 1.0 / total_count) / unigram_freqs[key[0]]
    return bi_count

# generate the next random word using unigram model
def get_next_word_unigram(corpus):
    keys = [key for key in sorted(corpus, key=corpus.get)]
    probs = [corpus[key] for key in sorted(corpus, key=corpus.get)]
    return np.random.choice(keys, 1, probs)[0]
    
# generate the next random word using bigram model
def get_next_word_bigram(sentence, corpus):
    last_word = sentence[len(sentence) - 1]
    candidates = defaultdict(float)
    total_prob = 0.0
    for key in corpus:
        if key[0] == last_word:
            candidates[key[1]] = corpus[key]
            total_prob += corpus[key]
    
    for key in candidates:
        candidates[key] /= total_prob
    
    keys = [key for key in sorted(candidates, key=candidates.get)]
    probs = [candidates[key] for key in sorted(candidates, key=candidates.get)]
    return np.random.choice(keys, 1, probs)[0]

pos_file = 'SentimentDataset/Train/pos.txt'
neg_file = 'SentimentDataset/Train/neg.txt'
pos_corpus = get_corpus(pos_file)
neg_corpus = get_corpus(neg_file)


# In[126]:
#generate unigram models for postive and negative files.
pos_unigram_freqs = get_unigram_freqs(pos_corpus)
neg_unigram_freqs = get_unigram_freqs(neg_corpus)
#pos_unigram_freqs


# In[127]:
#generate bigram models for positive and negative files
pos_bigram_freqs = get_bigram_freqs(pos_corpus, pos_unigram_freqs)
neg_bigram_freqs = get_bigram_freqs(neg_corpus, neg_unigram_freqs)
#pos_bigram_freqs


# In[140]:

# Generate a sentence using unigram model
def generate_unigram_sentence(length, model):
    e = pos_unigram_freqs
    if model == 0:
        e = neg_unigram_freqs
    start = ['<s>']
    for i in range(0, length):
        nxt = get_next_word_unigram(e)
        if nxt == '</s>' or nxt == '.':
            break
        start.append(nxt)
        
    print(' '.join(start[1:]))

print "Generate Unigram Sentence using positive sentiment file:"
generate_unigram_sentence(20,1)


# In[141]:

# Generate a sentence using bigram model
def generate_bigram_sentence(length, model):
    e = pos_bigram_freqs
    if model == 0:
        e = neg_bigram_freqs
    bi_start = ['<s>']
    for i in range(0, length):
        nxt = get_next_word_bigram(bi_start, e)
        if nxt == '</s>' or nxt == '.':
            break
        bi_start.append(nxt)

    print(' '.join(bi_start[1:]))

print "Generate Bigram Sentence using positive sentiment file:"
generate_bigram_sentence(20,1)

print ""
print "Generate Unigram Sentence using negative sentiment file:"
generate_unigram_sentence(20,0)
print "Generate Bigram Sentence using negative sentiment file:"
generate_unigram_sentence(20,0)
