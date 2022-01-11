import classes
import methods
import time 

def run():

    input_list = [] #[center, range, max, threshold, reverse_geocoding]

    #If we actually want the center value we would have to call the index position 0 example to yeild the cetner value "input_list[0].get_center()"

    center = methods.center_point()

    if "CENTER FILE" in center:
        
        file_lat_lon = classes.CenterFile(center[12:])

        the_center = file_lat_lon.get_center() 

    elif "CENTER NOMINATIM" in center:
        
        api_lat_lon = classes.CenterApi(center[17:])

        the_center = api_lat_lon.get_center() 

    #We will get the range and append that to the input_list to keep track of inputs

    the_range = methods.range_in_miles()

    #Now we'll decide the AQI threshold and append this to the list to keep a track of inputs

    the_threshold = methods.threshold_aqi()

    #Finally we'll get the max and append that to the input_list to keep track of inputs

    the_max = methods.max_number()

    ### Now we have the center object stored along with the range,threshold, and max

    #print(input_list[0].get_center()) ###PAY ATTENTION TO THIS YOU MUST CALL THE METHOD ON THE CENTER TO YIELD THE VALUE

    printable_latitude, printable_longitude = the_center #.get_center()

    #for each instance you want to print
    #AQI Value 
    #methods.print_format_latlon(latitude,longitude_
    #methods.reverse_geocoding(latitude,longitude)

    aqi_url = 'https://www.purpleair.com/data.json' #<not the actual aqi_url
    
    aqi_api_or_file = methods.where_are_we_getting_aqi_dictionairy()
    
    if "AQI FILE" in aqi_api_or_file:

        aqi_dictionairy = classes.AqiFile(aqi_api_or_file[9:]) #Should return the name of the filepath we'd have to call .get_aqi() on the function to yield the proper value
        
    elif "AQI PURPLEAIR" in aqi_api_or_file:

        aqi_dictionairy = classes.AqiApi(aqi_url)

    lists = methods.filter_list(aqi_dictionairy.get_aqi(), the_center, int(the_range), int(the_threshold), int(the_max))

    reverse = input()

    print("CENTER ", end ='')
    methods.print_format_latlon(printable_latitude,printable_longitude)

    if "REVERSE NOMINATIM" in reverse:

        for value_list in lists:

            print(f'AQI {value_list[0]}')

            methods.print_format_latlon(value_list[1],value_list[2])

            print(classes.ReverseApi(value_list[1],value_list[2]).get_reverse())

            time.sleep(2)

    
    elif "REVERSE FILES" in reverse:  #paths seperated by spaces like path1 path2 path3

        files = reverse[14:].split()

        for index in range(len(lists)):

            value_list = lists[index]

            reverse_file = files[index]

            print(f'AQI {value_list[0]}')

            methods.print_format_latlon(value_list[1],value_list[2])
            
            print(classes.ReverseFile([reverse_file],value_list[1],value_list[2]).get_reverse())

            
if __name__ == '__main__':

    run()

   

   
