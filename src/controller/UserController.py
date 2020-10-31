from flask import make_response, request, jsonify
from flask import Blueprint


def UserController(service, admin_service):
    """

    :param service: Holds the service for 'User' schema
    :param admin_service: Holds the service for 'Admin' schema

    """
    user_controller = Blueprint('user_controller', __name__)

    @user_controller.route("/login_user", methods=['GET'])
    def login_user():
        """
        Check if the user_name/password are a match.
        If so then returns the first and last name with status 200

        :param user_name: user_name to login
        :param password: The password of the user

        :return:
            501: If the user_name/password isn't correct
            500: Server/DB error
            200: User is logged in
        """
        try:
            user_name = request.args.get('user_name')
            password = request.args.get('password')
            user = service.validate_user_login(user_name, password)
            if not user:
                return make_response("Could not fetch user\nuser name or password is not correct", 501)
        except Exception as e:
            print(e)
            return make_response(
                "Could not fetch user\n"
                "user_name: " + user_name, 500)
        return make_response(jsonify(first_name=user.first_name, last_name=user.last_name), 200)

    @user_controller.route("/insert_telegram_id", methods=['PUT'])
    def insert_telegram_id():
        """
        Insert chat id to User table.
        Should be use when a user is registers to the service on the telegram bot

        :param user_name: user_name that is registering the service
        :param telegram_id: The chat_id of the user on telegram


        :return:
            500: If failed
            200: User is now registered to the telegram bot
        """
        try:
            user_name = request.args.get('user_name')
            telegram_id = request.args.get('telegram_id')
            service.insert_telegram_id(user_name, telegram_id)
        except Exception as e:
            print(e)
            return make_response(
                "Could not update user telegram id\n"
                "user_name: " + user_name + "\n"
                                            "telegram_id: " + str(telegram_id), 500)
        return make_response(
            "Update user telegram id\n"
            "user_name: " + user_name + "\n"
                                        "telegram_id: " + str(telegram_id), 200)

    @user_controller.route("/insert_user", methods=['POST'])
    def insert_user():
        """
        Insert new user to User table.
        Also, Checking if the user is the first user in the system before.
        If the user is the first one then the also adding him as a admin

        :param user_name: field user_name. Mandatory.
        :param password: password. Mandatory.
        :param first_name: first_name.
        :param last_name: last_name.
        :param email: email.

        :return:
            500: If failed
            200: User is now registered
            201: User is now registered and his is the sys admin
        """
        try:
            user_name = request.args.get('user_name')
            first_name = request.args.get('first_name')
            last_name = request.args.get('last_name')
            email = request.args.get('email')
            password = request.args.get('password')
            service.insert_user(
                user_name,
                first_name,
                last_name,
                email,
                password)
            is_sys_admin = admin_service.insert_system_admin_if_empty(user_name)
        except Exception as e:
            print(e)
            return make_response(
                "Could not insert user", 500)
        return make_response(
            "Insert new user to table\n"
            "user_name: " + user_name, 200 + is_sys_admin)

    return user_controller
