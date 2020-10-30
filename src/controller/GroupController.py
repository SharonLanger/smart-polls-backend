from flask import make_response, request
from flask import Blueprint


def GroupController(service, answer_service, group_users_service):
    """

    :param service: Holds the service for 'Group' schema
    :param answer_service: Holds the service for 'Answer' schema
    :param group_users_service: Holds the service for 'GroupUsers' schema

    """
    group_controller = Blueprint('group_controller', __name__)

    @group_controller.route("/make_group", methods=['POST'])
    def make_group():
        """
        Creating a group base on a poll&answer
        All users who answered the same answer to the poll will be added to the new group

        :param name: Name of the new group
        :param poll_id: The poll that the answers will greate the group
        :param answer: The answer of the poll which all users who answered will be joined to the group

        :return:
            500: If failed to crete group
            200: Group was created
        """
        try:
            poll_id = request.args.get('poll_id')
            answer = request.args.get('answer')
            name = request.args.get('name')
            group_id = poll_id + ":" + str(answer)
            service.create_new_group(group_id, poll_id, name)
            users = answer_service.get_users_by_answer(poll_id, answer)
            group_users_service.insert_users_to_group(users, group_id)
        except Exception as e:
            print("ERROR: in make_group():")
            print(e)

            return make_response(
                "Failed to make_group\n"
                "poll id: " + poll_id, 500)
        return make_response(
            "OK, in make_group:\n"
            "poll id: " + poll_id, 200)

    return group_controller
