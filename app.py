from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB bağlantısı
client = MongoClient(os.getenv("MONGODB_URI"))
db = client['BOOKSTORE']
collection = db['bookstore']

# CRUD işlemleri
@app.route('/books', methods=['GET'])
def get_books():
    books = collection.find()
    return jsonify([book for book in books])

@app.route('/book', methods=['POST'])
def add_book():
    book = request.json
    collection.insert_one(book)
    return jsonify(book), 201

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = request.json
    collection.update_one({'_id': id}, {'$set': book})
    return jsonify(book)

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    collection.delete_one({'_id': id})
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
