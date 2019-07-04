import pandas as pd
import re
import nltk
import os
from flashtext import KeywordProcessor

df = pd.read_csv("country_code.csv")


def getPhone(inputString, debug=False):
    number = None
    try:
        pattern = re.compile(
            r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        # Understanding the above regex
        # +91 or (91) -> [+(]? \d+ -?
        # Metacharacters have to be escaped with \ outside of character classes; inside only hyphen has to be escaped
        # hyphen has to be escaped inside the character class if you're not incidication a range
        # General number formats are 123 456 7890 or 12345 67890 or 1234567890 or 123-456-7890, hence 3 or more digits
        # Amendment to above - some also have (0000) 00 00 00 kind of format
        # \s* is any whitespace character - careful, use [ \t\r\f\v]* instead since newlines are trouble
        match = pattern.findall(inputString)
        # match = [re.sub(r'\s', '', el) for el in match]
        # Get rid of random whitespaces - helps with getting rid of 6 digits or fewer (e.g. pin codes) strings
        # substitute the characters we don't want just for the purpose of checking
        match = [re.sub(r'[,.]', '', el) for el in match if len(re.sub(r'[()\-.,\s+]', '', el)) > 6]
        # Taking care of years, eg. 2001-2004 etc.
        match = [re.sub(r'\D$', '', el).strip() for el in match]
        # $ matches end of string. This takes care of random trailing non-digit characters. \D is non-digit characters
        match = [el for el in match if len(re.sub(r'\D', '', el)) <= 15]
        # Remove number strings that are greater than 15 digits
        try:
            for el in list(match):
                # Create a copy of the list since you're iterating over it
                if len(el.split('-')) > 3: continue  # Year format YYYY-MM-DD
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
    return (number)


def country_code_number(number, code):
    result_dict = {}
    if (number[:len(code)] == code):
        if (code == "91"):
            if (len(number) == 10):
                result_dict["country_code"] = ""
                result_dict["number"] = number
            if (len(number) == 12):
                result_dict["country_code"] = code
                result_dict["number"] = number[len(code):]

        else:
            result_dict["country_code"] = code
            result_dict["number"] = number[len(code):]
    return (result_dict)


def extract_phone(input_text):
    result_dict = {}
    try:
        number = ''.join([n for n in getPhone(input_text)[0] if n.isdigit()])
        for i in range(df.shape[0]):
            result_dict = country_code_number(number, str(df.loc[i, 'Code']))
            if (len(result_dict) > 1):
                return (result_dict)
                break
            elif (i == df.shape[0]):
                result_dict["country_code"] = ""
                result_dict["number"] = number
                return (result_dict)
    except:
        return (result_dict)


# print(extract_phone("My number is 917755057892"))


# Let's try to get result in input format of model
def match_string(str1, str2):
    str2 = str2.lower()
    str1 = str1.lower()
    if (re.search(" " + str2 + " ", str1)):
        match = re.search(" " + str2 + " ", str1)
        return (match.start())
    else:
        match = re.search(str2 + " ", str1)
        if (match is not None):
            if (match.start() == 0):
                return (match.start())
            else:
                return (-1)
        else:
            return (-1)


def line_count(start, line_index_dict):
    for k, v in line_index_dict.items():
        if (v > start):
            return (k)
    return (k + 1)


def board_list(document, line_index_dict):
    board_dict = {}
    with open("doc_qualification/education_board.txt") as fp:
        lines = fp.read().splitlines()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(lines)
    found = processor.extract_keywords(document, span_info=True)
    for count, value in enumerate(found):
        line_number = line_count(value[1], line_index_dict)
        board_dict[value[0]] = line_number
    return (board_dict)


def college_list(document, line_index_dict):
    college_dict = {}
    with open("doc_qualification/college.txt") as fp:
        lines = fp.read().splitlines()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(lines)
    found = processor.extract_keywords(document, span_info=True)
    for count, value in enumerate(found):
        line_number = line_count(value[1], line_index_dict)
        college_dict[value[0]] = line_number
    return (college_dict)


def specialization_list(document, line_index_dict):
    specialization_dict = {}
    with open("doc_qualification/highest_specialization.txt") as fp:
        lines = fp.read().splitlines()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(lines)
    found = processor.extract_keywords(document, span_info=True)
    for count, value in enumerate(found):
        line_number = line_count(value[1], line_index_dict)
        specialization_dict[value[0]] = line_number
    return (specialization_dict)


def year_list(lines):
    year_dict = {}
    for count, line in enumerate(lines):
        if re.search(r'\b[21][09][8901][0-9]', line.lower()):
            value = re.findall(r'\b[21][09][8901][0-9]', line.lower())
            year_dict[max(value)] = str(count)
    #            year_dict[value[0]] = str(count) + ":" + str(re.search(r'\b[21][09][8901][0-9]', line.lower()).start())
    return (year_dict)


def degree_list(document, line_index_dict):
    degree_dict = {}
    with open("doc_qualification/highest_qualification.txt") as fp:
        lines = fp.read().splitlines()
    processor = KeywordProcessor()
    processor.add_keywords_from_list(lines)
    found = processor.extract_keywords(document, span_info=True)
    for count, value in enumerate(found):
        line_number = line_count(value[1], line_index_dict)
        degree_dict[value[0]] = line_number
    return (degree_dict)


def match_line_dict(line_index, comp_dict):
    maxi = 0
    temp_dict = {}
    for k, v in comp_dict.items():
        if (int(v) >= line_index):
            temp_dict[v] = 1 / (abs(line_index - int(v)) + 1)
            if (maxi < 1 / (abs(line_index - int(v)) + 1)):
                maxi = 1 / (abs(line_index - int(v)) + 1)
    for k, v in temp_dict.items():
        if v == maxi and maxi > 0.05:
            for key, value in comp_dict.items():
                if (k == value):
                    return (key)


def qualification(file_path):
    print(file_path)
    result = list()
    lines = []
    line_index_dict = {}
    text ='''College/Institutes Board/ University Year Aggregate B.Tech(CSE) A.I.E.T Lucknow U.P.T.U. Lucknow 2009-2013 68.92% M.Sc(Math) B.S Mehta Bharwari Kausambi C.S.J.M.U. Kanpur 2005-2007 53.80% B.Sc(PCM) R R P G Amethi Dr.R M L Avadh University Faizabad 2003-2005 51.50% H.S.C RRIC Amethi UP UP Board 2001-2002 58.40% S.S.C SSPIC Amethi UP UP Board 1999-2000 60.00% Aggregate 68.92% Branch Computer Science.'''
    for count, line in enumerate(text):
        if (count > 0):
            line_index_dict[count] = len(''.join(line)) + (line_index_dict[int(count) - 1])
        else:
            line_index_dict[count] = len(''.join(line))
        lines.append(line)

    if (len(lines) == 1):
        lines = nltk.sentence_tokenize(lines)

    document = ''.join(lines)
    print(document, line_index_dict)
    d_dict = degree_list(document, line_index_dict)
    y_dict = year_list(lines)
    c_dict = college_list(document, line_index_dict)
    b_dict = board_list(document, line_index_dict)
    for k, v in d_dict.items():
        result_dict = {}
        result_dict["degree"] = k
        result_dict["year"] = match_line_dict(int(v), y_dict)
        result_dict["college"] = match_line_dict(int(v), c_dict)
        result_dict["board"] = match_line_dict(int(v), b_dict)
        result.append(result_dict)
    return (result)


# =============================================================================
# input_files_list = os.listdir("resumes/v1/resume_txt")
# =============================================================================
# =============================================================================
#
# =============================================================================
print(qualification('doc_qualification/test.txt'))