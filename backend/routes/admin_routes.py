
from flask import Blueprint, jsonify

from services.queue_service import (
    serve_customer,
    get_queue
)

admin_bp = Blueprint("admin", __name__)


# View current queue status
@admin_bp.route("/queue", methods=["GET"])
def admin_queue():

    customers = get_queue()

    return jsonify({
        "total_waiting": len(customers),
        "customers": customers
    })


# Serve the next customer
@admin_bp.route("/serve", methods=["POST"])
def serve_next_customer():

    customer = serve_customer()

    if customer is None:
        return jsonify({
            "message": "Queue is empty!"
        }), 400

    return jsonify({
        "message": "Customer served successfully!",
        "served_customer": customer
    })


# Admin dashboard summary
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():

    customers = get_queue()

    return jsonify({
        "system": "QueueMind AI",
        "total_waiting": len(customers),
        "next_token": customers[0]["token_number"] if customers else None
    })
