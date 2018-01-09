from flask import Flask
from services.agents_manager.api.base import base

# Initialization
app = Flask(__name__)
app.config.from_object("services.agents_manager.config.Default")

# Blueprints
app.register_blueprint(base)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["AGENTS_MANAGER_PORT"])
