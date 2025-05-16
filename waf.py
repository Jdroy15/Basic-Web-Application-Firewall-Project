from flask import Flask, request, jsonify
import requests
import json
import socket
import logging

app = Flask(__name__)

# Log to both console and a file named waf.log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("waf.log")
    ]
)

# Get local IP address of the server
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# Load WAF rules
def load_rules():
    with open("rules.json") as f:
        return json.load(f)

rules = load_rules()
TARGET_APP = "http://localhost:5000"  # Backend web application

@app.before_request
def waf_filter():
    client_ip = request.remote_addr
    full_request = (
        request.path +
        str(request.args) +
        request.get_data(as_text=True) +
        str(request.form) +
        str(dict(request.headers))
    )

    logging.info(f"REQUEST: Client IP: {client_ip}, Path: {request.path}, Data: {full_request}")

    # Block based on IP address
    if client_ip in rules["blocked_ips"]:
        logging.warning(f"BLOCKED: IP {client_ip} is blacklisted.")
        return jsonify({"message": "Blocked by WAF: IP blacklisted"}), 403

    # Block based on pattern matching
    for pattern in rules["patterns"]:
        if pattern.lower() in full_request.lower():
            logging.warning(f"BLOCKED: Pattern '{pattern}' matched from IP {client_ip}")
            return jsonify({"message": f"Blocked by WAF: Detected pattern '{pattern}'"}), 403

# Proxy logic
@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    url = f"{TARGET_APP}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    server_ip = get_local_ip()
    logging.info(f"🌐 WAF running on: http://{server_ip}:8080 (Local IP)")
    app.run(port=8080)
