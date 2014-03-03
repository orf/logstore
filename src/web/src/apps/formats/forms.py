from django import forms
from .models import Format, Splitter, Field, Transform
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Row, Column, Fieldset, Layout, HTML, Submit, ButtonHolder


class AddFormatForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            'Add a server',
            Row(
                Column('name', css_class='small-9'),
                Column(HTML("<label>&nbsp;</label>"), Submit('submit', 'Submit', css_class="tiny"), css_class='small-3')
            )
        )
    )

    class Meta:
        model = Format
        fields = ("name",)


class SplitterForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            'Create Splitter',
            "type", "args"
        ),
        ButtonHolder(Submit('submit', 'Submit', css_class="small"))
    )

    def __init__(self, *args, **kwargs):
        if "instance" in kwargs and kwargs["instance"]:
            self.helper.layout.fields[0].legend = "Modify Splitter"
        super(SplitterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Splitter
        fields = ("type", "args")


class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                'Add Field',
                "name", "type", "source_index"
            ),
            ButtonHolder(Submit('submit', 'Submit', css_class="small"))
        )

        if "instance" in kwargs and kwargs["instance"]:
            self.helper.layout.fields[0].legend = "Modify Field"
        super(FieldForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Field
        fields = ("name", "type", "source_index")


class TransformForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                'Add Transformation',
                "type", "args"
            ),
            ButtonHolder(Submit('submit', 'Submit', css_class="small"))
        )

        if "instance" in kwargs and kwargs["instance"] is not None:
            self.helper.layout.fields[0].legend = "Modify Transformation"
        super(TransformForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Transform
        fields = ("type", "args")