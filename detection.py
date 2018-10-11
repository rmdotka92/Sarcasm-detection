import nltk
from nltk.tokenize import word_tokenize
import regex as re
import random
from nltk.corpus import movie_reviews
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI
from statistics import mode
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.stem import WordNetLemmatizer


short_pos = open('short_reviews/positive.txt','r').read()
short_neg = open('short_reviews/negative.txt','r').read()
short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)
all_posneg_words = []
for w in short_pos_words:
    all_posneg_words.append(w.lower())
for w in short_neg_words:
    all_posneg_words.append(w.lower())

fd1 = nltk.FreqDist(all_posneg_words)
most_common_words = list(fd1.keys())[:5000]

docs = []
for r in short_pos.split('\n'):
    docs.append((r,'pos'))
for r in short_neg.split('\n'):
    docs.append((r,'neg'))
#
def find_posnegfeat(document):
    words = word_tokenize(document)
    features = {}
    for w in most_common_words:
        features[w] = (w in words)
    return features
#
# featsets = [(find_posnegfeat(rev), category) for (rev,category) in docs]
# random.shuffle(featsets)
# training_set = featsets[:10000]
# testing_set = featsets[10000:]
# clfposneg = nltk.NaiveBayesClassifier.train(training_set)

# save_clf = open('posnegnaivebayes.pickle','wb')
# pickle.dump(clfposneg, save_clf)
# save_clf.close()

classifier_f = open('posnegnaivebayes.pickle','rb')
clfposneg = pickle.load(classifier_f)
classifier_f.close()

########### Phase 2 ########

f = open('clean_twitDB_sarcasm.txt','r')
sarcasm_data = f.read()
f.close()
fact_data = open('clean_twitDB_fact.txt','r').read()

sarcasm_list = sarcasm_data.split('\n')
fact_list = fact_data.split('\n')

all_sents = []
for sent in sarcasm_list:
    all_sents.append((sent, 'sarcasm'))
for sent in fact_list:
    all_sents.append((sent, 'fact'))
random.shuffle(all_sents)

wnl = WordNetLemmatizer()


def all_features(sentence):
    features = {}
    split_sent = [sentence.split(' ')]
    for sent in split_sent:
        lemmas = [wnl.lemmatize(word) for word in sent]

    bigrams = nltk.bigrams(lemmas)
    bigrams = [part[0] + ' ' + part[1] for part in bigrams]

    trigrams = nltk.trigrams(lemmas)
    trigrams = [part[0] + ' ' + part[1] + ' ' + part[2] for part in trigrams]

    for feat in bigrams:
        features['contains({})'.format(feat)] = True

    for feat in trigrams:
        features['contains({})'.format(feat)] = True

    length = len(lemmas)
    seg_1 = lemmas[:int(length/2)]
    seg_2 = lemmas[int(length/2):]
    seg1str = ''.join(seg_1)
    seg2str = ''.join(seg_2)
    features['sentiment'] = clfposneg.classify(find_posnegfeat(seg1str)) == clfposneg.classify(find_posnegfeat(seg2str))
    return features

featset = [(all_features(w), category) for (w, category) in all_sents]
print(featset[0])
training_set = featset[:3000]
testing_set = featset[3000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print(nltk.classify.accuracy(classifier, testing_set))
classifier.show_most_informative_features(50)

print(classifier.classify(all_features('Watch out ! We got a badass over here !')),'detected!')
print(classifier.classify(all_features('Is this sarcasm ?')),'detected!')

# print(classifier.classify(all_features('That is a thing actually')),'detected!')
# print(classifier.classify(all_features('So lovely to be discriminated against')),'detected!')
# print(classifier.classify(all_features('Dogs love to eat feces')),'detected!')



