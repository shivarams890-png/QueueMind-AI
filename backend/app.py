
from flask import Flask, jsonify, render_template

from database import create_tables
from routes.queue_routes import queue_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)

# Initialize database
create_tables()

# Register API routes
app.register_blueprint(queue_bp, url_prefix="/api/queue")
app.register_blueprint(admin_bp, url_prefix="/api/admin")


# Customer website
@app.route("/")
def home():
    return render_template("index.html")


# Admin dashboard
@app.route("/admin")
def admin():
    return render_template("admin.html")


# Health check
@app.route("/api/health")
def health():
    return jsonify({
        "status": "success",
        "message": "QueueMind Backend is running!"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
