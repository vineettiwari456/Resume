#Extract Phone
import pandas as pd
import re
from flashtext import KeywordProcessor
from nltk import sent_tokenize

class extract_phone_details:
    
    def __init__(self, input_text):
        self.input_text = input_text
        self.df = pd.read_csv("country_code.csv")
        
    
    def getPhone(self, inputString, debug=False):
        number = None
        try:
            pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
            match = pattern.findall(inputString)
            match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el))>6]
            match = [re.sub(r'\D$', '', el).strip() for el in match]
            match = [el for el in match if len(re.sub(r'\D','',el)) <= 15]
                # Remove number strings that are greater than 15 digits
            try:
                for el in list(match):
                    # Create a copy of the list since you're iterating over it
                    if len(el.split('-')) > 3: continue # Year format YYYY-MM-DD
                    for x in el.split("-"):
                        try:
                            # Error catching is necessary because of possibility of stray non-number characters
                            # if int(re.sub(r'\D', '', x.strip())) in range(1900, 2100):
                            if x.strip()[-4:].isdigit():
                                if int(x.strip()[-4:]) in range(1900, 2100):
                                    # Don't combine the two if statements to avoid a type conversion error
                                    match.remove(el)
                        except:
                            pass
            except:
                pass
            number = match
        except:
            pass
        return(number)
        
    def country_code_number(self, code):
        result_dict = {}
        if(self.number[:len(code)] == code):
            if(code =="91"):
                if(len(self.number) == 10):
                    result_dict["country_code"]= ""
                    result_dict["number"] = self.number
                if(len(self.number) == 12):
                    result_dict["country_code"]= code
                    result_dict["number"] = self.number[len(code):]
            else:
                result_dict["country_code"]= code
                result_dict["number"] = self.number[len(code):]
        return(result_dict)
        
    def extract_phone(self):
        result_dict = {}
        try:
            self.number = ''.join([n for n in self.getPhone(self.input_text)[0] if n.isdigit()])
            for i in range(self.df.shape[0]):
                result_dict = self.country_code_number(str(self.df.loc[i,'Code']))
                if(len(result_dict) > 1):
                    return(result_dict)
                    break
                elif(i == self.df.shape[0]):
                    result_dict["country_code"]= ""
                    result_dict["number"] = self.number
                    return(result_dict)
        except:
            return(result_dict)
        

class extract_education_details:
    
    def __init__(self, input_text):
        self.input_text = input_text
        self.degree_file_path = "doc_qualification/highest_qualification.txt"
        self.college_file_path = "doc_qualification/college.txt"
        self.board_file_path = "doc_qualification/education_board.txt"
        self.specialization_file_path = "doc_qualification/highest_specialization.txt"
        
    def line_count(self,start):
        for k, v in self.line_index_dict.items():
            if(v > start):
                return(k)
        return(k+1)
        
    def degree_list(self):
        degree_dict ={}
        with open(self.degree_file_path) as fp:
            lines = fp.read().splitlines()
        processor = KeywordProcessor()
        processor.add_keywords_from_list(lines)
        found = processor.extract_keywords(self.document, span_info=True)
        for count, value in enumerate(found):
            line_number = self.line_count(value[1])
            degree_dict[value[0]] = line_number
        return(degree_dict)
        
    def board_list(self):
        board_dict = {}
        with open(self.board_file_path) as fp:
            lines = fp.read().splitlines()
        processor = KeywordProcessor()
        processor.add_keywords_from_list(lines)
        found = processor.extract_keywords(self.document, span_info=True)
        for count, value in enumerate(found):
            line_number = self.line_count(value[1])
            board_dict[value[0]] = line_number
        return(board_dict)
    
    def college_list(self):
        college_dict = {}
        with open(self.college_file_path) as fp:
            lines = fp.read().splitlines()
        processor = KeywordProcessor()
        processor.add_keywords_from_list(lines)
        found = processor.extract_keywords(self.document, span_info=True)
        for count, value in enumerate(found):
            line_number = self.line_count(value[1])
            college_dict[value[0]] = line_number
        return(college_dict)
    
    def specialization_list(self):
        specialization_dict = {}
        with open(self.specialization_file_path) as fp:
            lines = fp.read().splitlines()
        processor = KeywordProcessor()
        processor.add_keywords_from_list(lines)
        found = processor.extract_keywords(self.document, span_info=True)
        for count, value in enumerate(found):
            line_number = self.line_count(value[1])
            specialization_dict[value[0]] = line_number
        return(specialization_dict)
    
    def year_list(self):
        year_dict = {}
        for count, line in enumerate(self.lines):
            if re.search(r'\b[21][09][8901][0-9]', line.lower()):
                value = re.findall(r'\b[21][09][8901][0-9]',line.lower())
                year_dict[max(value)] = str(count)
    #            year_dict[value[0]] = str(count) + ":" + str(re.search(r'\b[21][09][8901][0-9]', line.lower()).start())
        return(year_dict)
        
    def match_line_dict(self,line_index, comp_dict):
        maxi = 0
        temp_dict = {}
        for k,v in comp_dict.items():
            if(int(v) >= line_index):
                temp_dict[v] = 1/(abs(line_index - int(v))+1)
                if (maxi < 1/(abs(line_index - int(v))+1)):
                    maxi = 1/(abs(line_index - int(v))+1)
        for k , v in temp_dict.items():
            if v == maxi and maxi > 0.05:
                for key,value in comp_dict.items():
                    if(k == value):
                        return(key)
        
    
    def extract_qualification(self):
        result = list()
        lines = []
        line_index_dict = {}
        for count, line in enumerate(sent_tokenize(self.input_text)):
            if (count > 0):
                line_index_dict[count] = len(''.join(line)) + (line_index_dict[int(count)-1])
            else:
                line_index_dict[count] = len(''.join(line))
            lines.append(line)
        self.lines = lines
        self.line_index_dict = line_index_dict
        self.document = ''.join(lines)
        d_dict = self.degree_list()
        for k,v in d_dict.items():
            result_dict = {}
            result_dict["degree"] = k
            result_dict["year"] = self.match_line_dict(int(v), self.year_list())
            result_dict["college"] = self.match_line_dict(int(v), self.college_list())
            result_dict["board"] = self.match_line_dict(int(v), self.board_list())
            result.append(result_dict)       
        return(result)
        

# result = extract_phone_details("My number is 917755057892")
# print(result.extract_phone())
import time
st = time.time()
result_q = extract_education_details('''College/Institutes Board/ University Year Aggregate B.Tech(CSE) A.I.E.T Lucknow U.P.T.U. Lucknow 2009-2013 68.92% M.Sc(Math) B.S Mehta Bharwari Kausambi C.S.J.M.U. Kanpur 2005-2007 53.80% B.Sc(PCM) R R P G Amethi Dr.R M L Avadh University Faizabad 2003-2005 51.50% H.S.C RRIC Amethi UP UP Board 2001-2002 58.40% S.S.C SSPIC Amethi UP UP Board 1999-2000 60.00% Aggregate 68.92% Branch Computer Science.''')
print(result_q.extract_qualification())
        
print(time.time()-st)


