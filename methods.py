#ICS 32A Thorton
#Sebu Eisaian
#Project 3

import math
import json
import urllib.error
import urllib.request
from pathlib import Path

#IMPORT URLS!!!
    
    
def open_json(the_file: Path):

    opened = None

    the_file = Path(the_file)
    
    try:
    
        opened = the_file.open('r')
        dic = json.loads(opened.read())
        return dic

    except:

        print("FAILED")
        print(the_file)
        print("MISSING")

    finally:
        
        if opened != None:
            opened.close()
            

def open_url(url: str) -> dict:
    '''
    This function takes a URL and returns a Python dictionary representing the
    parsed JSON response.

    def json_dictionairy(json_file) -> dict:

    #Converts a json file into a dictionairy so we can use it!
        dictionairy = json.loads(json_file)
        
    '''
    response = None

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')

        return json.loads(json_text)

    except urllib.error.HTTPError as error:
        print("FAILED")
        print(f'{error.code} {url}')
        print("NOT 200")
        
    finally:
        if response != None:
            response.close()

def json_dictionairy(json_file) -> dict:
    '''
    Converts a json file into a dictionairy so we can use it!
    '''
    dictionairy = json.loads(json_file.read())
    return dictionairy             


def center_point() -> str:

    query = input()

    return query

def where_are_we_getting_aqi_dictionairy() -> str:

    alright = input()

    return alright


#to be passed into the location function to determine coordinates of place


def range_in_miles() -> int:
    '''
    Prompts user to enter mile range and returns value as an int
    '''

    while True:
        
        ran = input()

        #EXPECTED INPUT IS "RANGE " + "INTEGER" so it should return 6:

        command = ran[0:5]

        integer = ran[6:].strip()

        if not (integer.isdigit() and int(integer) > 0):
            continue
        break
    
    return int(integer)


def threshold_aqi() -> int:
    '''
    Prompts user to enter AQI threshold and returns value as an int
    '''

    while True:
        
        aqi = input()

        command = aqi[0:9] #"THRESHOLD "

        integer = aqi[10:].strip()

        if not (integer.isdigit() and int(integer) >= 0):
            continue
        break
    
    return int(integer)


def max_number() -> int:
    '''
    Prompts user to enter number of searches/locations we want in our search 
    '''

    while True:
        
        search = input()

        command = search[0:3] #"MAX "

        integer = search[4:].strip()

        if not (integer.isdigit() and int(integer) >= 0):
            continue
        break
    
    return int(integer)



def distance_between_points(coord_a: tuple, coord_b: tuple) -> float:
    '''
    Great Circle Distance : equirectangular approximation
    Function receives two tuples and finds the distance between coordinates
    '''

    #CONVERSION TO RADIANS REQUIRED
    
    dlat = float(coord_a[0]) - float(coord_b[0])

    dlon = float(coord_a[1]) - float(coord_b[1])

    dlat = math.radians(dlat)

    dlon = math.radians(dlon)

    average_latitude = math.radians((float(coord_a[1]) + float(coord_b[1]))/2 )

    earth_radius = 3958.8

    x = dlon * math.cos(average_latitude)

    distance = math.sqrt(x**2 + dlat**2) * earth_radius

    return distance


def values_from_api(dictionairy: dict): #FIGURING THAT OUT:
    '''
    At this point we have obtained the dictionairy from the json_dictionairy replicating the json file
    Now we will pull all the valueable values from it including pm,age,Type,LAt,Lon

    #return lists[1]   #pm: current reading of PM2.5 in the air reported in micrograms per meter cubed a density 
     #return lists [4]  #age: the amount of seconds since this sensor last reported #we're interested in time < 3600 seconds
      #return lists [25] #Type: type of sensor (INDOOR/OUTDOOR) 0 = sensor is outdoors, 1 = sensor is indoors #WE ONLY WANT OUTDOOR SENSORS
       #return lists [27] #Lat: latitude in degress (to be converted to radians)
        #return lists [28] #Lon: longitude in degrees (to be converted to radians)def values_from_api(dictionairy: dict): #FIGURING THAT OUT:
    '''
  
    #IF the value returned for one of these in NULL or something we wouldn't expect we PASS/IGNORE 
    #"data" is the key that holds all the lists of values we want
    #Make sure to package LAT and LON IN A TUPLE LIKE RETURN (LAT,LON)

    pm = 0
    age = 0
    sensor_type = 0
    latitude = 0
    longitude = 0

    result_list = []
    
    
    for values in dictionairy['data']:
        pm = values[1]
        age = values[4]
        sensor_type = values[25]
        latitude = values[27]
        longitude = values[28]

        if pm == None or age == None or sensor_type == None or sensor_type ==1 or latitude == None or longitude == None:
            continue
        
        aqi = density_to_aqi(pm)

        result_list.append([aqi,age,sensor_type,latitude,longitude])
    
    return result_list

