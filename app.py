from flask import Flask

from Controllers.people_controller import PeopleController
from config import SECRET_KEY, db
from os import environ, path, getcwd
from dotenv import load_dotenv

load_dotenv(path.join(getcwd(), '.env'))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initialized Successfully")

    with app.app_context():
        people_controller = PeopleController()

        @app.route('/')
        def index():
            return "Hello World"

        @app.route('/create', methods=['POST'])
        def add_people():
            return people_controller.add_people()

        @app.route('/read', methods=['GET'])
        def retrieve_all_people():
            return people_controller.retrieve_all_people()

        @app.route('/read/<int:person_id>')
        def retrieve_single_person(person_id):
            return people_controller.retrieve_single_person(person_id)

        @app.route('/update/<int:person_id>', methods=['PUT', 'PATCH'])
        def update_people(person_id):
            return people_controller.update_people(person_id)

        @app.route('/delete/<int:person_id>/', methods=['DELETE'])
        def delete_person(person_id):
            return people_controller.delete_person(person_id)

        # db.drop_all()
        db.create_all()
        db.session.commit()

        return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=5069)
