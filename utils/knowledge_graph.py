
import os
IMAGE_DIR = os.path.join('static', 'media')

import spacy
from spacy.pipeline import TextCategorizer, Sentencizer
from spacy.lang.en import English
from spacy.matcher import Matcher 
from spacy.tokens import Span 
nlp = English()
nlp = spacy.load("en_core_web_sm",disable=['ner','textcat'])
nlp.max_length = 3000000
stopwords = nlp.Defaults.stop_words
tokenizer = nlp.Defaults.create_tokenizer(nlp)

import nltk
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

import time



def validateString(s):
    for ch in s:
        if ch.isalpha():
            return True
        if ch.isdigit():
          return True
    return False
    
def validateAlpha(s):
  for ch in s:
    if ch.isalpha():
      return True
  return False


def removeStop(s):
  without_stop = []
  [without_stop.append(word.text) for word in tokenizer(s) if word.text not in stopwords and word.text != '']
  return "".join(without_stop)


subjects = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
objects = ["dobj", "dative", "attr", "oprd"]

def get_entities(sent):
  if validateAlpha(sent) == True:

    entity1 = entity2 = ""
    prv_dep = prv_txt = "" 

    prefix = ""
    modifier = ""
    
    for tok in nlp(sent):
      if tok.dep_ != "punct":
        if tok.dep_ == "compound":
          prefix = tok.text
          if prv_dep == "compound":
            prefix = prv_txt + " " + tok.text
        
        if tok.dep_.endswith("mod") == True:
          modifier = tok.text
          if prv_dep == "compound":
            modifier = prv_txt + " " + tok.text
        
        if tok.dep_ in subjects:
          entity1 = modifier + " " + prefix + " " + tok.text
          entity1 = entity1.strip()
          prefix = modifier = prv_dep = prv_txt = ""      

        if tok.dep_ in objects:
          entity2 = modifier + " " + prefix + " " + tok.text
          entity2 = entity2.strip()
          prefix = modifier = prv_dep = prv_txt = ""       
          
        prv_dep = tok.dep_
        prv_txt = tok.text

    return [entity1, entity2]
  else:
    return ['','']



def get_relation(sent):
  doc = nlp(sent)
  doc
  matcher = Matcher(nlp.vocab)

  pattern1 = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},
            {'POS':'ADJ','OP':"?"}]

  matcher.add("matching_1", None, pattern1)

  pattern2 = [{'POS': 'VERB', 'OP': '?'},
           {'POS': 'ADV', 'OP': '*'},
           {'POS': 'VERB', 'OP': '+'}]

  matcher.add("matching_2", None, pattern2)
  matches = matcher(doc)
  k = len(matches) - 1
  span = doc[matches[k][1]:matches[k][2]] 
  return(span.text)



def generate_knowledge_graph(text):
  doc_title = str(time.time())
  sentencizer = Sentencizer()
  # nlp.add_pipe(sentencizer)
  doc = nlp(text)
  clean_data = []
  n=0
  for sents in doc.sents:
    if len(str(sents).replace("\n",""))>0:
          clean = str(sents).replace("\n","")
          if clean.strip()!="" and validateString(clean):
            clean_data.append(clean)
            n=n+1
  print(n)
  entity_pairs = []
  for data in tqdm(clean_data):
    entity_pairs.append(get_entities(data))
  print("\nEntity Extraction completed")

  relations = [get_relation(i) for i in clean_data]
  source = []
  target = []
  edge = []
  indexes = []

  for i in tqdm(range(len(entity_pairs))):
    if validateAlpha(entity_pairs[i][0]) and validateAlpha(entity_pairs[i][1]) and validateString(relations[i]):
      ent1 = removeStop(entity_pairs[i][0])
      ent2 = removeStop(entity_pairs[i][1])
      rel = relations[i] 
      if validateAlpha(ent1.lower()) and validateAlpha(ent2.lower()):
        source.append(ent1.lower().strip())
        target.append(ent2.lower().strip())
        edge.append("".join(rel).strip())
        indexes.append(i)
  print("\nTotal number of extracted pairs:", len(edge))
  print("\nEdges: ", edge)
  print("\nEntities: ",entity_pairs)
  if(len(edge)==0 or len(entity_pairs)==0):
    return False
  else:
    G = nx.DiGraph(directed=True)

    for i in tqdm(range(len(edge))):
      G.add_weighted_edges_from([(source[i],target[i],i)])
      
    print("\nGraph generated")
    size=20
    if len(edge)/2 > 20:
      size = len(edge)/2
    plt.figure(figsize=(size,size))
    edge_labels=dict([((u,v,),edge[d['weight']])
                    for u,v,d in G.edges(data=True)])

    pos = nx.spring_layout(G,k=0.4)
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=1000, edge_color='r', edge_cmap=plt.cm.Blues, pos = pos, font_size=11)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels, font_size=9)

    plt.title("KNOWLEDGE GRAPH FOR DOCUMENT: " + doc_title, fontdict={'fontsize': 50})
    plt.savefig(os.path.join(IMAGE_DIR,doc_title + ".png"))

    return os.path.join(IMAGE_DIR,doc_title + ".png")






