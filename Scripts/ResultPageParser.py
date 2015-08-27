import os
from bs4 import BeautifulSoup as bs

def parse_web_page(page_name):
    """Extracts the relevant information from a results webpage.
    Returns a list of dicts"""

    def get_athlete_details(athlete):
        """Logic to extract athlete details from the athlete tags.
        Accepts a bs tag"""

        athlete_strings = [str(i) for i in list(athlete.contents)]
        athlete_multiline_string = "".join(athlete_strings)
        athlete_oneline_string = "".join(athlete_multiline_string.split())
        athlete_id = re.findall(r'\d*\d',athlete_oneline_string)[0]

        name_strings = [i[0:i.find('<')] for i in athlete_oneline_string.split('>')]
        name_strings_formatted = [i for i in filter(lambda x: x, name_strings)]

        athlete_first_name = name_strings_formatted[0].replace(' ','')
        athlete_last_name = name_strings_formatted[1].replace(' ','')    

        results = {
            'id' : athlete_id,
            'first_name' : athlete_first_name,
            'last_name' : athlete_last_name
        }

        return results


    def get_mark_details(mark):
        """Logic to extract country from the mark tags.
        Accepts a bs tag"""

        mark_strings = [str(i) for i in list(mark.contents)]
        mark_multiline_string = "".join(mark_strings)
        mark_oneline_string = "".join(mark_multiline_string.split())

        if mark_oneline_string == "DNF" or \
            mark_oneline_string == "DNS" or \
            mark_oneline_string == "DQ":
            return {'total_time' : None}

        vals = [float(val) for val in mark_oneline_string.split(':')]
        multiple = [math.pow(60,i) for i in reversed(range(0,len(vals)))]
        total_seconds = sum([i*j for i,j in zip(vals,multiple)])

        return {'total_time' : total_seconds}


    def get_country_details(country):
        """Logic to extract country from the country tags. 
        Accepts a bs tag"""

        country_strings = [str(i) for i in list(country.contents)]
        #print(country_strings)
        country_multiline_string = "".join(country_strings)
        #print(country_multiline_string)
        country_oneline_string = "".join(country_multiline_string.split())
        val_start = country_oneline_string.rfind('>')+1
        country_name = country_oneline_string[val_start:]
        return {'country_name' : country_name}
    
    
    
    page = bs(open(page_name))
    
    # Get whether it was a men's or women's event
    split_name = page_name.split()
    if 'women' in split_name[2]:
        gender = ['women']
    else:
        gender = ['men']
    
    # Get the location of the championships
    while True:
        res = split_name.pop()
        #print(res)
        if '(' in res or ")" in res:
            pass
        elif 'de' in res:
            pass
        else:
            location = [res.rstrip()]
            break
    
    # Get the number of the championship
    champ_number_unformatted = split_name[7]
    if len(champ_number_unformatted) > 3:
        championship_number = [int(champ_number_unformatted[0:2])]      
    else:
        championship_number = [int(champ_number_unformatted[0])]
    
    
    # Get athlete name and ID number
    athletes = page.find_all('td',attrs = {'data-th' : 'athlete'})
    athlete_details = [get_athlete_details(athlete) for athlete in athletes]
    athlete_first_names = [athlete['first_name'] for athlete in athlete_details]
    athlete_last_names = [athlete['last_name'] for athlete in athlete_details]
    athlete_ids = [athlete['id'] for athlete in athlete_details]
    
    # Get mark tags
    marks = page.find_all('td',attrs = {'data-th' : 'MARK'})
    mark_details = [get_mark_details(mark) for mark in marks]
    mark_times = [mark['total_time'] for mark in mark_details]
    
    # Get places (ie first, second, third)
    places = page.find_all('td',attrs = {'data-th' : 'POS'})
    places = list(range(1,len(athletes)+1))
    
    # Get athlete countries
    countries = page.find_all('td',attrs = {'data-th' : 'COUNTRY'})
    country_details = [get_country_details(country) for country in countries]
    country_names = [country['country_name'] for country in country_details]
    
    # Get the length of the event, ie 100m, 200m, etc
    event_meta_info = page.title.contents[0].split()
    distance = [event_meta_info[0].replace(',','')] * len(athletes)
    
    # The number of the championship (eg 1 represents 1983 Helsinki)
    championship_number = championship_number * len(athletes)
    
    # Make athlete gender list
    gender = gender * len(athletes)
    
    # Make location list (locations are Helsinki, Roma, etc)
    location = location * len(athletes)
    
    # Generates row values    
    data_values = zip(
        athlete_first_names,
        athlete_last_names,
        athlete_ids,
        mark_times,
        places,
        country_names,
        distance,
        championship_number,
        location,
        gender
    )

    # Defining the column names of the dataframe
    col_names = ['athlete_first_name','athlete_last_name',\
                     'athlete_id','mark_time','place','country',\
                     'distance','championship_number','location',\
                     'gender']

        
    results = [dict(zip(col_names,row)) for row in data_values]
    
    return results
