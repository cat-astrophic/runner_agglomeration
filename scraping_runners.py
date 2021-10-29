# This script scrapes runner location data from the USATF marathon trials

# Importing required modules

import urllib
from bs4 import BeautifulSoup as bs
import pandas as pd

# Specifiying your username and output directory

username = ''
direc = 'C:/Users/' + username + '/Documents/Data/runner_agglomeration/'

# Getting data for 2020

# Declaring a lists to contain data

athletes = []
locations = []

# Scraping data

url = 'https://www.atlanta2020trials.com/athletes'
page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(page)
soup = bs(response, 'html.parser')
data = soup.find_all('a')[30:229]

for d in data:
    
    d = str(d)
    idx = d.index('">')
    d = d[idx+2:]
    idx2 = d.index('<br')
    rnr = d[:idx2]
    athletes.append(rnr)

# Creating links from athletes

links = [a.replace(' ','-') for a in athletes]

to_fix = ['Matthew-McDonald', 'Scott-Smith', 'Elkanah-Kibet', 'Tyler-McCandless',
          'Chris-Derrick', 'Chris-Bendtsen', 'John-(JJ)-Santana', 'Adam-Schroer-',
          'Kevin-Scott-Colón', 'Jonathan-Mott', "Austin-O'Brien", 'Anthony-Tomisch',
          'Everett-Hackett']

updates = ['Matthew-McDonald-2', 'scott_smith/56', 'Elkanah-Kibet-not-yet-registered',
           'Tyler-McCandless-2', 'Chris-Derri', 'Chris-Bendtsen-2', 'JJ-Santana',
           'Adam-Schroer', 'Kevin-Scott-Colón', 'Jonothan-Mott', "Austin-OBrien",
           'Anthony-Tomsich', 'Everett-Hacket']

links = [updates[to_fix.index(l)] if l in to_fix  else l for l in links]

# Collecting athlete specific data

for l in links:
    
    if l == 'Kevin-Scott-Colón':
        
        locations.append('Seattle, WA')
        
    else:
        
        url = 'https://www.atlanta2020trials.com/fan-zone/athletes/' + l
        page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(page)
        soup = bs(response, 'html.parser')
        data = soup.find_all('p')
        d = str(data[5])
        idx = d.index('/strong>')
        d = d[idx+8:]
        idx2 = d.index('</p>')
        loc = d[:idx2]
        
        if loc[0] == ' ':
            
            loc = loc[1:]
            
        loc = loc.replace('\xa0','')
        loc = loc.replace('<strong>Residence:\xa0</strong>','')
        loc = loc.replace('<strong>Residence:</strong>','')
        locations.append(loc)

# Make a dataframe

athletes = pd.Series(athletes, name = 'Name')
locations = pd.Series(locations, name = 'Location')
years = pd.Series([2020]*len(athletes), name = 'Year')
df2020 = pd.concat([years, athletes, locations], axis = 1)

# Getting data for 2016

# Declaring a lists to contain data

athletes = []
locations = []

# Scraping data

url = 'https://www.flotrack.org/events/5009827-2016-us-olympic-team-marathon-trials/entries'
page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(page)
soup = bs(response, 'html.parser')
data = soup.find_all('tr')[1:169]

for d in data:
    
    tmp = d.find_all('td')
    athletes.append(str(tmp[0]).replace('<td>','').replace('</td>','').replace('\n\t',''))
    loc = str(tmp[2]).replace('<td>','').replace('</td>','').replace('\n\t','') + ', ' + str(tmp[3]).replace('<td>','').replace('</td>','').replace('\n\t','')
    locations.append(loc)

# Make a dataframe

athletes = pd.Series(athletes, name = 'Name')
locations = pd.Series(locations, name = 'Location')
years = pd.Series([2016]*len(athletes), name = 'Year')
df2016 = pd.concat([years, athletes, locations], axis = 1)

# Getting data for 2012

# Declaring a lists to contain data

athletes = []
locations = []

# Scraping data

url = 'http://oldserver.usatf.org/events/2012/OlympicTrials-Marathon/results/Men.asp'
page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(page)
soup = bs(response, 'html.parser')
data = soup.find_all('tr')[4:89]

