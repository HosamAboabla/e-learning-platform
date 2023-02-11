from application.data_base.database_migration import Module, db, Cour
from datetime import date
from flask import jsonify

from application.entities.cours import cour_serialize , header_cour_serialize



def module_serialize(module):
    return{
        'id': module.id,
        'title': module.title,
        'description': module.description,
        'date_created': module.date_created,
        'user_id' : module.user_id,
        'cours': [*map(cour_serialize,Cour.query.filter_by(module_id = module.id).all())]
    }

def header_module_serialize(module):
    return{
        'id': module.id,
        'title': module.title,
        'cours': [*map(header_cour_serialize,Cour.query.filter_by(module_id = module.id).all())]
    }

def add_module(request_data):
    moDule = Module(
        title=request_data['title'],
        description=request_data['description'],
        user_id=1,
        date_created=str(date.today())
    )
    db.session.add(moDule)
    db.session.commit()


def get_all_module():
    return jsonify([*map(module_serialize, Module.query.all())])


def get_on_module(id_user):
    return module_serialize(Module.query.get(id_user))


def update_module(request_data):
    print(request_data["id"])
    db.session.query(Module).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()


def delete_module(id_module):
    message = 'not exist'
    valid = Module.query.filter_by(id=id_module).delete()
    db.session.commit()
    if valid:
        message = '"The deletion has occurred"'
    return {"message": message}
