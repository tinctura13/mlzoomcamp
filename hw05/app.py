from flask import Flask
from flask import request, jsonify
import pickle 


app = Flask("service")

with open("model1.bin", "rb") as fin:
    model = pickle.load(fin)

with open("dv.bin", "rb") as fin:
    dv = pickle.load(fin)
    

@app.route("/predict", methods=["POST"])
def predict():
    client = request.get_json()
    print(type(client), client)
    X = dv.transform(client)
    proba = model.predict_proba(X)
    response = {
        "proba": proba.tolist()
    }
    return jsonify(response)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify("pong")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)