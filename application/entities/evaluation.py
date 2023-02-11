from datetime import date

from application.data_base.database_migration import db, Question, Evaluation
from application.entities.question import question_serialize


def evaluation_serialize(evaluation):
    return{
        'id': evaluation.id,
        'title': evaluation.title,
        'description': evaluation.description,
        'date_created': evaluation.date_created,
        'cours_id' : evaluation.cours_id,
        "questions" : [*map(question_serialize,Question.query.filter_by(evaluation_id = evaluation.id).all())]
    }



def header_evaluation_serialize(evaluation):
    return{
        'title': evaluation.title,
    }



def evaluation_serializez(evaluation):
    return{
        'id': evaluation.id,
        'title': evaluation.title,
        'description': evaluation.description,
        'date_created': evaluation.date_created,
        'cours_id' : evaluation.cours_id,
    }

def add_evaluation(request_data):
    evaluation = Evaluation(
        title=request_data['title'],
        cours_id=request_data['cours_id'],
        description=request_data['description'],
        user_id = (int)(request_data['user_id']),
        date_created=str(date.today()),
    )
    db.session.add(evaluation)
    db.session.commit()


def add_Question(request_data):
    question = Question(
        title=request_data['title'],
        description=request_data['description'],
        evaluation_id=(int)(request_data['evaluation_id']),
        date_created=str(date.today()),
        propo1=request_data['propo1'],
        propo2=request_data['propo2'],
        propo3=request_data['propo3'],
        file=request_data['file'],
        reponse=request_data['reponse'], # answer / reply
        Niveau=request_data['Niveau'], # level
        duree =request_data['duree'], # term / duration
        valider= request_data['valider'], # to validate
    )
    db.session.add(question)
    db.session.commit()

def question_serializez(question):
    return{
        'id': question.id,
        'title': question.title,
        'description': question.description,
        'date_created': question.date_created,
        'propo1' : question.propo1,
        'propo2' : question.propo2,
        'propo3' : question.propo3,
        'file' : question.file,
        'Niveau': question.Niveau,
        'reponse' : question.reponse,
    }

