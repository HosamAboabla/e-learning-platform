import sqlite3
from application.core.image.image_refactor import get_image_doc
from application.data_base.database_migration import db, User, bcrypt
from flask import jsonify
from datetime import date


def user_serialize(user):
    return{
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        "password":user.password,
        'profile': user.profile,
        'date_created': user.date_created,
        'date_of_birth': user.date_of_birth,
        'specialty': user.specialty,
        'address': user.address,
        'city': user.city,
        'country': user.country,
        'postal_code': user.postal_code,
        'role': user.role
    }


def user_serializez(user):
    return{
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'profile': user.profile,
        'date_created': user.date_created,
        'date_of_birth': user.date_of_birth,
        'specialty': user.specialty,
        'address': user.address,
        'city': user.city,
        'country': user.country,
        'postal_code': user.postal_code,
        'image': user.image,
        'role': user.role
    }


def get_all_user():
    return jsonify([*map(user_serializez,User.query.all())])


def get_one_user(id_user):
    user = user_serialize(User.query.get(id_user))
    return user


def delete_user(id_user):
    message = 'not exist'
    valid = User.query.filter_by(id=id_user).delete()
    db.session.commit()
    if valid:
        message = jsonify({"delete" : "The deletion has occurred"})
    return message


def update_user(request_data):
    db.session.query(User).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()


def find_by_username(email):
    connection = sqlite3.connect('projet.db')
    cursor = connection.curso
    try:
        data = cursor.execute('SELECT * FROM user WHERE email=? ', (email,)).fetchone()
        if data:
            return data
    finally:
        connection.close()


def add_user(request_data):
    row_password = request_data['password']
    pw_hash = bcrypt.generate_password_hash(row_password)
    try:
        user = User(
            firstname=request_data['firstname'],
            lastname=request_data['lastname'],
            email=request_data['email'],
            password=pw_hash,
            profile=request_data['profile'],
            date_created=str(date.today()),
            date_of_birth=request_data['date_of_birth'],
            specialty=request_data['specialty'],
            address=request_data['address'],
            city=request_data['city'],
            country=request_data['country'],
            postal_code=request_data['postal_code'],
            image=request_data['image'],
            role=request_data['role']
        )
        db.session.add(user)
        db.session.commit()
        return True
    except:
        return False