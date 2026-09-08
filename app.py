import os
from flask import Flask, jsonify, request

app = Flask(__name__)
COEFFICIENTS = {'hours': 0.0021, 'cycles': .014, 'temp_excursions': .031}
BIAS= -.4
SECRET_TOKEN= os.environ.get("SCORING_API_TOKEN")
PORT = int(os.environ.get("PORT", 5100))

@app.route("/")
def home():
    return jsonify({'status': 'the sever is alive'})

@app.route("/score", methods = ["POST"])
def score():

    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return jsonify({'error': "missing Authorization header"}), 401
    else:
        authorization = auth_header.split()
        if len(authorization) != 2:
            return jsonify({'error': "incorrect Authorization header"}), 401
        if authorization[0] == 'Bearer':
            if authorization[1] == SECRET_TOKEN:
                pass
            else:
                return jsonify({'error': "incorrect Authorization header"}), 401
        else: 
            return jsonify({'error': 'not authorized'}), 401
    
    data = request.get_json()

    risk_score = BIAS+((COEFFICIENTS['hours']*data['hours'])+(COEFFICIENTS['cycles']*data['cycles'])+(COEFFICIENTS['temp_excursions']*data['temp_excursions']))
    return jsonify({'risk_score': risk_score})

@app.route("/part/<part_id>")
def part(part_id):
    return jsonify({"you_asked_for":part_id})


app.run(port=PORT, host= "0.0.0.0")