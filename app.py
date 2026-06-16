from flask import Flask
import os

app = Flask(__name__)

version = os.getenv("VERSION", "BLUE")

@app.route("/")
def home():
    return f"Blue-Green App Running - {version}"

app.run(host="0.0.0.0", port=5000)
