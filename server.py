from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connect to the Free MySQL Database
db = mysql.connector.connect(
    host="sql305.infinityfree.com",
    user="if0_38619812",
    password="z34NQJXOcbY",
    database="if0_38619812_canteen_db"
)

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    cursor = db.cursor()
    sql = "INSERT INTO orders (name, item) VALUES (%s, %s)"
    cursor.execute(sql, (data['name'], data['item']))
    db.commit()
    
    # Notify Admin Panel (Real-Time)
    socketio.emit('new_order', {'name': data['name'], 'item': data['item']})

    return jsonify({"message": "Order placed successfully"}), 201

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
