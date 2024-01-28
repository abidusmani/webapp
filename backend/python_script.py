import sys
import json
from flask import app
import pandas as pd
import numpy as np
# import python_script_2
from python_script_2 import topsis, topsis_gre;
port = 5000
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin' , '*')
    return response
# from flask import Flask
# app = Flask(__name__)
# @app.route("\project\src\components\About.js")
# def hello():
#     return "Welcome to machine learning vnfvhorho model APIs !"

# @app.route("/")
# def mem():
#     return "Welcome to machine learning cls model APIs !"


# if __name__=='__main__':
#     app.run(debug=True,)
@app.route("/topsis")
# def topsis_1(matrix_json):
def topsis_1(data):
    matrix_1 = topsis(data)
    result_1 = {"rank": matrix_1}
    print(result_1)
    # ...
    return json.dumps(result_1)
    # matrix = pd.read_json(matrix_json)
    # matrix = pd.read_json({[1,2,3],[2,5,8]})
    # matrix_1 = topsis("3,5,2,9,8,7;2,6,8,2,1,7;7,3,9,6,5,6;1,9,10,2,3,4;8,7,5,3,2,6")
    
    # Implement the TOPSIS method using pandas and numpy
    # ...
    # Calculate the result and return it as JSON

    

@app.route("/topsis_gre")
# def topsis_2(matrix_json):
def topsis_2(data):
    matrix_2 = topsis_gre(data)
    result_2 = {"rank": matrix_2}
    print(result_2)
    return json.dumps(result_2)
#     matrix = pd.read_json(matrix_jsosn)
#     matrix_1 = python_script_2.topsis_gre(matrix)
#     # Implement the TOPSIS method using pandas and numpy
#     # ...
#     # Calculate the result and return it as JSON

#     result = {matrix_1}

#     # ...
#     return result
# if __name__ == '__main__':
#     result = topsis_1()
#     app.run(debug=True,port = port)
#     matrix_json = sys.argv[1]
    
    # print(result)




# def process_matrix_data(data):
#     # Assuming the JSON data represents a square matrix,
#     # we can convert it into a 2D array for processing.
#     matrix = [[data[str(i)][str(j)] for j in range(len(data))] for i in range(len(data))]

#     # Process the matrix data as needed
#     # For this example, we'll just calculate the sum of all elements in the matrix
#     total_sum = sum(sum(row) for row in matrix)

#     # Create a result dictionary to be returned as JSON
#     result = {
#         "total_sum": total_sum,
#         "processed_matrix": matrix,
#     }
#     return result

if __name__ == "__main__":
    # Read the JSON data from standard input
    # data = json.loads(sys.stdin.read())
    # result_1 = topsis_1(data)

    # Convert the result dictionary to JSON format
    # json_result_1 = json.dumps(result_1)

    # Print the JSON result so that Node.js can capture it
    # print(json_result_1)

    # result_2 = topsis_2(data)

    # Convert the result dictionary to JSON format
    # json_result_2 = json.dumps(result_2)

    # Print the JSON result so that Node.js can capture it
    # print(json_result_2)




    # result = topsis_1()
    app.run(debug=True,port = port)
    # matrix_json = sys.argv[1]