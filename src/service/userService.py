class UserService:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def get_all_user_names(self):
        """

        :return:
            All users in the DB
        """
        return [itr.user_name for itr in self.table.query.all()]

    def insert_user(self, user_name, first_name, last_name, email, password):
        """
        Insert a new user to Users table

        :param user_name: field user_name. Mandatory.
        :param password: password. Mandatory.
        :param first_name: first_name.
        :param last_name: last_name.
        :param email: email.

        :return:
            Nothing or throws exception if fails

        """
        user_row = self.table(
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            telegram_id=None)
        self.db.session.add(user_row)
        self.db.session.commit()

    def check_user(self, user_name):
        """
        Check if a given user is in DB or not

        :param user_name: User under check

        :return:
            True: The user is in DB
            False: The user is not in DB
        """
        if user_name in [itr.user_name for itr in self.table.query.all()]:
            return True
        return False

    def validate_user_login(self, user_name, password):
        """
        Check if the user&password are in DB

        :param user_name: User under check
        :param password: Password under check
        :return:
            User object with the user_name&password or None
        """
        return self.table.query.filter_by(user_name=user_name).filter_by(password=password).first()

    def get_all_users_with_telegram_id(self):
        """
        Returns all the users that are registered to the telegram bot service
        :return:
            List of users
        """
        users_list_full = [itr for itr in self.table.query.all()]
        users_list = []
        for user in users_list_full:
            if user.telegram_id:
                users_list.append(user)
        return users_list

    def get_telegram_id_list(self):
        """
        Same as <get_all_users_with_telegram_id> but returns a list of chat_id and not the user objects

        :return:
            List of chat_id's
        """
        users_list_full = self.get_all_users_with_telegram_id()
        users_telegram_id_list = [itr.telegram_id for itr in users_list_full]
        return users_telegram_id_list

    def get_user_name_by_chat_id(self, chat_id):
        """
        Returns a user_name of a user with the given chat_id

        :param chat_id: chat_id to fetch the user for

        :return:
            user_name of the user with chat_id
        """
        user = self.table.query.filter_by(telegram_id=int(chat_id)).first()
        return user.user_name

    def get_chat_id_by_user_name(self, user_name):
        """
        Returns a chat_id of a user with the given user_name

        :param user_name: user_name to fetch the user for

        :return:
            chat_id of the user with user_name
        """
        user = self.table.query.filter_by(user_name=str(user_name)).first()
        return user.telegram_id

    def insert_telegram_id(self, user_name, telegram_id):
        """
        Insert chat_id to a user object in DB
        Use this to register a user to the telegram-bot service

        :param user_name: User to register for the telegram service
        :param telegram_id: chat_id as in the telegram bot user metadata

        """
        print("user_name: " + user_name)
        print("telegram_id: " + telegram_id)
        user = self.table.query.filter_by(user_name=user_name).first()
        print("user.user_name: " + user.user_name)
        user.telegram_id = telegram_id
        self.db.session.commit()
