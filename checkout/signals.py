# We've got the method to update the total already in the order model.
# We just need a way to call it each time a line item is attached to the order.
# To accomplish this we'll use a built-in feature of django called signals.
# In a new file called signals.py. which will live at the same level as models.py.
# I'll import two signals from django.db.models.signals
# post_save and post_delete. Post, in this case, means after.
# So this implies these signals are sent by django to the entire application
# after a model instance is saved and after it's deleted respectively.
# To receive these signals we can import receiver from django.dispatch.
# Of course since we'll be listening for signals from the OrderLineItem model we'll also need that.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    ---
     it'll take in parameters of sender, instance, created, and keyword arguments.
    This is a special type of function which will handle signals from the post_save event.
    So these parameters refer to:
    'sender' - The sender of the signal. In our case OrderLineItem.
    'instance' - The actual instance of the model that sent it.
    'created' - A boolean sent by django referring to whether this is a new instance or one being updated.
    '**kwargs' - Any keyword arguments.
    ---
    we just have to access instance.order which refers to the order this specific line item is related to.
    And call the update_total method on it. 
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem udelete
    ---
    Has no created
    """
    instance.order.update_total()

"""
And now to let django know that there's a new signals module with some listeners in it.
We just need to make a small change to apps.py in checkout app.
Overriding the ready method and importing our signals module.
"""
