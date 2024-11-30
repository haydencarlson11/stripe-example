# Stripe Example + Tech Share
Need to collect money from your website users? Look no further than [Stripe](https://stripe.com)!

Stripe is a service that empowers developers to easily implement purchasing mechanics in their website.
In this tech share we will show how to implement the following featueres of Stripe:
1. Using the Stripe dashboard to manage a product catalog, coupons, etc.
2. Implementing a [Stripe Hosted Form](https://docs.stripe.com/payments/accept-a-payment?platform=web&ui=stripe-hosted) for your website.
3. How to use stripe-cli and webhooks to test and manage your stripe service.
4. How to use Stripe [Advanced Integrations](https://docs.stripe.com/payments/accept-a-payment?platform=web&ui=elements), an incredibly flexible way to integrate the payment process into your website.

View our tech-share here: [https://drive.google.com/file/d/10RPJA2DCMMUE25DGK7B2hECd4M5I-nde/view?usp=sharing](https://drive.google.com/file/d/10RPJA2DCMMUE25DGK7B2hECd4M5I-nde/view?usp=sharing)

## Setup
1. Create a [stripe account](https://dashboard.stripe.com/login).
2. `git clone https://github.com/haydencarlson11/stripe-example.git`
3. Create a `.env` file based on `.env.template`. (Use the api keys in your stripe dashboard)
4. `pipenv install` (Install [pipenv](https://pypi.org/project/pipenv/) if not installed)
5. `pipenv shell`
6. `flask --app server.py run`

## Where to learn more about stripe?
* [https://testdriven.io/blog/flask-stripe-tutorial/](https://testdriven.io/blog/flask-stripe-tutorial/) (A great blog that helped us develop our application)
* [Stripe Documentation](https://docs.stripe.com) (The stripe documentation has tutorials, guides, code examples, and of course code documentation.)

## Authors
This Stripe tech share was produced for CSCI5117 at the University of Minnesota in Fall 2024:
* [Ryan Sauers](https://github.com/r-sauers)
* [Hayden Carlson](https://github.com/haydencarlson11)
* [Evan Burgstrand](https://github.com/EBurkstrand)
* [Lucas Lund](https://github.com/llun2102)
