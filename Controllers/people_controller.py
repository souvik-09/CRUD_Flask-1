from flask import jsonify, request
from Services.people_service import PeopleService


class PeopleController:
    def __init__(self):
        self.people_service = PeopleService()

    def add_people(self):
        data = request.get_json()
        name = data['name']
        email = data['email']
        phone = data['phone']
        result = self.people_service.add_people(name, email, phone)
        return jsonify(result)

    def retrieve_all_people(self):
        result = self.people_service.retrieve_all_people()
        return jsonify(result)

    def retrieve_single_person(self, person_id):
        result = self.people_service.retrieve_single_person(person_id)
        return jsonify(result)

    def update_people(self, person_id):
        data = request.get_json()
        result = self.people_service.update_people(person_id, data)
        return jsonify(result)

    def delete_person(self, person_id):
        result = self.people_service.delete_person(person_id)
        return jsonify(result)
