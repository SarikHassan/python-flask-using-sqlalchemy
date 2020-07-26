import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field can't be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name {} is already present".format(name)}, 400

        data = Item.parser.parse_args()
       # data = request.get_json()
       #  item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        # items.append(item)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting an item'}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()

        item = ItemModel.find_by_name(name)
        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
            item.save_to_db()
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

        # next(filter(lambda x: x['name'] == name, items), None)
        # updated_item = ItemModel(name, data['price'])

        # if item is None:
        #     try:
        #         updated_item.insert()
        #     except:
        #         return {'message': 'An error occurred inserting an item'}, 500
        # else:
        #     try:
        #         updated_item.update()
        #     except:
        #         return {'message': "An error occurred updating an item"}, 500
        # return updated_item.json()

    def delete(self, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        # return {'message': 'item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted'}


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1] })
        #
        # connection.close()
        # return {'items': items}
        return {'items': [item.json() for item in ItemModel.query.all()]}  #one way to use through list
        # return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))} Another way using labda function
