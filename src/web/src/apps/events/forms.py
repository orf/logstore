from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Row, Column, Fieldset, Layout, HTML, Submit, ButtonHolder

from .models import Event, EventQuery


class AddEventForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            'Add an Event',
            Row(
                Column('name', css_class='small-9'),
                Column(HTML("<label>&nbsp;</label>"), Submit('submit', 'Submit', css_class="tiny"), css_class='small-3')
            )
        )
    )

    class Meta:
        model = Event
        fields = ("name",)


class AddEventQueryForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            "Add a query",
            Row(
                Column("name", css_class="medium-6 small-8"),
                Column("weight", css_class="medium-6 small-4"),
            ),
            Row(
                Column("query", css_class="small-12")
            )
        ),
        ButtonHolder(
            Submit("submit", "Add")
        )
    )

    class Meta:
        model = EventQuery
        fields = ("name", "weight", "query")


class EventFilesForm(forms.Form):
    files = forms.CharField(max_length=1024)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                'Edit Files',
                "files"
            ),
            ButtonHolder(Submit('submit', 'Submit', css_class="small"))
        )

        if "instance" in kwargs and kwargs["instance"] is not None:
            self.helper.layout.fields[0].legend = "Modify Transformation"
        super(EventFilesForm, self).__init__(*args, **kwargs)