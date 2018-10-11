import nltk
from nltk.tokenize import word_tokenize
import regex as re

def preprocess(file, hashtag):
    file_open = open(file +'.txt', 'r').read().lower()
    replaced = file_open.replace('"','\'')
    split = replaced.split("'\nb'")
    conditional_sent = []
    for sent in split:
        if re.search(hashtag, sent, re.I) is not None:
            conditional_sent.append(sent)

    #Grammar definition
    remove_hashtags = re.compile(r'#+\w+[\s\'":! ]?', re.I)
    remove_newline = re.compile(r'\\n', re.I)
    remove_friendtag = re.compile(r'@\w+\s?')
    remove_links = re.compile(r'[htps:]+\/\/[a-z.-]+\/[a-z0-9.?/]+', re.I)
    remove_punctuation = re.compile(r'[,?!.-:;$*]+')

    clean_data = []
    for line in conditional_sent:
        tmp = remove_hashtags.sub('', line)
        tmp = remove_friendtag.sub('',tmp)
        tmp = remove_links.sub('',tmp)

        words = word_tokenize(tmp)
        alpha_words = [w for w in words if w.isalpha()]
        if len(alpha_words) > 4:
            tmp = remove_newline.sub('',tmp)
            tmp = remove_punctuation.sub(' ',tmp)
            tmp_str = ' '.join(tmp.split())  # remove useless space
            if tmp_str not in clean_data:
                clean_data.append(tmp_str)

    test = '\n'.join(clean_data)
    saveFile = open('clean_'+ file +'.txt', 'a')
    saveFile.write(test)
    saveFile.write('\n')
    saveFile.close()

preprocess('twitDB_fact', r'#fact')
preprocess('twitDB_sarcasm', r'#sarcasm')
