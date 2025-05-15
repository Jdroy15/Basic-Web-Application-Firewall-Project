from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Load rules
def load_rules():
    with open("rules.json") as f:
        return json.load(f)

rules = load_rules()

TARGET_APP = "http://localhost:5000"  # Actual web app

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
    print(">>> FULL REQUEST DATA:", full_request)

    # Block by IP
    if client_ip in rules["blocked_ips"]:
        return jsonify({"message": "Blocked by WAF: IP blacklisted"}), 403

    # Block by pattern
    for pattern in rules["patterns"]:
        if pattern.lower() in full_request.lower():
            return jsonify({"message": f"Blocked by WAF: Detected pattern '{pattern}'"}), 403

@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    url = f"{TARGET_APP}/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(port=8080)
