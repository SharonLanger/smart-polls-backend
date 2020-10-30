from sqlalchemy import null


class AnswerService:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def insert_or_upsert_answer(self, poll_id, user_name):
        """
        Fetching a answer object from table.
        Used to check is the user answered the poll or not

        :param poll_id: Poll under check
        :param user_name: User under check

        :return:
            The answer of the user to the poll or 'None'
        """
        obj = self.table.query.filter_by(poll_id=int(poll_id), user_name=user_name).first()
        if obj is not None:
            return obj
        return None

    def insert_answer_new_answer(self, answer, poll_id, user_name):
        """
        Use this to insert new answer to Answer table.

        :param answer: Answer to insert to table
        :param poll_id: Poll of the answer
        :param user_name: User that answered

        """
        if user_name:
            obj = self.table()
            obj.user_name = user_name
            obj.answer = answer
            obj.poll_id = poll_id
            self.db.session.add(obj)
            self.db.session.commit()

    def insert_answer(self, answer, poll_id, user_name):
        """
        Insert an answer to table or updating an answer

        :param answer: Answer to insert to table
        :param poll_id: Poll of the answer
        :param user_name: User that answered

        """
        try:
            answer_obj = self.insert_or_upsert_answer(poll_id, user_name)
            if answer_obj:
                self.table.query.filter_by(poll_id=int(poll_id), user_name=user_name).update(dict(answer=answer))
            else:
                self.insert_answer_new_answer(answer, poll_id, user_name)
        except Exception as e:
            print(e)
            print("Answer is in table\nUpsert answer")
        self.db.session.commit()

    def get_users_by_answer(self, poll_id, answer):
        """
        Fetching the users that answered the same as <answer> to <poll_id>
        Use this to fetch users that will be added to a new group

        :param poll_id: Poll to get the users for
        :param answer: The answer of the poll to get the users for

        :return:
            A list of users
        """
        answers = self.table.query.filter_by(poll_id=int(poll_id)).filter_by(answer=str(answer)).all()
        users = [answer.user_name for answer in answers]
        return users

    def get_user_answer(self, user_name, poll_id):
        """
        Look for a user answer in Answers table

        :param user_name: User name to fetch the answer for
        :param poll_id: Poll to look the answer for
        :return:
            The answer of the user to the poll in table
            or an empty string
        """
        answer = self.table.query.filter_by(user_name=str(user_name)).filter_by(poll_id=str(poll_id)).first()
        if answer is None:
            return ''
        return answer.answer

    def get_users_answered_to_poll(self, poll_id):
        return [itr.user_name for itr in self.table.query.filter_by(poll_id=str(poll_id)).all()]




