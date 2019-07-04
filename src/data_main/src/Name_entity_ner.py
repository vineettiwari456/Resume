# -*-coding:utf-8 -*-
import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words("english")

class NameEntity:
    def __init__(self):
        self.main_candidate_names = []

        self.person_ending_text = []
        m_name_cap = open("data_main/person_male.txt")
        self.main_candidate_names.extend([m.strip() for m in m_name_cap.readlines()])
        m_name_cap.close()
        m_name_low = open("data_main/person_male_cap.txt")
        self.main_candidate_names.extend([m.strip() for m in m_name_low.readlines()])
        m_name_low.close()
        f_name_cap = open("data_main/person_female.txt")
        self.main_candidate_names.extend([m.strip() for m in f_name_cap.readlines()])
        f_name_cap.close()
        f_name_low = open("data_main/person_female_cap.txt")
        self.main_candidate_names.extend([m.strip() for m in f_name_low.readlines()])
        f_name_low.close()
        c_name_low = open("data_main/person_ending.txt")
        self.person_ending_text.extend([m.strip() for m in c_name_low.readlines()])
        c_name_low.close()
        # self.person_name_start = list(set([i.lower().strip() for i in self.main_candidate_names]))
    def get_regex_personname(self,fname, rdata, is_full = True):
        person_text = None
        for mat_name in self.person_ending_text:
            if is_full:
                # regex = r"((%s)\s+(.*)(?:\s*)(%s)\s+)" % (fname.lower(), mat_name.lower())
                regex =r"(%s\s+(.*?)%s\s+)"% (fname.lower(), mat_name.lower())
            else:
                regex = r"((%s)\s+)" % (fname.lower())
            # print(regex)
            person_name = re.findall(
                regex,
                rdata.lower())
            # print(person_name)
            if len(person_name) > 0:
                if len(person_name[0][0]) < 30:
                    # print(person_name)
                    person_text = person_name[0][0]
                    break
        return person_text

    def check_stopwords(self,person):
        is_stop= False
        for m in stop:
            # print(str(m), person.split())
            if str(m) in person.split():
                is_stop = True
        return is_stop

    def get_candidate_name(self,rdata):
        rdata = ' '.join(rdata.split())
        # print(rdata.lower())
        person_name = ""
        # print(self.person_name_start)
        for fname in self.main_candidate_names:
            if fname.lower() in [i.strip() for i in rdata.lower().split()]:
                is_person_name = self.get_regex_personname(fname,rdata)
                if is_person_name:
                    # print(is_person_name)
                    is_stopword = self.check_stopwords(is_person_name)
                    if not is_stopword:
                        person_name = is_person_name.strip()
                        break
        if person_name=="":
            for fname in [i.lower() for i in self.main_candidate_names]:
                if fname.lower() in [i.strip() for i in rdata.lower().split()]:
                    is_person_name = self.get_regex_personname(fname, rdata, is_full=False)
                    if is_person_name:
                        person_name = is_person_name.strip()
                        break
        return person_name.capitalize()

if __name__=="__main__":
    obj = NameEntity()
    # raw_data="Street 5, Saharanpur aquib javed khan krishnakc1121@gmail.com"
    raw_data = 'Krishan Chandra Joshi Mobile : +918377876652 Mail Id : krishnakc1121@gmail.com'
    # raw_data = "Street 5, Saharanpur 9999121214,9898979656,9089786756 Asiaw@live.com , Sandeep33@gmail.com , sre@gmail.com www.Linkedin.com/in/santest Street 5, Saharanpur 9999121214,9898979656,9089786756 Asiaw@live.com , Sandeep33@gmail.com , sre@gmail.com www.Linkedin.com/in/santest SANDEEP KUMAR SHARMA Recent graduate with excellent research, time management and problem solving skills. Ability to function at a high level in a wide variety of settings. Monster India Noida EXPERIENCE Monster India Noida"
    name  = obj.get_candidate_name(raw_data)
    print(name.capitalize())