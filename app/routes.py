from flask import render_template, request, jsonify, flash
from app import app
from app import database as db_helper
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin


global search_pets
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(UID):
    uid = db_helper.get_user_id(UID)
    print(str(uid))
    return User(uid)

class User(UserMixin):

    def __init__(self, UID, authenticate = False):
        self.UID = UID
        self.auth = authenticate

    def to_json(self):
        return {"UID": self.UID}

    def is_authenticated(self):
        return self.auth

    def set_auth(self, input_pwd):
        self.auth = db_helper.authenticate(self.UID, input_pwd)

    def get_id(self):
        return str(self.UID)
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data["UID"]
    input_pwd = data["Password"]
    
    curr_user = User(user_id)
    try:
        curr_user.set_auth(input_pwd)
    except:
        return jsonify(curr_user.to_json())

    if login_user(curr_user):
        flash("Logged in!")

    return jsonify(curr_user.to_json())

@app.route("/logout", methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        flash("Logged out.")
        result = {'success': True, 'response': 'log out'}
    except:
        result = {'success': False, 'response': "log out err"}

    return jsonify(result)

@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    user_id = data["UID"]
    input_pwd = data["Password"]
    try:
        db_helper.signup_user(user_id, input_pwd)
        result = {'success': True, 'response': 'sign up success'}
    except:
        result = {'success': False, 'response': "err"}
    
    return jsonify(result)

@app.route("/delete/<int:pet_id>", methods=['POST'])
def delete(pet_id):
    try:
        db_helper.remove_pet_by_id(pet_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        err = str(pet_id)+ " error"
        result = {'success': False, 'response': err}

    return jsonify(result)


@app.route("/edit/<int:pet_id>", methods=['POST'])
def update(pet_id):
    data = request.get_json()
    print(data)

    if "pet_condition" in data:
        db_helper.update_condition_entry(pet_id, data["pet_condition"])
        result = {'success': True, 'response': 'Condition Updated'}
    else:
        result = {'success': True, 'response': 'Nothing Updated'}

    return jsonify(result)

@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    print(data)
    if data['pet_id'] == '':
        db_helper.insert_new_pre(data['pet_type'], data['pet_color'], data['pet_uid'])
        result = {'success': True, 'response': 'Done'}
        return jsonify(result)
    db_helper.insert_new_pet(data['pet_id'], data['pet_type'], data['pet_color'], data['pet_cond'], data['pet_uid'], data['pet_loc'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
    pets = db_helper.fetch_pet()
    tops = db_helper.fetch_top()
    return render_template("index.html", items=pets, items1=tops)

@app.route("/search", methods=['POST','GET'])
def search():
    data = request.get_json()
    global search_pets
    global search_pets_
    try:
        search_pets = db_helper.search_pet(data["search_id"])
        search_pets_ = db_helper.search_pet_(data["search_id"])
        result = {'success': True, 'response': 'successful searched'}
    except:
        result = {'success': True, 'response': 'search failed'}
    return render_template("search_result.html", items=search_pets, items1=search_pets_)

@app.route("/match", methods=['POST','GET'])
def match():
    global pre
    global favor
    global match
    data = request.get_json()
    if current_user.get_id() != None:
        try:
            pre,favor,match = db_helper.match_pet(int(current_user.get_id()),data["fav"])
            result = {'success': True, 'response': 'successful searched'}
        except:
            result = {'success': True, 'response': 'search failed'}
        return render_template("match_result.html", items=pre, items1=favor, items2=match)
    
    try:
        pre,favor,match = db_helper.match_pet(data["search_id"],data["fav"])
        result = {'success': True, 'response': 'successful searched'}
    except:
        result = {'success': True, 'response': 'search failed'}
    return render_template("match_result.html", items=pre, items1=favor, items2=match)
