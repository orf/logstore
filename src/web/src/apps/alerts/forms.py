from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Row, Column, Fieldset, Layout, HTML, Submit, ButtonHolder, Button
import pushbullet

from .models import Alert, EventTriggeredCondition, EventCountCondition, EventPercentageCondition,\
    EmailContact, PushBulletContact, TextContact


class BaseModelForm(forms.ModelForm):
    has_submit = False

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                self.get_title(),
                *self.get_fieldset_content()
            ),
            ButtonHolder(Submit('submit', 'Submit', css_class="success"),
                         Button('back', 'Back', onclick="history.back(); return false;")) if not self.has_submit else None
        )

        super(BaseModelForm, self).__init__(*args, **kwargs)


    def get_title(self):
        raise NotImplementedError()

    def get_fieldset_content(self):
        raise NotImplementedError()


class AddAlertForm(BaseModelForm):
    has_submit = True

    def get_title(self):
        return "Add an Alert"

    def get_fieldset_content(self):
        return Row(
            Column('name', css_class='small-9'),
            Column(HTML("<label>&nbsp;</label>"),
                   Submit('submit', 'Submit', css_class="tiny"),
                   css_class='small-3')
        )

    class Meta:
        model = Alert
        fields = ("name",)


class AddAlertConditionPercentageForm(BaseModelForm):
    def get_title(self):
        return "Add a percentage condition"

    def get_fieldset_content(self):
        return (
            Row(Column('event_query')),
            Row(Column("percentage")),
            Row(
                Column("time_value", css_class="small-6"),
                Column("time_choice", css_class="small-6")
            )
        )

    class Meta:
        model = EventPercentageCondition
        fields = ("event_query", "percentage", "time_value", "time_choice")


class AddAlertConditionBucketCountForm(BaseModelForm):
    def get_title(self):
        return "Add a count condition"

    def get_fieldset_content(self):
        return (
            Row(Column('event_query')),
            Row(Column("threshold")),
            Row(
                Column("time_value", css_class="small-6"),
                Column("time_choice", css_class="small-6")
            )
        )

    class Meta:
        model = EventCountCondition
        fields = ("event_query", "threshold", "time_value", "time_choice")


class AddAlertConditionEventTriggeredForm(BaseModelForm):
    def get_title(self):
        return "Add a trigger condition"

    def get_fieldset_content(self):
        return (
            Row(Column('event_query')),
            Row(
                Column("time_value", css_class="small-6"),
                Column("time_choice", css_class="small-6")
            )
        )

    class Meta:
        model = EventTriggeredCondition
        fields = ("event_query", "time_value", "time_choice")


class AddAlertEmailContactForm(BaseModelForm):
    def get_title(self):
        return 'Add an email'

    def get_fieldset_content(self):
        return Row(Column('email_address'))

    class Meta:
        model = EmailContact
        fields = ("email_address",)


class AddAlertTextContactForm(BaseModelForm):
    def get_title(self):
        return "Add a phone number"

    def get_fieldset_content(self):
        return Row(Column('phone_number'))

    class Meta:
        model = TextContact
        fields = ("phone_number",)


def get_pushbullet_choices():
    p = pushbullet.PushBullet(settings.PUSHBULLET_API_KEY)
    return [(d.device_id, "%s %s (%s)" % (d.manufacturer, d.model, d.android_version)) for d in p.devices]


class AddAlertPushBulletContactForm(BaseModelForm):
    device = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        self.declared_fields["device"].choices = get_pushbullet_choices()
        super(AddAlertPushBulletContactForm, self).__init__(*args, **kwargs)

    def get_title(self):
        return "Add a device"

    def get_fieldset_content(self):
        return Row(Column('device'))

    def modify_instance(self):
        self.instance.device_id = self.cleaned_data["device"]
        self.instance.device_name = dict(self.fields["device"].choices)[int(self.instance.device_id)]

    class Meta:
        model = PushBulletContact
        fields = tuple()