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
 1. Visit the main page at http://127.0.0.1:5000/
 2. Register a new user or login with existing credentials
 3. Navigate pages (products, add to cart, etc.)
 4. Each action is automatically logged and monitored by the AI model

## Requirements

- Python 3.12+
- Flask
- pandas
- joblib
- scikit-learn
- before using first setup all the required files/folders as mentioned in https://github.com/0Manav0/AI-threat-detect.git

## Setup Instructions

just copy-paste the deploy.py(of this repo) into the previously created deploy.py in src(folder).

Change all the templates(folder)'s files with this repo's template also change static(folder).


```bash

# 1. Install dependencies
pip install flask pandas joblib scikit-learn


# 1. Run the Flask app
python deploy.py

# 3. Access the app in your browser
# Open: http://127.0.0.1:5000
# AI predictions are automatically logged for these actions.
