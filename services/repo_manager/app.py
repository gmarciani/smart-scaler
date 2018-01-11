import sys, os
from flask import Flask
_ppath = os.path.join(os.path.realpath(__file__), "..", "..")
print(_ppath)
sys.path.append(_ppath)

from services.repo_manager.api.base import base

# Initialization
app = Flask(__name__)
app.config.from_object("config.Default")

# Blueprints
app.register_blueprint(base)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["REPO_MANAGER_PORT"])
