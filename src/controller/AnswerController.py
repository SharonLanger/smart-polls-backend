from flask import make_response, request
from flask import Blueprint
from joblib.testing import param


def AnswerController(service, user_service):
    """

    :param service: Holds the service for 'Answer' schema
    :param user_service: Holds the service for 'User' schema

    """
    answer_controller = Blueprint('answer_controller', __name__)

    @answer_controller.route("/insert_answer_from_telegram", methods=['POST'])
    def insert_answer_from_telegram():
        """
        Endpoint for the telegram bot.
        To be used by the telegram bot after user is registered to the service in the bot

        :param chat_id: Telegram chat id of the user answering the poll. The chat id will be replaced by a user_name
        :param answer: Answer to insert
        :param poll_id: Poll answered by user

        :return:
            200: If answer was inserted
            501: If the chat id isn't in User table.
            500: Any other error

        """
        try:
            chat_id = request.args.get('chat_id')
            answer = request.args.get('answer')
            poll_id = request.args.get('poll_id')
            user_name = user_service.get_user_name_by_chat_id(chat_id)
            if user_service.check_user(user_name):
                service.insert_answer(answer, poll_id, user_name)
            else:
                return make_response("Could not find user_name", 501)

        except Exception as e:
            print(e)
            return make_response("Could not insert answer", 500)
        return make_response(
            "Insert answer\n" +
            "\nPoll id:" + str(poll_id) +
            "\nUser name:" + str(user_name) +
            "\nAnswer:" + str(answer), 200)

    @answer_controller.route("/insert_answer", methods=['POST'])
    def insert_answer():
        """
        Same as <insert_answer_from_telegram> but with user_name instead of chat_id
        To be used by the UI microservice

        :param user_name: User that is answering the poll
        :param answer: Answer to insert
        :param poll_id: Poll answered by user

        :return:
            200: If answer was inserted
            501: If the chat id isn't in User table.
            500: Any other error
        """
        try:
            answer = request.args.get('answer')
            poll_id = request.args.get('poll_id')
            user_name = request.args.get('user_name')
            if user_service.check_user(user_name):
                service.insert_answer(answer, poll_id, user_name)
            else:
                return make_response("Could not find user_name", 501)

        except Exception as e:
            print(e)
            return make_response("Could not insert answer", 500)
        return make_response(
            "Insert answer\n" +
            "\nPoll id:" + str(poll_id) +
            "\nUser name:" + str(user_name) +
            "\nAnswer:" + str(answer), 200)

    @answer_controller.route("/get_user_answer_to_poll", methods=['GET'])
    def get_user_answer_to_poll():
        """
        Gets the user answer to a poll

        :param user_name: User that answered the poll
        :param poll_id: Poll to look the answer for

        :return:
            200: If the answer was found
            204: If the answer wasn't found
            500: Error
        """
        try:
            poll_id = request.args.get('poll_id')
            user_name = request.args.get('user_name')
            answer = service.get_user_answer(user_name, poll_id)
            if answer == '':
                return make_response(answer, 204)
            return make_response(str(answer), 200)

        except Exception as e:
            print(e)
            return make_response("Failed while fetching the answer", 500)

    return answer_controller
