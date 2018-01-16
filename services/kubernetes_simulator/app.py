from flask import Flask
from api.status import status
from api.pods import pods
from api.smart_scalers import smart_scalers

# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Routes
app.register_blueprint(status)
app.register_blueprint(pods)
app.register_blueprint(smart_scalers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["KUBERNETES_PORT"], threaded=True)
