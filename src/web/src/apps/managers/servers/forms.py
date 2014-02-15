from django.forms import ModelForm
from apps.managers.servers.models import Server
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, ButtonHolder, Fieldset, Submit, Row, Column


class BaseServerForm(ModelForm):
    TITLE, SUBMIT = None, None

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                self.TITLE,
                "name", "ip"
            ),
            ButtonHolder(
                Submit("submit", self.SUBMIT, css_class="small")
            )
        )

        super(BaseServerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Server
        fields = ('name', 'ip')


class AddServerForm(ModelForm):
    helper = FormHelper()
    helper.form_id = "add_server_form"
    helper.layout = Layout(
        Row(
            Column("name", css_class="medium-7"),
            Column("ip", css_class="medium-5")
        ),
        Row(
            Column(Submit("submit", "Add"), css_class="medium-12")
        )
    )

    class Meta:
        model = Server
        fields = ('name', 'ip')


class ModifyServerForm(BaseServerForm):
    TITLE = "Modify Server"
    SUBMIT = "Save"