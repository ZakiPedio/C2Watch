import plotly.graph_objects as go
import pycountry
import os
import json
import shodan
import re

def convert_alpha2_to_alpha3(alpha_2_code):
    try:
        alpha3 = pycountry.countries.get(alpha_2=alpha_2_code).alpha_3
    except AttributeError:
        # Handle the case where the country code is not found
        alpha3 = "Unknown"
    return alpha3


def count_country_codes(country_codes):
    count_dict = {}
    
    # Count occurrences of each country code
    for code in country_codes:
        if code in count_dict:
            count_dict[code] += 1
        else:
            count_dict[code] = 1
    
    # Convert the dictionary to a list of tuples
    count_list = [(k, v) for k, v in count_dict.items()]
    
    return count_list

#TODO improva alg (not getting all country, i think)
def jsonGetCountry(query_file):
    file_path = os.path.join(os.path.dirname(__file__), '../data/', query_file)
    country_codes = []
    with open(file_path) as jsonFile:
        for line in jsonFile:
            if 'country_code' in line:
                country_codes.append(line.split('"')[3])
    return country_codes



def createMap(query_file):
    countries = jsonGetCountry(query_file)
    map_data = count_country_codes(countries)

    country_codes = [country[0] for country in map_data]
    country_counts = [country[1] for country in map_data]
    country_names = []
    country_alpha3 = []

    for code in country_codes:
        alpha3 = convert_alpha2_to_alpha3(code)
        if alpha3 != "Unknown":
            country_names.append(pycountry.countries.get(alpha_3=alpha3).name)
            country_alpha3.append(alpha3)
        else:
            country_names.append("Unknown")
            
    fig = go.Figure(data=go.Choropleth(
        locations=country_alpha3,
        z=country_counts,
        text=country_names,  # Include country names as text labels
        colorscale='sunsetdark',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='miller',
            showcountries=True
        )
    )
    
    # Adjust the height and width of the figure
    fig.update_layout(height=800, width=1200)

    return fig




# TODO make it better with json parsing
def jsonGetHost():
    file_path = os.path.join(os.path.dirname(__file__), '../data/default.json')
    hosts = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        try:
            if line.split('"')[1] == 'host':
                hosts.append(line.split('"')[3])
        except:
            continue
    return hosts
        #host_value = data['http']['host']

#TODO i think it gets only 100 first ip, need to update this...
def refresh_json(query_file, query, api_key):
    output_file = os.path.join(os.path.dirname(__file__), '../data/', query_file)
    
    # Initialize the Shodan API client
    api = shodan.Shodan(api_key)
    
    try:
        # Perform a Shodan search query
        results = api.search(query)
        
        # Write the prettified JSON data to the output file
        with open(output_file, 'w') as file:
            file.write(json.dumps(results, indent=4))
        
        return True  # Return True if successful
    except Exception as e:
        print("Error:", e)
        return False  # Return False if an error occurs
        

def updateQuery(query_name, query_value, query_file):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_directory, '../data')

    # Load queries from the JSON file
    with open(os.path.join(data_folder, 'query.json'), 'r') as file:
        queries = json.load(file)
    
    # Find the highest index of existing queries
    query_indices = [int(key.replace('query', '')) for key in queries.keys() if key.startswith('query') and key.replace('query', '').isdigit()]
    max_index = max(query_indices) if query_indices else 0
    
    # Create a new query with the next index
    new_query_key = f"query{max_index + 1}"
    new_query = {
        "queryName": query_name,
        "queryValue": query_value,
        "queryFile": "query_data/"+query_file
    }
    queries[new_query_key] = new_query
    
    # Save the updated queries back to the JSON file
    with open(os.path.join(data_folder, 'query.json'), 'w') as file:
        json.dump(queries, file, indent=4)

def validateIpAddress(ipAddress):
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ipAddress):
        return True
    else:
        return False

def getIpFromJson(ipAddr, query_files):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_directory, '../data')

    for qfile in query_files:
        # Load queries from the JSON file
        with open(os.path.join(data_folder, qfile), 'r') as file:
            data = json.load(file)
        
        # Extract "cobalt_strike_beacon" objects from each item in "matches"
        for item in data.get('matches', []):
            if item.get('ip_str') == ipAddr:
                return item

def main():
	i = 0

if __name__ == "__main__":
    main()

