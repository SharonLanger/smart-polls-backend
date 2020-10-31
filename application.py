from configparser import RawConfigParser
from flask import Flask, make_response
from flask_cors import CORS
from flask_rest_jsonapi import Api, ResourceList, ResourceDetail
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema

from src.controller.AdminController import AdminController
from src.controller.GroupController import GroupController
from src.controller.GroupUsersController import GroupUsersController
from src.controller.PollController import PollController
from src.controller.UserController import UserController
from src.controller.AnswerController import AnswerController

from src.service.adminService import AdminService
from src.service.answerService import AnswerService
from src.service.groupService import GroupService
from src.service.groupUsersService import GroupUsersService
from src.service.pollService import PollService
from src.service.userService import UserService

# Get profile properties
# ======================
config = RawConfigParser()
config.read('profile-dev.properties')

# ============================================
# ============================================

app = Flask(__name__)
CORS(app)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DatabaseSection', 'database.db_url')
db = SQLAlchemy(app)


# ==============================================================================
# ==============================================================================
# ==============================================================================

class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'user_one'
        self_view_kwargs = {'user_name': '<user_name>'}
        self_view_many = 'user_many'

    id = fields.Integer()
    # Telegram_id is the chat_id in the telegram-bot user metadata
    telegram_id = fields.Str()
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()


class User(db.Model):
    telegram_id = db.Column(db.String)
    user_name = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


class UserMany(ResourceList):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserOne(ResourceDetail):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


# ==============================================================================
# ==============================================================================
# ==============================================================================


class GroupSchema(Schema):
    class Meta:
        type_ = 'group'
        self_view = 'group_one'
        self_view_kwargs = {'group_id': '<group_id>'}
        self_view_many = 'group_many'

    id = fields.Str()
    group_id = fields.Str(required=True)
    poll_id = fields.Integer(required=True)
    name = fields.Str(required=True)


class Group(db.Model):
    # Convention: Group_id=<poll_id>:<answer>
    group_id = db.Column(db.String, primary_key=True)
    poll_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class GroupMany(ResourceList):
    schema = GroupSchema
    data_layer = {'session': db.session,
                  'model': Group}


class GroupOne(ResourceDetail):
    schema = GroupSchema
    data_layer = {'session': db.session,
                  'model': Group}


# ==============================================================================
# ==============================================================================
# ==============================================================================


class GroupUsersSchema(Schema):
    class Meta:
        type_ = 'group_users'
        self_view = 'group_users_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'group_users_many'

    # id=group_id
    # Convention: id=<poll_id>:<answer>
    id = fields.Str(required=True)
    user_name = fields.Str(required=True)


class GroupUsers(db.Model):
    # id=group_id
    # Convention: id=<poll_id>:<answer>
    id = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String, primary_key=True)


class GroupUsersMany(ResourceList):
    schema = GroupUsersSchema
    data_layer = {'session': db.session,
                  'model': GroupUsers}


class GroupUsersOne(ResourceDetail):
    schema = GroupUsersSchema
    data_layer = {'session': db.session,
                  'model': GroupUsers}


# ==============================================================================
# ==============================================================================
# ==============================================================================


class AnswerSchema(Schema):
    class Meta:
        type_ = 'answer'
        self_view = 'answer_one'
        self_view_kwargs = {'poll_id': '<poll_id>'}
        self_view_many = 'answer_many'

    id = fields.Integer()
    poll_id = fields.Integer(required=True)
    user_name = fields.Str(required=True)
    answer = fields.Str(required=True)


class Answer(db.Model):
    poll_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, primary_key=True)
    answer = db.Column(db.String)


class AnswerMany(ResourceList):
    schema = AnswerSchema
    data_layer = {'session': db.session,
                  'model': Answer}


class AnswerOne(ResourceDetail):
    schema = AnswerSchema
    data_layer = {'session': db.session,
                  'model': Answer}


# ==============================================================================
# ==============================================================================
# ==============================================================================


