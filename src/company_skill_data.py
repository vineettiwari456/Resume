# -*- encoding:utf-8 -*-
import time
import re, ast
import string
class CompanyData:
    def __init__(self):
        self.company_dict = {}
        self.city_dict={}
        self.skills_dict={}
        self.designation_dict ={}
        self.punchuation = string.punctuation
        self.read_data()
    # def make_n_grams_dict(self, skills_list, tmp_dict):
    #     for skill in skills_list:
    #         temp_skill = skill.strip().split(' ')[0]
    #         try:
    #             if temp_skill[-1] in string.punctuation:
    #                 temp_skill = temp_skill[:-1]
    #             tmp_dict[temp_skill].append(skill)
    #         except:
    #             if temp_skill[-1] in string.punctuation:
    #                 temp_skill = temp_skill[:-1]
    #             tmp_dict[temp_skill] = [skill]

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
        fcompany = open("data_main/company_name_new.txt")
        companies = list(set([m.strip().lower() for m in fcompany.readlines()]))
        fcompany.close()
        # self.make_company_dict(companies,self.company_dict)
        self.make_n_grams_dict(companies,self.company_dict)

        skilldata = open("data_main/skill")
        skillset = ast.literal_eval(skilldata.read())
        skilldata.close()
        # self.make_n_grams_dict(skillset, self.skills_dict)
        self.make_n_grams_dict(skillset, self.skills_dict)
        fcity = open("data_main/city.txt")
        cities=list(set([m.strip().lower() for m in fcity.readlines()]))
        fcity.close()
        # self.make_n_grams_city_dict(cities, self.city_dict)
        self.make_n_grams_dict(cities, self.city_dict)
        designations =[]
        fdesignation = open("data_main/jobtitles.txt")
        designations.extend([m.strip().lower() for m in fdesignation.readlines()])
        fdesignation.close()
        fdesignation1 = open("data_main/jobtitles_cap.txt")
        designations.extend([m.strip().lower() for m in fdesignation1.readlines()])
        fdesignation1.close()
        self.make_n_grams_dict(list(set(designations)), self.designation_dict)


    def found_company(self, string1):
        string1 = string1.lower()
        temp_str = re.sub(r'[^\w\s]', ' ', string1)
        temp_str = temp_str.split(' ')
        company_only = []
        temp1=[]
        for word in temp_str:
            try:
                all_companys = self.company_dict[word]
                all_companys.sort(key=lambda s: len(s))
                for sk_ in all_companys[::-1]:
                    # if (self.find_word(string,sk_)) and (sk_ not in company_only):
                    if (sk_ in string1) and (sk_ not in company_only) and (sk_ not in ' '.join(company_only)): #and (str(sk_)+"." not in string1):
                        company_only.append(sk_)
                    elif (sk_ in string1) and (sk_ not in company_only) and (str(sk_)+"." not in string1):
                        temp1.append(sk_)
            except :
                pass
        temp = []
        company_only.sort(key=lambda s: len(s),reverse=True)
        for sk_ in company_only:
            if (sk_ not in temp) and (sk_ not in ' '.join(temp)):
                temp.append(sk_)
        # print('+++++++++++',temp)
        temp.extend([str(j).split("ltd")[0].strip() for j in company_only if 'ibm india ltd' in str(j).lower()])
        return list(set(temp))

    def found_skills(self,string1):
        string1 = string1.lower()
        # temp_str = string1.lower().split(' ')
        temp_str = re.sub(r'[^\w\s]', ' ', string1)
        temp_str = temp_str.split(' ')
        skills_only = []
        for word in temp_str:
            try:
                # if word[-1] in string.punctuation:
                #     word = word[:-1]
                all_skills = self.skills_dict[word]
                for sk_ in all_skills:
                    if (sk_ in string1) and (sk_ not in skills_only):
                        skills_only.append(sk_)
            except:
                pass
        return skills_only

    def found_cities(self,string1):
        string1 = str(string1).lower()
        temp_str = re.sub(r'[^\w\s]', ' ', string1)
        temp_str = string1.split(' ')
        city_only = []
        for word in temp_str:
            try:
                # if word[-1] in string.punctuation:
                #     word = word[:-1]
                all_citys = self.city_dict[word]
                all_citys.sort(key=lambda s: len(s))
                for sk_ in all_citys[::-1]:
                    if (sk_ in string1) and (sk_ not in city_only):
                        city_only.append(sk_)
            except Exception as e:
                # print(e)
                pass
        return city_only
    def found_designations(self,string1):
        string1 = str(string1).lower()
        temp_str = re.sub(r'[^\w\s]', ' ', string1)
        temp_str = temp_str.split(' ')
        designation_only = []
        for word in temp_str:
            try:
                # if word[-1] in string.punctuation:
                #     word = word[:-1]
                all_designation = self.designation_dict[word]
                all_designation.sort(key=lambda s: len(s))
                for sk_ in all_designation[::-1]:
                    # if (sk_ in string) and (sk_ not in designation_only) and len([g.start() for g in re.finditer('(\()?\\b' + (sk_) + '(?!,|\))\\b(\))?', string)])>0:
                    regex = "\\b("+sk_+")\\b"
                    # print(regex)
                    if (sk_ in string1) and (sk_ not in designation_only) and len([g.start() for g in re.finditer(regex, string1)]) > 0 and (sk_ not in ' '.join(designation_only)):
                        designation_only.append(sk_)
            except Exception as e:
                # print(e)
                pass
        return designation_only

