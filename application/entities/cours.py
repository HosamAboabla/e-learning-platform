from datetime import date

from application.data_base.database_migration import Evaluation, Cour, db
from application.entities.evaluation import evaluation_serialize


def cour_serialize(cour):
    return{
        'id': cour.id,
        'title': cour.title,
        'description': cour.description,
        'file': cour.file,
        'date_created': cour.date_created,
        'module_id' : cour.module_id,
        'evaluations' : [*map(evaluation_serialize, Evaluation.query.filter_by(cours_id = cour.id).all())]
    }


def add_cours(request_data):
    cours = Cour(
        title=request_data['title'],
        description=request_data['description'],
        module_id=(int)(request_data['module_id']),
        date_created=str(date.today()),
        file=request_data['file'],
    )
    db.session.add(cours)
    db.session.commit()
