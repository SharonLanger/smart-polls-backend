from flask import json
from service.telegramService import send_poll_telegram


class PollService:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def get_poll_data(self, poll_id, poll_answers):
        """
        Returns the poll data in google-charts format

        :param poll_id: Poll to fetch the data for
        :param poll_answers: The list of options to answer to the poll
        :return:
            Poll data in google chart format
        """
        data = []
        data.clear()

        charts_columns = self.get_poll_options_service(poll_id)
        data.append(["column", "value"])
        print(str(charts_columns))
        answers = {k: 0 for k in charts_columns}
        print("answers:" + str(answers))
        print(str(poll_answers))
        for answer in poll_answers:
            print("answer.answer:" + str(answer.answer))
            answers[answer.answer] = answers[answer.answer] + 1
        for key in answers.keys():
            print("key:" + key)
            data.append([key, answers[key]])
        print("data:")
        print(data)
        return json.dumps(data)

    def send_poll_to_users(self, poll_id, users_list):
        """
        Sending a notification on the telegram bot to a list of users for a poll

        :param poll_id: Poll to send the notification for
        :param users_list: List of users to send the notification

        """
        poll = self.table.query.filter_by(id=poll_id).first()
        print(poll)
        for user in users_list:
            if user:
                print("Sending poll by telegram to chat_id: " + str(user))
                res = send_poll_telegram(poll_id, poll.poll_question, poll.poll_answers, user)
                print("response: " + str(res.status_code))

    def get_poll_options_service(self, poll_id):
        """

        :param poll_id:
        :return:
        """
        try:
            charts_columns = []
            poll_options = self.table.query.filter_by(id=int(poll_id)).first()
            # print("poll answers:")
            for i, option in enumerate(poll_options.poll_answers.split('&')):
                charts_columns.append(option)
                print("option " + str(i) + ": " + option)
        except Exception as e:
            print("Could not load poll options.\nPoll id:" + poll_id)
            print(e)
            return []
        print("Fetched poll options.\nPoll id:" + poll_id)
        return charts_columns

    def get_poll_groups(self, poll_groups):
        """

        :param poll_groups:
        :return:
        """
        poll_groups_list = []
        try:
            for i, group in enumerate(poll_groups.split('&')):
                poll_groups_list.append(group)
        except Exception as e:
            print("Could not get poll groups")
            print(e)
            return []
        return poll_groups_list
