from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str ,required=True, help='This field cannot be blank')
    parser.add_argument('password',type=str ,required=True, help='This field cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args()
        username_check = data['username'] and not data['username'].isspace()
        password_check = data['password'] and not data['password'].isspace()

        if username_check and password_check:
            if UserModel.find_by_username(data['username']):
                return {'message':'User already exist!'}, 400
            user = UserModel(**data)
            user.insert()
            return {'message': 'User has been created successfully'}, 201
        return {'message': 'Username / Password can\'t be empty'}, 400
