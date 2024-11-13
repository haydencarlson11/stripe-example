from os import environ as env
import stripe
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

#securely configures our secret key 
stripe.api_key = env.get("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

#The client needs a public key to set up a secure connection,
#which it requests via this URL.
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": env.get("STRIPE_PUBLISHABLE_KEY")}
    return jsonify(stripe_config)

#When the client makes a purchase, the server needs to generate a Checkout Session ID,
#and send the ID back to the client
@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = env.get("DOMAIN_URL")
    # stripe.api_key = stripe_env["secret_key"] #secret key is sent automatically when we make a request to a new Checkout session

    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[ 
                {
                    'price': 'price_1QKUUZGEAUaOFAvq840jfJuW', #this is the price id of the item being bought, which can be found on stripe dashboard
                    'quantity': 1,
                },
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

#This endpoint allows our server to handle asynchronous events as they occur in our Stripe account
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, env.get("STRIPE_ENDPOINT_SECRET")
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle different events
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
    elif event["type"] == "charge.dispute.created":
        print("Customer is disupting the charge")
    elif event["type"] == "charge.succeeded":
        print("We sold something!")
    else:
        print(f"unhandled event type {event['type']}")

    return "Success", 200

if __name__ == "__main__":
    app.run()