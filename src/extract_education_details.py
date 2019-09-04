# -*- encoding:utf-8 -*-
import time
import re, ast
import string
from nltk import ngrams
import copy
from dateutil.parser import parse


class EducationDetails:
    def __init__(self):
        self.colleges_dict = {}
        self.board_dict = {}
        self.highest_qualification_dict = {}
        self.designation_dict = {}
        self.punchuation = string.punctuation
        self.qualification_master_data={}
        self.colleges_master_data={}
        self.read_data()

    def make_n_grams_dict(self, skills_list, tmp_dict):
        for skill in skills_list:
            temp_skill = re.sub(r'[^\w\s]', ' ', skill)
            temp_skill = temp_skill.split(' ')
            temp_skill = temp_skill[0]
            try:
                tmp_dict[temp_skill].append(skill)
            except:
                tmp_dict[temp_skill] = [skill]

    def read_data(self):
        fcollege = open("education_data/all_colleges")
        colleges = ast.literal_eval(fcollege.read())
        fcollege.close()
        fschool = open("education_data/all_schools_list")
        colleg = ast.literal_eval(fschool.read())
        colleges.extend(colleg)
        fschool.close()
        fcoll = open("education_data/college")
        collgs = list(set([m.strip().lower() for m in fcoll.readlines()]))
        fcoll.close()

        colleges.extend(collgs)
        print(len(colleges))
        # self.make_company_dict(companies,self.company_dict)
        self.make_n_grams_dict(list(set(colleges)), self.colleges_dict)

        # skilldata = open("data_main/skill")
        # skillset = ast.literal_eval(skilldata.read())
        # skilldata.close()
        # # self.make_n_grams_dict(skillset, self.skills_dict)
        # self.make_n_grams_dict(skillset, self.skills_dict)
        fboard = open("education_data/education_board")
        boards = list(set([m.strip().lower() for m in fboard.readlines()]))
        fboard.close()
        self.make_n_grams_dict(boards, self.board_dict)
        highest_qualifications = []
        fhighestquali = open("education_data/highest_qualification")
        highest_qualifications.extend([m.strip().lower() for m in fhighestquali.readlines()])
        fhighestquali.close()
        self.make_n_grams_dict(list(set(highest_qualifications)), self.highest_qualification_dict)
        qualificationfile = open("uuid/highest_qualification_uuid", encoding='ISO-8859-1')
        self.qualification_master_data = ast.literal_eval(qualificationfile.read())
        qualificationfile.close()
        collegesfile = open("uuid/colleges_uuid", encoding='ISO-8859-1')
        self.colleges_master_data = ast.literal_eval(collegesfile.read())
        collegesfile.close()

    def get_years(self, raw_text):
        years = []
        # regex =r"((((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{2,4}|(\d{1,2}(\/|-)\d{1,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{4})\s*(to till|to|-|To|TO|-|–)?\s*((((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|(Present|till|Till|PRESENT|current|Current|CURRENT))?)".lower()
        regex = r"((since)?\s*?(((\d{1,2}\s*)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\s)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)(-|.)\s*\d{2,4}|(\d{1,2}(\/|-)\d{1,4})|(\d{4}(\/)\d{1,2})|(\b(\d{4})\b)|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?(,)\s\d{4})\s*(to till|to|-|to|to|-|–)?\s*((((\d{1,2}\s*)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\s)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)(-|.)\s*\d{2,4}|(\d{4}(\/)\d{1,2})|(\b(\d{4})\b)|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?(,)\s\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|\b(19|20)\d{2}|(present|till|till|present|current|current|current|ongoing))?)".lower()
        rawyear = re.findall(
            regex,
            raw_text.lower().replace("th", '').replace(",", ''))
        # print(rawyear)
        if len(rawyear) > 0:
            for yr in rawyear:
                try:
                    # dt = parse(yr[0])
                    # date_time_obj =str(dt.year)+":"+str(dt.month)+":"+str(dt.day)
                    # years.append(date_time_obj)
                    if len(re.findall(r"(\d{4})",str(yr[0])))>0:
                        years.append(yr[0].strip())
                except:
                    pass
        return years

    def get_all_index(self, data, data_find):
        offsets = [i for i in range(len(data)) if data.startswith(data_find, i)]
        offsets_withid = {i: data_find for i in range(len(data)) if data.startswith(data_find, i)}
        # offsets_withid = {data_find: i for i in range(len(data)) if data.startswith(data_find, i)}
        # offsets_withid = {g.group().strip(): g.start() for g in re.finditer('\\b' + (data_find) + '(?!,|\))\\b', data)}
        # offsets = [g.start() for g in re.finditer('\\b' + (data_find) + '(?!,|\))\\b', data)]
        return offsets, offsets_withid

    def get_index_value(self, keyword_list, main_string):
        dict_list = {}
        for kl in keyword_list:
            word_indexs, offsets_id = self.get_all_index(main_string, kl)
            # print(word_indexs, offsets_id)
            if len(word_indexs) > 0:
                rawli = sorted(list(offsets_id.keys()))
                if len(rawli)>1:
                    dict_list.update({rawli[0]:offsets_id.get(rawli[0])})
                else:
                    dict_list.update(offsets_id)
        return dict_list

    def sepertation_string(self, degree_index):
        new_degree_list = []
        for i, j in enumerate(degree_index):
            try:
                new_degree_list.append([degree_index[i], degree_index[i + 1]])
            except:
                new_degree_list.append([degree_index[i]])
        return new_degree_list

    def found_year_college_board(self, string1, is_temp=False):
        string1 = str(string1).lower()
        years_only = self.get_years(string1)
        temp_str = re.sub(r'[^\w\s]', ' ', string1)
        temp_str = temp_str.split(' ')
        colleges_only = []
        boards_only = []
        string_coll = copy.deepcopy(string1)
        for word in temp_str:
            try:
                if not is_temp:
                    all_boards = self.board_dict[word]
                    all_boards.sort(key=lambda s: len(s), reverse=True)
                    for sk_ in all_boards:
                        # if (sk_ in string) and (sk_ not in designation_only) and len([g.start() for g in re.finditer('(\()?\\b' + (sk_) + '(?!,|\))\\b(\))?', string)])>0:
                        regex = "\\b(" + sk_ + ")\\b"
                        # print(regex)
                        if (sk_ in string1) and (sk_ not in boards_only) and len(
                                [g.start() for g in re.finditer(regex, string1)]) > 0 and (
                                sk_ not in ' '.join(boards_only)):
                            boards_only.append(sk_)
            except Exception as e:
                # print(e)
                pass
            # try:
            #     all_colleges = self.colleges_dict[word]
            #     all_colleges.sort(key=lambda s: len(s), reverse=True)
            #     for chunks in all_colleges:
            #         for i in reversed(range(1, 11)):
            #             sixgrams = ngrams(chunks.split(), i)
            #             for grams in sixgrams:
            #                 sk_ = " ".join(grams)
            #                 # print(sk_)
            #                 regex = "\\b(" + sk_ + ")\\b"
            #                 # print(regex)
            #                 if (sk_ in string_coll) and (sk_ not in colleges_only) and len(
            #                         [g.start() for g in re.finditer(regex, string_coll)]) > 0 and (
            #                         sk_ not in ' '.join(colleges_only)):
            #                     colleges_only.append(sk_)
            #                     string_coll = re.sub(sk_,' ',string_coll)
            # except Exception as e:
            #     # print(e)
            #     pass
            try:
                all_colleges = self.colleges_dict[word]
                all_colleges.sort(key=lambda s: len(s), reverse=True)
                for sk_ in all_colleges:
                    regex = "\\b(" + sk_ + ")\\b"
                    # print(regex)
                    if (sk_ in string1) and (sk_ not in colleges_only) and len(
                            [g.start() for g in re.finditer(regex, string1)]) > 0 and (
                            sk_ not in ' '.join(colleges_only)):
                        colleges_only.append(sk_)
            except Exception as e:
                # print(e)
                pass
        # print(colleges_only, boards_only, years_only)
        return colleges_only, boards_only, years_only

    def get_individual_year(self,raw_year):
        val_date = ""
        try:
            temp_date = []
            regex = r"(\b(\d{4})\b)"
            rawyears = re.findall(
                regex,
                raw_year.replace("th", ' ').replace("nd", ' ').replace(",", ""))
            # print(rawyear)
            if len(rawyears) > 0:
                for j in rawyears:
                    if int(j[0])>1800:
                        temp_date.append(int(j[0]))
            val_date = str(max(temp_date))
        except:
            pass
        return val_date


    def mapping_degree_college_year(self, degree_list, main_string):
        education_list = []
        # degree_keyword_index = {}
        degree_keyword_index = self.get_index_value(degree_list, main_string)
        degree_index = sorted(degree_keyword_index.keys())
        new_degree_list = self.sepertation_string(degree_index)
        is_start = False
        k=0
        tmpcoll = ""
        for i, mk in enumerate(degree_index):
            # print(i)
            dict = {}
            qualification_name = degree_keyword_index.get(mk, '')
            dict["highestQualification"] = {"name":qualification_name,"uuid":self.qualification_master_data.get(qualification_name,"")}
            indexval = new_degree_list[i]
            is_check = False
            temp_str = ""
            if len(indexval) == 2:
                if indexval[0]>20  and (is_start or i==0):
                    check_year_st = self.get_years(main_string[indexval[0]-20:indexval[0]])
                    if len(check_year_st)>0:
                        if i==0:
                            is_start = True
                        separte_string = main_string[indexval[0]-20:indexval[1]]
                    else:
                        separte_string = main_string[indexval[0]:indexval[1]]
                else:
                    separte_string = main_string[indexval[0]:indexval[1]]
                if indexval[0]>35:
                    temp_str = main_string[indexval[0] - 35:indexval[1]]
            elif len(indexval) == 1:
                if len(new_degree_list)==1:
                    separte_string = main_string
                    is_check = True
                elif indexval[0]>20 and not is_check and is_start:
                    check_year_st = self.get_years(main_string[indexval[0]-20:indexval[0]])
                    if len(check_year_st)>0:
                        separte_string = main_string[indexval[0]-20:]
                    else:
                        separte_string = main_string[indexval[0]:indexval[0]+150]
                else:
                    separte_string = main_string[indexval[0]:indexval[0]+150]
                if indexval[0]>35:
                    temp_str = main_string[indexval[0] - 35:]
            # print('++++++: ',separte_string)
            # separte_string = re.sub(qualification_name,' ',separte_string)
            coll, board, year = self.found_year_college_board(separte_string)
            # print('---------',coll)
            # if len(coll)>1:
            #     ds = coll[-1].split()
            #     if len(ds)>=3:
            #         k=i+1
            #         tmpcoll = coll[-1]
            #         coll=coll[:-1]
            if len(coll)==0:
                coll, boards, yearls = self.found_year_college_board(temp_str, is_temp=True)
            # print('=====',coll)
            # if len(coll)>1:
            #     coll_name = ' '.join(coll[:1])
            # else:
            coll_name = ', '.join(coll)
            # if i==k:
            #     coll_name = tmpcoll
            dict["college"] = {"name":coll_name,"uuid":self.colleges_master_data.get(coll_name,'')}
            if len(year)>0:
                dict["yearOfPassing"] = self.get_individual_year(str(year[0]).strip())
            else:
                dict["yearOfPassing"] = ''
            dict["board"] = ' '.join(board)
            education_list.append(dict)
        return education_list

    def found_educations(self, string):
        string1 = ' '.join(str(string).lower().split()).replace("highschool","high school").replace("10+2","12th").replace("(10)","10th")
        # print(string1)
        string2 = copy.deepcopy(string1)
        temp_str = re.sub(r'[^\w\s]', ' ', string1)
        temp_str = temp_str.split(' ')
        highest_degree_only = []
        for word in temp_str:
            try:
                all_qualifications = self.highest_qualification_dict[word]
                all_qualifications.sort(key=lambda s: len(s), reverse=True)
                for sk_ in all_qualifications:
                    # if (sk_ in string) and (sk_ not in designation_only) and len([g.start() for g in re.finditer('(\()?\\b' + (sk_) + '(?!,|\))\\b(\))?', string)])>0:
                    regex = "\\b(" + sk_ + ")\s*\\b"
                    # print(regex)
                    #and len([g.start() for g in re.finditer(regex, string1)]) > 0 and (sk_ not in ' '.join(highest_degree_only))
                    if (sk_ in string1) and (sk_ not in highest_degree_only):
                        highest_degree_only.append(sk_)
                        string1 = re.sub(sk_,' ',string1)
            except Exception as e:
                # print(e)
                pass
        final_dict = self.mapping_degree_college_year(highest_degree_only, string2)
        return final_dict


