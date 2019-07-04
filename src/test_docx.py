# -*- coding: utf-8 -*-

# -*- coding:utf-8 -*-
# import nltk
# from nltk.tag.stanford import StanfordNERTagger
# import os
# from itertools import groupby
# java_path = "C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"
# os.environ['JAVAHOME'] = java_path
# claas_file = os.path.join(os.getcwd(),'stanford-ner/stanford_company_ner.ser.gz')
# ner_file = os.path.join(os.getcwd(),'stanford-ner/stanford-ner.jar')
# st = StanfordNERTagger(claas_file, ner_file)
# def get_continuous_chunks(tagged_sent):
#     continuous_chunk = []
#     current_chunk = []
#     for token, tag in tagged_sent:
#         if tag != "O":
#             current_chunk.append((token, tag))
#         else:
#             if current_chunk: # if the current chunk is not empty
#                 continuous_chunk.append(current_chunk)
#                 current_chunk = []
#     # Flush the final current_chunk into the continuous_chunk, if any.
#     if current_chunk:
#         continuous_chunk.append(current_chunk)
#     return continuous_chunk
#
# # for sent in nltk.sent_tokenize(text):
# def extract_person_name_location(text):
#     tokens = nltk.tokenize.word_tokenize(text)
#     ne_tagged_sent = st.tag(tokens)
#     print(ne_tagged_sent)
#     person_name =""
#     current_location = ""
#     named_entities = get_continuous_chunks(ne_tagged_sent)
#     named_entities = get_continuous_chunks(ne_tagged_sent)
#     named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
#     named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]
#     if len(named_entities_str_tag)>0:
#         for m in named_entities_str_tag:
#             if m[1]=='PERSON':
#                 person_name = m[0].strip()
#                 break
#         for nl in named_entities_str_tag:
#             if nl[1]=='LOCATION':
#                 current_location = nl[0].strip()
#                 break
#     print('calling NER--------',person_name.strip(),current_location.strip())
#     return person_name.strip(),current_location.strip()
text ='''
Garima Seth                                                                                                            
E-Mail:  garima.101@gmail.com , Contact: +919825526871 

Result oriented approach and having 3.2 years of IT Experience in Software Testing exposed to Manual Testing approaches for various web based applications & Overall 7.2 Years of experience. Involved in offshore assignments for providing software services to the finest global organizations.

Experience

Company : Concentrix 
Designation : Quality Analyst
Duration : October 2016 – March 2019
Project Name : Knowledge Management Tool , Noval Vox  Tool & Wheels
Detail & Domain : CRM & Telecom
Environment: SQL server 2012 & Windows XP, Windows 7, Service Now.
Project Summary: Its Knowledge Management CRM system for training and skill development platform             & resolving customer issues as per their query. It contains online portal for learning, FAQ, User Guide ,Store Address etc.
Roles & Responsibilities: 
●	Understating project requirements & specification and creating test cases and test scenarios as per sprint stories.
●	Prepare Test Cases according to Application Requirement Specification and contribute towards Test deduction.
●	After the execution, documented all the test results, defects, and prepared test reports.
●	Defect Logging, Bug Reporting, Bug Tracking, Execute User Acceptance testing (UAT).
●	Involvement in RTM Preparation.
●	Involved in a use case document & Prototype.
•	Perform Manual Testing (Functional, Regression, GUI & Compatibility Testing).
•	Involved in data Migration Testing.
•	Coordinate with peers in the team for clarity on the requirements.
•	Intensive and quick communication with developers, business and Project Managers to ensure timely delivery of functionalities.
•	Good experience in preparation, review and execution of Testing according to Testing Targets.
•	Experience in telecom & e commerce.
•	Sanity Testing & Smoke testing to ensure a ready environment.
     
Company : Getit Infomedia Services
Designation : Quality Assurance Analyst
Duration : November 2014 – August 2016
Project Name : ERP-Payment Integration
Detail & Domain : CRM, E-commerce, Finance, Payment Integration
Back End: Oracle DBA, My SQL.

Roles & Responsibilities:
Project Name: Askmebazar-CRM
Duration: November 2014 – August 2016
Role: Mobile Testing, Manual Testing, UAT, Functional Testing, Database Testing
Environment/Testing Tools: CRM, JIRA, IOS and Android 
Project Summary:  It was a CRM handling different tools, aspects and related to E-commerce 

Responsibilities:
●	Understanding project requirements and creating test cases and test scenarios as per sprint stories
●	Creating and Executing Test cases and Defect Reporting
●	Defect Regression and Defect tracking.
●	Preparation of Test plan and Test Cases based on the Test Design Specifications for Regression and Functional Testing.
●	Review of Test Design Documents, Testing Schedules.
●	Execution of test cases on software application. Identifying bug and raising defect to maintain software application Quality.
●	Sanity testing & Smoke testing to ensure a ready environment using testing tools like HP Quality Center.
●	Mentoring of newly joined associates to ensure that they learn quickly and are able to contribute in the best possible manner.
●	Intensive and quick communication with developers, business and Project Managers to ensure timely delivery of functionalities.
●	Good experience in preparation, review and execution of Testing according to Testing Targets

Company : SatSan Web Technologies
Designation: Quality Analytics
Duration :  December 2013 – October 2014

Project Name: Kittybee CRM
Domain: Social networking 
Environment: SQL Server & CRM 
Description: CRM for customer enquiry and booking. Redeem points allocation and redemption.
Integrate with IVR for automated restaurants booking.

Project: Satsan Helpdesk
Domain: Customer Support
Environment/Database: SQL Server & CRM
Project Summary :Helpdesk to support customers with products and technical queries

Roles & Responsibilities:
•	Involved in analyzing the user requirements.
•	Derived the test scenarios and designed the manual test cases.
•	Generated the test data and prepared the weekly status reports.
•	Involved in manual test execution and in various testing phases like Sanity, Functional, Retesting, System, Smoke Testing, Integration, Usability ,GUI Testing & Regression Testing
•	Involved in defect review meetings with the development team.
•	Involved in peer reviews and preparation of traceability matrix.
•	Integration testing based on business transaction scenarios.
•	Tested compatibility for different platforms as per the specifications.

Company       : Express KCS.
Designation  : Application Support Engineer
Duration        : November 2012 – November 2013

Roles & Responsibilities:
•	Providing Software support through Email, Chat, Phone & Remote Assistance on Windows systems.
•	Analyze the issue and document the issue within sheet on central storage within 36 hours.
•	Identifying the area/module where the problem is occurring & sharing with
Development Team.
•	Responsible for providing administrative support of Oracle DBA.
•	Managing DB security. Creating & assigning appropriate roles & privileges to users depending on the user activity.
•	Working on Complex SQL queries.
•	Maintaining & sharing daily reports using Oracle DBA. Monitor database events through Cacti tool.
•	Working on Linux based web/database servers & using simple Linux Commands for monitoring And Killing the processes.

Company        : Majestic IT Services Ltd.
Designation   : Research Executive
Duration         : February 2012 – October-2012

Roles & Responsibilities:
•	Providing Software support & Troubleshooting of various issues.
•	Working on Linux based web/database servers & using simple Linux Commands for monitoring & killing the processes.
•	Searching of Company details on internet. It includes Company's Name, Address, Phone Numbers, Customer Care Numbers, Business Type, Office Type, Product & Services on internet.
•	Re-Confirm/ Validate the information over the internet by surfing.
•	Convert the information into processed data on MS Excel. Adding areas & pin codes using V lookup & other MS Excel formulas.
•	 Analyzing Database for the company for different Organization and presenting a cumulative report.
•	Sourcing, Structuring and Curing Data data for different enterprises and making it appropriate for the next level.
•	Creation of searchable tags for the data- The words which are used by people to search a particular data on internet are known as tags.

SCHOLASTICS                    
DEGREE	INSTITUTE	YEAR	CGPA/Percentage
Mtech (EC)	Yamuna College Of Engineering	2014-2018	Pass-Result Awaited
Btech (EIE)	Maharishi Markandeshwar Engineering College	2007-2011	7.64/10.0
12th	Khalsa School	2006-2007	61%
10th	Sophia Girl’s High School	2004-2005	70%

                                                                                                                                                               
Regards
Garima Sethi
'''
# print(extract_person_name_location(text))
# print(extract_person_name_location('6541 Fairway Hill Ct mqroberge@hotmail.com Orlando, Fl 32835 Cell: 832-279-8776 Melissa Q. Burton'))

# 5555
# a=int(input)
# i=3
# while (i>=0):
#     j=3
#     while(j<=i):
#         print(j,end=" ")
#         j-=1
#     print()
#     i-=1
# # n=1
# for i in range(1,6):
#     # n=1
#     for j in range(i,0,-1):
#         print(j, end="")
#         # n+=1
#     print()



for i in range(1,10):
    if i<5:
        # print('NO')
        continue
    print(i)

