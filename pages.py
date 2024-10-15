from flask import Blueprint, render_template, request, jsonify, redirect, url_for

import os
import json
from .src import misc_utils

SHODAN_API_KEY = 'SHODAN_API_KEY_HERE'

bp = Blueprint("pages", __name__)



@bp.route("/")
def home():
	# Initialize the data folder path
	current_directory = os.path.dirname(os.path.realpath(__file__))
	data_folder = os.path.join(current_directory, 'data')

	# Load queries from the JSON file
	with open(os.path.join(data_folder, 'query.json'), 'r') as file:
		queries = json.load(file)
	return render_template('pages/home.html', queries=queries)

@bp.route("/show")
def show_query():
    query = request.args.get("query")
    # Initialize the data folder path
    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_directory, 'data')

    # Load queries from the JSON file
    with open(os.path.join(data_folder, 'query.json'), 'r') as file:
        queries = json.load(file)

    query_file = None  # Initialize query file variable

    # Iterate through each query key
    for key, value in queries.items():
        # Check if the query parameter is in the value of the "queryValue" key
        if query in value.get('queryValue', ''):
            # If found, set the query file to the value of the "queryFile" key
            query_file = value.get('queryFile', '')
            break  # Stop iterating once a match is found

    # If query file is still None, set it to "default.json"
    if query_file is None:
        query_file = 'default.json'

    # Call the createMap() function with the appropriate query file
    fig = misc_utils.createMap(query_file)

    return render_template("pages/show.html", query=query, queries=queries, fig=fig)

# Route to handle the refresh request
@bp.route('/refresh', methods=['GET'])
def refresh():
    query = request.args.get("query")
    # Initialize the data folder path
    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_directory, 'data')

    # Load queries from the JSON file
    with open(os.path.join(data_folder, 'query.json'), 'r') as file:
        queries = json.load(file)

    query_file = None  # Initialize query file variable

    # Iterate through each query key
    for key, value in queries.items():
        # Check if the query parameter is in the value of the "queryValue" key
        if query in value.get('queryValue', ''):
            # If found, set the query file to the value of the "queryFile" key
            query_file = value.get('queryFile', '')
            break  # Stop iterating once a match is found

    # If query file is still None, set it to "default.json"
    if query_file is None:
        query_file = 'default.json'
        
    if misc_utils.refresh_json(query_file, query, SHODAN_API_KEY):
    	print("JSON data refreshed successfully.")
    else:
    	print("Error refreshing JSON data.")
    
    # Your code to update JSON files and refresh the page goes here

    return jsonify({'success': True}), 200
    
@bp.route('/addQuery', methods=['GET', 'POST'])
def add_query():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_directory, 'data')

    # Load queries from the JSON file
    with open(os.path.join(data_folder, 'query.json'), 'r') as file:
        queries = json.load(file)
        
    if request.method == 'POST':
        # Get form data
        query_name = request.form['query_name']
        query_value = request.form['query_value']
        query_file = request.form['query_file']

        misc_utils.updateQuery(query_name, query_value, query_file)

        # Process the query data (e.g., save to database)
        # Replace this with your actual logic

        # Redirect to the homepage or any other page
        return redirect(url_for('pages.home'))
    else:
        # Render the add_query.html template
        return render_template('pages/addQuery.html', queries=queries)

@bp.route("/ipSearch", methods=['GET', 'POST'])
def ip_search():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_folder = os.path.join(current_directory, 'data')

    # Load queries from the JSON file
    with open(os.path.join(data_folder, 'query.json'), 'r') as file:
        queries = json.load(file)
        
    if request.method == 'POST':
        ip_query = request.form['ip_query']
        if not misc_utils.validateIpAddress(ip_query):
            return render_template("pages/ipSearch.html", queries=queries)
        else:
            print("HERE")
            query_files = [query['queryFile'] for query in queries.values()]
            print(query_files)
            ip_json = misc_utils.getIpFromJson(ip_query, query_files)

        return render_template("pages/ipSearch.html", queries=queries, ip_json=ip_json)
    else:
        return render_template("pages/ipSearch.html", queries=queries)


@bp.route("/about")
def about():
	# Initialize the data folder path
	current_directory = os.path.dirname(os.path.realpath(__file__))
	data_folder = os.path.join(current_directory, 'data')

	# Load queries from the JSON file
	with open(os.path.join(data_folder, 'query.json'), 'r') as file:
		queries = json.load(file)
	# Call the createMap() function to get the Plotly figure
	fig = misc_utils.createMap()
	return render_template("pages/about.html", fig=fig, queries=queries)

