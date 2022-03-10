import requests
from bs4 import BeautifulSoup
import re
import numpy as np


# We download the source code to avoid making queries each time we want to use our system
# with open("./codesourceInfoJDM.html") as fp:
#     soup = BeautifulSoup(fp, 'html.parser')

vgm_url = 'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=toto&rel='
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')


page = soup.find('code').getText()

# Delete all the comments (whitespace can be seen as \s in regex.)
pattern ="^\/\/ *.*"
prepro = re.sub(pattern, '', page, flags=re.MULTILINE)

# Delete all the blank lines (only the first and last one remained)
prepro2=re.sub(r'\n\s*\n','\n',prepro,re.MULTILINE)

# Make this as a list
prepro3 = prepro2.split("\n")

# Removing single quote from the list
for singleQuote in range(0,len(prepro3)):
    prepro3[singleQuote] = prepro3[singleQuote].replace("'","")

print(prepro3)

# Convert raw data into semi-structured data (in this case csv format file)
np.savetxt("KnowledgeBase.csv", prepro3, delimiter =",", fmt ='%s')