from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Since the React code sends JSON, we use get_json()
    data = request.get_json()
    email = data.get('user_email')
    
    if email:
        with open("emails.txt", "a") as f:
            f.write(email + "\n")
        # Return a JSON response so the React "isLoading" state can finish
        return jsonify({"message": "Success", "email": email}), 200
        
    return jsonify({"message": "Invalid email"}), 400

if __name__ == '__main__':
    app.run(debug=True)