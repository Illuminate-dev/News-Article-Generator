import argparse
from enum import Enum
from math import exp, pow, sqrt

import nltk
import spacy
import tensorflow as tf
import tensorflow_hub as hub
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs_sim
from textstat.textstat import textstat

nlp = spacy.load("en_core_web_md")

class VectorizerType(Enum):
    WORD2VEC = 1 
    COUNT = 2
    TFIDF = 3

# https://newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python
def jaccard_similarity(x,y):
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)

def normalize(text):
    stemmer = nltk.stem.PorterStemmer()
    tokens = nltk.word_tokenize(text.lower())
    return [stemmer.stem(word) for word in tokens]

 
def squared_sum(x):
  """ return 3 rounded square rooted value """
 
  return round(sqrt(sum([a*a for a in x])),3)
 
def euclidean_distance(x,y):
  """ return euclidean distance between two lists """
 
  return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

def distance_to_similarity(distance):
    """ For euclidian distance to percentage"""
    return 1/exp(distance)

def cosine_similarity(x,y):
    """ return cosine similarity between two lists"""
    numerator = sum(a*b for a,b in zip(x,y))
    denominator = squared_sum(x)*squared_sum(y)
    return round(numerator/float(denominator),3)

def jaccard(reference, generated):
    sentences = [normalize(reference), normalize(generated)]
    jaccard_score = jaccard_similarity(sentences[0], sentences[1])
    return jaccard_score

def euclidian(reference, generated, type: VectorizerType):
    if type == VectorizerType.WORD2VEC:
        embeddings = [nlp(sentence).vector for sentence in [reference, generated]]
        return distance_to_similarity(euclidean_distance(embeddings[0], embeddings[1]))
    vectorizer = CountVectorizer()
    if type == VectorizerType.TFIDF:
        vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([reference, generated]).toarray()
    return distance_to_similarity(euclidean_distance(X[0], X[1]))

def cosine(reference, generated, type: VectorizerType):
    if type == VectorizerType.WORD2VEC:
        embeddings = [nlp(sentence).vector for sentence in [reference, generated]]
        return cosine_similarity(embeddings[0], embeddings[1])
    vectorizer = CountVectorizer()
    if type == VectorizerType.TFIDF:
        vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([reference, generated]).toarray()
    return cs_sim(X)[0][1]


def google_use(sentences):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
    model = hub.load(module_url)
    embeddings = model(sentences)
    similarity = cs_sim(embeddings)
    return similarity[0][1]

def stsb(sentences):
    model = SentenceTransformer('stsb-roberta-large')
    embeddings = model.encode(sentences, convert_to_tensor=True)

    similarity = []
    for i in range(len(sentences)):
        row = []
        for j in range(len(sentences)):
            row.append(util.pytorch_cos_sim(embeddings[i], embeddings[j]).item())
        similarity.append(row)
    return similarity[0][1]

def main(file1, file2):
    with open(file1, "r") as f:
        reference = f.read()

    with open(file2, 'r') as f:
        generated = f.read()
    bleu_score = sentence_bleu(reference, generated, smoothing_function=SmoothingFunction().method4)

    # Jaccard Index
    jaccard_score = jaccard(reference, generated)

    # Euclidian Distance
    euclidian_word2vec = euclidian(reference, generated, VectorizerType.WORD2VEC)
    euclidian_count = euclidian(reference, generated, VectorizerType.COUNT)
    euclidian_tfidf = euclidian(reference, generated, VectorizerType.TFIDF)

    # Cosine Similarity

    cosine_word2vec = cosine(reference, generated, VectorizerType.WORD2VEC)
    cosine_count = cosine(reference, generated, VectorizerType.COUNT)
    cosine_tfidf = cosine(reference, generated, VectorizerType.TFIDF)

    use_score = google_use([reference, generated])

    stsb_score = stsb([reference, generated])

    flesch_kincaid_1 = file1 + ": " +str(textstat.flesch_kincaid_grade(reference))
    flesch_kincaid_2 = file2 + ": " +str(textstat.flesch_kincaid_grade(generated))
    
    flesch_reading_1 = file1 + ": " +str(textstat.flesch_reading_ease(reference))
    flesch_reading_2 = file2 + ": " +str(textstat.flesch_reading_ease(generated))

    readability_1 = textstat.text_standard(reference, float_output=True)
    readability_2 = textstat.text_standard(generated, float_output=True)



    print(f"""{bleu_score=}\n{jaccard_score=}\n{euclidian_word2vec=}\n{euclidian_count=}\n{euclidian_tfidf=}\n{cosine_word2vec=}\n{cosine_count=}\n{cosine_tfidf=}\n{use_score=}
{stsb_score=}\n{flesch_kincaid_1}\n{flesch_kincaid_2}\n{flesch_reading_1}\n{flesch_reading_2}\n{readability_1=}\n{readability_2=}""")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog = 'SemanticTest',
                        description = 'Semantically compares two text files')
    parser.add_argument('file1') 
    parser.add_argument('file2')
    args = parser.parse_args()
    main(args.file1, args.file2)
