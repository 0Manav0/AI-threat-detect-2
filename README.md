# AI Threat Detection Demo for Web Requests

This project demonstrates how an AI-driven threat detection system can be integrated into a web application to monitor user actions in real-time. It tracks requests, logs activity, predicts suspicious behavior, and provides explanations for predictions.

> **Note:** This setup is for demonstration purposes only. You can modify `deploy.py` and templates to adapt it to your own web application.

---

## Features

- Tracks user actions (logins, page visits, product interactions, etc.).
- Predicts suspicious behavior using a pre-trained Random Forest model (`threat_detector_rf.pkl`).
- Provides real-time explanations for predictions.
- Stores history of predictions for later analysis.
- Simple admin dashboard to view all logged actions.
- Session-based user management (login, logout, registration).
- Demonstrates how AI monitoring can be integrated into any website.

---

## Note:
 - This setup is for demo/educational purposes only
 - Modify `deploy.py` and templates as needed for your own web application
 - The model's thresholds, logging, and monitored features can be customized
 - Do not deploy this setup in production without proper security checks


## Folder Structure
similar to the previous one just modifications in deploy.py and some files of templates folder else no changes

---

## how to use:
 1. Visit '/' to see the main page
 2. Register a new user or login with existing credentials
 3. Navigate pages (products, add to cart, etc.)
 4. Each action is automatically logged and monitored by the AI model

## Requirements

- Python 3.12+
- Flask
- pandas
- joblib
- scikit-learn

Install dependencies using:
```bash
pip install flask pandas joblib scikit-learn


## Setup Instructions


# 1. Clone the repository
git clone <repository-url>
cd project

# 2. Install dependencies
pip install flask pandas joblib scikit-learn

# 3. Ensure the model file exists
# The `models/threat_detector_rf.pkl` file must exist.
# If not, train your own model or download a compatible one.

# 4. Run the Flask app
python deploy.py

# 5. Access the app in your browser
# Open: http://127.0.0.1:5000
AI predictions are automatically logged for these actions.
