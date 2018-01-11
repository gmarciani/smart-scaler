from flask import Flask
from api.status import status
from api.pods import pods

# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Routes
app.register_blueprint(status)
app.register_blueprint(pods)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["KUBERNETES_PORT"])
