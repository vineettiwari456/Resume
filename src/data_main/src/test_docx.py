# -*- coding: utf-8 -*-
from docx import Document
import sys
import os
import re

# ini_dict ={'monsterindia.com': {0}, 'monster worldwide': {139}, 'monster.com': {400, 593, 74}, 'dimension india': {704, 788}}
# print(ini_dict.keys())
# tmp= {}
# tmp_dict = {}
# for j in ini_dict.keys():
#     print(j)
#     if j[:7] in tmp.keys():
#         tmp_dict[tmp[j[:7]]].extend(list(ini_dict[j]))
#         tmp_dict[tmp[j[:7]]] = tmp_dict[tmp[j[:7]]]
#     else:
#         tmp_dict[j]=list(ini_dict[j])
#         tmp[j[:7]]=j
# print(tmp_dict)
# t = [1, 3, 6]
#
# p = {j:j-i for i, j in zip(t[:-1], t[1:])}
# print(p)
raw_dat ="""Abhinandan Malhotra
SKILLED ENGINEER WITH A KEEN INTEREST IN MATHEMATICAL MODELING & DATA ANALYSIS

97, Bank Enclave, Laxmi Nagar, Delhi, New Delhi 110092, India
 (+91) 9891949473

|

 abhinandan.malhotra@gmail.com

Professional Summary
Results driven data science professional with mathematical modeling & analytical skills, an advanced degree in engineering and looking for data driven decision making roles. Creative, pragmatic and proactive problem solver. Organized and
attentive to detail with demonstrated time management , data analysis & quantitative skills gained from previous work experience. Skilled in machine learning, numerical/quantitative methods, statistics and programming. Dynamic Oral, Writing,
Interpersonal and Presentation skills.

Education
IIST(Indian Institute of Space Science and Technology), DoS
M.TECH IN AEROSPACE ENGINEERING

Kerala, India
Aug. 2013 - July. 2015

• Ranked among the top 5 students in my M.Tech Class. GPA of 8.31
• Master’s Project : Emphasis on Quantitative Analysis of large experimental data sets including Time-Frequency Analysis, Statistical Analysis, Uncertainty Analysis, Signal Processing & Design of Data collection and analysis procedure. (For Master’s
Thesis).
• Mathematical modeling for solving differential/integral equations using Numerical methods like finite difference and finite
volume methods for problems in engineering domain.
• Secured 99 percentile in GATE (a national level exam) out of a total of 163000+ students to get admission in M.Tech course.

Guru Gobind Singh Indraprastha University
B.TECH IN MECHANICAL ENGINEERING

Delhi, India
Aug. 2007-June 2011

• Secured 78.41 % during B.Tech
• Ranked in the top 10% students throughout my B.Tech out of a class of around 80 students.

Experience
Tango IT Solutions Private Ltd, Chennai

Chennai, India

DATA SCIENTIST

March. 2018 - Current

• Fulfilled all data science duties for the firm, serving clients like National Payments Corporation of India (NPCI), Unified Payments Interface (UPI) etc. leveraging AI/ML techniques for an improved end-user experience.
• Created and presented models for data ranging from network logs, system logs, financial data, transaction data etc.
• Created models that monitor, analyze and predict insights and patterns from data as per business requirements using machine learning algorithms, time series techniques and have also worked extensively with anomaly detection & dimensionality
reduction techniques.
• Worked on creating Proof of Concept (PoC) models as well as reproducing novel ML/Deep Learning algorithms from research
papers to be implemented for the business use cases.
• Working with deep learning in a computer vision project for a client in the area of security and access control.

Indian Institute of Science, Bangalore

Bengaluru, India

RESEARCH/PROJECT ASSOCIATE

July. 2017 - February,2018

• Worked in the High Speed research lab at Indian Institute of Science on multiple government funded projects from agencies
such as DRDO, ISRO, Brahmos for research in the aerospace domain.
• Worked in the area of scientific computing, developing computational mathematics codes for sets of partial differential equations for fluid mechanics and using numerical techniques like finite difference methods, finite volume methods.
• Performing statistical analysis of large experimental data sets, and implemented data driven & mathematical methods like
optimization for best design and Machine Learning methods for prediction of performance parameters.
• Preliminary analytical model development for a new type of engine and it’s parametric study.
• Developing computational models simulating the experimental systems using commercial/Open source softwares and writing in-house codes.

Indian Institute of Technology, Delhi

New Delhi, India

SENIOR RESEARCH FELLOW

Sept. 2015 - 2017

• Developed mathematical and quantitative models for predicting the performance parameters for improved process.
• Performed Primary and Secondary research for developing the mathematical models and carried out statistical analysis of
collected data to predict an empirical model for the involved parameters.
• Statistical Analysis of large scale experimental data sets and their corroboration with model data.
• Development of transient numerical models using commercial packages as well as making in-house computational codes
(MATLAB/C++) for solution of a system of conjugate partial differential equations.
• Prepared presentations, abstracts, and reports.

OCTOBER 25, 2018

ABHINANDAN MALHOTRA · RÉSUMÉ

1


Indian Institute of Space Science and Technology
GRADUATE TEACHING ASSISTANT

Kerala, India
Aug. 2013 - July. 2015

• Worked in the Mathematical Modeling Simulation and Analysis lab as a teaching assistant and was involved in the numerical
modeling of differential equations and development of associated mathematical models for flight trajectory, shell trajectory
& other numerical methods and their grading for undergraduate students.
• Designed course materials, led discussion sessions, maintained correspondence with undergraduate students and organized
lectures.

Mahindra & Mahindra Ltd.

Chennai, India

ASSISTANT MANAGER (VEHICLE INTEGRATION DIVISION (NEW PROJECTS)

Aug. 2011 - Oct. 2012

• Liaised directly with multiple departments as a Vehicle Integration resource to achieve safe component placement (engine,
suspension etc.) for a new design proposal in line with the government regulations, capacity constraints, vehicle class etc.
• Concept Design and Feasibility studies for a new class of vehicle, benchmarking studies & design proposals according to Govt.
regulations (CMVR rules) and making layouts in CATIA & CAVA and their presentation to senior management.
• Identification of benchmark vehicles for data Collection and the Qualitative & Quantitative analysis of the collected vehicle
data.
• Involved with the analytics team to understand the future trends and customer demands & prepared reports and presentations for the team.

Skills
MATLAB, Python (NumPy, Pandas, scipy, scikit-learn, Matplotlib, Jupyter, Plotly, Seaborn etc.), C/C++, Octave, SAS, Advanced Excel, MS-Office Suite, SQL, Data Analysis, Mathematical modeling, Linear Algebra, Statistics and Probability, numerical methods, time-series analysis, Optimization techniques, Signal processing techniques, Machine Learning Algorithms
(Supervised, Unsupervised and dimensionality reduction techniques).
TensorFlow and Keras (for Deep Learning).

Honors & Awards
AWARDS & CERTIFICATIONS
2013-15
2016
2017
2017
2017
2018

MHRD GATE Scholarship, Ministry of Human Resources Development, GoI
2nd best Poster award at 4th National Symposium on Shock Waves.,
Statistical Analysis, ANOVA, Regression and Logistic Regression, SAS Academy e-course
Introduction to Statistical Concepts, SAS Academy e-course
Python for Data Science, University of Michigan, MOOC
Deep Learning Specialization: Set of 5 deep learning courses, deeplearning.ai

99 Percentile
SAS e-learning
SAS e-learning
Coursera
Coursera

HONORS
Authored papers in international journals and presented my work in conferences & symposiums to eminent personalities of
the engineering domain in areas of signal processing and analysis, and statistical analysis of experimental datasets.

OCTOBER 25, 2018

ABHINANDAN MALHOTRA · RÉSUMÉ"""
# print(raw_dat)
#
#
#
#
# d ="""(((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{2,4}|(\d{1,2}\s*)?(-)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,|-)\s*\d{2,4})"""
# print(d.lower())
#
# data ="careers in data careers"
# data_find = "career"
# print(data.index(data_find))
# offsets = [i for i in range(len(data)) if data.startswith(data_find, i)]
# offsets_withid = {data_find: i for i in range(len(data)) if data.startswith(data_find, i)}
# print(offsets,offsets_withid)
# import re
#
# string = 'This is laugh laughing laugh'
#
# a = re.search(r'\b(laugh)\b', string)
#
# print(a.start())
# import re
# m = [m.start() for m in re.finditer('((careers)\b)', 'careers in data careers')]
# print(m)


