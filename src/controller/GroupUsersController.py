from flask import make_response, request, jsonify
from flask import Blueprint


def GroupUsersController(service, user_service):
    """

    :param service: Holds the service for 'GroupUsers' schema
    :param user_service: Holds the service for 'User' schema

    """
    group_users_controller = Blueprint('group_users_controller', __name__)

    @group_users_controller.route("/get_group_users", methods=['GET'])
    def get_group_users():
        """
        Returns a list of users in a group

        :param group_id: Group to get the users list for.

        :return:
            500: If couldn't fetch users list
            200: If the users list is fetched
        """
        try:
            group_id = request.args.get('group_id')
            if str(group_id) == '0':
                return make_response(jsonify(user_service.get_all_user_names()), 200)
            users = service.get_group_users(group_id)
            return make_response(jsonify(users), 200)
        except Exception as e:
            print("ERROR: in get_group_users():")
            print(e)
            return make_response(
                "Could not get group users", 500)

    @group_users_controller.route("/get_user_groups", methods=['GET'])
    def get_user_groups():
        """
        Returns a list of groups the user is a member of

        :param user_name: User to get the groups he's a member of

        :return:
            500: If couldn't fetch users list
            200: If the users list is fetched
        """
        try:
            user_name = request.args.get('user_name')
            groups = service.get_user_groups(user_name)
            return make_response(jsonify(groups), 200)
        except Exception as e:
            return make_response(
                "Could not fetch user groups", 500)

    return group_users_controller