if __name__=="__main__":
    ts = time.time()
    obj = CompanyData()
    text ="""jul 17, 2017 - present associate software engineer appster, gurgaon project description ejogajog (gim) description  goods in motion (gim) is an online platform that books transportation online, connecting transporters with customer. gim focuses on bridging the gap between smes, large enterprises and individuals with transporters. duration  june 2018 - present role  java developer technology used  java8 (backend apis), angular js(web) & android(mobile app), aws services (server, rds, s3 bucket), fcm push, j-unit testing, sendgrid mail service, ssl commerz sms service site  https//gim.com.bd/ momentor description  momentor lets you explore events happening around you. you can create events and the people matching your defined interests can only see the event. a better way to ensure you are meeting and planning an activity of like minded people. duration  april 2018 - june 2018 role  java developer technology used  java8 (backend apis), android & ios (mobile app), aws services (server, rds, s3 bucket), fcm & apns push services, sendgrid mail service site  https//prod.momentor.com.au/momentor/ nos (network of sobriety) description  nos is a platform to help drug addicts to achieve sobriety by keeping track of their daily exercises & routine. sharing the updates with an accountability partner to keep him/her aware of their patients condition and level of sobriety. duration  november 2017 - february 2018 role  java developer technology used  java8 (backend apis), android & ios (mobile app), angular js (admin cms) , aws services (server, rds, s3 bucket), sns mobilepush service, twilio sms service modurn description  the modurn collection is a contemporary and thoughtful way to honour a life. together with innovative design and technology, families can store and share a loved one's life story, today and for future generations. the urns and mementos act as beacons that can alert your device to a near by loved one or life story. duration  august 2017 - october 2017 role  java developer technology used  java8 (backend apis), ionic (hybrid mobile app), aws services (server, rds, s3 bucket), fcm & apns push services site  https//www.modurngroup.com/ https//www.visualcv.com/abhinav_verma core java server management effective communication spring mvc junit team leadership hibernate flyway integration research & analysis mysql database j-meter management project management aws management sonarqube handling process improvements eclipse mysql workbench postman swagger j-meter"""
    text = "Spark-Developer, March 2018 to Current Turning Cloud Solutions Pvt. Ltd. – Gurgaon, Haryana Project Supply Mint \uf0b7 Supply Mint creates efficiencies, raises profits, lower costs, boosts collaboration and more. \uf0b7 Supply Mint enables companies to better manage demand, carry the right amount of inventory, keep costs to minimum and meet the customer demand in the most effective way possible. Roles and Responsibilities \uf0b7 Developing spark jobs in PYTHON. \uf0b7 Automate the process of allocation by developing spark jobs in PYTHON. \uf0b7 Created trigger for scheduling the jobs. \uf0b7 Retrieving the data for forecasting and data cleaning. \uf0b7 Responsible for retrieving data from the clients. Spark-Developer August 2017 to February 2018 Aptivi Technology Pvt. Ltd.- Sec 63 Noida, UP Roles and Responsibilities \uf0b7 Developing spark jobs in PYTHON. \uf0b7 Responsible for retrieving data from the client. \uf0b7 Automate the process of raw data to meaningful information. Hadoop and Spark Developer (Trainee) January 2017 to June 2017 Simplilearn Solutions Pvt. Ltd. - Bangalore, Karnataka Project Real Time Marketing Analysis The Portuguese banking institution ran a marketing campaign to convince potential customers to invest in bank term deposit. Information related to direct marketing campaigns of the bank are as follows. The marketing campaigns were based on phone calls. Often, the same customer was contacted more than once through phone, in order to asses if they would want to subscribe to the bank term deposit or not."
    city = obj.found_company(' '.join(text.split()).lower())
    print (city)
    print (time.time()-ts)






