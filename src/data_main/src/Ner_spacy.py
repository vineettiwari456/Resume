# import en_core_web_sm
#
# nlp = en_core_web_sm.load()
# doc = nlp('92-P,Huda Plot ,Sec-56, Gurgaon, Abhishek Gupta  Haryana,122011 | | C: 9468422687 | | abishake287@gma')
# print(doc)
# # for token in doc:
# #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
# #           token.shape_, token.is_alpha, token.is_stop)
# print(doc.ents)
# for token in doc.ents:
#     print(token.text, token.lemma_,token.label_)

# import spacy
# # nlp = spacy.load("en_core_web_sm")
# nlp = spacy.load("C:\\Users\\vktiwari\\PycharmProjects\\Resume_Parser\\venv\\src\\model_name/en_code_web_pr")
# doc = nlp(u"Vineet Kumar Tiwari Data Scientist | Primus Software Corporation | Noida mridulsaran@outlook.com | +91 92064 37548, +91 99971 31965 Data Scientist with 3.3 years ".capitalize())
# for ent in doc.ents:
#     print( '===========',ent.text, ent.start_char, ent.end_char, ent.label_)

# from spacy.tokens import Span
#
# doc = nlp(u"FB is hiring a new VP of global policy")
# doc.ents = [Span(doc, 0, 1, label=doc.vocab.strings[u"ORG"])]
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)

# import spacy
# import random
# nlp = spacy.load("en_core_web_sm")
# train_data = [(u"Vineet Kumar Tiwari", {"entities": [(0, 19, "PERSON")]})]
#
# other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
# with nlp.disable_pipes(*other_pipes):
#     optimizer = nlp.begin_training()
#     for i in range(10):
#         random.shuffle(train_data)
#         for text, annotations in train_data:
#             nlp.update([text], [annotations], sgd=optimizer)
# nlp.to_disk("C:\\Users\\vktiwari\\PycharmProjects\\Resume_Parser\\venv\\src\\model_name/en_code_web_pr")
# #

d = {"aa": 3, "bb": 4, "cc": 2, "dd": 1}
s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=False)]
print(s)






