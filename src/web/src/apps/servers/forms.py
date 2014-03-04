from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Row, Column, Fieldset, Layout, HTML, Submit

from .models import Server


class AddServerForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            'Add a server',
            Row(
                Column('name', css_class='small-6'),
                Column('ip', css_class='small-4'),
                Column(HTML("<label>&nbsp;</label>"), Submit('submit', 'Submit', css_class="tiny"), css_class='small-2')
            )
        )
    )

    class Meta:
        model = Server
        fields = ("name", "ip")