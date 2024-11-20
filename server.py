from os import environ as env
import stripe
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# securely configures our secret key
stripe.api_key = env.get("STRIPE_SECRET_KEY")

products = [
    {
        "id": 0,
        "title": "Popcorn",
        "image": "/static/images/popcorn.jpg",
        "description": "Salty, savory, yum!",
        "price_per_ounce": 100,
    },
    {
        "id": 1,
        "title": "Assorted Gummies",
        "image": "/static/images/assorted_gummies.jpg",
        "description": "So sweet!",
        "price_per_ounce": 400,
    },
    {
        "id": 2,
        "title": "Mixed Nuts",
        "image": "/static/images/mixed_nuts.jpg",
        "description": "Salty, savory, yum!",
        "price_per_ounce": 300,
    }
]


@app.route("/products")
def get_products(jsonify=True):
    products = stripe.Product.list()
    for product in products.data:
        product["price"] = stripe.Price.retrieve(product["default_price"])
    if jsonify:
        return jsonify(products)
    else:
        return products


@app.route("/")
def index():
    return render_template("index.html", products=get_products(False))


@app.route("/tshirt")
def subscriptions():
    return render_template("tshirt.html")

# The client needs a public key to set up a secure connection,
# which it requests via this URL.


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": env.get("STRIPE_PUBLISHABLE_KEY")}
    return jsonify(stripe_config)

# When the client makes a purchase, the server needs to generate a Checkout
# Session ID,
# and send the ID back to the client


@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = env.get("DOMAIN_URL")
    # stripe.api_key = stripe_env["secret_key"] #secret key is sent
    # automatically when we make a request to a new Checkout session

    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url +
            "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    # this is the price id of the item being bought, which can be found on stripe dashboard
                    'price': 'price_1QKUUZGEAUaOFAvq840jfJuW',
                    'adjustable_quantity': {"enabled": True, "minimum": 1, "maximum": 10},
                    'quantity': 1,
                },
                {
                    'price': 'price_1QNJXRGEAUaOFAvqUDSMQpNr',
                    'quantity': 1,
                },
            ],
            allow_promotion_codes = True
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/update-snack-payment", methods=["POST"])
def update_snack_payment():
    data = request.json
    amount = 0
    products = get_products(False)
    for product in products:
        amount += int(data["product_amounts"][str(product["id"])]
                      ) * product["price"]["unit_amount"]

    intent = stripe.PaymentIntent.modify(
        data["payment_intent_id"],
        amount=amount
    )
    return jsonify(client_secret=intent.client_secret, amount=intent.amount)


@app.route("/create-snack-payment", methods=["POST"])
def create_snack_payment():
    data = request.json
    amount = 0
    products = get_products(False)
    for product in products:
        amount += int(data["product_amounts"][str(product["id"])]
                      ) * product["price"]["unit_amount"]

    if amount == 0:
        amount = 50
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )
    return jsonify(payment_intent_id=intent.id, client_secret=intent.client_secret, amount=intent.amount)


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")

# This endpoint allows our server to handle asynchronous events as they occur in our Stripe account


@app.route("/complete")
def complete():
    return render_template("complete.html")


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
