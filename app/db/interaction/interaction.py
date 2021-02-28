from app.db.client.client import MySQLConnection
from app.db.exceptions import UserNotFoundException
from app.db.models.models import Base, User


class DbInteraction:
    def __init__(self, host, port, user, password, db_name, rebuild_db=False):
        self.mysql_connection = MySQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.engine = self.mysql_connection.connection.engine
        if rebuild_db:
            self.create_table_users()
            self.create_table_musical_compositions()

    def create_table_users(self):
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['users'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS users')
            Base.metadata.tables['users'].create(self.engine)

    def create_table_musical_compositions(self):
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['musical_compositions'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS musical_compositions')
            Base.metadata.tables['musical_compositions'].create(self.engine)

    def add_user_info(self, username, email, password):
        user = User(username=username, password=password, email=email)
        self.mysql_connection.session.add(user)
        return self.get_user_info(username, )

    def get_user_info(self, username):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            self.mysql_connectiofn.session.expire_all()
            return {'username': user.username, 'email': user.email, 'password': user.password}
        else:
            raise UserNotFoundException('User not found!')

    def edit_user_info(self, username, new_username=None, new_password=None, new_email=None):
        user = self.mysql_connection.session.query(User).filter_by(username=username).first()
        if user:
            if new_username is not None:
                user.username = new_username
            if new_password is not None:
                user.password = new_password
            if new_email is not None:
                user.email = new_email
            return self.get_user_info(username)
        else:
            raise UserNotFoundException('User not found.')
