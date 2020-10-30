class GroupService:
    def __init__(self, db, table):
        self.db = db
        self.table = table

    def create_new_group(self, group_id, poll_id, name):
        """
        Create a new group in DB

        :param group_id: The group to add
        :param poll_id: Base on that poll the group was created
        :param name: The nice name of the group

        """
        obj = self.table()
        obj.group_id = str(group_id)
        obj.poll_id = poll_id
        obj.name = name
        self.db.session.add(obj)
        self.db.session.commit()

    def get_group_name(self, group_id):
        """
        Return a group nice name

        :param group_id: The group to fetch the name for

        :return:
            The group name
        """
        group = self.table.query.filter_by(group_id=group_id).first()
        return group.name


