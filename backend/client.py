import requests
import json

# Sample matrix data for testing TOPSIS
matrix_data = [
    [10, 5, 7],
    [8, 9, 6],
    [7, 4, 3],
    ]

# URL of the Flask server
url = 'http://localhost:5000/'

# Create a dictionary containing the matrix data
data = {
    'matrixData': matrix_data
}

# Convert the data dictionary to JSON
json_data = json.dumps(data)

# Set the headers for the POST request
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request to the Flask server
response = requests.post(url, data=json_data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print('TOPSIS Result:')
    print(result['topsisResult'])
else:
    print('Error:', response.json())
