from tensorflow.python.keras.backend import set_session
import tensorflow as tf

tf_config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=2)
sess = tf.compat.v1.Session(config=tf_config)
graph = tf.compat.v1.get_default_graph()
set_session(sess)

from application.core.face_recognition.emotion import Emotion
from application.core.face_recognition.face import face_base64
from flask import request, jsonify , render_template
import json
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from application.entities.cours import cour_serialize, add_cours
from application.entities.evaluation import evaluation_serialize, add_evaluation, add_Question, evaluation_serializez , question_serializez
from application.entities.question import question_serialize
from application.entities.user import add_user, user_serializez, get_all_user
from application.entities.module import add_module, module_serialize
from application.data_base.database_migration import app, User, bcrypt, db, Module, Cour, Evaluation, Question

emotion_class = Emotion()

# create_access_token() function is used to actually generate the JWT.
@app.route("/api/login", methods=["POST"])
@cross_origin(supports_credentials=True)
def login():
    email = request.json.get("email", None)
    passwo = request.json.get("password", None)
    
    peter =  User.query.filter_by(email=email).first()

    if peter and bcrypt.check_password_hash(peter.password,passwo):
        access_token = create_access_token(identity=email)
        return jsonify({"access_token":access_token},{"user": user_serializez(peter)})
    else:
        return jsonify({"msg": "Bad email or password"}), 401





