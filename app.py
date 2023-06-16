from flask import Flask, jsonify, request
from config import SECRET_KEY, db
from Models.people import People
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
        @app.route('/')
        def index():
            return jsonify("Hello World")

        @app.route('/create', methods=['POST'])
        def add_people():
            if request.method == 'POST':
                name = request.form['name']
                email = request.form['email']
                phone = request.form['phone']
                people = People(name=name, email=email, phone=phone)
                db.session.add(people)
                db.session.commit()

                people_dict = {
                    'id': people.id,
                    'name': people.name,
                    'email': people.email,
                    'phone': people.phone
                }

                return jsonify(people_dict)

        @app.route('/read', methods=['GET'])
        def retrieve_all_people():
            people = People.query.all()
            people_list = []

            for person in people:
                person_dict = {
                    'id': people.id,
                    'name': person.name,
                    'email': person.email,
                    'phone': person.phone
                }
                people_list.append(person_dict)

            return jsonify(people_list)

        @app.route('/read/<int:id>')
        def retrieve_single_person(id):
            people = People.query.filter_by(id=id).first()
            if people:
                people_dict = {
                    'id': people.id,
                    'name': people.name,
                    'email': people.email,
                    'phone': people.phone
                }
                return jsonify(people_dict)
            else:
                return jsonify(f"Person with id {id} Doesn't exist!")

        @app.route('/update/<int:id>', methods=['PUT', 'PATCH'])
        def update_people(id):
            people = db.session.get(People, id)
            if not people:
                return jsonify({'message': 'Person not found'})

            if request.method == 'PUT':

                name = request.form['name']
                email = request.form['email']
                phone = request.form['phone']
                people.name = name
                people.email = email
                people.phone = phone
            elif request.method == 'PATCH':
                # Handle partial update with PATCH method
                if 'name' in request.form:
                    people.name = request.form['name']
                if 'email' in request.form:
                    people.email = request.form['email']
                if 'phone' in request.form:
                    people.phone = request.form['phone']

            db.session.add(people)  # Add the updated object to the session
            db.session.commit()

            # Create a dictionary representation of the updated People object
            people_dict = {
                'id': people.id,
                'name': people.name,
                'email': people.email,
                'phone': people.phone
            }

            return jsonify(people_dict)

        @app.route('/delete/<int:id>/', methods=['DELETE'])
        def delete_person(id):
            if request.method == 'DELETE':
                people = People.query.filter_by(id=id).first()
                if people:
                    db.session.delete(people)
                    db.session.commit()
                    return jsonify("Person Successfully Deleted!")
                else:
                    return jsonify(f"Person cannot be deleted because none of the people exists with id {id}")

        # db.drop_all()
        db.create_all()
        db.session.commit()
        return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=5069)
