from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # override default __init__
    # First we call the default init method to set the form up as it would be by default.
    # After that, I've created a dictionary of placeholders which will show up
    # in the form fields rather than having clunky looking labels and empty text boxes in the template.
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # Next we're setting the autofocus attribute on the full name field to true
        # so the cursor will start in the full name field when the user loads the page.
        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                # And finally we iterate through the forms fields adding a star to the placeholder
                # if it's a required field on the model.
                # Setting all the placeholder attributes to their values in the dictionary above.
                # Adding a CSS class we'll use later.
                # And then removing the form fields labels.
                # Since we won't need them given the placeholders are now set.
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
