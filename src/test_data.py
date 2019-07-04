#-*-coding:utf-8 *-*

# import os
# gazate_file = "C:\\Users\\vktiwari\\Desktop\\gazetteer"
# lists = os.listdir(gazate_file)
# for file in lists:
#     if ".lst" in file:
#         print(file)
#         f=open(gazate_file+"/"+file,'r')
#         da = f.read()
#         # da = [m.strip()for m in f.readlines()]
#         # print(da)
#         f.close()
#         pa ="data/"+os.path.splitext(file)[0]+".txt"
#         fw = open(pa,"w")
#         fw.writelines(da)
#         fw.close()
        # break
# from dateutil.parser import parse
# print(parse('Jun 06'))



# import pandas as pd
# import numpy as np
# df = pd.Series([1,2,np.nan])
# print(df.head(1))
# print(df.index)
# print(np.random.randn(6,4))
# D12316
# import docx
#
# def getText(filename):
#     doc = docx.Document(filename)
#     fullText = []
#     for para in doc.paragraphs:
#         print(para.text)
#         fullText.append(para.text)
#     return '\n'.join(fullText)
path ="doc_file/Resume_Multiple_Email_Mobile_Rows.docx"
# print(getText(path))

import docxpy
text = docxpy.process(path)
print(text)




