
from flask import Blueprint, request, jsonify

from services.queue_service import (
    add_customer,
    get_queue,
    cancel_customer
)

queue_bp = Blueprint("queue", __name__)

# Customer joins the queue
@queue_bp.route("/join", methods=["POST"])
def join_queue():

    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({
            "error": "Customer name is required"
        }), 400

    customer = add_customer(name)

    return jsonify({
        "message": "Successfully joined the queue!",
        "customer": customer
    }), 201

# View all waiting customers
@queue_bp.route("/", methods=["GET"])
def view_queue():

    customers = get_queue()

    return jsonify({
        "total_customers": len(customers),
        "queue": customers
    })

# Cancel a queue token
@queue_bp.route("/cancel/<int:token_number>", methods=["DELETE"])
def cancel_queue(token_number):

    success = cancel_customer(token_number)

    if not success:
        return jsonify({
            "error": "Token not found or already processed"
        }), 404

    return jsonify({
        "message": "Queue token cancelled successfully"
    })