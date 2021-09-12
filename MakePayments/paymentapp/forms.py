from django import forms
from .models import NgoDonation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class NgoDonationForm(forms.ModelForm):
    class Meta:
        model = NgoDonation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'amount',
            Submit('submit', 'Donate', css_class = 'button white btn-block btn-dark', css_id = "ok-btn")
        )