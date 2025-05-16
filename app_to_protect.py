from flask import Flask, request, render_template_string

app = Flask(__name__)

# Serve the frontend form on GET /
@app.route('/', methods=['GET'])
def home():
    # HTML form served via Flask template string
    html_form = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>WAF Test Form</title>
    </head>
    <body>
        <h2>Test WAF POST Request</h2>
        <form method="POST" action="http://localhost:8080/">
            <label for="inputData">Enter some text or script:</label><br /><br />
            <textarea id="inputData" name="inputData" rows="6" cols="60" placeholder="Try &lt;script&gt;alert('XSS')&lt;/script&gt;"></textarea><br /><br />
            <button type="submit">Send POST Request</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_form)

# Example POST endpoint
@app.route('/login', methods=['POST'])
def login():
    # For demo, just echo that the endpoint was reached
    return "Login endpoint reached"

if __name__ == '__main__':
    app.run(port=5000)
