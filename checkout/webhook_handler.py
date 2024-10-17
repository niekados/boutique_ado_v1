from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle Stripe webhooks

    ---

    Now let's create a class called stripeWH_handler and give it an __init__ method.
    The __init__ method of the class is a setup method that's called every time an instance of the class is created.
    For us we're going to use it to assign the request as an attribute of the class
    just in case we need to access any attributes of the request coming from stripe.
    Now I'll create a class method called handle event which will take the event stripe is sending us
    and simply return an HTTP response indicating it was received.
    With our webhook handler started I'm going to commit my changes.
    And in the next video, we'll add a couple more methods to it and start using it
    to handle webhooks from stripe.
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
