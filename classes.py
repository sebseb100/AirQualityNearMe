import methods


class CenterFile:

    def __init__(self, path):
        self.path = path
            

    def get_center(self):

        return methods.forward_geocoding_file(self.path)

        
class CenterApi:

    def __init__(self, location_name):
        self.location_name = location_name
        

    def get_center(self):

        return methods.forward_geocoding(self.location_name)


class AqiFile:

    def __init__(self, path):
        self.path = path

    def get_aqi(self):

        dictionairy = methods.open_json(self.path)

        return methods.values_from_api(dictionairy)


class AqiApi:

    def __init__(self, url):
        self.url = url

    def get_aqi(self):

        dictionairy =  methods.open_url(self.url)

        return methods.values_from_api(dictionairy)



#yield the name from the file
    #json_load returns list of dicts grab the first one [0] then grab 'display_name' value 

    
class ReverseFile:

    def __init__(self, list_of_files, latitude, longitude):
        self.list_of_files = list_of_files
        self.latitude = latitude
        self.longitude = longitude

    def get_reverse(self):
        
        return methods.reverse_geocoding_file(self.list_of_files,self.latitude,self.longitude)

        
#yield the name from the file
#find corresponding sensor
    
class ReverseApi:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def get_reverse(self):

        return methods.reverse_geocoding(self.latitude,self.longitude)
    


        


    

    
