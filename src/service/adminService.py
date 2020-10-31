class AdminService:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def insert_system_admin_if_empty(self, user_name):
        """
        Making user_name the sys-admin if the system have no admin yet

        :param user_name: User to insert

        :return:
            1: The user is now sys-admin
            0: The table wasn't empty

        """
        if len(self.table.query.all()) == 0:
            print("The table Admin is empty")
            print("Inserting user_name: " + user_name + " As SYS-Admin")
            admin_row = self.table(user_name=user_name, id=str(0))
            self.db.session.add(admin_row)
            self.db.session.commit()
            return 1
        #
        # if self.table.query.filter_by(user_name=user_name).filter_by(id='0').first():
        #     return True
        return 0

    def is_user_system_admin(self, user_name):
        """
        Returns True/false if the user_name is a system admin

        :param user_name: User under check

        :return:
            True: The user is sys-admin
            False: The user is not sys-admin
        """
        if self.table.query.filter_by(user_name=user_name).filter_by(id='0').first():
            return True
        return False

    def get_group_admins(self, group_id):
        """

        :param group_id: group under check

        :return:
            List of user_names that are the admin for a given group
        """
        admins = [itr.user_name for itr in self.table.query.filter_by(id=str(group_id)).all()]
        admins += [itr.user_name for itr in self.table.query.filter_by(id='0').all()]
        admins = list(dict.fromkeys(admins))
        return admins

    def get_user_groups_with_admin_roles(self, user_name):
        """

        :param user_name: user_name to fetch the data for.

        :return:
            List of groups that the user is the group admin
        """
        return [itr.id for itr in self.table.query.filter_by(user_name=user_name).all()]

    def check_if_user_is_admin(self, user_name, group_id):
        """

        :param user_name: User under check
        :param group_id: Group under check

        :return:
            True: The user is an admin of group_id
            False: The user is not an admin of group_id
        """
        if self.is_user_system_admin(user_name):
            return True
        if self.table.query.filter_by(user_name=user_name).filter_by(id=str(group_id)).first():
            return True
        return False

    def check_if_user_is_admin_for_group_list(self, user_name, group_list):
        """
        Same as <check_if_user_is_admin> but with a list of groups
        Use this to check if a user is the admin of all the groups of a specific poll

        :param user_name: User under check
        :param group_list: Group list under check

        :return:
            True: The user is an admin of the groups list
            False: The user is not an admin of the groups list
        """
        if len(group_list) == 0:
            return True
        if self.is_user_system_admin(user_name):
            return True
        for itr in group_list.split('&'):
            print("user:" + user_name + ", Group: " + itr)
            if not self.check_if_user_is_admin(user_name, itr):
                print("False")
                return False
        print("True")
        return True
