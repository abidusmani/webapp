from flask import Flask, jsonify, request
import json
from pyahp import parse
from flask_cors import CORS
import numpy as np
from topsis_gra import TOPSIS_GRA
from topsis_euclidian import TopsisEuclidian
from saw import SAW
from pymcdm.methods import TOPSIS
from pymcdm.methods import VIKOR
from pymcdm.helpers import rrankdata 

app = Flask(__name__)
CORS(app)

# Enable CORS for all routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/')
def home():
    return "hello, world"

@app.route('/api/topsis-analysis4', methods=['POST'])
def topsis_analysis4():
    try:
        data = request.json
        # Print received data for debugging
        print("Received Data:", data)

        if not data:
            return jsonify({'error': 'Invalid data'}), 400
        # ahp_model = parse(data)
        # priorities = ahp_model.get_priorities()
        # print(priorities)
        matrix_data = data['matrixData']
        weights = data['weights']
        is_benefit = data['is_benefit']
        

        # Print the matrix_data for debugging
        print("Matrix Data:", matrix_data)
       
        #is_benefit = np.where(is_benefit, 1, -1)
        # Convert the matrix data to a NumPy array
        matrix = np.array(matrix_data)
        weights=np.array(weights)
        is_benefit = np.array(is_benefit)
        #boolean_array = np.array([True, False, True, False, True])

        # Convert True to 1 and False to -1
        types1 = is_benefit.astype(int) * 2 - 1

        #is_benefit=np.array(is_benefit)

        # Print the matrix for debugging
        print("Matrix:", matrix_data)

        # Convert null values to False in is_benefit array
        #is_benefit = [item if item is not None else False for item in is_benefit]

        # Print the weights and is_benefit for debugging
        print("Weights:", weights)
        print("Is Benefit:", is_benefit)
        print(types1)

        # 
    # alts = np.array([
    # [4, 4],
    # [1, 5],
    # [3, 2],
    # [4, 2]
    # ], dtype='float')

    # # Define weights and types
    # weights = np.array([0.5, 0.5])
        # types = np.array([1, -1, 1])

    # Create object of the method
        topsis_base = TOPSIS()

        # Determine preferences and ranking for alternatives
        pref = topsis_base(matrix, weights, types1)
        ranking = rrankdata(pref)
        # print(ranking)
        # ranking_arr=np.array(ranking)
        list_1 = ranking.tolist()
        print(list_1)
        list_1 = {'topsisResult': list_1}
        # for r, p in zip(ranking, pref):
        #     print(r, p)
        return jsonify(list_1)
    except Exception as e:
        # Print any errors for debugging
        print("Error:", e)
        return jsonify({'error': str(e)}), 500




