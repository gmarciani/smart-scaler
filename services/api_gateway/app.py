from flask import Flask
from services.api_gateway.api.base import base

# Initialization
app = Flask(__name__)
app.config.from_object("services.api_gateway.config.Default")

# Blueprints
app.register_blueprint(base)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["API_GATEWAY_PORT"])
