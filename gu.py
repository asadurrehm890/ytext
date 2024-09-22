import os
from flask import Flask, request, jsonify, session
from flask_session import Session
from youtube_transcript_api import YouTubeTranscriptApi
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.getenv('SECRET_KEY')  # Use the secret key from .env
Session(app)

# Get user data from environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')



# Hash the password for storage
users = {
    'user1': generate_password_hash(password)
}

@app.route('/login', methods=['POST'])
def login():
    input_username = request.json.get('username')
    input_password = request.json.get('password')

    if input_username in users and check_password_hash(users[input_username], input_password):
        session['username'] = input_username
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/transcript', methods=['GET'])
def get_transcript():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access'}), 403

    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'No video_id provided'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)

    except Exception as e:
        return jsonify({'error': f'Failed to fetch transcript: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
