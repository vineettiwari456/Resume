# -*- coding:utf-8 -*-
import nltk
from nltk.tag.stanford import StanfordNERTagger
import os
from itertools import groupby
java_path = "C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"
os.environ['JAVAHOME'] = java_path
claas_file = os.path.join(os.getcwd(),'stanford-ner/english.all.3class.distsim.crf.ser.gz')
ner_file = os.path.join(os.getcwd(),'stanford-ner/stanford-ner.jar')
st = StanfordNERTagger(claas_file, ner_file)
text = 'College/Institutes Board/ University Year Aggregate B.Tech(CSE) A.I.E.T Lucknow U.P.T.U. Lucknow 2009-2013 68.92% M.Sc(Math) B.S Mehta Bharwari Kausambi C.S.J.M.U. Kanpur 2005-2007 53.80% B.Sc(PCM) R R P G Amethi Dr.R M L Avadh University Faizabad 2003-2005 51.50% H.S.C RRIC Amethi UP UP Board 2001-2002 58.40% S.S.C SSPIC Amethi UP UP Board 1999-2000 60.00% Aggregate 68.92% Branch Computer Science.'
text ='''Wayne E. Sutton

wayne_sutton158@yahoo.com
1198 Lilac Circle, Warrenton, Mo, 63383
(314) 225-6638


Objectives

To obtain gainful employment in the industrial/labor industry.

Education

Berkeley Senior High School
G.E.D 1993


Experience

9 years experience in the Labor/Industrial field.
'''
def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk

# for sent in nltk.sent_tokenize(text):
def extract_person_name_location(text):
    tokens = nltk.tokenize.word_tokenize(text)
    ne_tagged_sent = st.tag(tokens)
    print(ne_tagged_sent)
    person_name =""
    current_location = ""
    named_entities = get_continuous_chunks(ne_tagged_sent)
    named_entities = get_continuous_chunks(ne_tagged_sent)
    named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]
    if len(named_entities_str_tag)>0:
        for m in named_entities_str_tag:
            if m[1]=='PERSON':
                person_name = m[0].strip()
                break
        for nl in named_entities_str_tag:
            if nl[1]=='LOCATION':
                current_location = nl[0].strip()
                break
    print('calling NER--------',person_name.strip(),current_location.strip())
    return person_name.strip(),current_location.strip()
# print(extract_person_name_location('6541 Fairway Hill Ct mqroberge@hotmail.com Orlando, Fl 32835 Cell: 832-279-8776 Melissa Q. Burton'))