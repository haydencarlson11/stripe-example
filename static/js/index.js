document.addEventListener("DOMContentLoaded", function () {
  //Immediately get the Stripe publishable key
  fetch("/config")
    .then((result) => {
      return result.json();
    })
    .then(init);
});

function init(data) {
  //Initialize Stripe.js. Script containing Stripe class is included in base.html
  const stripe = Stripe(data.publicKey);

  stripeHostedInit(stripe); // sets up stripe hosted form
  embededInit(stripe); // sets up embeded form
}

function stripeHostedInit(stripe) {
  // Event handler
  document.querySelector("#hosted-form").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session")
      .then((result) => {
        return result.json();
      })
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({ sessionId: data.sessionId });
      })
      .then((res) => {
        console.log(res);
      });
  });
}









var g_elements;
var g_payment_intent_id;

// retrieves product quantities from webpage
function getProductAmounts() {
  let body = {
    product_amounts: {},
  };
  let els = document.querySelectorAll(".snack-product-qty");
  for (el of els) {
    body["product_amounts"][el.attributes["product_id"].value] = el.value;
  }
  return body;
}

// updates page to display purchase amount
function displayPurchaseAmount(amount) {
  document.getElementById("payment-amount").innerText =
    "$" + parseInt(amount / 100).toFixed(2);
}

// creates payment for selected products
function generatePaymentForm(stripe) {
  fetch("/create-snack-payment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(getProductAmounts()),
  })
    .then((result) => result.json())
    .then((data) => {
      g_payment_intent_id = data.payment_intent_id;
      clientSecret = data.client_secret;
      amount = data.amount;

      const options = {
        clientSecret: clientSecret,
        // Fully customizable with appearance API.
        appearance: {
          theme: "night",
          labels: "floating",
        },
      };

      // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in a previous step
      g_elements = stripe.elements(options);

      // Create and mount the Payment Element
      const paymentElement = g_elements.create("payment");
      paymentElement.mount("#payment-element");

      // Create an Address Element for shipping
      const addressElement = g_elements.create("address", {
        mode: "shipping",
      });
      addressElement.mount("#address-element");
      addressElement.on("change", (event) => {
        if (event.complete) {
          console.log(event.value.address);
        }
      });

      displayPurchaseAmount(amount);
    });
}

// updates payment to reflect selected products
function updatePaymentForm(stripe) {
  data = getProductAmounts();
  data["payment_intent_id"] = g_payment_intent_id;
  fetch("/update-snack-payment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((result) => result.json())
    .then((data) => displayPurchaseAmount(data.amount));
}

// initializes event handlers for embedded form
function embededInit(stripe) {
  // set up handlers for quantity changes
  let els = document.querySelectorAll(".snack-product-qty");
  for (el of els) {
    el.addEventListener("input", (evt) => {
      updatePaymentForm(stripe);
    });
  }

  generatePaymentForm(stripe);

  // set up purchase handler
  const form = document.getElementById("payment-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const { error } = await stripe.confirmPayment({
      //`Elements` instance that was used to create the Payment Element
      elements: g_elements,
      confirmParams: {
        return_url: "http://localhost:5000/complete",
      },
    });

    if (error) {
      // This point will only be reached if there is an immediate error when
      // confirming the payment. Show error to your customer (for example, payment
      // details incomplete)
      const messageContainer = document.querySelector("#error-message");
      messageContainer.textContent = error.message;
    } else {
      // Your customer will be redirected to your `return_url`. For some payment
      // methods like iDEAL, your customer will be redirected to an intermediate
      // site first to authorize the payment, then redirected to the `return_url`.
    }
  });
}