# def find_all(a_str, sub):
#     start = 0
#     while True:
#         start = a_str.find(sub, start)
#         if start == -1: return
#         yield start
#         start += len(sub) # use start += 1 to find overlapping matches
#
# print(list(find_all('careers in data careers', 'career')))

# import re
#
# s = 'careers in data careers'
# for words in ['careers']:
#     if re.search(r'\b' + words + r'\b', s):
#         print('{0} found'.format(words))
#         print(re.search(r'\b' + words + r'\b', s).start())

word = 'careers in data careers'
# tmp = 0
# index = []
# for i in range(len(word)):
#    tmp = word.find('career', tmp)
#    if tmp >= 0:
#        index.append(tmp)
#        tmp += 1
#
# print(index)
print({g.group():g.start() for g in re.finditer('\\b(career)\\b',word)})
m = '''| |Apr 2017 to Till Date Times | |Internet Ltd. | |Product Manager | |Roles |Responsible for product strategy of the ET Rise Biz Listings, release | |& |level feature choice and whole product thinking. | |Responsibil|- Worked with internal business team and UI team and successfully | |ities |revamped the complete Mobile site UI. | | |- Was involved in finalizing wire frames, basic theme and UI screens. | | |API integration to keep app and web in | | |sync. | | |Taking care of user on-boarding, profiling & user experience of buyers | | |and Service providers on ET Rise Biz Listings platform. | | |Designed the complete Lead Management system which include Lead | | |distribution workflow, Lead Management and Feedback Management. | | |- Developed strategies for user acquisition, engagement and retention | | |features/enhancements. | | |Using Google Analytics and other tools to enhance content, landing pages,| | |customer conversion funnel and market communication. | | |- Preparing timely reports to carry out data analysis on monitor micro | | |and macro conversions. | |Mar 2016 to Apr 2017 NDTV | |Assistant Product Manager | |Roles |Responsible for product strategy of the bandbaajaa.com, release level | |& |feature choice, economic rationale for every major effort and whole | |Responsibil|product thinking. | |ities |Introduced and implemented user centered design with defining conversion | | |parameters. Regular monitoring of Internet Traffic, Bounce Rate, Site | | |performance, revenue and conversion. | | |Major areas include creating wireframes, usability testing, A/B testing, | | |site analytics, bugs handling | | |Work closely with all the cross-functional teams to get the task done and| | |deliver the project within the timeline. | | |Proactively identify and resolve strategic issues and risks that may | | |impact the teams ability to meet goals. | | |Designed the complete lead management console for vendors to stay on top | | |of leads generated for them thereby resulting in 50% higher conversions | | |and vendor lead panel for the Vendors. | | |Spearheaded implementation of Financial Reconciliation module, which | | |enabled team to reconcile entries with auto-generated reports resulting | | |in 80% savings in vendor remittances & refunds leakages, vernacular | | |(Hindi) support to target NDTV Hindi audience. | |Feb 2014 to Feb 2016 IndiaMART | |InterMESH Ltd. Assistant Product Manager | |Roles |To create a roadmap for the product and plan new ideas with proper gap | |& |analysis and after impact analysis | |Responsibil|Improve the existing product by implementing new features depending on | |ities |the market & customer needs. | | |Redesigned and redeveloped the whole Buy Lead approval CRM and reduced | | |the AHT of the agents. | | |Built the complete online OVP process from scratch and closely monitored | | |and analyzed the data to increased the online OVP success rate from 20% | | |to 75% | | |Define success metrics & reports for analysis to monitor post-launch | | |performance of Features/enhancements. | | |Analyze data to understand user behaviour and use the insights to improve| | |the product continuously. | |Apr 2013 to Jan 2014 Zealicon | |Technologies Assistant Manager Product & Marketing | |Roles |Responsible for managing the complete SDLC & maintenance post launch. | |& |Conceptualizing and developing new products for various media platforms | |Responsibil|and Devices – for Mobile and Web. | |ities |Modifications/Enhancements in existing products to increase revenue | | |Worked closely with the Designers, Technical team and Content Writers to | | |get the task done. | |Jan 2011 to Apr 2013 One97 | |Communications Ltd ( Paytm ) Associate Products | |Roles |Ideation and Brain Storming for new product solutions apt for non-telecom| |& |industries. | |Responsibil|Designing of new products for different industry segments based on | |ities |requirement, target segment and the access points available to the end | | |customers. | | |Integration of Paytm payment gateway in M-commerce Products. | | |Managed and facilitated the technical development of applications in | | |coordination with Engineering team. | | |Ideation and deployment of M- commerce IVRs for various Enterprise | | |Clients. | | |Modifications/Enhancements in products for Innovations and Revenue | | |Enhancement. | |',
  'Profile_Name': 'Akshay Kumar Tank +918800161188 akshaykumartank@gmail.com |'''
print(m.replace('|',''))


