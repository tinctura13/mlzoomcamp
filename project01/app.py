from flask import Flask
from flask import request, jsonify
import pickle 


app = Flask("service")

with open("model.pkl", "rb") as fin:
    model, dv = pickle.load(fin)
    

@app.route("/predict", methods=["POST"])
def predict():
    flat = request.json["flat"]
    print(type(flat), flat)
    X = dv.transform([flat])
    proba = model.predict(X)
    response = {
        "price": round(proba[0], 2)
    }
    return jsonify(response)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify("pong")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)