@app.route('/api/users', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def create_user():
    if request.method == 'POST':
        try:
            request_data = json.loads(request.data)
            if add_user(request_data):
                return jsonify({"add": "create successfully"})
            else:
                return jsonify({"error": "Email must be unique!"})
        except ValueError:
            return jsonify({"email", "should be unique"})
    else:
        return get_all_user()


@app.route('/api/one_user/<id_user>')
@cross_origin(supports_credentials=True)
def get_user(id_user):
    user = user_serializez(User.query.get(id_user))
    return jsonify(user)


@app.route("/api/delete/<id_user>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_collection(id_user):
    message = {}
    valid = User.query.filter_by(id=id_user).delete()
    db.session.commit()
    return jsonify({"delete": "deleted successfully"})


@app.route("/api/update_user", methods=["POST"])
@cross_origin(supports_credentials=True)
def update_user_app():
    request_data = json.loads(request.data)
    db.session.query(User).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()
    return jsonify({"update": "updated successfully"})


@app.route('/api/modules', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def create_module():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        add_module(request_data)
        return {" 201 ": "create successfully"}
    else:
        return jsonify([*map(module_serialize, Module.query.all())])


@app.route('/api/one_module/<id_user>')
@cross_origin(supports_credentials=True)
def get_module(id_user):
    return module_serialize(Module.query.get(id_user))


@app.route("/api/delete_module/<id_module>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_on_module(id_module):
    Module.query.filter_by(id=id_module).delete()
    db.session.commit()
    return {"delete": "deleted successfully"}


@app.route("/api/update_module", methods=["POST"])
@cross_origin(supports_credentials=True)
def update_module_app():
    request_data = json.loads(request.data)
    db.session.query(Module).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()
    return jsonify({"update": "updated successfully"})


@app.route("/api/getCourByModule/<id_module>/", methods=["GET"])
@cross_origin(supports_credentials=True)
def getCoursByModule(id_module):
    return jsonify([*map(cour_serialize,Cour.query.filter_by(module_id = id_module).all())])


@app.route('/api/cours', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def create_cours():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        print(request_data['module_id'])
        add_cours(request_data)
        return {"add": "create successfully"}
    else:
        return jsonify([*map(cour_serialize, Cour.query.all())])


@app.route('/api/one_cours/<id_cours>')
@cross_origin(supports_credentials=True)
def getOneCours(id_cours):
    return cour_serialize(Cour.query.get(id_cours))


@app.route("/api/update_cours", methods=["POST"])
@cross_origin(supports_credentials=True)
def update_cours():
    request_data = json.loads(request.data)
    db.session.query(Cour).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()
    return {" 201 ": "create successfully"}


@app.route("/api/delete_cours/<id_cours>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_cours(id_cours):
    Cour.query.filter_by(id=id_cours).delete()
    db.session.commit()
    return {" 201 ": "create successfully"}


@app.route("/api/getEvaluationByCours/<id_cours>", methods=["GET"])
@cross_origin(supports_credentials=True)
def getEvaluatinByCours(id_cours):
    return jsonify([*map(evaluation_serialize,Evaluation.query.filter_by(cours_id = id_cours).all())])


@app.route('/api/evaluation', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def create_evaluation():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        add_evaluation(request_data)
        return {" 201 ": "create successfully"}
    else:
        return jsonify([*map(evaluation_serialize, Evaluation.query.all())])


@app.route('/api/one_evaluation/<id_evaluation>')
@cross_origin(supports_credentials=True)
def getOneEvaluation(id_evaluation):
    return evaluation_serializez(Evaluation.query.get(id_evaluation))


@app.route("/api/update_evaluation", methods=["POST"])
@cross_origin(supports_credentials=True)
def update_evaluation():
    request_data = json.loads(request.data)
    db.session.query(Evaluation).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()
    return {" 201 ": "create successfully"}


@app.route("/api/delete_evaluation/<id_evaluation>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_Evaluation(id_evaluation):
    Evaluation.query.filter_by(id=id_evaluation).delete()
    db.session.commit()
    return {" 201 ": "create successfully"}


@app.route("/api/getQuestionByEvaluation/<id_evaluation>", methods=["GET"])
@cross_origin(supports_credentials=True)
def getQuestionByEvalution(id_evaluation):
    return jsonify([*map(question_serialize,Question.query.filter_by(evaluation_id = id_evaluation).all())])


@app.route('/api/question', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def create_question():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        add_Question(request_data)
        return {" 201 ": "create successfully"}
    else:
        return jsonify([*map(question_serialize, Question.query.all())])


@app.route('/api/one_question/<id_question>')
@cross_origin(supports_credentials=True)
def getOneQuestion(id_question):
    return question_serializez(Question.query.get(id_question))


@app.route("/api/update_question", methods=["POST"])
@cross_origin(supports_credentials=True)
def update_question():
    request_data = json.loads(request.data)
    db.session.query(Question).filter_by(id=request_data["id"]).update(request_data)
    db.session.commit()
    return {" 201 ": "create successfully"}


@app.route("/api/delete_questions/<id_question>", methods=["DELETE"])
@cross_origin(supports_credentials=True)
def delete_Question(id_question):
    Question.query.filter_by(id=id_question).delete()
    db.session.commit()
    return {" 201 ": "create successfully"}


@app.route("/api/face", methods=["POST"])
@cross_origin(supports_credentials=True)
def face_compare():
    request_data = json.loads(request.data)
    image1 = request_data['image1']
    image2 = request_data['image2']
    face_ = face_base64(image1, image2)
    return {'face': face_}


@app.route("/api/emotion_image", methods=["POST"])
@cross_origin(supports_credentials=True)
def emotion_function():
    request_data = json.loads(request.data)
    image = request_data['image']
    global sess
    global graph
    with graph.as_default():
        set_session(sess)
        emotion_class.get_emotion_predict(image)
    return "access"

'''
@app.route("/api/get_level", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_level():
    y, n = emotion_class.get_level_evaluation()
    return {'level': n, 'emotion': y}
'''


@app.route("/api/get_level", methods=["POST"])
@cross_origin(supports_credentials=True)
def get_level():
    image = json.loads(request.data)['image1']
    import time
    t1 = time.time()
    global sess
    global graph
    with graph.as_default():
        set_session(sess)
        emotion_class.get_emotion_predict(image)

    y, n = emotion_class.get_level_evaluation()
    t2 = time.time()

    return {'level': n, 'emotion': y}


@app.route("/")
@cross_origin(supports_credentials=True)
def test():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
