from flask import Flask, request, jsonify
import pickle
from fuzzywuzzy import process

# Load the pre-trained model
with open('command_classifier.pkl', 'rb') as f:
    model = pickle.load(f)

# Predefined standard commands
COMMANDS = [
    "activate do not disturb",
    "deactivate do not disturb",
    "decline the call",
    "pick up the call",
    "play the music",
    "pause the music",
    "play the next song",
    "play the previous song",
    "increase the volume",
    "decrease the volume",
    "increase the brightness",
    "decrease the brightness",
    "start the vehicle",
    "stop the vehicle",
]

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Command Classifier API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input JSON
        data = request.get_json()
        user_input = data.get('command', '')

        if not user_input:
            return jsonify({'error': 'No command provided'}), 400

        # Predict with the model
        prediction = model.predict([user_input])[0]

        # Fuzzy matching fallback
        if prediction not in COMMANDS:
            prediction, _ = process.extractOne(user_input, COMMANDS)

        return jsonify({'command': prediction}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
