from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_cors import CORS

from config import API_KEY
from mail import send_mail, connect_mail
from gsheets import add_to_google_sheets, connect_google_sheets
from encryption import Decrypt_File

app = Flask(__name__)
CORS(app)

bp = Blueprint('bp', __name__)


# Before Request
@bp.before_request
def before_request():
    # Check if argument api_key equal to API_KEY
    if request.args.get('api_key') != API_KEY:
        return 'Invalid API Key'


@bp.route('/api/v1/send', methods=['POST'])
def send():
    print('Received request...')

    # Get the request body
    data = request.get_json()
    accepted = data['accepted']
    numberOfGuests = data['numberOfGuests']
    selectedRoom = data['selectedRoom']
    guests = data['guests']

    # Mail contents
    subject = f"RSVP from {guests[0]['Name']} ({'Accepted' if accepted == 'Yes' else 'Declined'})"
    contents = [
        f"Accepted: {accepted}",
        f"Number of Guests: {numberOfGuests}",
        f"Selected Room: {selectedRoom}",
        "Guests:" + '\n' + '\n'.join([f"Name: {guest['Name']}, DateOfBirth: {guest['DateOfBirth']}, American Airlines #: {guest['AaId']}, E-Mail: {guest['Email']}" for guest in guests])
    ]

    # Send email
    smtp = connect_mail()
    send_mail(smtp, subject, '\n'.join(contents))

    Decrypt_File('service-account.bin', 'service-account.json')

    # Add to Google Sheets
    rows = [
        [accepted, numberOfGuests, selectedRoom, guest['Name'], guest['DateOfBirth'], guest['AaId'], guest['Email']] for guest in guests
    ]
    gsheets = connect_google_sheets()
    add_to_google_sheets(gsheets, rows)

    print('Request completed!')
    return 'Success'


app.register_blueprint(bp, url_prefix='/')


if __name__ == '__main__':
    app.run()