
import requests
import time, csv

class ResumeResponse:
    def __init__(self, list_dir_filepath):
        self.url = "http://rfs.monsterindia.com/resumeParser"
        self.list_dir_filepath = list_dir_filepath
        fieldnames=["Person_Name","Email","Location","Phone_Number","Skills","Designation_Name","Current_Company","Description","StartDate","EndDate","Is_Current"]
        self.hed = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
       }
        printout = "C:\\home\\ResumeOutput\\" + time.strftime('%y%m%d_%H%M%S',
                                                                     time.localtime()) + '_resume_response.csv'
        self.fp = open(str(printout), 'w')
        # self.fp.write(u'\ufeff'.encode('utf8'))
        self.writer = csv.DictWriter(self.fp, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        self.writer.writeheader()

    def extract_response(self):
        filepath = "C:\\Users\\vktiwari\\Documents\\backupC\personal\\vineettiwari_newdocx.docx"
        files = {'file': open(filepath, 'rb')}
        res = requests.post(self.url, data={},files = files, headers = self.hed)
        json_data_raw = res.json()
        json_data = json_data_raw.get("data",{})
        raw_personalinfo = json_data.get("personal_info",{})
        print (json_data)
        phone_number = ', '.join(raw_personalinfo.get("phones",[]))
        emails = ', '.join(raw_personalinfo.get("emails",[]))
        person_name= raw_personalinfo.get("name",'')
        location = raw_personalinfo.get("location",{}).get("name","")
        # print person_name,location
        resume_dict = json_data.get("resume",{})
        skills = ', '.join([j.get("name","") for j in resume_dict.get("skills",[])])
        # print (skills)
        work_exp_list = resume_dict.get("work_exps",[])
        workexp_dict = {}
        if len(work_exp_list)>0:
            workexp_dict = work_exp_list[0]
        # print(workexp_dict)
        designation_name = workexp_dict.get("designation",{}).get("name","")
        company_name = workexp_dict.get("company",{}).get("name","")
        start_date = workexp_dict.get("start_date","")
        end_date = workexp_dict.get("end_date","")
        is_current = workexp_dict.get("is_current","")
        description = workexp_dict.get("desc","")
        eduction_list = resume_dict.get("educations",[])
        print(eduction_list)
        # print(person_name,location,emails,phone_number,designation_name,company_name,description, start_date,end_date,is_current)

        dict ={}
        dict["Person_Name"] = person_name
        dict["Email"] = emails
        dict["Location"] = location
        dict["Phone_Number"] = phone_number
        dict["Skills"] = skills
        dict["Designation_Name"]=designation_name
        dict["Current_Company"] = company_name
        dict["Description"] = description.encode("utf8")
        dict["StartDate"] = start_date
        dict["EndDate"] = end_date
        dict["Is_Current"] = str(is_current)

        print(dict)
        self.writer.writerow(dict)

if __name__=="__main__":
    obj = ResumeResponse("doc_file")
    obj.extract_response()

# url = "http://10.216.204.36:9000/resumeParser"
# filepath  = "C:\\Users\\vktiwari\\Documents\\backupC\personal\\vineettiwari_newdocx.docx"
# files = {'file': open(filepath, 'rb')}
#
# hed = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
#        }
