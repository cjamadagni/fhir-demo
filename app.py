from flask import Flask, request, send_file, render_template, json
app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to fhir-demo"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
