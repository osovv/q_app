import threading
import argparse

from werkzeug.exceptions import abort

from app.api.utils import config_parser
from flask import Flask, request, jsonify

from app.db.exceptions import UserNotFoundException, UserAlreadyExistsException
from app.db.interaction.interaction import DbInteraction


class Server:
    def __init__(self, host: str, port: int, db_host: str, db_port: int, user: str, password: str, db_name: str,
                 rebuild_db: bool = False):
        self.host = host
        self.port = port

        self.db_interaction = DbInteraction(
            host=db_host,
            port=db_port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.app = Flask(__name__)
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})

        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/user/<username>', view_func=self.get_user, methods=['GET'])
        self.app.add_url_rule('/users', view_func=self.add_user_info, methods=['POST'])
        self.app.add_url_rule('/user/<username>', view_func=self.update_user, methods=['PUT'])
        self.app.add_url_rule('/user/<username>', view_func=self.delete_user, methods=['DELETE'])
        self.app.add_url_rule('/users', view_func=self.get_users, methods=['GET'])
        self.app.register_error_handler(404, self.page_not_found)

    @staticmethod
    def page_not_found(error_description: str) -> tuple[str, int]:
        return jsonify(error=str(error_description)), 404

    @staticmethod
    def shutdown() -> None:
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()

    @staticmethod
    def get_home() -> str:
        return 'Hello, api server.'

    def run(self) -> threading.Thread:
        self.server.start()
        return self.server

    def shutdown_server(self) -> None:
        request.get(f'http://{self.host}:{self.port}/shutdown')

    def add_user_info(self) -> tuple[str, int]:
        request_body = dict(request.json)
        username = request_body.get('username', None)
        password = request_body.get('password', None)
        email = request_body.get('email', None)
        try:
            self.db_interaction.add_user_info(
                username=username,
                password=password,
                email=email
            )
            return f'Successfully added {username}', 201
        except UserAlreadyExistsException:
            return f'User {username} already exists.', 403

    def get_user(self, username: str) -> tuple[dict[str, str], int]:
        try:
            user_info = self.db_interaction.get_user_info(username)
            return user_info, 200
        except UserNotFoundException:
            abort(404, description='User not found')

    def update_user(self, username: str) -> tuple[str, int]:
        request_body = dict(request.json)
        new_username = request_body.get('username', None)
        new_password = request_body.get('password', None)
        new_email = request_body.get('email', None)
        try:
            self.db_interaction.edit_user_info(
                username=username,
                new_username=new_username,
                new_password=new_password,
                new_email=new_email
            )
            return f'Successfully edited {username}', 200
        except UserNotFoundException:
            abort(404, description='User not found')

    def delete_user(self, username: str) -> tuple[str, int]:
        try:
            self.db_interaction.delete_user_info(username)
            return f'Successfully deleted {username}', 200
        except UserNotFoundException:
            abort(404, description='User not found')

    def get_users(self):
        return self.db_interaction.get_all_users(), 200


if __name__ == 'app.api.server':
    server = Server(
        host='0.0.0.0',
        port=5501,
        db_host='0.0.0.0',
        db_port=5432,
        user='tests',
        password='tests',
        db_name='flask_app_tests_db',
        rebuild_db=True
    )
    test_client = server.app.test_client()
    server.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')

    args = parser.parse_args()

    config = config_parser(args.config)
    SERVER_HOST = config['SERVER_HOST']
    SERVER_PORT = int(config['SERVER_PORT'])
    DB_HOST = config['DB_HOST']
    DB_PORT = int(config['DB_PORT'])
    DB_USER = config['DB_USER']
    DB_PASSWORD = config['DB_PASSWORD']
    DB_NAME = config['DB_NAME']

    server = Server(
        host=SERVER_HOST,
        port=SERVER_PORT,
        db_host=DB_HOST,
        db_port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db_name=DB_NAME,
    )
    server.run()
