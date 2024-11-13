from os import environ as env
import stripe
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stripe_keys = {
    "secret_key": env.get("STRIPE_SECRET_KEY"),
    "publishable_key": env.get("STRIPE_PUBLISHABLE_KEY")
}

#securely configures our secret key 
stripe.api_key = stripe_keys["secret_key"]

@app.route("/")
def index():
    return render_template("index.html")

#The client needs a public key to set up a secure connection,
#which it requests via this URL.
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

#When the client makes a purchase, the server needs to generate a Checkout Session ID,
#and send the ID back to the client
@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"] #secret key is sent automatically when we make a request to a new Checkout session

    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "T-shirt",
                        },
                        "unit_amount": 2000,  # Amount in cents
                    },
                    "quantity": 1,
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")

if __name__ == "__main__":
    app.run()