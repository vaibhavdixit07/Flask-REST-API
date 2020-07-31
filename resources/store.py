from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store with name {name} already exist'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured while inserting into store'}, 500 #Internal server error as issue with some server

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'An error occured while deleting store'}, 500
            return {'message': 'Item deleted successfully'}

        return {'message': f'No store with name {name} found'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.query.all()]}
