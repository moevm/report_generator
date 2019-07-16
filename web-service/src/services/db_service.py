from flask_mongoengine import MongoEngine
from app import app

MONGO_ENGINE = None


def getMongo():
    global MONGO_ENGINE
    if MONGO_ENGINE is None:
        MONGO_ENGINE = MongoEngine(app)
    return MONGO_ENGINE