for d in data:
    
    tmp = d.find_all('td')
    athletes.append(str(tmp[1]).replace('<td><font size="-1">','').replace('</font></td>',''))
    locations.append(str(tmp[3]).replace('<td><font size="-1">','').replace('</font></td>',''))

# Make a dataframe

athletes = pd.Series(athletes, name = 'Name')
locations = pd.Series(locations, name = 'Location')
years = pd.Series([2012]*len(athletes), name = 'Year')
df2012 = pd.concat([years, athletes, locations], axis = 1)

# Getting data for 2008

# Declaring a lists to contain data

athletes = []
locations = []

# Scraping data

url = 'http://legacy.usatf.org/events/2008/OlympicTrials-Marathon-Men/results.asp'
page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(page)
soup = bs(response, 'html.parser')
data = soup.find_all('tr')[2:]

for d in data:
    
    tmp = d.find_all('td')
    athletes.append(str(tmp[2]).replace('<td>','').replace('</td>',''))
    locations.append(str(tmp[4]).replace('<td>','').replace('</td>',''))

# Make a dataframe

athletes = pd.Series(athletes, name = 'Name')
locations = pd.Series(locations, name = 'Location')
years = pd.Series([2008]*len(athletes), name = 'Year')
df2008 = pd.concat([years, athletes, locations], axis = 1)

# Getting data for 2004

# Declaring a lists to contain data

athletes = []
locations = []

# Scraping data

url = 'http://legacy.usatf.org/events/2004/OlympicTrials-Marathon-Men/results.asp'
page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(page)
soup = bs(response, 'html.parser')
data = str(soup.find_all('tr'))[str(soup.find_all('tr')).index('===== ========================== === ================== =======')+65:]

while len(data) > 10:
    
    while data[0] == ' ': # gets to place
        
        data = data[1:]
        
    data = data[data.index(' ')+1:] # find next name
    
    idx = len(data) # find age
    
    for i in range(10):
        
        try:
            
            idx = min(data.index(str(i)),idx)
            
        except:
            
            continue
        
    rnr = data[:idx] # get runner name
    
    while rnr[-1] == ' ': # cleans runner name
        
        rnr = rnr[:-1]
        
    if rnr == 'href="results-splits.asp">Results with splits</a></p>\n</td></tr>]': # test for end of loop
        
        break
        
    else:
        
        athletes.append(rnr)
        
        data = data[idx+2:] # get rid of the age
        
        while data[0] == ' ': # find location
            
            data = data[1:]
        
        idx = data.index('\r\n') # find time
        loc = data[:idx-7] # get location
        
        while loc[-1] == ' ': # clean location
            
            loc = loc[:-1]
            
        loc = loc[:-3] + ',' + loc[-3:] # add comma
        locations.append(loc)
        data = data[idx+2:] # ready for next iteration

# Make a dataframe

athletes = pd.Series(athletes, name = 'Name')
locations = pd.Series(locations, name = 'Location')
years = pd.Series([2004]*len(athletes), name = 'Year')
df2004 = pd.concat([years, athletes, locations], axis = 1)

# Getting data for 2000

# Declaring a lists to contain data

athletes = []
locations = []

# Scraping data

url = 'https://runnersweb.com/running/us_omt.html'
page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(page)
soup = bs(response, 'html.parser')
data = soup.find_all('tr')[2:]

for d in data:
    
    tmp = d.find_all('td')
    athletes.append(str(tmp[2]).replace('<td>','').replace('</td>',''))
    loc = str(tmp[3]).replace('<td>','').replace('</td>','') + ', ' + str(tmp[4]).replace('<td>','').replace('</td>','').replace(' ','')
    locations.append(loc)

# Make a dataframe

athletes = pd.Series(athletes, name = 'Name')
locations = pd.Series(locations, name = 'Location')
years = pd.Series([2000]*len(athletes), name = 'Year')
df2000 = pd.concat([years, athletes, locations], axis = 1)

# Create a single dataframe with all results

df = pd.concat([df2020, df2016, df2012, df2008, df2004, df2000], axis = 0).reset_index(drop = True)

# Write output to file

df.to_csv(direc + '/data/trials_data.csv', index = False)

##### 2012 does not contain DNFs so some runners are missing... cannot find this info anywhere

