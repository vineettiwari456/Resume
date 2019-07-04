# -*- coding:utf-8 -*-
import os, operator, re
import docx2txt, datetime
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from dateutil.parser import parse
import nltk, time, subprocess
import ast
from nltk.corpus import stopwords

stop = stopwords.words("english")
from nltk.corpus import wordnet
import string
from flashtext import KeywordProcessor
from Name_entity_ner import NameEntity
from nltk_ner_extract_name import extract_person_name_location
# from name_entity_extraction import extract_ner
from get_phone_number import getPhone
from pdf_text_extraction import PdfExtractor


class ResumeParser:
    def __init__(self):
        # self.filepath = filepath
        self.obj_ner = NameEntity()
        self.obj_pdf = PdfExtractor()
        self.main_keywordlist = []
        self.mapping_dict = {}
        self.companylist = []
        self.designations = []
        self.cities = []
        self.skilllist = []
        cmpfile = open("uuid/company_uuid", encoding='ISO-8859-1')
        self.cmp_master_data = ast.literal_eval(cmpfile.read())
        cmpfile.close()
        desigfile = open("uuid/designation_uuid", encoding='ISO-8859-1')
        self.desig_master_data = ast.literal_eval(desigfile.read())
        desigfile.close()
        locfile = open("uuid/location_uuid", encoding='ISO-8859-1')
        self.locations_master_data = ast.literal_eval(locfile.read())
        locfile.close()
        qualificationfile = open("uuid/qualifications_uuid", encoding='ISO-8859-1')
        self.qualification_master_data = ast.literal_eval(qualificationfile.read())
        qualificationfile.close()
        skillfile = open("uuid/skills_uuid", encoding='ISO-8859-1')
        self.skills_master_data = ast.literal_eval(skillfile.read())
        skillfile.close()
        # print(type(cmp_master_data))
        skilldata = open("data_main/skill")
        skillset = ast.literal_eval(skilldata.read())
        self.skilllist.extend(skillset)
        skilldata.close()
        fdesignation = open("data_main/jobtitles.txt")
        self.designations.extend([m.strip() for m in fdesignation.readlines()])
        fdesignation.close()
        fcity = open("data_main/city.txt")
        self.cities.extend([m.strip() for m in fcity.readlines()])
        fcity.close()
        fdesignation1 = open("data_main/jobtitles_cap.txt")
        self.designations.extend([m.strip() for m in fdesignation1.readlines()])
        fdesignation1.close()
        faccoum = open("data_main/accomplishments.txt")
        accomplishments = [m.strip() for m in faccoum.readlines()]
        self.main_keywordlist.extend(accomplishments)
        faccoum.close()
        self.mapping_dict.update(dict(zip(accomplishments,
                                          ["Academic_achievement"] * len(accomplishments))))
        fedutrain = open("data_main/education_and_training.txt")
        education_and_training = [m.strip() for m in fedutrain.readlines()]
        self.main_keywordlist.extend(education_and_training)
        # self.mapping_dict.update(dict(zip([m.strip() for m in fedutrain.readlines()], "education_and_training")))
        fedutrain.close()
        self.mapping_dict.update(dict(zip(education_and_training,
                                          ["education_and_training"] * len(education_and_training))))
        fextracurr = open("data_main/extracurricular.txt")
        extracurricular = [m.strip() for m in fextracurr.readlines()]
        self.main_keywordlist.extend(extracurricular)
        fextracurr.close()
        self.mapping_dict.update(dict(zip(extracurricular,
                                          ["extra_activity"] * len(extracurricular))))
        extra_text = open("data_main/extra")
        extraraw = [m.strip() for m in extra_text.readlines()]
        self.main_keywordlist.extend(extraraw)
        extra_text.close()
        self.mapping_dict.update(dict(zip(extraraw,
                                          ["extra_option"] * len(extraraw))))

        fmisc = open("data_main/misc.txt")
        hobbie = [m.strip() for m in fmisc.readlines()]
        self.main_keywordlist.extend(hobbie)
        fmisc.close()
        self.mapping_dict.update(dict(zip(hobbie,
                                          ["profile_details"] * len(hobbie))))
        fqualification = open("data_main/qualification.txt")
        qualification = [m.strip() for m in fqualification.readlines()]
        self.main_keywordlist.extend(qualification)
        fqualification.close()
        self.mapping_dict.update(dict(zip(qualification,
                                          ["qualifications"] * len(qualification))))
        fskills = open("data_main/skills.txt")
        skills = [m.strip() for m in fskills.readlines()]
        self.main_keywordlist.extend(skills)
        fskills.close()
        self.mapping_dict.update(dict(zip(skills,
                                          ["skills"] * len(skills))))
        fsummary = open("data_main/summary.txt")
        summary = [m.strip() for m in fsummary.readlines()]
        self.main_keywordlist.extend(summary)
        fsummary.close()
        self.mapping_dict.update(dict(zip(summary,
                                          ["summary"] * len(summary))))
        self.check_work = []
        fwork_experience = open("data_main/work_experiences.txt")
        work_experiences = [m.strip() for m in fwork_experience.readlines()]
        self.main_keywordlist.extend(work_experiences)
        self.check_work = work_experiences
        fwork_experience.close()
        self.mapping_dict.update(dict(zip(work_experiences,
                                          ["work_experiences"] * len(work_experiences))))
        self.mapping_dict["Profile_Name"] = "Profile_Name"
        fcompany = open("data_main/company_name_new.txt")
        companies = list(set([m.strip().lower() for m in fcompany.readlines()]))
        self.companylist.extend(companies)
        fcompany.close()
        self.check_month = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7,
                            "august": 8, "september": 9, "october": 10, "november": 11, "December": 12,
                            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7,
                            "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12, }
        # self.processor = KeywordProcessor()

    def get_pdf2text(self, fname, pages=None):
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = open(fname, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        # print(text)
        return text

    def get_text(self, paths):
        ftext = open(paths, 'r', encoding="ISO-8859-1")
        textd = ' '.join(ftext.read().split())
        ftext.close()
        return textd

    def get_cmd_output(self, *args, **kwargs):
        """Returns text output of a command."""
        encoding = kwargs.get("encoding", "utf-8")
        # logger.debug("get_cmd_output(): args = {}".format(repr(args)))
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode(encoding, errors='ignore')

    def convert_doc_to_text(self, filename=None, blob=None):
        if filename:
            return self.get_cmd_output(
                'antiword',  # IN CASE OF FAILURE: sudo apt-get install antiword
                filename)
        # else:
        #     return get_cmd_output_from_stdin(
        #         blob,
        #         'antiword',  # IN CASE OF FAILURE: sudo apt-get install antiword
        #         '-')

    def convert_pdf_to_txt(self, filename=None, blob=None):
        """Pass either a filename or a binary object."""
        # Memory-hogging method:

        # with get_filelikeobject(filename, blob) as fp:
        #     rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
        #     retstr = cStringIO.StringIO()
        #     codec = ENCODING
        #     laparams = pdfminer.layout.LAParams()
        #     device = pdfminer.converter.TextConverter(
        #         rsrcmgr, retstr, codec=codec, laparams=laparams)
        #     interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
        #     password = ""
        #     maxpages = 0
        #     caching = True
        #     pagenos = set()
        #     for page in pdfminer.pdfpage.PDFPage.get_pages(
        #             fp, pagenos, maxpages=maxpages, password=password,
        #             caching=caching, check_extractable=True):
        #         interpreter.process_page(page)
        #     text = retstr.getvalue().decode(ENCODING)
        # return text

        # External command method:
        if filename:
            return self.get_cmd_output(
                'pdftotext',  # Core part of Linux?
                filename,
                '-')
        # else:
        #     return get_cmd_output_from_stdin(
        #         blob,
        #         'pdftotext',  # Core part of Linux?
        #         '-',
        #         '-')

    def get_docx_doc_pdf_text(self, filepath):
        file_name = os.path.basename(filepath)
        filename, file_extension = os.path.splitext(file_name)
        print(filename, file_extension)
        fdata = ""
        if file_extension.lower() == ".docx":
            fdata = docx2txt.process(filepath)
        if file_extension.lower() == ".doc":
            fdata = self.convert_doc_to_text(filepath)
        if file_extension.lower() == ".pdf":
            # fdata = self.get_pdf2text(filepath)
            if "abhinandan" in filename.lower():
                fdata = self.convert_pdf_to_txt(filepath)
            else:
                fdata = self.obj_pdf.get_pdf_text(filepath)
            # fdata = self.convert_pdf_to_txt(filepath)
        if file_extension.lower() == ".txt":
            fdata = self.get_text(filepath)
        return fdata

    def getText(self, filename):
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '(ppp)'.join(fullText)

    def found_keword(self, datalist, rawtext, is_lower=True):
        found = []
        datalist.sort(key=lambda s: len(s))
        if is_lower:
            mainddatalist = [i.strip().lower() for i in datalist[::-1]]
        else:
            mainddatalist = [i.strip() for i in datalist[::-1]]
        processor = KeywordProcessor()
        processor.add_keywords_from_list(mainddatalist)
        if is_lower:
            found = processor.extract_keywords(rawtext.lower())
        else:
            found = processor.extract_keywords(rawtext)
        # print(found)
        return found

    def get_all_index(self, data, data_find):
        # offsets = [i for i in range(len(data)) if data.startswith(data_find, i)]
        # offsets_withid = {data_find: i for i in range(len(data)) if data.startswith(data_find, i)}
        offsets_withid = {g.group().strip(): g.start() for g in re.finditer('\\b'+(data_find)+'\\b', data)}
        offsets = [g.start() for g in re.finditer('\\b'+(data_find)+'\\b', data)]
        return offsets, offsets_withid

    def seperation_block_index(self, main_keywordlist, raw_data):
        dict_map = {}
        sort_keyword_index = {}
        for kl in list(set(main_keywordlist)):
            try:
                word_indexs, offsets_id = self.get_all_index(str(raw_data).strip(), kl)
                if len(word_indexs) > 0:
                    # print(word_indexs, offsets_id)
                    sort_keyword_index.update(offsets_id)
                    for word_index in word_indexs:
                        # word_index = str(raw_data).strip().index(str(kl))
                        # print(kl,'---------------------', word_index)
                        # if "\n" in str(raw_data).strip()[word_index+len(kl):word_index+len(kl)+30] or "\t" in str(raw_data).strip()[word_index+len(kl):word_index+len(kl)+30]:
                        if kl + "." in str(raw_data).strip()[word_index:word_index + len(kl) + 10]:
                            # dict_map[kl] = word_index
                            # print(kl)
                            main_keywordlist.remove(kl)
                        else:
                            dict_map[kl] = word_index
                            main_keywordlist.remove(kl)
                            break
                            # if kl in self.check_work:
                            #     if len(self.found_keword(self.designations, raw_data[word_index:word_index+200]))>0:
                            #         dict_map[kl] = word_index
                            #         main_keywordlist.remove(kl)
                            # else:
                            #     dict_map[kl] = word_index
                            #     main_keywordlist.remove(kl)
                            # break
            except Exception as e:
                # print(e)
                pass

        raw_temp = self.get_multiple_same_index(dict_map)
        dict_map = {}
        for m, n in raw_temp.items():
            # print(m, max(n))
            dict_map[max(n)] = m
        print(dict_map)
        new_dict = list(sorted(dict_map.items(), key=operator.itemgetter(1)))
        new_dict = [('Profile_Name', 0)] + new_dict

        op_dict = {}
        for i in range(len(new_dict)):
            tmp_data = [new_dict[i][1]]
            if i < (len(new_dict) - 1):
                tmp_data.append(new_dict[i + 1][1])
            op_dict[new_dict[i][0]] = tmp_data
        # print(op_dict)
        final_dic = {}
        for m in op_dict.keys():
            # print(m, op_dict[m])
            main_text = ""
            if len(op_dict[m]) == 2:
                x = op_dict[m][0]
                y = op_dict[m][1]
                if m == "Profile_Name":
                    main_text = str(raw_data).strip()[x:y].strip()
                else:
                    main_text = str(raw_data).strip()[x + len(m):y].replace(":", '').strip()
            else:
                x = op_dict[m][0]
                # y = op_dict[m][1]
                main_text = str(raw_data).strip()[x + len(m):].replace(":", '').strip()
            if main_text:
                final_dic[m] = main_text
        # print(final_dic)
        return final_dic, sort_keyword_index

    def get_years(self, raw_text):
        years = []
        # regex = r"(((?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?\d{4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-)\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{4})"
        # print(regex)
        # regex = r"((((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{4})\s*(to till|to|-|To|TO|-|–)?\s*((((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{4})|(Present|till|Till|PRESENT|current|Current|CURRENT))?)".lower()
        # regex =r"((((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{2,4}|(\d{1,2}(\/|-)\d{1,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{4})\s*(to till|to|-|To|TO|-|–)?\s*((((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,)\s\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|(Present|till|Till|PRESENT|current|Current|CURRENT))?)".lower()
        regex = r"((since)?\s*?(((\d{1,2}\s*)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\s)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)(-|.)\s*\d{2,4}|(\d{1,2}(\/|-)\d{1,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?(,)\s\d{4})\s*(to till|to|-|to|to|-|–)?\s*((((\d{1,2}\s*)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\s)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)(-|.)\s*\d{2,4}|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?(,)\s\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|\b(19|20)\d{2}|(present|till|till|present|current|current|current|ongoing))?)".lower()
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
                    years.append(yr[0])
                except:
                    pass
        return years

    def get_orginal_segmented_dic(self, dic, kewindexdic):
        additional_info = []
        essential_keys = {}
        for k, v in self.mapping_dict.items():
            essential_keys[k] = v
        essential_key_list = essential_keys.values()
        final_dic = {}
        tmp_json = {}
        kewindexdic["Profile_Name"] = 0
        kewoindex = [(k, kewindexdic[k]) for k in sorted(kewindexdic, key=kewindexdic.get, reverse=False)]
        for k, v in kewoindex:
            try:
                k1 = essential_keys[k]
            except:
                pass
            try:
                if k1 == 'work_experiences':
                    if len(self.get_years(dic.get(k, ""))) > 0:
                        k1 = k1
                    else:
                        k1 = 'Profile_Name'
                if k1 in final_dic.keys():
                    final_dic[k1] = final_dic[k1] + " " + dic.get(k, "")
                else:
                    final_dic[k1] = dic.get(k, "")
            except Exception as e:
                print(e)
                pass

        remaining_keys = set(essential_key_list) - set(final_dic.keys())
        # print remaining_keys
        for r in remaining_keys:
            final_dic[r] = ""
        # print(final_dic)
        return final_dic

    def get_email_id(self, raw_text):
        email_id = ""
        regex = r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)"
        # print(regex)
        rawemail = re.findall(
            regex,
            raw_text)
        if len(rawemail) > 0:
            email_id = rawemail
        return email_id

    def get_candidate_name(self, blockdict):
        pers_name = ""
        rdic = list(blockdict)
        rdc = ["Profile_Name", "profile_details", "work_experiences", "skills", "qualifications",
               "education_and_training",
               "extra_activity", "summary", "Academic_achievement"]
        # rdic.remove("Profile_Name")
        # rdic.insert(0,"Profile_Name")
        for j in rdc:
            rawname = self.obj_ner.get_candidate_name(blockdict.get(j, ''))
            if rawname:
                pers_name = rawname
                break
        return pers_name

    def get_string_match_index(self, string_text, wl):
        index = 0
        try:
            if "(" in wl:
                wl = wl.replace("(", "\(")
            if ")" in wl:
                wl = wl.replace(")", "\)")
            regex = r"\b(%s)[\s+|,|.]" % (wl)
            # print(regex)
            indexes = []
            in_wl = {}
            wl_ind = {}
            for m in re.finditer(regex, string_text):
                # print('----------->',m)
                indexes.append(m.start(0))
                in_wl.update({m.start(0): wl})
                wl_ind.update({wl: m.start(0)})
            return indexes, in_wl, wl_ind
            # a = re.search(regex, string_text)
            # index = a.start()
            # return [index], {index: wl}, {wl: index}
        except Exception as e:
            # print(e)
            pass
        return [], {}, {}

    def get_current_keyword_index(self, raw_workexp_text, companylist):
        # print(raw_workexp_text,self.companylist)
        sort_company_index = {}
        sort_key_index = {}
        companylist.sort(key=lambda s: len(s))
        companylist = companylist[::-1]
        for kl in companylist:
            # word_indexs, offsets_id = self.get_all_index(str(raw_workexp_text).strip().lower(), kl.lower())
            word_indexs, offsets_id, key_index = self.get_string_match_index(str(raw_workexp_text).strip().lower(),
                                                                             kl.lower())
            if len(word_indexs) > 0:
                sort_company_index.update(offsets_id)
                sort_key_index.update(key_index)
        # print(sort_company_index)
        return sort_company_index, sort_key_index

    def get_current_duration(self, year_duration, is_current=True, is_birth=False):
        foyearsindex = sorted(year_duration)
        currentyear = ""
        start_date = ""
        end_date = ""
        birth_date = ""
        if is_current:
            if len(foyearsindex) > 0:
                currentyear = year_duration.get(foyearsindex[0], "").lower()
        else:
            currentyear = year_duration.lower()
        if currentyear:
            if is_birth:
                regex = r"(((\d{1,2}\s*)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\s)|(\d{1,2}(\.|-|\/)\d{1,2}(-|\/|\.)\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)(-|.)\s*\d{2,4}|(\d{1,2}\s*)?(-)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?(,|-)\s*\d{2,4})".lower()
            else:
                regex = r"(((\d{1,2}\s*)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?\d{2,4})|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\s)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(\d{1,2}(\/|-)\d{1,4})|(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)(-|.)\s*\d{2,4}|(\d{1,2}\s*)?(-)?(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|sept)\s*(\d{1,2}\s*)?(,|-)\s*\d{2,4}|\b(19|20)\d{2})".lower()
            # regex = r"(((\d{1,2}\s*)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Sept)\s*(\d{1,2}\s*)?\d{2,4}?(,|-)?\s*\d{4}?)|(^\d\d\d\d(\/|-|.)(0?[1-9]|1[0-2])(\/|-|.)(0?[1-9]|[12][0-9]|3[01])\S)|(\d{1,2}(-|\/)\d{1,2}(-|\/)\d{2,4})|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(-|.)\s*\d{2,4}|(\d{1,2}\s*)?(-)?(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{1,2}\s*)?(,|-)\s*\d{2,4})".lower()
            rawyears = re.findall(
                regex,
                currentyear.replace("th", ' ').replace(",", ""))
            # print(rawyear)
            if len(rawyears) > 0:
                temp_date = []
                for yr in rawyears:
                    try:
                        dval = yr[0]
                        # print(dval)
                        for ds in list(self.check_month.keys()):
                            if yr[0].lower().startswith(ds.lower()):
                                if len(yr[0]) <= len(ds) + 3:
                                    dval = str(self.check_month[ds]) + " " + yr[0]
                        # print(dval)
                        dt = parse(dval)
                        date_time_obj = ""
                        if is_birth and dt:
                            birth_date = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year)
                            break
                        else:
                            date_time_obj = str(dt.month) + "/" + str(dt.year)
                        temp_date.append(date_time_obj)
                    except Exception as e:
                        print(e)
                        pass
                # print(temp_date)
                if len(temp_date) == 2:
                    start_date = temp_date[0]
                    end_date = temp_date[1]
                elif len(temp_date) == 1:
                    start_date = temp_date[0]
                    end_date = ""

        return start_date, end_date, birth_date

    def get_first_preference_name(self, unbalanced_dic):
        findex = sorted(unbalanced_dic)
        currentval = ""
        if len(findex) > 0:
            current = unbalanced_dic.get(findex[0], "")
            currentval = max(list(current))
        return currentval

    def get_multiple_same_index(self, ini_dict):
        rev_dict = {}
        for key, value in ini_dict.items():
            rev_dict.setdefault(value, set()).add(key)
        # print(rev_dict)
        return rev_dict

    def get_location_uuid(self, locs, master_data, is_list=False):
        if not is_list:
            uuid = master_data.get(str(locs).lower().strip(), '')
            return {"uuid": uuid, "name": locs}
        else:
            total_list = []
            for loc in locs:
                dic = {}
                dic["name"] = loc
                dic["uuid"] = master_data.get(str(loc).lower().strip(), '')
                total_list.append(dic)
            return total_list

    def get_individual_designation_work_exp(self, rawworkexp, st, end, st_check):
        ind_designation = ""
        designation_text = ""
        is_previous = False
        if st < 50:
            st = 0
        else:
            st = st
        if end:
            designation_text = rawworkexp[st:end]
        else:
            designation_text = rawworkexp[st:]
        ls_year = []
        if st > 0 and end:
            if st_check:
                found_ind_desg = self.found_keword(self.designations, rawworkexp[st - 45:st + 20])
                if len(found_ind_desg) > 0:
                    ind_designation = found_ind_desg[0].strip()
                    is_previous = True
                ls_year_temp = self.get_years(rawworkexp[st - 22:st + 5])
                if len(ls_year_temp) > 0:
                    for d in ls_year_temp:
                        if "to" in d.lower():
                            ls_year.append(d)
                            break
                        else:
                            ls_year.append(d)
            else:
                ls_year_temp = self.get_years(rawworkexp[st - 22:st + 5])
                if len(ls_year_temp) > 0:
                    for d in ls_year_temp:
                        if "to" in d.lower():
                            ls_year.append(d)
                            break
                        else:
                            ls_year.append(d)
        elif not end:
            if not st_check:
                found_ind_desg = self.found_keword(self.designations, rawworkexp[st:])
            else:
                found_ind_desg = self.found_keword(self.designations, rawworkexp[st - 40:st + 20])
            if len(found_ind_desg) > 0:
                ind_designation = found_ind_desg[0].strip()
                is_previous = True
        ld = 300
        if len(ls_year) == 0:
            ls_year_temp = self.get_years(designation_text[:ld])
            for ls in ls_year_temp:
                if ls.lower().startswith("since") and "to" in ls.lower():
                    ls_year.append(ls.lower().replace("since", '').strip())
                else:
                    ls_year.append(ls)
        if ind_designation == "":
            found_ind_desg = self.found_keword(self.designations, designation_text[:ld])
            if len(found_ind_desg) > 0:
                ind_designation = found_ind_desg[0].strip()
        if len(ls_year) == 0:
            if end:
                if st > 40:
                    designation_text = rawworkexp[st - 51: end]
                else:
                    designation_text = rawworkexp[:end]
            else:
                if st > 40:
                    designation_text = rawworkexp[st - 52:]
                else:
                    designation_text = rawworkexp[:]
            ls_year_temp = self.get_years(designation_text[:])
            for ls in ls_year_temp:
                if ls.lower().startswith("since") and "to" in ls.lower():
                    ls_year.append(ls.lower().replace("since", '').strip())
                else:
                    ls_year.append(ls)
        if ind_designation == "":
            if end:
                if st > 50:
                    designation_text = rawworkexp[st - 50:end]
                else:
                    designation_text = rawworkexp[:end]
            else:
                if st > 50:
                    designation_text = rawworkexp[st - 50:]
                else:
                    designation_text = rawworkexp[:]
            found_ind_desg = self.found_keword(self.designations, designation_text[:95])
            if len(found_ind_desg) > 0:
                is_previous = True
                ind_designation = found_ind_desg[0].strip()
            # print('iiiiiiiiiiiiiii>',ls_year)
        return ind_designation, is_previous, ls_year

    def get_complete_work_experince(self, cmpdic, rawworkexp, current_designation):
        cmpdict = {}
        temp_index = {}
        temp_num = 0
        for k, v in cmpdic.items():
            cmpdict[max(list(v)) + "_" + str(temp_num)] = k
            temp_index[k] = max(list(v))
            temp_num += 1
        # print(cmpdict)
        temp = []
        for i in cmpdict.keys():
            if len(i) > 2:
                if i.lower().strip()[:3].startswith(tuple(cmpdict.keys())):
                    temp.append(i)
        if len(temp) > 1:
            remove_str = min(temp)
            del cmpdict[remove_str]
        # print(cmpdict)
        new_dict = list(sorted(cmpdict.items(), key=operator.itemgetter(1)))
        # print(new_dict)
        op_dict = {}
        for i in range(len(new_dict)):
            tmp_data = [new_dict[i][1]]
            if i < (len(new_dict) - 1):
                tmp_data.append(new_dict[i + 1][1])
            op_dict[new_dict[i][0]] = tmp_data
        # print(op_dict)
        total_work_experience = []
        # yrlis = sorted(yeardic)
        if len(new_dict) == 1:
            for m, n in enumerate(new_dict):
                temp = {}
                temp["is_current"] = False
                n_temp = n[0].split("_")[0]
                temp["company"] = self.get_location_uuid(n_temp.replace("\\", '').strip().capitalize(),
                                                         self.cmp_master_data)
                found_ind_de = self.found_keword(self.designations, rawworkexp[:200])
                ind_designation = ""
                if len(found_ind_de) > 0:
                    ind_designat = max(found_ind_de).strip()

                temp["desc"] = rawworkexp.strip().capitalize()
                year_list = self.get_years(temp["desc"])
                # print(year_list)
                start_dat = ""
                end_dat = ""
                if len(year_list) > 0:
                    try:
                        start_dat, end_dat, birday = self.get_current_duration(year_list[0],
                                                                               is_current=False)
                        if "since" in year_list[0].lower() or "till" in year_list[0].lower() or "current" in year_list[
                            0].lower() or "present" in year_list[0].lower() or "ongoing" in year_list[0].lower():
                            temp["is_current"] = True
                            end_dat = "Present"
                    except:
                        pass
                temp["start_date"] = start_dat
                temp["end_date"] = end_dat
                if temp["end_date"] == "Present" and ind_designat == "":
                    ind_designat = current_designation
                temp["designation"] = self.get_location_uuid(ind_designat.capitalize(), self.desig_master_data)
                # if ind_designat:
                total_work_experience.append(temp)
        else:
            start_check = True
            for mk, jk in enumerate(new_dict):
                list_year = []
                datatp = op_dict.get(jk[0])
                jk_temp = jk[0].split("_")[0]
                temp_exp = {}
                temp_exp["is_current"] = False
                temp_exp["company"] = self.get_location_uuid(jk_temp.replace("\\", '').strip().capitalize(),
                                                             self.cmp_master_data)

                # if mk==0:
                #     keyword_index = self.found_keword(self.designations,rawworkexp)
                #     if len(keyword_index)>0:
                #         if jk[1]<rawworkexp.index(keyword_index[0]):
                #             start_check = False
                designation_text = ""
                is_check_designation = False
                if len(datatp) == 2:
                    keyword_index = self.found_keword(self.designations, rawworkexp[datatp[0]:datatp[1]][:50])
                    if len(keyword_index) > 0:
                        if jk[1] < rawworkexp.index(keyword_index[0]):
                            start_check = False
                    designation_text, is_previous, list_year = self.get_individual_designation_work_exp(rawworkexp,
                                                                                                        datatp[0],
                                                                                                        datatp[1],start_check)
                    # temp_exp["desc"] = '. '.join(rawworkexp[datatp[0]:datatp[1]].split(".")[:-1]).strip().capitalize()
                    # print('is_previous===>',is_previous)
                    if is_previous:
                        if len(rawworkexp[datatp[0]:datatp[1]].split(". ")) > 1 and len(
                                rawworkexp[datatp[0]:datatp[1]].split(". ")[-1]) < 30:
                            temp_exp["desc"] = ' '.join(
                                rawworkexp[datatp[0]:datatp[1]].split(". ")[:-1]).strip().capitalize()
                        else:
                            dscraw = ' '.join(
                                rawworkexp[datatp[0]:datatp[1]].split(". ")[:]).strip().capitalize()
                            # if "worked as" in dscraw.lower():
                            #     dscraw = dscraw[:dscraw.index("worked as")].strip()
                            temp_exp["desc"] = dscraw
                    else:
                        dstemp = rawworkexp[datatp[0]:datatp[1]].strip().capitalize()
                        # if "worked as" in dstemp.lower():
                        #     dstemp = dstemp[:dstemp.index("worked as")].strip()
                        temp_exp["desc"] = dstemp

                elif len(datatp) == 1:
                    keyword_index = self.found_keword(self.designations, rawworkexp[datatp[0]:])
                    if len(keyword_index) > 0:
                        if jk[1] < rawworkexp.index(keyword_index[0]):
                            start_check = False
                    designation_text, is_previous, list_year = self.get_individual_designation_work_exp(rawworkexp,
                                                                                                        datatp[0],
                                                                                                        None,start_check)
                    # designation_text=rawworkexp[datatp[0]:].strip()
                    # temp_exp["desc"] = '. '.join(rawworkexp[datatp[0]:].split(".")[:-1]).strip().capitalize()
                    if is_previous:
                        if len(rawworkexp[datatp[0]:].split(". ")) > 1 and len(rawworkexp[datatp[0]:].split(". ")) < 30:
                            rawtsc = ' '.join(rawworkexp[datatp[0]:].split(". ")[:-1]).strip().capitalize()
                            # if "worked as" in rawtsc.lower():
                            #     rawtsc = rawtsc[:rawtsc.index("worked as")].strip()
                            temp_exp["desc"] = rawtsc
                        else:
                            temdsc = ' '.join(rawworkexp[datatp[0]:].split(". ")[:]).strip().capitalize()
                            # if "worked as" in temdsc.lower():
                            #     temdsc = temdsc[:temdsc.index("worked as")].strip()
                            temp_exp["desc"] = temdsc
                    else:
                        dstemps = rawworkexp[datatp[0]:].strip().capitalize()
                        # if "worked as" in dstemps.lower():
                        #     dstemps = dstemps[:dstemps.index("worked as")].strip()
                        temp_exp["desc"] = dstemps

                else:
                    temp_exp["desc"] = ""

                # print('==================',found_ind_desg)
                # list_year = self.get_years(temp_exp["desc"])
                if mk == 0:
                    if len(list_year) == 0:
                        list_year = self.get_years(rawworkexp[:datatp[1]])
                # print('listyear====>',list_year)
                if len(list_year) > 1:
                    # print(total_work_experience)
                    if len(total_work_experience) > 0:
                        last_record = total_work_experience[-1]
                        if last_record.get("start_date", "") == "":
                            star_datlast = ""
                            en_datlast = ""
                            try:
                                star_datlast, en_datlast, brdylast = self.get_current_duration(list_year[1],
                                                                                               is_current=False)
                                if "since" in list_year[1].lower() or "till" in list_year[1].lower() or "current" in \
                                        list_year[1].lower() or "present" in \
                                        list_year[1].lower() or "ongoing" in list_year[1].lower():
                                    last_record.update({"is_current": True})
                                    en_datlast = 'Present'
                            except:
                                pass
                            last_record.update({"start_date": star_datlast, "end_date": en_datlast})
                star_dat = ""
                en_dat = ""
                if len(list_year) > 0:
                    try:
                        star_dat, en_dat, brdy = self.get_current_duration(list_year[0], is_current=False)
                        if "since" in list_year[0].lower() or "till" in list_year[0].lower() or "current" in list_year[
                            0].lower() or "present" in list_year[0].lower() or "ongoing" in list_year[0].lower():
                            temp_exp["is_current"] = True
                            en_dat = 'Present'
                    except:
                        pass
                temp_exp["start_date"] = star_dat
                temp_exp["end_date"] = en_dat
                if temp_exp["end_date"] == "Present" and designation_text == "":
                    designation_text = current_designation
                if len(temp_exp.get("desc","")[len(temp_exp.get("company","").get("name","")):]) >= 15:
                    desig_uuid = self.get_location_uuid(designation_text.capitalize(), self.desig_master_data)
                    temp_exp["designation"] = desig_uuid
                    total_work_experience.append(temp_exp)
                else:
                    print("++++++++++++++++",temp_exp)
        # print(total_work_experience)
        return total_work_experience

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def get_location_uuid(self, locs, master_data, is_list=False):
        if not is_list:
            uuid = master_data.get(str(locs).lower().strip(), '')
            return {"uuid": uuid, "name": locs}
        else:
            total_list = []
            for loc in locs:
                dic = {}
                dic["name"] = loc
                dic["uuid"] = master_data.get(str(loc).lower().strip(), '')
                total_list.append(dic)
            return total_list

    def get_multiple_name_with_same_index(self, ini_dict):
        tmp = {}
        tmp_dict = {}
        for j in ini_dict.keys():
            if j[:5] in tmp.keys():
                tmp_dict[tmp[j[:5]]].extend(list(ini_dict[j]))
                tmp_dict[tmp[j[:5]]] = tmp_dict[tmp[j[:5]]]
            else:
                tmp_dict[j] = list(ini_dict[j])
                tmp[j[:5]] = j
        return tmp_dict

    def get_temp_company_index(self, ini_dict, raw_text):
        rev_dict = {}
        for key, value in ini_dict.items():
            rev_dict.setdefault(value, set()).add(key)
        raw_rev_dict = self.get_multiple_name_with_same_index(rev_dict)
        temp_id = []
        max_value = [sorted(list(j)) for j in raw_rev_dict.values()]
        for mf in max_value:
            if mf[0] > 35 and len(mf) > 2 :
                if (max([j-i for i, j in zip(mf[:-1], mf[1:])])-min([j-i for i, j in zip(mf[:-1], mf[1:])]))>500:
                    for j in mf:
                        yrls = self.get_years(raw_text[j - 35:j + 200])
                        if len(yrls) > 0:
                            # temp_id.append(mf[0])
                            temp_id.append(j)
                else:
                    temp_id.append(mf[0])
                    # break
            elif len(mf)==2:
                temp_id.extend(mf)
            elif max(mf) - min(mf) <= 600:
                temp_id.append(mf[0])
            else:
                temp_id.extend(mf)
        recv_dict = {}
        for m in temp_id:
            recv_dict[m] = ini_dict.get(m)
        return recv_dict

    def extract_block(self, filepath):
        # raw_data = self.getText(self.filepath)
        a = time.time()
        raw_dat = self.get_docx_doc_pdf_text(filepath)
        if raw_dat:
            # print(raw_dat)
            print('aaaaaaaaaa', a - time.time())
            b = time.time()
            raw_da = ' '.join(raw_dat.split())
            # raw_da = raw_dat
            raw_data = raw_da.replace("\xe2\x80\x93", "-").replace("", "-")
            raw_data = raw_data.replace("", '-').replace("’", '').replace("|",'')
            raw_data = ' '.join(raw_data.split())
            # print(raw_data)
            self.main_keywordlist.sort(key=lambda s: len(s))
            main_keywordlist = self.main_keywordlist[::-1]
            block_seprated_dict, keyword_index_dict = self.seperation_block_index(main_keywordlist,
                                                                                  raw_data.replace('\u200b', ''))

            print(block_seprated_dict)
            # print('bbbbbbbbb', b - time.time())
            c = time.time()
            rdpSet = set(block_seprated_dict)
            namesSet = set(keyword_index_dict)
            kwdict = {}
            for name in rdpSet.intersection(namesSet):
                kwdict[name] = keyword_index_dict[name]
            segmented_dic = self.get_orginal_segmented_dic(block_seprated_dict, kwdict)
            # print('cccccccc', c - time.time())
            d = time.time()
            segmented_dic["Profile_Name"] = segmented_dic["Profile_Name"] + " " + "xxxxxxxxxxxxxx"
            print(segmented_dic)
            found_cities = self.found_keword(self.cities,
                                             segmented_dic.get("Profile_Name", "") + " " + segmented_dic.get(
                                                 "profile_details", "") + " " + segmented_dic.get("work_experiences",
                                                                                                  ""), is_lower=False)
            city = ""
            if len(found_cities) > 0:
                city = found_cities[0].strip()
            # if len(foundcity) > 0:
            #     city = found_cities.get(foundcity[0], "")
            # print("city==========",found_cities)
            print('ddddddddddd', time.time() - d)
            e = time.time()
            email_id = self.get_email_id(raw_data)
            candidate_name = self.get_candidate_name(segmented_dic)
            location = ""
            if candidate_name == "":
                candidate_name, location = extract_person_name_location(raw_data)
            if city == "":
                city = location
            mobile_number = ""
            location_uuid = self.get_location_uuid(city, self.locations_master_data)
            rawmobile = getPhone(raw_dat)
            if len(rawmobile) > 0:
                mobile_number = rawmobile
            if len(rawmobile) > 2:
                mobile_number = rawmobile[:2]
            # print(segmented_dic)
            birthdate = ""
            dobtext = ""
            if ' dob ' in raw_data.lower():
                dobtext = raw_data.lower().split(" dob ")[-1]
            elif 'date of birth' in raw_data.lower():
                dobtext = raw_data.lower().split("date of birth")[-1]
            elif 'd.o.b.' in raw_data.lower():
                dobtext = raw_data.lower().split("d.o.b.")[-1]
            if dobtext:
                stddate, enddat, birthdate = self.get_current_duration(dobtext,
                                                                       is_birth=True, is_current=False)
            if birthdate == "":
                raw_bdate_text = segmented_dic.get("profile_details", "") + " " + segmented_dic.get("Profile_Name", "")
                for mn in mobile_number:
                    raw_bdate_text = raw_bdate_text.replace(mn, '')
                stddate, enddat, birthdate = self.get_current_duration(raw_bdate_text,
                                                                   is_birth=True, is_current=False)
            resume_dict = {}
            resume_dict["personal_info"] = {"phones": [''.join(str(j).split()) for j in list(set(mobile_number))], "name": candidate_name,
                                            "emails": list(set(email_id)),
                                            "location": location_uuid, "date_of_birth": birthdate}
            print('eeeeeeeeeee', time.time() - e)
            hg = time.time()
            cmp_data_raw = segmented_dic.get("work_experiences", "").lower()
            pvt_ltd_raw_data = re.sub(r"(pvt)[.]\s*(ltd)\s*[.]?", "pvt ltd ", cmp_data_raw)
            if ' • • • • ' in pvt_ltd_raw_data:
                pvt_ltd_raw_data = ' '.join(pvt_ltd_raw_data.split(" • • • • ")[:-1])
            found_cmp = self.found_keword(self.companylist, pvt_ltd_raw_data)
            print(found_cmp)
            print('foundcmp', time.time() - hg)
            # print(pvt_ltd_raw_data)
            found_cmp_index, compkeyindex = self.get_current_keyword_index(pvt_ltd_raw_data, found_cmp)
            print(found_cmp_index, compkeyindex)
            temp_cmp_index = self.get_temp_company_index(found_cmp_index, pvt_ltd_raw_data)
            print('temp_cmp_index--', temp_cmp_index)
            found_cmp_ind = {}
            for key, value in temp_cmp_index.items():
                found_cmp_ind[key] = {value}
            # found_cmp_ind = self.get_multiple_same_index(compkeyindex)
            print('======>>', found_cmp_ind)
            d = time.time()
            found_designation = self.found_keword(self.designations, raw_data)
            found_designation_index, desigkeyindex = self.get_current_keyword_index(raw_data, found_designation)
            # print(found_designation_index)
            found_designation_ind = self.get_multiple_same_index(desigkeyindex)
            found_designation_name = self.get_first_preference_name(found_designation_ind)
            # print(found_designation_name)
            print(time.time() - d)
            # print(raw_data)
            # print(pvt_ltd_raw_data)
            # found_years = self.get_years(pvt_ltd_raw_data)
            # # # print(found_years)
            # found_years_index, yearkeyindex = self.get_current_keyword_index(pvt_ltd_raw_data, found_years)
            # print(found_years_index)
            # start_date, end_date, birth = self.get_current_duration(found_years_index)
            # print(start_date, end_date)
            df = time.time()
            found_skills = self.found_keword(self.skilllist, raw_data)
            skills = list(set(found_skills))
            skills_uuid = self.get_location_uuid(skills, self.skills_master_data, is_list=True)
            ds = time.time()
            # print(found_years_index)
            # print(pvt_ltd_raw_data)
            all_workexp = self.get_complete_work_experince(found_cmp_ind, pvt_ltd_raw_data,
                                                           found_designation_name)
            # all_workexp = self.get_complete_work_experince(found_cmp_ind, found_years_index, pvt_ltd_raw_data, found_designation_name)
            resume_dict["resume"] = {"skills": skills_uuid, "work_exps": all_workexp}
            # print(segmented_dic)
            print(time.time() - ds)
            print(resume_dict)
            return resume_dict
        else:
            empty_dic = {}
            empty_dic["personal_info"] = {}
            empty_dic["resume"] = {}
            return empty_dic


