document.addEventListener("DOMContentLoaded", function() {
  //Immediately get the Stripe publishable key
  fetch("/config")
    .then((result) => {
      return result.json();
    })
    .then((data) => {
      //Initialize Stripe.js. Script containing Stripe class is included in base.html
      const stripe = Stripe(data.publicKey);

      // Event handler
      document.querySelector("#subscribeBtn").addEventListener("click", () => {
        // Get Checkout Session ID
        fetch("/create-checkout-session")
        .then((result) => { return result.json(); })
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
          console.log(res);
        });
      });
    });
});
