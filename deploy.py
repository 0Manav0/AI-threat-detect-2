from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import joblib
import secrets
import os
import json
from datetime import datetime

# Store all predictions here
PREDICTION_HISTORY = []
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = secrets.token_hex(16)  # Use a secure random string in production

# Load the trained model
MODEL_PATH = "models/threat_detector_rf.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

# Automatically get feature names from the model
FEATURE_COLUMNS = list(model.feature_names_in_)

# --- User Management ---
users_db = {"admin": "admin123"}  # default admin account
LOG_FILE = "user_logs.json"


def log_action(username, action):
    """Save user activity in log file."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "username": username,
        "action": action
    }
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


def current_user():
    return session.get("username", "guest")


# ------------------- ROUTES -------------------

@app.route('/products')
def products():
    products_list = [{"name": "AI Widget", "price": 99}, {"name": "Threat Detector", "price": 149}]
    return render_template('products.html', products=products_list)

@app.route("/")
def index():
    user = current_user()
    if user == "guest":
        log_action(user, "forbidden_index")
        return redirect(url_for("login"))
    log_action(user, "index")
    return render_template("index.html", feature_columns=FEATURE_COLUMNS)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users_db and users_db[username] == password:
            session["username"] = username
            log_action(username, "successful_login")
            return redirect(url_for("index"))
        else:
            log_action(username if username else "guest", "failed_login")
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", error="Username and password required")

        if username in users_db:
            return render_template("register.html", error="User already exists")

        users_db[username] = password
        log_action(username, "register")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    user = current_user()
    if user != "guest":
        session.clear()  # clears all session data
        return render_template("login.html")
    return jsonify({"error": "No active session"}), 400



@app.route("/predict", methods=["POST"])
def predict():
    user = current_user()
    if user == "guest":
        log_action(user, "forbidden_predict")
        return jsonify({"error": "Unauthorized"}), 403

    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        pred, conf = model_predict(df)

        # Generate simple rule-based issues
        issues = []
        if data.get("num_failed_logins", 0) > 3:
            issues.append("Multiple failed login attempts detected.")
        if data.get("root_shell", 0) == 1:
            issues.append("Root shell access detected.")
        if data.get("su_attempted", 0) > 0:
            issues.append("Switch user attempts detected.")
        if not issues:
            issues.append("No obvious threats detected.")

        # Add warning if prediction=1 and confidence > 0.55
        warning = ""
        if pred[0] == 1 and conf[0] > 0.55:
            warning = "⚠ Warning: High confidence threat detected!"

        # Store explanation in session
        session['explanation'] = {
            'prediction': int(pred[0]),
            'confidence': round(conf[0], 2),
            'explanation': "The system identified potential issues.",
            'features': issues,
            'warning': warning
        }

        # Store in prediction history
        if 'PREDICTION_HISTORY' not in session:
            session['PREDICTION_HISTORY'] = []
        session['PREDICTION_HISTORY'].append({
            'input': data,
            'prediction': int(pred[0]),
            'confidence': round(conf[0], 2),
            'issues': issues,
            'warning': warning
        })

        log_action(user, "predict")

        # Return JSON to JS
        return jsonify({
            "success": True,
            "prediction": pred.tolist(),
            "confidence": conf.tolist(),
            "issues": issues,
            "warning": warning
        })

    except Exception as e:
        return jsonify({"error": str(e)})




def model_predict(df):
    pred = model.predict(df)
    conf = model.predict_proba(df)[:, 1]
    return pred, conf


# --- Before each request ---
@app.before_request
def track_requests():
    if request.endpoint not in ("static",):
        user = current_user()
        action = request.endpoint if request.endpoint else "unknown"
        log_action(user, action)


if __name__ == "__main__":
    app.run(debug=True)
