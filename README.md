# 🛡️ Web Application Firewall (WAF)

This project is a custom Web Application Firewall (WAF) built using Python and Flask. It filters HTTP requests for malicious content such as XSS, SQL injection, and command injection, and forwards clean traffic to a protected backend web application.

---

## 🚀 Features

- ✅ Detects and blocks common web attacks (XSS, SQLi, etc.)
- 🔄 Self-updates threat detection rules from external threat feeds
- 🔍 Logs all blocked and forwarded requests
- 🧪 Runs locally for testing 

---

## 🧱 Project Structure

```bash
.
├── waf.py               # Main WAF application
├── app_to_protect.py    # Dummy web app to simulate backend
├── threat_feed.json     # Sample threat signatures (used by WAF)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
