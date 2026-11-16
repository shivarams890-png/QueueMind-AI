
import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "queue_data.csv")
model_path = os.path.join(BASE_DIR, "queue_model.json")

X = []
y = []

with open(csv_path, "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)

    for row in reader:

        # Skip blank lines and header rows
        if not row or row[0].strip() == "customers_ahead":
            continue

        if len(row) < 4:
            continue

        try:
            X.append([
                float(row[0]),
                float(row[1]),
                float(row[2])
            ])

            y.append(float(row[3]))

        except ValueError:
            continue

print("Records loaded:", len(X))

if len(X) == 0:
    print("No valid training data found!")
    raise SystemExit

# Linear Regression using Gradient Descent
n = len(X)
features = 3

weights = [0.0, 0.0, 0.0]
bias = 0.0
learning_rate = 0.001

for epoch in range(10000):

    dw = [0.0, 0.0, 0.0]
    db = 0.0

    for i in range(n):

        prediction = bias

        for j in range(features):
            prediction += weights[j] * X[i][j]

        error = prediction - y[i]

        for j in range(features):
            dw[j] += error * X[i][j]

        db += error

    for j in range(features):
        weights[j] -= learning_rate * dw[j] / n

    bias -= learning_rate * db / n

# Evaluate model
total_error = 0

for i in range(n):

    prediction = bias

    for j in range(features):
        prediction += weights[j] * X[i][j]

    total_error += abs(prediction - y[i])

mae = total_error / n

# Save trained model
model = {
    "weights": weights,
    "bias": bias
}

with open(model_path, "w") as file:
    json.dump(model, file, indent=4)

print("\nQueueMind ML Training Completed!")
print("Training records:", n)
print("Mean Absolute Error:", round(mae, 2))
print("Model saved successfully!")
