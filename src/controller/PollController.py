from flask import make_response, request, jsonify
from flask import Blueprint


def PollController(service, user_service, answer_service, group_users_service):
    """

    :param service: Holds the service for 'Poll' schema
    :param user_service: Holds the service for 'User' schema
    :param answer_service: Holds the service for 'Answer' schema
    :param group_users_service: Holds the service for 'GroupUsers' schema

    """
    poll_controller = Blueprint('poll_controller', __name__)

    @poll_controller.route("/get_poll_data", methods=['GET'])
    def get_poll_data():
        """
        Returns the poll data in the format of google-charts:
            data={[['Task', 'Hours per Day'],['Work', 11],['Eat', 2],['Commute', 2],['Watch TV', 2],['Sleep', 7],]}

        :param poll_id: Poll to get the data for.

        :return:
            500: If couldn't fetch poll data
            200: If the poll data is fetched
        """
        try:
            poll_id = request.args.get('poll_id')
            poll_answers = answer_service.table.query.filter_by(poll_id=int(poll_id)).all()
            data = service.get_poll_data(poll_id, poll_answers)
        except Exception as e:
            print(e)
            return make_response(
                "Could not load poll data", 500)
        return make_response(data, 200)

    # data={[['Task', 'Hours per Day'],['Work', 11],['Eat', 2],['Commute', 2],['Watch TV', 2],['Sleep', 7],]}
    @poll_controller.route("/get_poll_options", methods=['GET'])
    def get_poll_options():
        """
        Returns the poll answering options
        Use this to get the answers that the user can choose from

        :param poll_id: Poll to get the options for.

        :return:
            500: If couldn't fetch poll options
            200: If the poll options is fetched
        """
        try:
            poll_id = request.args.get('poll_id')
            charts_columns = service.get_poll_options_service(poll_id)
            return make_response(jsonify(charts_columns), 200)
        except Exception as e:
            print("ERROR: in get_poll_options():")
            print(e)
            return make_response(
                "Could not load poll options", 500)

    @poll_controller.route("/send_poll", methods=['POST'])
    def send_poll():
        """
        Send the poll to the users that are registered to the telegram service

        :param poll_id: Poll to send

        :return:
            500: If couldn't send  poll
            200: If the poll is sent
        """
        try:
            poll_id = request.args.get('poll_id')
            poll = service.table.query.filter_by(id=poll_id).first()
            # List of users that didn't answered the poll
            poll_user_who_answered = answer_service.get_users_answered_to_poll(str(poll_id))
            print("poll_user_who_answered:")
            print(str(poll_user_who_answered))
            users_list = []
            if poll.groups_id == '0':
                poll_users_who_answered_chat_id = [user_service.get_chat_id_by_user_name(itr) for itr in poll_user_who_answered]
                users_list += list(set(user_service.get_telegram_id_list()) - set(poll_users_who_answered_chat_id))
            else:
                for poll_itr in service.get_poll_groups(poll.groups_id):
                    group_user_names_list = list(set(group_users_service.get_group_users(poll_itr)) - set(poll_user_who_answered))
                    # List of all users with chat_id
                    telegram_users = user_service.get_all_users_with_telegram_id()
                    users_list += [itr.telegram_id for itr in telegram_users if itr.user_name in group_user_names_list]
            users_list = list(dict.fromkeys(users_list))
            print('users_list:')
            print(str(users_list))
            service.send_poll_to_users(poll_id, users_list)
        except Exception as e:
            print("ERROR: in send_poll():")
            print(e)
            return make_response(
                "Failed to send poll:\n"
                "poll id: " + poll_id, 500)
        return make_response(
            "Send poll:\n"
            "poll id: " + poll_id, 200)

    @poll_controller.route("/get_poll_users", methods=['GET'])
    def get_poll_users():
        """
        Returns the poll users list base on the groups that the poll is created for
        Note: group=0 is the default group that holds all the system users

        :param poll_id: Poll to get the users list for.

        :return:
            500: If couldn't fetch poll users list
            200: If the poll users list fetched
        """
        try:
            poll_id = request.args.get('poll_id')
            poll = service.table.query.filter_by(id=poll_id).first()
            poll_group_list = service.get_poll_groups(poll.groups_id)
            if '0' in poll_group_list:
                return make_response(jsonify(user_service.get_all_user_names()), 200)
            poll_users = []
            for itr in poll_group_list:
                poll_users += group_users_service.get_group_users(itr)
            poll_users = list(dict.fromkeys(poll_users))
        except Exception as e:
            print(e)
            return make_response("", 500)
        return make_response(jsonify(poll_users), 200)

    @poll_controller.route("/get_user_polls", methods=['GET'])
    def get_user_polls():
        """
        Returns the user polls list base on the groups that the user is in and the groups that the poll is created for
        Returns in format of {id,poll_question}

        :param user_name: User to get the poll list for.

        :return:
            500: If couldn't fetch the user polls list
            200: If the user polls list is fetched
        """
        try:
            user_name = request.args.get('user_name')
            user_groups = group_users_service.get_user_groups(user_name)
            user_polls = []
            poll_list = service.table.query.all()
            for poll in poll_list:
                poll_groups_list = service.get_poll_groups(poll.groups_id)
                if '0' in poll_groups_list:
                    user_polls.append({
                        'id': poll.id,
                        'poll_question': poll.poll_question
                    })
                else:
                    for group in list(dict.fromkeys(poll_groups_list)):
                        print(group)
                        if group in user_groups:
                            user_polls.append({
                                'id': poll.id,
                                'poll_question': poll.poll_question
                            })
        except Exception as e:
            print(e)
            return make_response("", 500)
        user_polls_sorted = sorted([dict(t) for t in {tuple(sorted(d.items())) for d in user_polls}], key=lambda k: k['id'])
        return make_response(jsonify(user_polls_sorted), 200)

    return poll_controller
