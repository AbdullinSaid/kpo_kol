import sqlite3
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import re

app = Flask(__name__)
api = Api(app).default_namespace

current_cart = {}

cart_book_model = api.model('cart model', {
    'id': fields.Integer(description='user if', required=True),
    'number': fields.Integer(description='number of books', required=True)
})

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


@api.route('/books')
class Books(Resource):
    def get(self):
        connection = get_db_connection()
        books = connection.execute('SELECT * FROM books').fetchall()
        connection.close()
        print(books)
        result = []
        for book in books:
            result.append({'id': book['id'], 'name': book['name'],
                           'author': book['author'], 'genre': book['genre'],
                           'price': book['price'], 'number_in_shop': book['number']})
        resp = jsonify(result)
        resp.status_code = 200
        return resp


@api.route('/books/<int:id>')
class Book(Resource):
    def get(self, id):
        connection = get_db_connection()
        book = connection.execute(f'SELECT * FROM books WHERE id IN ({id})').fetchone()
        connection.close()
        if not book:
            resp = jsonify('message: no book with such id')
            resp.status_code = 404
            return resp
        result = {'id': book['id'], 'name': book['name'],
                  'author': book['author'], 'genre': book['genre'],
                  'price': book['price'], 'number_in_shop': book['number']}
        resp = jsonify(result)
        resp.status_code = 200
        return resp


@api.route('/cart')
class Cart(Resource):
    @api.doc(body=cart_book_model)
    def post(self):
        connection = get_db_connection()
        id = request.json['id']
        book = connection.execute(f'SELECT * FROM books WHERE id IN ({id})').fetchone()
        if not book:
            resp = jsonify('message: no book with such id')
            resp.status_code = 404
            return resp
        if request.json['number'] < 1:
            resp = jsonify('message: zero or less books')
            resp.status_code = 401
            return resp
        if request.json['number'] > book['number']:
            resp = jsonify('message: too much books')
            resp.status_code = 401
            return resp
        if not current_cart.get(id):
            current_cart[id] = 0
        current_cart[id] += request.json['number']
        new_number = book['number'] - request.json['number']
        connection.execute(f'UPDATE books SET number={new_number} WHERE id IN ({id})')
        connection.commit()
        connection.close()
        resp = jsonify('added to cart')
        resp.status_code = 200
        return resp


@api.route('/orders')
class Orders(Resource):
    def post(self):
        total_price = 0
        connection = get_db_connection()
        for key, value in current_cart.items():
            book = connection.execute(f'SELECT * FROM books WHERE id IN ({key})').fetchone()
            total_price += book['price'] * value
        current_cart.clear()
        resp = jsonify(f'Total price is {total_price}')
        resp.status_code = 200
        return resp


if __name__ == '__main__':
    app.run(debug=True)
