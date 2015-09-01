import datetime as dt
import os
import requests
from bs4 import BeautifulSoup as bs

print('Started: ' + str(dt.datetime.now()))

base_url = 'http://www.iaaf.org/competitions/iaaf-world-championships'

championships = [
    # '15th-iaaf-world-championships-4875',
    '14th-iaaf-world-championships-4873',
    '13th-iaaf-world-championships-in-athletics-4147',
    '12th-iaaf-world-championships-in-athletics-3658',
    '11th-iaaf-world-championships-in-athletics-3653',
    '10th-iaaf-world-championships-in-athletics-3365',
    '9th-iaaf-world-championships-in-athletics-2962',
    '8th-iaaf-world-championships-2639',
    '7th-iaaf-world-championships-in-athletics-1822',
    '6th-iaaf-world-championships-in-athletics-1274',
    '5th-iaaf-world-championships-in-athletics-441',
    '4th-iaaf-world-championships-in-athletics-1',
    '3rd-iaaf-world-championships-in-athletics-5',
    '2nd-iaaf-world-championships-in-athletics-4',
    '1st-iaaf-world-championships-in-athletics-3',
]

genders = [
    'men',
    'women'
]

events = [
    '100',
    '200',
    '400',
    '800',
    '1500',
    '3000',
    '5000',
    '10000'
]

generic_url = '/{0}/results/{1}/{2}-metres/final/result'

pages = [base_url + generic_url.format(c,g,e) 
         for c in championships \
         for g in genders \
         for e in events]

collection_folder_name = 'RawEventPage'

if __name__ == "__main__":
    
    try:
        os.mkdir(collection_folder_name)
    # except:

    log_file = open('LogResults.txt','w')
    not_found_pages = []
    found_pages = []

    for p in pages:
        page = requests.get(p)
        page_soup = bs(page.text)

        if "Page Not Found" in page_soup.title.contents[0]:
            # Not all events were ran every year - the women ran 3K until
            # 1983 before switching to the 5k
            not_found_pages.append(p)
            log_file.write('Didn\'t find: '+p + "\n")
            pass

        else:
            found_pages.append(p)
            file_name = page_soup.find_all('meta')[3]['content'] + ".html"
            file_path = os.path.join(
                collection_folder_name, 
                file_name
                )

            page_file = open(file_path,'w')
            page_file.write(str(page_soup))
            log_file.write('Did find: '+p + "\n")

            
            
print('Finished at: ' + str(dt.datetime.now()))            