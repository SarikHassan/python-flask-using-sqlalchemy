import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help="This field can't be left blank")
    parser.add_argument('password', required=True, type=str, help="This field can't be left blank")

    def post(self):
        data = RegisterUser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "An user with this username is already exist"}, 400

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES(NULL, ?,?)"
        # cursor.execute(query, (data['username'], data['password']))
        #
        # connection.commit()
        # connection.close()
        user = UserModel(**data)
        user.save_to_db()

        return {"message": " user created successfully"}, 201
