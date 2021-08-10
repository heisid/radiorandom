import requests

class Connector:
    def __init__(self):
        self.BASE_URL = 'https://radio.garden/api'
        self.cities_cache = list()
        self.countries_cache = list()
        self.get_cities()
    
    def get_response(self, endpoint: str) -> str:
        try:
            req = requests.get(f'{self.BASE_URL}{endpoint}')
            return req.json()
        except requests.ConnectionError:
            raise NetworkError
        
    def get_cities(self) -> list:
        endpoint = '/ara/content/places'
        resp = self.get_response(endpoint)
        cities = resp['data']['list']
        self.cities_cache =  [{'city_id': city['id'], \
                'city_name': city['title'], \
                'country': city['country']} for city in cities]

    def get_cities_by_country(self, country: str) -> list:
        if not self.cities_cache:
           self.get_cities()
        cities_filtered = list()
        for city in self.cities_cache:
           if city['country'] == country:
               cities_filtered.append(city)
        return cities_filtered

    def get_countries(self) -> list:
        if not self.cities_cache:
            self.get_cities()
        countries = list()
        for city in self.cities_cache:
            if city['country'] not in countries:
                countries.append(city['country'])
        self.countries_cache = countries

    def get_stations(self, city_id: str) -> list:
        endpoint = f'/ara/content/page/{city_id}'
        resp = self.get_response(endpoint)
        stations = resp['data']['content'][0]['items']
        return [{'station_id': station['href'].split('/')[-1], \
            'station_name': station['title']} for station in stations \
            if 'href' in station ]
    
    def get_stream_url(self, station_id: str) -> str:
        return f'{self.BASE_URL}/ara/content/listen/{station_id}/channel.mp3'