if __name__ == "__main__":
    sttime = time.time()
    # print('tie----->',sttime)
    path = "doc_file/vineettiwaritest.docx"
    # path = "doc_file/vineettiwari_newdocx.docx"
    # path = "doc_file/NeerajKumarYadav.pdf"
    path= "doc_file/Abhishek_Gupta.pdf"
    # path = "doc_file/103_Neha_Thakur.docx"
    # path="doc_file/Aquib_Javed_k.pdf"
    # path ="doc_file/96297505.docx"
    # path="doc_file/Resume1.txt"
    # path = "doc_file/MridulSaran.pdf"
    # path = "doc_file/15205851.docx"
    # path = "doc_file/Abhishek_Gupta1.pdf"
    # path = "doc_file/sagar_singh_resume.pdf"
    # path = "doc_file/Santosh_Data Scientist_Nokia.docx"
    # path = "doc_file/101_MREvaluation_RGS_41_Lc_1513235_resume_5807472e0eb088180bc6aec9.docx"
    # path ="doc_file/S001_MREvaluation_RT_4814_Hc_Li76__Tb2_1214006_Dice_Resume_5807098a0eb08830acf17051.docx"
    # path = "doc_file/Pankaj Sunal_Java.pdf"
    # path = "doc_file/Resume_DOCX.docx"
    # path = "doc_file/Shivam_Sharma_Resume.docx"
    # path = "doc_file/Abijeet Singh.docx"
    # path ="doc_file/102_MREvaluation_RGS_51_Lc_1307001_wayne_sresume_580742f90eb088180bc69e8c.docx"
    # path = "doc_file/103_MREvaluation_RGS_58_Lc_Li15_1301761_Courtney_Hughey_580744580eb088180bc6a38a.docx"
    # path ="doc_file/Avneesh Atri_7 yrs.docx"

    # path = "doc_file/Pankaj Sunal_Java.pdf"
    # path ="doc_file/105_VikramReddy Gajjala.pdf" Abhishek Gupta_Product Manager
    # path = "doc_file/S002_MREvaluation_RT_4561_Hc_Li88__Tb1_2100561_SAP_BW_BI_HANA_Architect_11Yrs_SRI_5807093a0eb08830acf16fc7.docx"
    path = "doc_file/104_RAMGOPAL BATTU.pdf"
    # path = "doc_file/Narender_Singh.docx"
    # path="doc_file/Avneesh Atri_7 yrs (1).docx"
    # path = "doc_file/Pankaj Tripathi_Data Scientist_Optum.docx"
    # path = "doc_file/Abhishek Gupta_Product Manager.docx"
    # path = "doc_file/Abhinav Verma_2 yrs_Appster.pdf"
    # path = "doc_file/Krishan_Java_Mobiloitte.docx"
    # path ="doc_file/Resume_Multiple_Email_Mobile_Rows.docx" # issue with parser--------------
    # path = "doc_file/test.doc"
    # path = "doc_file/Resume_Single_Column.docx"
    # path = "doc_file/Resume_Multiple_Column.docx"
    # path = "doc_file/Resume.docx"
    # path = "doc_file/multiple Rows_Multiple Column _Tabular Form Resume.docx"
    # path = "doc_file/Abhijit Das_Power2SME.pdf"
    # path = "doc_file/Aarjav Jain_Product Manager_Mettl_6 yrs (1).docx"
    # path = "doc_file/Garima CV Testing-3.2 Yrs.docx"
    # path = "doc_file/Abhinandan Malhotra_Data Scientist_IIT.pdf"
    # path = "doc_file/AbhishekLuthra[2_8].pdf"
    # path = "doc_file/Aditya Jain_Product Manager.pdf"
    # path ="doc_file/Aditya Pappula_Product Manager_Vmock.pdf"
    # path ="doc_file/Akash Srivastav_JPMorgan.pdf"
    # path ="doc_file/Ajeet kumar_7 yrs_Java_Appster.docx"
    # path = "doc_file/AkashPandey[1_5]_Java_Wipro.docx"
    # path ="doc_file/Akash_Gupta_Product Manager_Study Pad.pdf"
    # path = "doc_file/Mo TAVISH ANSARI (5).pdf"

    obj = ResumeParser()
    obj.extract_block(path)
    # print('+++++++++++',time.time())
    print(time.time() - sttime)
    # os.remove("C:\\Users\\vktiwari\\PycharmProjects\\Resume_Parser\\venv\\src\\doc_file\\MridulSaran.pdf")
    # for pa in ["5b77bfe5a38d04de1d1c8463.docx"]:
    # # # for pa in os.listdir("Evaluation300/")[10:15]:
    #     path = "Evaluation200/" + pa
    #     print(path)
    #     obj = ResumeParser(path)
    #     obj.extract_block()
