class GroupUsersService:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def insert_users_to_group(self, users, group_id):
        """
        Insert A list of users with a group id to DB.

        :param users: List of users to be inserted
        :param group_id: Group of the users

        """
        for user in users:
            self.insert_user_to_group(user, group_id)

    def insert_user_to_group(self, user_name, group_id):
        """
        Same as <insert_users_to_group> but with a single user

        :param user_name: User to insert
        :param group_id: Group of the user

        """
        group_row = self.table(user_name=user_name, id=str(group_id))
        self.db.session.add(group_row)
        self.db.session.commit()

    # To get all users use users service
    def get_group_users(self, group_id):
        """
        Returns a list of users that are a member in a group

        :param group_id: The group to get the users for

        :return:
            A list of members in the group
        """
        if group_id == '0':
            print("WARN!!!!!")
            print("Called get_group_users with group 0")
            print("Try calling users service to get all users in system")
            return []
        return [itr.user_name for itr in self.table.query.filter_by(id=str(group_id)).all()]

    # def get_group_users_chat_id(self, group_id):
    #     """
    #     Returns a list of users that are a member in a group
    #
    #     :param group_id: The group to get the users chat_ids for
    #
    #     :return:
    #         A list of chat_ids of the members in the group
    #     """
    #     if group_id == '0':
    #         print("WARN!!!!!")
    #         print("Called get_group_users with group 0")
    #         print("Try calling users service to get all users in system")
    #         return []
    #     users_list = [itr.user_name for itr in self.table.query.filter_by(id=str(group_id)).all()]
    #
    #     return [itr.user_name for itr in self.table.query.filter_by(id=str(group_id)).all()]

    def get_user_groups(self, user_name):
        """
        Returns a list of groups that the user is a member of

        :param user_name: User to fetch the groups list for

        :return:
            List of groups the user is a member
        """
        return [itr.id for itr in self.table.query.filter_by(user_name=user_name).all()]
