#import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib.request
import csv

urlpage =  'http://www.fasttrack.co.uk/league-tables/tech-track-100/league-table/'

#create a new firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(urlpage)

# query the website and return the html to the variable 'page'
page = urllib.request.urlopen(urlpage)
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')

#print(soup)

table = soup.find('table', attrs={'class': 'tableSorter'})
results =  table.find_all('tr')
print('Number of results', len(results))

#create headers
rows = []
rows.append(['Rank', 'Company Name', 'Webpage', 'Description', 'Location', 'Year end', 'Annual sales rise over 3 years', 'Sales $000s', 'Staff', 'Comments'])
#print(rows)

#loop over results
for result in results:
    data = result.find_all('td')
    if len(data) == 0:
        continue

    # write columns to variables
    rank = data[0].getText()
    company = data[1].getText()
    location = data[2].getText()
    yearend = data[3].getText()
    salesrise = data[4].getText()
    sales = data[5].getText()
    staff = data[6].getText()
    comments = data[7].getText()

    #print('Company is', company)
    #print('Sales', sales)

    # extract description from the name
    companyname = data[1].find('span', attrs={'class':'company-name'}).getText()    
    description = company.replace(companyname, '')
        
    # remove unwanted characters
    sales = sales.strip('*').strip('†').replace(',','')

    # go to link and extract company website
    url = data[1].find('a').get('href')
    page = urllib.request.urlopen(url)
    # parse the html 
    soup = BeautifulSoup(page, 'html.parser')
    # find the last result in the table and get the link
    try:
        tableRow = soup.find('table').find_all('tr')[-1]
        webpage = tableRow.find('a').get('href')
    except:
        webpage = None

    # write each result to rows
    rows.append([rank, companyname, webpage, description, location, yearend, salesrise, sales, staff, comments])
print(rows)

# Create csv and write rows to output file
with open('techtrack100.csv','w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)
