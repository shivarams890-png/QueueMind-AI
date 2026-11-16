
import json
import os

def predict_waiting_time(customers_ahead, avg_service_time, current_waiting):

    model_path = os.path.join(
        os.path.dirname(__file__),
        "queue_model.json"
    )

    with open(model_path, "r") as file:
        model = json.load(file)

    weights = model["weights"]
    bias = model["bias"]

    prediction = (
        weights[0] * customers_ahead +
        weights[1] * avg_service_time +
        weights[2] * current_waiting +
        bias
    )

    return max(0, round(prediction, 2))
