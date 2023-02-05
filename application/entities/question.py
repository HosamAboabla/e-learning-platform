def question_serialize(question):
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
        'evaluation_id' : question.evaluation_id,
    }

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

