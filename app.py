import os
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_sheet():
    """Connects to Google Sheets using credentials from environment variables."""
    try:
        json_creds = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
        if not json_creds:
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable not found.")
            
        service_account_info = json.loads(json_creds)
        
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        client = gspread.authorize(credentials)
        
        # Using your specific Sheet ID for reliability
        return client.open_by_key("1fej397TsJUy5vd7QDxhDvCh2BDrBeCx5G2SNZ7YaX9o").sheet1
    except Exception as e:
        print(f"FAILED TO CONNECT TO SHEET: {e}")
        raise e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('user_email')
    
    # Get current timestamp in a clean format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"DEBUG: Received subscription attempt for: {email}")

    if email:
        try:
            sheet = get_sheet()
            
            # append_row is more efficient than finding row + update_cell
            # It automatically finds the first empty row for you.
            # We are saving both the email and the time they joined.
            sheet.append_row([email, timestamp])
            
            print(f"DEBUG: Successfully added {email} at {timestamp}")
            return jsonify({"message": "Success"}), 200
            
        except Exception as e:
            print(f"SERVER ERROR: {e}")
            return jsonify({"message": "Internal server error"}), 500
            
    return jsonify({"message": "Invalid email address"}), 400

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