@app.route('/api/topsis-analysis3', methods=['POST'])
def topsis_analysis3():
    try:
        data = request.json
        # Print received data for debugging
        print("Received Data:", data)

        if not data:
            return jsonify({'error': 'Invalid data'}), 400
        # ahp_model = parse(data)
        # priorities = ahp_model.get_priorities()
        # print(priorities)
        matrix_data = data['matrixData']
        weights = data['weights']
        is_benefit = data['is_benefit']
        

        # Print the matrix_data for debugging
        print("Matrix Data:", matrix_data)
       
        #is_benefit = np.where(is_benefit, 1, -1)
        # Convert the matrix data to a NumPy array
        matrix = np.array(matrix_data)
        weights=np.array(weights)
        is_benefit = np.array(is_benefit)
        #boolean_array = np.array([True, False, True, False, True])

        # Convert True to 1 and False to -1
        types1 = is_benefit.astype(int) * 2 - 1

        #is_benefit=np.array(is_benefit)

        # Print the matrix for debugging
        print("Matrix:", matrix_data)

        # Convert null values to False in is_benefit array
        #is_benefit = [item if item is not None else False for item in is_benefit]

        # Print the weights and is_benefit for debugging
        print("Weights:", weights)
        print("Is Benefit:", is_benefit)
        print(types1)

        # ahp_model = parse()
        # priorities = ahp_model.get_priorities()
        # print(priorities)
    # alts = np.array([
    # [4, 4],
    # [1, 5],
    # [3, 2],
    # [4, 2]
    # ], dtype='float')

    # # Define weights and types
    # weights = np.array([0.5, 0.5])
        # types = np.array([1, -1, 1])

    # Create object of the method
        topsis_vikor = VIKOR()

        # Determine preferences and ranking for alternatives
        pref = topsis_vikor(matrix, weights, types1)
        ranking = rrankdata(pref)
        # print(ranking)
        # ranking_arr=np.array(ranking)
        list_1 = ranking.tolist()
        print(list_1)
        list_1 = {'topsisResult': list_1}
        # for r, p in zip(ranking, pref):
        #     print(r, p)
        return jsonify(list_1)
    except Exception as e:
        # Print any errors for debugging
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/api/topsis-analysis', methods=['POST'])
def topsis_analysis():
    try:
        data = request.json
        # Print received data for debugging
        print("Received Data:", data)

        if not data:
            return jsonify({'error': 'Invalid data'}), 400

        matrix_data = data['matrixData']
        weights = data['weights']
        is_benefit = data['is_benefit']

        # Print the matrix_data for debugging
        print("Matrix Data:", matrix_data)

        # Convert the matrix data to a NumPy array
        matrix = np.array(matrix_data)
        weights=np.array(weights)
        is_benefit=np.array(is_benefit)

        # Print the matrix for debugging
        print("Matrix:", matrix_data)

        # Convert null values to False in is_benefit array
        #is_benefit = [item if item is not None else False for item in is_benefit]

        # Print the weights and is_benefit for debugging
        print("Weights:", weights)
        print("Is Benefit:", is_benefit)

        # Create an instance of the TOPSIS_GRA class
        topsis_instance = TopsisEuclidian(matrix, weights, is_benefit)

        # Perform TOPSIS-GRG analysis with the matrix data using the topsis_euc method
        topsis_result = topsis_instance.topsis_euc()

        # Print the TOPSIS result for debugging
        print("TOPSIS Result:", topsis_result)

        # Return the TOPSIS result as JSON
        result = {'topsisResult': topsis_result}
        return jsonify(result)

    except Exception as e:
        # Print any errors for debugging
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/topsis-analysis5', methods=['POST'])
def topsis_analysis5():
    try:
        data = request.json
        # Print received data for debugging
        print("Received Data:", data)

        if not data:
            return jsonify({'error': 'Invalid data'}), 400

        matrix_data = data['matrixData']
        weights = data['weights']
        is_benefit = data['is_benefit']

        # Print the matrix_data for debugging
        print("Matrix Data:", matrix_data)

        # Convert the matrix data to a NumPy array
        matrix = np.array(matrix_data)
        weights=np.array(weights)
        is_benefit=np.array(is_benefit)

        # Print the matrix for debugging
        print("Matrix:", matrix_data)

        # Convert null values to False in is_benefit array
        #is_benefit = [item if item is not None else False for item in is_benefit]

        # Print the weights and is_benefit for debugging
        print("Weights:", weights)
        print("Is Benefit:", is_benefit)

        # Create an instance of the TOPSIS_GRA class
        topsis_instance5 = SAW(matrix, weights)

        # Perform TOPSIS-GRG analysis with the matrix data using the topsis_euc method
        topsis_result5 = topsis_instance5.calculate_scores()

        # Print the TOPSIS result for debugging
        print("TOPSIS Result:", topsis_result5)

        # Return the TOPSIS result as JSON
        result = {'topsisResult': topsis_result5}
        return jsonify(result)

    except Exception as e:
        # Print any errors for debugging
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/topsis-analysis2', methods=['POST'])
def topsis_analysis2():
    # return "hello, world"
    try:
        data = request.json
        # print(data); return data
        # return jsonify(data)

        if not data:
            return jsonify({'error': 'Invalid data'}), 400

        # matrix_data = data['matrixData']
        # matrix_data = data
        matrix_data = data['matrixData']
        weights = data['weights']
        is_benefit = data['is_benefit']

        # Print the matrix_data for debugging
        print("Matrix Data:", matrix_data)

        # Convert the matrix data to a NumPy array
        matrix = np.array(matrix_data)
        weights=np.array(weights)
        is_benefit=np.array(is_benefit)


        # # Print the matrix_data
        # # print("Matrix Data:", matrix_data)

        # # Convert the matrix data to a NumPy array
        # matrix = np.array(matrix_data)
        # print(matrix)
        # # Define the weights and is_benefit arrays
        # weights = np.array([0.4, 0.3, 0.3])  # Modify according to your needs
        # is_benefit = np.array([True, True, False])  # Modify according to your needs
        # weights = data['weights']
        # is_benefit = data['is_benefit']
        # Create an instance of the TOPSIS_GRA class
        instance_gra = TOPSIS_GRA(matrix, weights, is_benefit)

        # Perform TOPSIS-GRG analysis with the matrix data using the calculate_gra method
        gra_result = instance_gra.calculate_gra()
        # topsis_result = TOPSIS_GRA.calculate_gra(matrix, weights, is_benefit)
        print(gra_result)
        # Return the TOPSIS result as JSON
        result = {'topsisResult': gra_result}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
