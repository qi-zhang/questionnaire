# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os.path
import ConfigParser
import gspread
home = os.path.expanduser("~")
configfile = os.path.join(home, 'stat157.cfg')
config = ConfigParser.SafeConfigParser()
config.read(configfile)
username = config.get('google', 'username')
password = config.get('google', 'password')
print username
docid = config.get('questionnaire', 'docid')
client = gspread.login(username, password)
spreadsheet = client.open_by_key(docid)
worksheet = spreadsheet.get_worksheet(0)
print docid
fieldnames = ['What is your learning style?','In which of these topics would you feel confident being a technical lead for other students?']
print fieldnames
filtered_data = []
for row in worksheet.get_all_records():
   filtered_data.append({k:v for k,v in row.iteritems() if k in fieldnames})
print "Number of rows: {}".format(len(filtered_data))
for row in (filtered_data):
   print row
questionnaire = filtered_data
from pandas import DataFrame, read_csv
from xml.etree import ElementTree
import pandas as pd
questdf = DataFrame(questionnaire)

questdf['Visual'] = questdf['What is your learning style?']
questdf['Aural'] = questdf['What is your learning style?']
questdf['Read/Write'] = questdf['What is your learning style?']
questdf['Kinesthetic'] = questdf['What is your learning style?']
questdf["TechLead"] = questdf["In which of these topics would you feel confident being a technical lead for other students?"]
Style=questdf['What is your learning style?']
import re

def extract(Name,Record,ExtraPattern):
    pattern=Name+'.*[0-9]+'
    if len(ExtraPattern) > 0:
        pattern=pattern+'|'+ExtraPattern+'.*[0-9]+'    # Record no.32 needs special handling
    result=re.findall(pattern,Record)      # Use Regular expression to search
    if len(result) >0:
        result=int(re.findall('[0-9]+',result[0])[0])
    else:
        result= "NA"
    return result

Visual = questdf['Visual']
Aural = questdf['Aural']
ReadWrite = questdf['Read/Write']
Kinesthetic = questdf['Kinesthetic']

for i in range(len(Style)):
    Visual[i]= extract("Visual",Style[i],"")
    Aural[i]= extract("Aural",Style[i],"")
    ReadWrite[i]= extract("Read/Write",Style[i],"Reading/Writing")    # Record no.32 needs special handling
    Kinesthetic[i]= extract("Kinesthetic",Style[i],"")

del questdf["What is your learning style?"]
del questdf["In which of these topics would you feel confident being a technical lead for other students?"]
#print questdf

SkillList=["github","Python","XML","HTML5","LaTeX","jQuery","Statistics","Probability","R","JavaScript","Blogging","Academic Publishing"]
TechLead=questdf["TechLead"]
for skill in SkillList:
    questdf[skill]=questdf["TechLead"]
    x=questdf[skill]
    for i in range (len(TechLead)):
        x[i]=skill in TechLead[i]

print "new table"
#del questdf["TechLead"]
print  questdf

