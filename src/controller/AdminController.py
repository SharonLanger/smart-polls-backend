from flask import make_response, request, jsonify
from flask import Blueprint


def AdminController(service, group_service):
    """

    :param service: Holds the service for 'Admin' schema
    :param group_service: Holds the service for 'Group' schema

    """
    admin_controller = Blueprint('admin_controller', __name__)

    @admin_controller.route("/get_group_admins", methods=['GET'])
    def get_group_admins():
        """
        :param group_id: Id of the group

        :return:
            List of users that are admins for param 'group_id'
            Or 500 for error
        """
        try:
            group_id = request.args.get('group_id')
            users_admin = service.get_group_admins(group_id)
        except Exception as e:
            print(e)
            return make_response("", 500)
        return make_response(jsonify(users_admin), 200)

    @admin_controller.route("/get_user_admin_groups", methods=['GET'])
    def get_user_admin_groups():
        """
        :param user_name: The user_name to get the results for

        :return:
            List of groups that the user is the admin
            Or 500 for error
        """
        try:
            user_name = request.args.get('user_name')
            group_id_list = service.get_user_groups_with_admin_roles(user_name)
            if '0' in group_id_list:
                group_id_list = [itr.group_id for itr in group_service.table.query.all()]
            print("group_id_list: " + str(group_id_list))
            groups_list = []
            for group in group_id_list:
                groups_list.append({
                    'id': group,
                    'name': group_service.get_group_name(group)
                })
        except Exception as e:
            print(e)
            return make_response("", 500)
        print("groups_list: " + str(groups_list))
        return make_response(jsonify(groups_list), 200)

    @admin_controller.route("/is_user_name_admin_for_group", methods=['GET'])
    def is_user_name_admin_for_group():
        """
        :param user_name: User to check
        :param group_id: Group to check is user is admin

        :return:
            True: If the user_name is the admin of group_id
            False: Otherwise
        """
        try:
            user_name = request.args.get('user_name')
            group_id = request.args.get('group_id')
            return make_response(jsonify(service.check_if_user_is_admin(user_name, group_id)), 200)
        except Exception as e:
            print(e)
            return make_response("", 500)

    return admin_controller