class PollSchema(Schema):
    class Meta:
        type_ = 'poll'
        self_view = 'poll_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'poll_many'

    id = fields.Integer()
    poll_question = fields.Str(required=True)
    # Format:
    # answer1&answer2&answer3&.......
    poll_answers = fields.Str(required=True)
    # Format:
    # group1&group2&group3&.....
    # group=0 is the group with all the users in the system
    groups_id = fields.Str(default='0')


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_question = db.Column(db.String)
    # Format:
    # answer1&answer2&answer3&.......
    poll_answers = db.Column(db.String)
    # Format:
    # group1&group2&group3&.....
    # group=0 is the group with all the users in the system
    groups_id = db.Column(db.String, default='0')


class PollMany(ResourceList):
    schema = PollSchema
    data_layer = {'session': db.session,
                  'model': Poll}


class PollOne(ResourceDetail):
    schema = PollSchema
    data_layer = {'session': db.session,
                  'model': Poll}


# ==============================================================================
# ==============================================================================
# ==============================================================================


class AdminSchema(Schema):
    class Meta:
        type_ = 'admin'
        self_view = 'admin_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'admin_many'

    # id=group_id
    # Convention: id=<poll_id>:<answer>
    id = fields.Str(required=True)
    user_name = fields.Str(required=True)


class Admin(db.Model):
    # id=group_id
    # Convention: id=<poll_id>:<answer>
    id = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String, primary_key=True)


class AdminMany(ResourceList):
    schema = AdminSchema
    data_layer = {'session': db.session,
                  'model': Admin}


class AdminOne(ResourceDetail):
    schema = AdminSchema
    data_layer = {'session': db.session,
                  'model': Admin}


# ==============================================================================
# ==============================================================================
# ==============================================================================


# Create the table
db.create_all()

api = Api(app)

api.route(PollMany, 'poll_many', '/poll/polls')
api.route(PollOne, 'poll_one', '/poll/polls/<int:id>')
api.route(UserMany, 'user_many', '/user/users')
api.route(UserOne, 'user_one', '/user/users/<string:user_name>')
api.route(AnswerMany, 'answer_many', '/answer/answers')
api.route(AnswerOne, 'answer_one', '/answer/answers/<int:poll_id>')
api.route(GroupMany, 'group_many', '/group/groups')
api.route(GroupOne, 'group_one', '/group/groups/<string:group_id>')
api.route(GroupUsersMany, 'group_users_many', '/group_users/group_users')
api.route(GroupUsersOne, 'group_users_one', '/group_users/group_users/<string:id>')
api.route(AdminMany, 'admin_many', '/admin/admins')
api.route(AdminOne, 'admin_one', '/admin/admins/<string:id>')


# If you need to drop all tables in db
@app.route("/reset_db", methods=['DELETE'])
def drop_db():
    db.drop_all('__all__')
    db.create_all()
    initDB()
    return make_response()


def initDB():
    # Add admin group to DB:
    try:
        admin_group = Group()
        admin_group.group_id = 0
        admin_group.poll_id = 0
        admin_group.name = 'ALL-SYS-USERS'
        db.session.add(admin_group)
        db.session.commit()
    except:
        return True


# main loop to run app in debug mode
if __name__ == '__main__':
    initDB()

    app.register_blueprint(UserController(
        UserService(db, User),
        AdminService(db, Admin)),
        url_prefix='/user')

    app.register_blueprint(PollController(
        PollService(db, Poll),
        UserService(db, User),
        AnswerService(db, Answer),
        GroupUsersService(db, GroupUsers)),
        url_prefix='/poll')

    app.register_blueprint(AnswerController(
        AnswerService(db, Answer),
        UserService(db, User)),
        url_prefix='/answer')

    app.register_blueprint(GroupController(
        GroupService(db, Group),
        AnswerService(db, Answer),
        GroupUsersService(db, GroupUsers)),
        url_prefix='/group')

    app.register_blueprint(AdminController(
        AdminService(db, Admin),
        GroupService(db, Group)),
        url_prefix='/admin')

    app.register_blueprint(GroupUsersController(
        GroupUsersService(db, GroupUsers),
        UserService(db, User)),
        url_prefix='/group_users')

    app.run(debug=True)
