# -*- coding:utf-8 -*-
import re

# df = pd.read_csv("country_code.csv")
input_text = "My number is 9451042288"


def getPhone(inputString, debug=False):
    '''
    Given an input string, returns possible matches for phone numbers. Uses regular expression based matching.
    Needs an input string, a dictionary where values are being stored, and an optional parameter for debugging.
    Modules required: clock from time, code.
    '''
    number = None
    try:
        pattern = re.compile(
            r'\b([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)\b')
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
                            if int(x.strip()[:]) in range(1900, 2100):
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
# input_text='Parth Shukla Parth_shukla158@yahoo.com 1198 Lilac Circle, Mumbai, RDM 17 (987) 225-6638 9 years experience in the Labor/Industrial field. Federal Gateway Moving and Storage 1975 Walton Rd. St. Louis, Mo, 63114'
# input_text='''GADADHASU SIVA Phone: 9704322068 Email: 2010 2007 sivagadadasu1995@yahoo.com CAREER OBJECTIVE: To secure a challenging position, effectively
# '''
# print(getPhone(input_text))
# input_text='''GADADHASU SIVA Phone: 9704322068 Email: sivagadadasu1995@yahoo.com CAREER OBJECTIVE: To secure a challenging position, effectively
# '''