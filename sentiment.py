#results are in sentiment_results.csv

#searches the final statements for words and phrases in the dictionary files.
#keeps a count of the sentiment in each statement.
from pprint import pprint
import nltk
import yaml
import sys
import os
import re
import csv

with open('allstatements.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):

    def __init__(self):
        pass
        
    def pos_tag(self, sentences):

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_ofrem(sentiment):
    if sentiment == 'remorse': return 1
    return 0

def value_ofrel(sentiment):
    if sentiment == 'religion': return 1
    return 0

def value_ofden(sentiment):
    if sentiment == 'denial': return 1
    return 0

def rem_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_ofrem(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return rem_score(sentence_tokens[1:], current_token, acum_score + token_score)
    
def rel_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_ofrel(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return rel_score(sentence_tokens[1:], current_token, acum_score + token_score)
    
def den_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_ofden(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return den_score(sentence_tokens[1:], current_token, acum_score + token_score)


def sentimentrem_score(review):
    return sum([rem_score(sentence, None, 0.0) for sentence in review])
def sentimentrel_score(review):
    return sum([rel_score(sentence, None, 0.0) for sentence in review])
def sentimentden_score(review):
    return sum([den_score(sentence, None, 0.0) for sentence in review])



if __name__ == "__main__":
    
    myfile = open('myfile.csv','wb')
    
    
    for x in range(0, len(your_list)):
        text = str(your_list[x])

        splitter = Splitter()
        postagger = POSTagger()
        dicttagger = DictionaryTagger([ 'dicts/remorse.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml', 'dicts/religion.yml', 'dicts/denial.yml'])

    

        splitted_sentences = splitter.split(text)
        #pprint(splitted_sentences)

        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
        pprint(pos_tagged_sentences)

        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        #pprint(dict_tagged_sentences)

        print("analyzing sentiment...")
        rscore = sentimentrem_score(dict_tagged_sentences)
        rescore = sentimentrel_score(dict_tagged_sentences)
        dscore = sentimentden_score(dict_tagged_sentences)
        print(rscore)
        print(rescore)
        print(dscore)
        
        
        wrtr = csv.writer(myfile, delimiter=',', quotechar='"')
        wrtr.writerow([rscore,rescore,dscore])
        myfile.flush() # whenever you want, and/or
         # when you're don
