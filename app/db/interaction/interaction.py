import re

from app.db.client.client import PostgreSQLConnection
from app.db.exceptions import UserNotFoundException, UsernameAlreadyExistsException, EmailAlreadyExistsException
from app.db.models.models import Base, User, MusicalComposition
from flask import jsonify
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


class DbInteraction:
    def __init__(self, host: str, port: int, user: str, password: str, db_name: str, rebuild_db: bool = False):
        self.postgresql_connection = PostgreSQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )
        self.engine = self.postgresql_connection.connection.engine

        if rebuild_db:
            Base.metadata.drop_all(self.engine)
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['users'].create(self.engine)
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['musical_compositions'].create(self.engine)

    def create_table_users(self) -> None:
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['users'].create(self.engine)

    def create_table_musical_compositions(self) -> None:
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['musical_compositions'].create(self.engine)

    def add_user_info(self, username: str, email: str, password: str) -> dict[str, str]:
        try:
            user = User(username=username, password=password, email=email)
            self.postgresql_connection.session.add(user)
            return self.get_user_info(username)
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            key_name = re.search('\((\w*)\)', e.args[0].split('\n')[1]).group(1)
            if key_name == 'email':
                raise EmailAlreadyExistsException from e
            if key_name == 'username':
                raise UsernameAlreadyExistsException from e

    def get_user_info(self, username: str) -> dict[str, str]:
        user = self.postgresql_connection.session.query(User).filter_by(username=username).first()
        if user:
            self.postgresql_connection.session.expire_all()
            return {'username': user.username, 'email': user.email, 'password': user.password}
        else:
            raise UserNotFoundException('User not found!')

    def edit_user_info(self, username: str, new_username: str = None, new_password: str = None,
                       new_email: str = None) -> dict[str, str]:
        user = self.postgresql_connection.session.query(User).filter_by(username=username).first()
        if user:
            if new_username is not None:
                user.username = new_username
            if new_password is not None:
                user.password = new_password
            if new_email is not None:
                user.email = new_email
            return self.get_user_info(username if new_username is None else new_username)
        else:
            raise UserNotFoundException('User not found.')

    def delete_user_info(self, username: str) -> None:
        user = self.postgresql_connection.session.query(User).filter_by(username=username).first()
        if user:
            self.postgresql_connection.session.delete(user)
        else:
            raise UserNotFoundException('User not found.')

    def get_all_users(self) -> str:
        users = self.postgresql_connection.session.query(User).all()
        return jsonify(users)

    def get_musical_composition_info(self) -> None:
        pass

    def list_all_musical_compositions(self) -> str:
        musical_compositions = self.postgresql_connection.session.query(MusicalComposition).all()
        return jsonify(musical_compositions)
