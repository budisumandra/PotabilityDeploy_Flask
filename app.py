from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
with open(
    "D:\\budi_projects\\flask_deploy\potability_flask\water_potability.bin", "rb"
) as f_in:
    dv, rf = pickle.load(f_in)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    key_features = [
        "ph",
        "hardness",
        "solids",
        "chloramines",
        "sulfate",
        "conductivity",
        "organic_carbon",
        "trihalomethanes",
        "turbidity",
    ]
    value_features = [int(x) for x in request.form.values()]
    features = dict(zip(key_features, value_features))

    def predict_single(potability_parameters):
        X = dv.transform([potability_parameters])
        y_pred = rf.predict_proba(X)[:, 1]
        return y_pred[0]

    def predict_water_potability(potability_parameters):
        prediction = predict_single(potability_parameters)
        potability = prediction >= 0.5
        result = {
            "Potability Probability": round(float(prediction), 2),
            "Is Potable?": "Potable" if potability else "Not Potable",
        }

        # return pd.DataFrame(result, index=[0])
        return f"|| Potability Probability: {round(float(prediction), 2)} || ||Is Potable? -> {'Potable' if potability else 'Not Potable'} ||"

    return render_template(
        "index.html", prediction_text=predict_water_potability(features)
    )


if __name__ == "__main__":
    app.run(debug=True)
