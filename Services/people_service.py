from flask import request
from Models.people import People


class PeopleService:
    def add_people(self, name, email, phone):
        people = People(name=name, email=email, phone=phone)
        people.save()
        people_dict = {
            'id': people.id,
            'name': people.name,
            'email': people.email,
            'phone': people.phone
        }
        return people_dict

    def retrieve_all_people(self):
        people = People.query.all()
        people_list = []

        for person in people:
            person_dict = {
                'id': person.id,
                'name': person.name,
                'email': person.email,
                'phone': person.phone
            }
            people_list.append(person_dict)

        return people_list

    def retrieve_single_person(self, person_id):
        person = People.query.get(person_id)
        if person:
            person_dict = {
                'id': person.id,
                'name': person.name,
                'email': person.email,
                'phone': person.phone
            }
            return person_dict
        else:
            return f"Person with id {person_id} doesn't exist!"

    def update_people(self, person_id, data):
        people = People.query.get(person_id)
        if not people:
            return {'message': 'Person not found'}

        if request.method == 'PUT':
            people.name = data['name']
            people.email = data['email']
            people.phone = data['phone']
        elif request.method == 'PATCH':
            if 'name' in data:
                people.name = data['name']
            if 'email' in data:
                people.email = data['email']
            if 'phone' in data:
                people.phone = data['phone']

        people.save()
        people_dict = {
            'id': people.id,
            'name': people.name,
            'email': people.email,
            'phone': people.phone
        }
        return people_dict

    def delete_person(self, person_id):
        person = People.query.get(person_id)
        if person:
            person.delete()
            return "Person Successfully Deleted!"
        else:
            return f"Person with id {person_id} doesn't exist!"
