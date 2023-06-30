from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/likes_db'  # Replace with your MongoDB connection URI
mongo = PyMongo(app)


# 1. Store Like Event
@app.route('/likes', methods=['POST'])
def store_like():
    data = request.get_json()
    user_id = data.get('user_id')
    content_id = data.get('content_id')

    if not user_id or not content_id:
        return jsonify({'error': 'user_id and content_id are required'}), 400

    # Check if the user has already liked the content
    existing_like = mongo.db.likes.find_one({'user_id': user_id, 'content_id': content_id})
    if existing_like:
        return jsonify({'error': 'User has already liked the content'}), 400

    # Store the like event
    like = {'user_id': user_id, 'content_id': content_id}
    mongo.db.likes.insert_one(like)

    total_likes = count_likes(content_id)

    # Check if the user reached 100 likes and log a push notification (placeholder)
    if total_likes == 100:
        log_push_notification(user_id, content_id)

    return jsonify({'message': 'Like event stored successfully'}), 201


# 2. Check if user has liked a particular content
@app.route('/likes/check', methods=['GET'])
def check_like():
    user_id = request.args.get('user_id')
    content_id = request.args.get('content_id')

    if not user_id or not content_id:
        return jsonify({'error': 'user_id and content_id are required'}), 400

    liked = mongo.db.likes.find_one({'user_id': user_id, 'content_id': content_id})
    return jsonify({'liked': bool(liked)})


# 3. Total likes for a content
@app.route('/likes/total', methods=['GET'])
def total_likes():
    content_id = request.args.get('content_id')

    if not content_id:
        return jsonify({'error': 'content_id is required'}), 400

    total_likes = count_likes(content_id)
    return jsonify({'total_likes': total_likes})


# Helper functions

def count_likes(content_id):
    total_likes = mongo.db.likes.count_documents({'content_id': content_id})
    return total_likes


def log_push_notification(user_id, content_id):
    # Placeholder code to log push notification
    print(f"Push notification sent to user {user_id} for reaching 100 likes on content {content_id}")


if __name__ == '__main__':
    app.run()
