"""Some language tools for the extraction of semantic head, lemmatization, ..."""
import json
import spacy
import graphviz
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES


class LanguageUtils(object):

    def __init__(self, language):
        self.nlp = spacy.load(language)
        self.lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    
    def semantic_head(self, text):
        """Extracts the semantic head, as a single word"""
        return str(list(self.nlp(text).sents)[0].root)
    
    def lemmatize(self, word):
        """Returns the lemma from the given words"""
        return self.lemmatizer(word, 'NOUN')
    
    def semantic_head_lemmatize(self, text):
        head = list(self.nlp(text).sents)[0].root
        lemma = head.lemma_
        if lemma == '-PRON-':
            # https://github.com/explosion/spaCy/issues/31
            if head.text in ('I', 'me', 'you', 'he', 'she', 'we', 'us', 'you', 'they', 'them'):
                lemma = 'person'
            elif head.text in ('it'):
                lemma = 'thing'
        return lemma


class HuricUtils(object):

    def __init__(self):
        with open('data/huric_alexa.json') as f:
            content = json.load(f)
        
        self.frame_elements = {}
        for t in content['interactionModel']['languageModel']['types']:
            self.frame_elements[t['name']] = [el['name']['value'] for el in t['values']]

    def get_frame_elements_values(self, frame):
        return self.frame_elements[frame]

class GraphUtils(object):

    def __init__(self):
        pass

    def create_graph(self, edges_list, clean_name_fn=lambda a: a):
        """sub_uri_count is how many last components in the URI to keep """
        graph = graphviz.Digraph('dot') # format='svg' or 'dot'
        nodes = set()
        for a_uri, b_uri, label in edges_list:
            a, b = clean_name_fn(a_uri), clean_name_fn(b_uri)
            nodes.add(a)
            nodes.add(b)
            graph.edge(a, b, label)
        
        for n in nodes:
            graph.node(n)
        
        return graph