from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the root URL
@app.route("/")
def home():
    return "Welcome to your Flask application!"

# Define another route
@app.route("/about")
def about():
    return "This is a basic Flask application."

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