def filter_list(result_list: list, center_tuple, max_distance, max_threshold, max_val) -> list:
    '''
    '''
    filtered_list = []
    
    for values in result_list:
        aqi = values[0]
        age = values[1]
        sensor_type = values[2]
        latitude = values[3]
        longitude = values[4]

        lat_lon = (float(latitude),float(longitude))

        distance = distance_between_points(lat_lon, center_tuple)

        #print(distance)
        #print(max_distance)
       # print(aqi)
        #print(max_threshold)

        if distance <= max_distance and aqi >= max_threshold:

            filtered_list.append([aqi,latitude,longitude,distance])

    filtered_list.sort(reverse=True)

    #return filtered_list[0:max_val]
    return filtered_list[0:max_val]
    

def density_to_aqi(density: float) -> int:

    #remember to round the floating point number then convert to an integer
    if 0.0 <= density < 12.1:
        return int(round((50/12) * density))

    elif 12.1 <= density < 35.5:
        return int(round(2.1*density + 25.55))

    elif 35.5 <= density < 55.5:
        return int(round(2.46*density + 13.59))

    elif 55.5 <= density < 150.5:
        return int(round(0.5163*density + 122.34))
    
    elif 150.5 <= density < 250.5:
        return int(round(0.991*density + 51.86))

    elif 250.5 <= density < 350.5:
        return int(round(0.991*density + 52.76))

    elif 350.5 <= density < 500.5:
        return int(round(0.66*density + 169.52))

    elif 500.5 <= density:
        return 501
    

def forward_geocoding(center) -> tuple:
    
    #open_url('https://nominatim.openstreetmap.org/?addressdetails=1&q=bakery+in+berlin+wedding&format=json&limit=1')

    BASE_URL = 'https://nominatim.openstreetmap.org/search?'

    addy = center #Addy

    query_parameters = [('q',addy),('format','json')]

    the_url = f'{BASE_URL}{urllib.parse.urlencode(query_parameters)}'

    #CONVERT TO DICTIONAIRY

    somehow_a_list = open_url(the_url)

    #get_lat_lon(dictionairy)

    #FIND DICTIONAIRY KEYS LAT AND LONG

    latitude = 0 

    longitude = 0

    dictionairy = somehow_a_list[0]
    
    latitide = dictionairy['lat']
       
    longitude = dictionairy['lon']
                
    #print(latitude)

    #print(longitude)

    return (float(dictionairy['lat']),float(dictionairy['lon']))

def forward_geocoding_file(center) -> tuple:

    file_path = Path(center)

    dictionairy_in_list = open_json(file_path)

    dictionairy = dictionairy_in_list[0]

    latitude = 0 

    longitude = 0
    
    latitide = dictionairy['lat']
       
    longitude = dictionairy['lon']          

    return (float(dictionairy['lat']),float(dictionairy['lon']))
    

def reverse_geocoding(latitude,longitude) -> str:

    BASE_URL = 'https://nominatim.openstreetmap.org/reverse?'

    query_parameters = [('lat',latitude),('lon',longitude),('format','json')]

    the_url = f'{BASE_URL}{urllib.parse.urlencode(query_parameters)}'

    string = open_url(the_url)

    string = string['display_name']

    return(string)

def reverse_geocoding_file(list_of_files,latitude,longitude) -> str:

    dicts = []

    for file in list_of_files:

        dicts.append(open_json(file))

    for diction in dicts:
        
        return diction['display_name']


def print_format_latlon(lat,lon):

    lat = float(lat)

    lon = float(lon)

    latitude = str(lat)

    longitude = str(lon)

    if lat > 0:
        latitude += '/N'
    else:
        latitude += '/S'

    if lon > 0:
        longitude += '/E'
    else:
        longitude += '/W'

    print(latitude + ' ' + longitude.replace('-',''))

def final_report():
    print("CENTER ")




  
  




