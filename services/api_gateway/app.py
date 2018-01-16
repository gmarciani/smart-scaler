from flask import Flask
from api.status import status
from api.kube import kube
from _ignore.test import test


# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Routes
app.register_blueprint(status)
app.register_blueprint(kube)
app.register_blueprint(test)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["API_GATEWAY_PORT"], threaded=True)
