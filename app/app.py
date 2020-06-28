import os

from flask import Flask, render_template, jsonify, request
from . import settings
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

project_dir = os.path.dirname(os.path.abspath(__file__))   


def register_extensions(db, app):
    """Register Flask extensions."""
    db.init_app(app)

    with app.app_context():
        db.create_all()
    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(controllers.home.blueprint)
    app.register_blueprint(controllers.auth.blueprint)
    app.register_blueprint(controllers.tutorial.blueprint)
    return None

def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return None

def register_requests(app):
    @app.route('/', methods=['GET'])
    def hello_world():
        return render_template('home/index.html')

    @app.route('/eye_data', methods=['GET'])
    def return_db():
        eyes = models.Eye_Data.query.all()
        results = [
            {
                "timestamp": x.timestamp,
                "score": x.score,
            } for x in eyes]
        return(jsonify(results[-1]))

    @app.route('/eye_data', methods=['POST'])
    def addEyeData():
        timestamp=request.form.get('timestamp')
        score=request.form.get('score')
        try:
            eye_data=models.Eye_Data(timestamp,score)
            db.session.add(eye_data)
            db.session.commit()
            return "Eye data added at {}. data id={}".format(timestamp,eye_data.id)
        except Exception as e:
            return(str(e))

    @app.route('/face_data', methods=['POST'])
    def addFaceData():
        timestamp=request.form.get('timestamp')
        try:
            face_data=models.Face_Data(timestamp)
            db.session.add(face_data)
            db.session.commit()
            return "Face data added at {}. data id={}".format(timestamp,face_data.id)
        except Exception as e:
            return(str(e))


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(settings)
from . import models

register_extensions(db,app)
# register_blueprints(app)
register_errorhandlers(app)
register_requests(app)


