from flask import Flask, jsonify, request, abort
from predictions_generator_ import generate_predictions
import json
import dotenv
import os

dotenv.load_dotenv()

MY_API_TOKEN = os.getenv("MY_API_TOKEN")

app = Flask(__name__)


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    validate_token(request.args.get('token'))
    if request.method == 'GET':
        try:
            predictions = {}
            with open('predictions_all.json', 'r') as handle:
                predictions = json.loads(handle.read())
            return jsonify(predictions)
        except:
            abort(500)
    elif request.method == 'POST':
        region_json = request.json
        region = region_json["region"]
        if region == 'all' or region == '':
            try:
                predictions = {}
                with open('predictions_all.json', 'r') as handle:
                    predictions = json.loads(handle.read())
                return jsonify(predictions)
            except:
                abort(500)
        else:
            predictions = {}
            try:
                with open('predictions_all.json', 'r') as handle:
                    predictions = json.loads(handle.read())
            except:
                abort(500)
            try:
                region_prediction = {
                    "last_model_train_time": predictions["last_model_train_time"],
                    "last_prediction_time": predictions["last_prediction_time"],
                    "regions_forecast": {region: (predictions["regions_forecast"])[region]}
                }
                return jsonify(region_prediction)
            except KeyError as err:
                abort(404)


@app.route('/update', methods=['GET'])
def update():
    
    validate_token(request.args.get('token'))
    
    try:
        generate_predictions()
        return jsonify({"msg": "Update successful"}), 200
    except:
        abort(500)

def validate_token(token):
    if token is None:
        abort(400)
    if token != MY_API_TOKEN:
        abort(403) 

if __name__ == '__main__':
    app.run(host='0.0.0.0')
