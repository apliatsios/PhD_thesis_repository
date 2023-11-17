import api_config as apic

def create_req_url(lat, lon, api_name):
    url = ""
    if api_name == apic.SupportedApis.WEATHERBIT.api_name:
        url = '{0}?lat={1}&lon={2}&hours=1'.format(apic.SupportedApis.WEATHERBIT.url, lat, lon)
        headers = apic.SupportedApis.WEATHERBIT.headers

    elif api_name == apic.SupportedApis.IQAIR.api_name:
        url = '{0}?lat={1}&lon={2}&key={3}'.format(apic.SupportedApis.IQAIR.url, lat, lon, apic.SupportedApis.IQAIR.key)
        headers = apic.SupportedApis.IQAIR.headers

    elif api_name == apic.SupportedApis.NINJAS_AIRQ.api_name:
        url = '{0}?lat={1}&lon={2}&X-Api-Key={3}'.format(apic.SupportedApis.NINJAS_AIRQ.url, lat, lon, apic.SupportedApis.NINJAS_AIRQ.key)
        headers = apic.SupportedApis.NINJAS_AIRQ.headers

    elif api_name == apic.SupportedApis.OPEN_WEATHER.api_name:
        url = '{0}?lat={1}&lon={2}&appid={3}'.format(apic.SupportedApis.OPEN_WEATHER.url, lat, lon, apic.SupportedApis.OPEN_WEATHER.key)
        headers = apic.SupportedApis.OPEN_WEATHER.headers
        
    return [url, headers]


async def parse_api(data,name,api_name,lat,long,ts):
    """ parse response data from get request and store required data 
    (PM2_5,PM10,SO2,NO2,O3) in a dictionary
    
    Arguments:
        data: get request response data in json format
        arg: String (the name of api)
    Returns:
        A dictionary with required data
    """
    new_data={}
    if api_name=='ninjas_airq':
        exclude_data=['overall_aqi','CO']
        for key,values in data.items():
            if key not in exclude_data:
                new_data.update({key.casefold():values['concentration']})
    if api_name=='open_weather':
        exclude_data=['no','co','nh3']
        for key,values in data['list'][0].items():
            if (key=='components'):
                for key2,value2 in data['list'][0][key].items():
                    if key2 not in exclude_data:
                        if key2=="pm2_5":
                            new_data.update({"pm2.5":value2})
                        else:
                            new_data.update({key2:value2})
    if api_name=='weatherbit':
        exclude_data=['aqi','co','mold_level','pollen_level_grass','pollen_level_tree','pollen_level_weed','predominant_pollen_type']
        for key,values in data['data'][0].items():
            if key not in exclude_data:
                new_data.update({key:values})
    new_data.update({'name':name})            
    new_data.update({'api_name':api_name})
    new_data.update({'lat':lat})
    new_data.update({'long':long})
    new_data.update({'timestamp':ts})
    return new_data