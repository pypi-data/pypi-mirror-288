# ZJountries-py is a package used for quicker access to data of countries
# (not 100% accurate, contains many inconssitencies).
# Copyright (C) 2024  Zilezia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# **Notification of Use**
# While this package is freely available, I would appreciate it if you
# could notify me of any significant usage or modifications. You can
# contact me at:
# https://x.com/JrezcI

import json
import pkg_resources

def get_place(by=None, value=None, fullText=False, fields=None):
    
    data_path = pkg_resources.resource_filename(__name__, 'data.json')
    # data_path = "./src/ZJountries/data.json"
    with open(data_path) as file:
        data = json.load(file)
        
    matching_data = []
    
    if by is not None and value is not None:
        byL = by.lower()
        valueL = value.lower()
        
        match byL:
            case "name":
                if fullText:
                    matches = [country for country in data if valueL == country['name']['common'].lower()]
                else:
                    matches = [country for country in data if valueL in country['name']['common'].lower()]
                
            case "capital":
                if fullText:
                    matches = [country for country in data if valueL == country['capital']['name']['common'].lower()]
                else:
                    matches = [country for country in data if valueL in country['capital']['name']['common'].lower()]
            
            case "continents":
                continent_alias = {
                    'north_a': 'North America',
                    'south_a': 'South America',
                    'europe': 'Europe',
                    'asia': 'Asia',
                    'africa': 'Africa',
                    'oceania': 'Oceania',
                    'australia': 'Oceania',
                    'antarctica': 'Antarctica',
                }
                
                actual_continent = continent_alias.get(valueL, value)
                
                matches = [country for country in data if actual_continent in country['continents']]
            
            case "iso2":
                matches = [country for country in data if actual_continent in country['code']['alpha-2']]
                
            case "iso3":
                matches = [country for country in data if actual_continent in country['code']['alpha-3']]
                
            case "isoN":
                matches = [country for country in data if actual_continent in country['code']['numeric']]
            
            case "language":
                matches = [country for country in data if actual_continent in country['official_lang']]
            
            case _:
                matches = [] # should output the whole data
            
        matching_data.extend(matches)
    
    if not matching_data:
        matching_data = data

    if fields is not None:
        if isinstance(fields, str):
            fields = [fields]
        filtered_data = []
        for record in matching_data:
            record_data = {}
            for field in fields:
                if field in record:
                    record_data[field] = record[field]
            filtered_data.append(record_data)
        
        return filtered_data

    return matching_data
