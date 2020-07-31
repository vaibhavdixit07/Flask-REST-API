from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be blank")
    parse.add_argument('store_id',
            type=float,
            required=True,
            help="Every item needs store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'No item found!'}, 404

    def post(self, name):
        data = Item.parse.parse_args()
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exist'}, 400 # It is bad request code(401 is Unauthorized access)

        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured while inserting item'}, 500 #Internal server error as issue with some server
        return item.json(), 201 # Item created in storage code (202 is item accepted but it can be delayed to get stored)

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
            except:
                return {'message': 'An error occured while deleting item'}, 500
            return {'message': 'Item deleted successfully'}

        return {'message': f'No element with name {name} found'}, 404

    def put(self, name):
        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price'] # This is updating in query
            item.store_id = data['store_id']

        try:
            item.save_to_db() # It can perform both update and insert
        except:
            return {'message': 'An error occured while inserting/updating item'}, 500 #Internal server error as issue with some server
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
