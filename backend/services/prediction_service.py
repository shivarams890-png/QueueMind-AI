
import json
import os

from config import SERVICE_TIME

# Locate the trained ML model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "queue_model.json")

def load_model():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("QueueMind ML model not found!")

    with open(MODEL_PATH, "r") as file:
        return json.load(file)

def predict_waiting_time(customers_ahead, total_waiting,
                         average_service_time=None):

    if average_service_time is None:
        average_service_time = SERVICE_TIME

    model = load_model()

    weights = model["weights"]
    bias = model["bias"]

    prediction = (
        bias
        + weights[0] * customers_ahead
        + weights[1] * average_service_time
        + weights[2] * total_waiting
    )

    return max(0, round(prediction))