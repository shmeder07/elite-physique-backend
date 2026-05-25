from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
# This allows your HTML file to talk to this server
CORS(app) 

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        # 1. Get the price and plan name from your front-end button
        client_data = request.json
        amount = client_data.get('amount')
        description = client_data.get('description')

        # 2. Build the Form Data dictionary for Belize Bank V2
        payment_data = {
            "userName": "BBL_Test_126-api", 
            "password": "BBLecomm2026!@", # <-- Put your password back here!
            "amount": amount,
            "currency": "840", # 840 is USD
            "orderNumber": f"FIT-V2-{int(time.time())}", 
            "returnUrl": "https://elite-physique-backend.onrender.com/success",
            "description": description
        }

        print(f"Sending request to Bank for {description}...")

        # 3. Send the POST request to the Bank as Form Data
        gateway_url = "https://sandbox.belizebank.com/payment/rest/register.do"
        response = requests.post(gateway_url, data=payment_data)
        bank_response = response.json() 

        print("Bank Response:", bank_response)

        # 4. Check if we got the green light (an orderId)
        if 'orderId' in bank_response:
            print("✅ Success! Redirect Link Generated.")
            return jsonify({
                "success": True, 
                "redirectUrl": bank_response['formUrl']
            })
        else:
            print(f"❌ Bank Error: {bank_response.get('errorMessage')}")
            return jsonify({
                "success": False, 
                "message": bank_response.get('errorMessage')
            }), 400

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"success": False, "message": "Internal Server Error"}), 500

# ---------------------------------------------------------
# THE NEW SUCCESS PAGE ROUTE
# ---------------------------------------------------------
@app.route('/success', methods=['GET'])
def success():
    # When the client clicks "Return to Merchant", they land here!
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Welcome to Elite Physique</title>
        <style>
            body {
                background-color: #0f172a;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                padding-top: 100px;
                line-height: 1.6;
            }
            h1 { color: #00f2fe; font-size: 3.5rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: #1e293b;
                padding: 50px;
                border-radius: 20px;
                border: 1px solid #334155;
                box-shadow: 0 20px 40px rgba(0, 242, 254, 0.1);
            }
            p { font-size: 1.1rem; color: #94a3b8; }
            .btn {
                display: inline-block;
                background: linear-gradient(to right, #00f2fe, #4facfe);
                color: #0f172a;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 30px;
                transition: transform 0.2s ease;
            }
            .btn:hover { transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Payment Successful!</h1>
            <p style="color: #00f2fe; font-weight: 600;">Welcome to the Elite Physique team.</p>
            <p>Your transaction has been securely processed. I will be reviewing your details and will send your personalized onboarding packet to your email shortly.</p>
            <p>Get ready to work.</p>
            <a href="https://startling-biscuit-0a56c0.netlify.app/" class="btn">Back to Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("-----------------------------------")
    print("Python V2 Gateway Server Running!")
    print("Port: 5000")
    print("-----------------------------------")
    app.run(port=5000, debug=True)