if __name__ == "__main__":
    ts = time.time()
    obj = EducationDetails()
    text = """jul 17, 2017 - present associate software engineer appster, gurgaon project description ejogajog (gim) description  goods in motion (gim) is an online platform that books transportation online, connecting transporters with customer. gim focuses on bridging the gap between smes, large enterprises and individuals with transporters. duration  june 2018 - present role  java developer technology used  java8 (backend apis), angular js(web) & android(mobile app), aws services (server, rds, s3 bucket), fcm push, j-unit testing, sendgrid mail service, ssl commerz sms service site  https//gim.com.bd/ momentor description  momentor lets you explore events happening around you. you can create events and the people matching your defined interests can only see the event. a better way to ensure you are meeting and planning an activity of like minded people. duration  april 2018 - june 2018 role  java developer technology used  java8 (backend apis), android & ios (mobile app), aws services (server, rds, s3 bucket), fcm & apns push services, sendgrid mail service site  https//prod.momentor.com.au/momentor/ nos (network of sobriety) description  nos is a platform to help drug addicts to achieve sobriety by keeping track of their daily exercises & routine. sharing the updates with an accountability partner to keep him/her aware of their patients condition and level of sobriety. duration  november 2017 - february 2018 role  java developer technology used  java8 (backend apis), android & ios (mobile app), angular js (admin cms) , aws services (server, rds, s3 bucket), sns mobilepush service, twilio sms service modurn description  the modurn collection is a contemporary and thoughtful way to honour a life. together with innovative design and technology, families can store and share a loved one's life story, today and for future generations. the urns and mementos act as beacons that can alert your device to a near by loved one or life story. duration  august 2017 - october 2017 role  java developer technology used  java8 (backend apis), ionic (hybrid mobile app), aws services (server, rds, s3 bucket), fcm & apns push services site  https//www.modurngroup.com/ https//www.visualcv.com/abhinav_verma core java server management effective communication spring mvc junit team leadership hibernate flyway integration research & analysis mysql database j-meter management project management aws management sonarqube handling process improvements eclipse mysql workbench postman swagger j-meter"""
    text = " Year Aggregate B.Tech(CSE) a.i.e.t Lucknow U.P.T.U. Lucknow 2009-2013 68.92% M.Sc(Math) B.S Mehta Bharwari Kausambi C.S.J.M.U. Kanpur 2005-2007 53.80% B.Sc(PCM) R R P G Amethi Dr.R M L Avadh University Faizabad 2003-2005 51.50% H.S.C RRIC Amethi UP UP Board 2001-2002 58.40% S.S.C SSPIC Amethi UP UP Board 1999-2000 60.00% Aggregate 68.92% Branch Computer Science."
    text = "EDUCATION 2011- 2013 M.S. COMPUTER SCIENCE, UNIVERSITY OF NEW ORLEANS NEW ORLEANS, LA 2004-2006 M.S. COMPUTER SCIENCE, UNIVERSITY OF PUNE PUNE, INDIA 2000-2003 SKILL SET B.S. COMPUTER SCIENCE, UNIVERSITY OF PUNE PUNE, INDIA "
    text = "Orissa Engineering College (Biju Patnaik University of Technology) Bhubaneswar, India B.TECH. IN MECHANICAL ENGINEERING Aug. 2012 - May. 2016"
    # text = "Bachelor of technology in (computer science and engineering) MallareddyCollege of Engineering 2017 with 70%. Intermediate from ShanthiJr.College 2013 with 80%. SSC from Z.P.S.S MutharamSchool in 2011 with 79%. TITLEMOBILE QUICK SURF Project DescriptionThis project is just like a mobile application it will able to provide the group of information together. The project Mobile Quick Surf is a personal easy search option for mobile user. This Android based application provides Good User Interface to search options like contacts, A customized to-do list by the user ,audio files and video files captured by user as well as in built this gives a mash up kind of look with integrated search. TITLE STUDENT MSNAGEMENT SYSTEM Project DescriptionThis is an android application use to maintain over all student information. Instead of maintain the web sites. It gives complete details, course details, academic details;day-to-day monitoring of the attendance and it tracks the progress of the student in the course. Student Management System is an automated version of manual. Student Management System which conveys the events, External Time Schedule, Results of external and internal are shown in form of notification. It is having three modules i) Faculty module ii) admin module iii) student module. In this application student cannot modify the data. Only faculty or admin can login and update the data. Student also having separate login details to check the details. ROLES AND RESPONSIBILITIES I had been the team lead for the team of 4 members I had collected the modules and distributed the work within team members. I had taken the responsibility of submitting the project within the given time. "
    # text = "Coin Collection (Collected 1200 coins of more than 30 Countries) 2011 - 2015 Bachelor of Technology Computer Science & Engineering • College Birla Institute of Applied Sciences, Bhimtal, Nainital, Uttarakhand • Aggregate Percentage 80.02% 2009 - 2010 Class 12th • School K.V. No. 2, J.L.A., Bareilly, Uttar Pradesh EDUCATION • Aggregate Percentage 70.33% 2007 - 2008 Class 10th • School K.V. No. 2, J.L.A., Bareilly, Uttar Pradesh • Aggregate Percentage 80.20%"
    # text = "964 w ambassador dr. 559-410-7528 tylerjcalderon@yahoo.com tyler calderon objective to gain a position in your establishment, and to have the opportunity to acquire new knowledge and skills. education highschool diploma hanford west high school 1150 w lacey blvd, 93230 xxxxxxxxxxxxxx"
    text = "experience click labs, chandigarh, india jan 2017 – may 2017 nodejs developer qualification master of computer applications (2015-2017)- 75% graphic era university, dehradun bachelor of computer applications (2012-2015) - 70% d.s.b campus, kumaun university, nainital hemann gmeiner school(bhimtal)(10+2) – 64% from cbse maharishi vidya mandir((bhowali)(10) – 70% from cbse permanent address parvati vihar, nainiband, bhowali (ntl), uttarakhand -263132 correspondent address gali no.7 , govindpuri kalkaji south delhi - 110019 date 2 april 2019 pankaj sunal contact: +91-7830265384 email id: pankajsunal66@gmail.com ● 2 years of experience of design and development in node application. ● with javascript, node js, es6 and blockchain. ● proficient with mongodb , elastic search. ● exposure to frontend technologies like angularjs and react native. ● well versed with agile development practices. ● fidelium wallet and web application it is a online platform where user can deposits ethereum based tokens (erc20) and ethereum into a wallet. so that he can collect all his tokens and ethereum into a single address and can transfer to various users. ○ technologies nodejs, javascript, mongodb. ○ role developer ○ duration 2 months ○ worked with a team of 3 developers highlights ● worked extensively with ethereum node and mongodb. ● use of cron job to collect transactions from outside wallet address. ● full-stack development. ● worked on rest apis to support the ionic app. ● bmct wallet app this is a coin which is a fork of bitcoin and contains the same rpc calls as bitcoin. we have developed native apps (ios and android) having the services of nodejs. there is a end to end aes 256 encryption in this app and all the requests are handled using socket.io to do transactions using bmct coin. ○ technologies nodejs, javascript, mongodb, socket.io. ○ role developer ○ duration 3 months ○ worked with a team of 5 developers highlights ● worked extensively with socket.io and encryption. ● full-stack development ● worked on rest apis and socket.io to support the ios and android app. ● text back chat application this a chat application based project similar to whatsapp having the functionality of sending text messages, media(audio, video) and emoticons. user can also archive the chats, block users, translate messages into spanish and also can delete messages. ○ technologies nodejs, javascript, socket.io, mongodb. ○ role developer ○ duration 3 months ○ worked with a team of 4 developers highlights ● worked extensively with mongodb and socket.io. ● worked on socket.io to support the ios and android app. ● trkit application this a web and mobile based application where in web it contains four admin panels (super admin, organization admin, route mapper and route analyst) ,an android application(driver app and user app) and an ios application(user app). this application provides the facility to users for tracking their children (students) in school transport system ○ technologies nodejs, javascript, mongodb, socket.io. ○ role developer ○ duration 5 months ○ worked with a team of 5 developers ■ worked extensively with mongodb aggregations ■ full-stack development ■ worked on rest apis to support the ios , android and web app. ● lawcunae it is a online platform where users can access the latest legal cases, articles,course content and recommend reading for all legal subjects anytime online. in this mainly web scraping is done and after getting useful content it is uploaded to elasticsearch and linked the document ids with postgresql database. ○ technologies node, javascript, mongodb, elastic search, neo4j, pgsql. ○ role developer ○ duration 5 months ○ worked with a team of 4 developers highlights ■ worked extensively with mongodb and elasticsearch. ■ full-stack development ■ worked on rest apis. ● rex cargo it is a online platform where user do shipment of his/her goods within an intercity, intracity and international by booking appropriate vehicles. he/she can request using an ios application where he/she can fill details of his/her shipment and move his goods. ○ technologies nodejs, javascript, mongodb. ○ role developer ○ duration 3 months ○ worked with a team of 5 developers highlights ■ worked extensively with mongodb aggregations ■ full-stack development ■ worked on rest apis to support the ios app ● hooxi(mobile dating app) it is a mobile dating app just like the tinder app where people can chat on the basis of their matches. ○ technologies node, javascript, mongodb, angularjs ○ role developer ○ duration 2 month ○ worked with a team of 3 developers highlights ■ worked extensively with mongodb aggregations ■ backend- development ■ worked on rest apis to support the android app xxxxxxxxxxxxxx"
    # text = "Degree Institute/University Score Year MBA (Marketing & Thapar University, Patiala 8.3/10 CGPA 2009-2011 Information Technology) B.Tech(Electronics & Punjab Technical 77% 2004-2008 Communication Engg) University, Jalandhar domain.  Have managed cross-functional teams and directly responsible for the day-to-day activities of several of these members  INTERESTS Very social person, who likes to travel and try new restaurants Other hobbies include – Baking (desserts), Art (Acrylic, water paints / Canvas Painting) and listening to music PALLAVI GUPTA pallavi11.gupta@gmail.com , Mobile: +91-9818562481 and Digital Transformation, Monetization/ Revenue Maximization, Google Adsense/Adx, DFP, Google analytics, Facebook Ad Manager, Zedo ad server, campaign strategy, Proficient in Microsoft Powerpoint/Excel. xxxxxxxxxxxxxx"
    ts = time.time()
    text = "executive program in global business management – indian institute of management calcutta, 2016-17 bachelors of engineering (electronics & telecommunication) – bit, chhattisgarh, 2008-12 achievements and interests received aspire award at times internet for launching etimes received machate raho award at snapdeal for improving csat by help center received x-men award at snapdeal for improving customer experience through revamped myorders secured 1st position in inter-college essay competition secured 1st position in inter-branch speech competition passionate about travelling arpita mukherjee product manager with 6+ years of experience in technology products iim calcutta alumnus 091-9319 arpita.engineer31@gmail.com www.linkedin.com/in/arpita-mukherjee-7072a6118/ xxxxxxxxxxxxxx"
    edudata = obj.found_educations(' '.join(text.split()).lower())
    # # city, coll = obj.found_educations(' '.join(text.split()).lower())
    # # print(city, coll)
    print(edudata)
    print(time.time() - ts)

    # chunks = "azad institue of engineering and technology, lucknow"
    # # chunks ="thomson digital (india) pvt"
    # for i in reversed(range(3,11)):
    #     sixgrams = ngrams(chunks.split(), i)
    #     for grams in sixgrams:
    #         grams = " ".join(grams)
    #         print(grams)
    #         if grams in text.lower():
    #             print('++++++++++++++++',grams)
    #             text = re.sub(grams,' ',text)
