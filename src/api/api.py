from flask import Flask, request
from simplejson import dumps

from ..controller import PreferenceController

app = Flask(__name__)


@app.route('/preferences/<user_id>')
def get_user_preferences(user_id):
    preferences = PreferenceController.get_user_preferences(user_id)

    return dumps(preferences)


@app.route('/preferences', methods=['POST'])
def add_user_preference():
    if request.method == 'POST':
        data = request.form

        return PreferenceController.add_user_preference(
            data['user_id'],
            data['items_string'],
            data['rating']
        )

    return False

