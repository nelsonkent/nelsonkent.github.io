from flask import Flask, request, jsonify
import json
from collections import defaultdict
from datetime import datetime
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to read data from file
def read_data_from_file(url):
    file_path = f"db/{url}.json"
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'comment': [], 'vote': defaultdict(int), 'voter_ip': []}

# Function to write data to file
def write_data_to_file(url, data):
    directory = 'db/'
    file_path = os.path.join(directory, f"{url}.json")

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w') as file:
        json.dump(data, file)

# Function to add a comment
@app.route('/add_comment/<path:url>', methods=['POST'])
def add_comment(url):
    data = read_data_from_file(url)
    comment = request.json.get('comment')
    email = request.json.get('email')
    author = request.json.get('author')
    if comment:
        data['comment'].append({'comment': comment, 'email': email, 'author': author, 'date': datetime.now().isoformat()})
        write_data_to_file(url, data)
        return jsonify({'message': 'Comment added successfully.'}), 201
    return jsonify({'error': 'Comment not provided.'}), 400

# Function to add a vote
@app.route('/add_vote/<path:url>', methods=['POST'])
def add_vote(url):
    data = read_data_from_file(url)
    voter_ip = request.remote_addr
    vote = request.json.get('vote')
    if vote:
        if voter_ip not in data['voter_ip']:
            print(data['vote'])
            data['vote'][vote] = data['vote'].get(vote, 0) + 1
            data['voter_ip'].append(voter_ip)
            write_data_to_file(url, data)
            return jsonify({'message': 'Vote added successfully.'}), 201
        else:
            return jsonify({'error': 'You have already voted for this page.'}), 400
    return jsonify({'error': 'Vote not provided.'}), 400

# Function to get comments sorted by date
@app.route('/get_comments/<path:url>', methods=['GET'])
def get_comments(url):
    data = read_data_from_file(url)
    sorted_comments = sorted(data['comment'], key=lambda x: x['date'], reverse=True)
    return jsonify({'comments': sorted_comments})

# Function to get total votes
@app.route('/get_votes/<path:url>', methods=['GET'])
def get_votes(url):
    data = read_data_from_file(url)
    total_votes = data['vote']
    return jsonify({'total_votes': total_votes})

if __name__ == '__main__':
    app.run(debug=True)
