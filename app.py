from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running in production!"

if __name__ == "__main__":
    app.run()  # This will only run locally; Gunicorn will be used in production.

