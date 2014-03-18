from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Row, Column, Fieldset, Layout, HTML, Submit, ButtonHolder, Button

from .models import Format, Field, Transform


class AddFormatForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            'Add a format',
            Row(
                Column('name', css_class='small-9'),
                Column(HTML("<label>&nbsp;</label>"), Submit('submit', 'Submit', css_class="tiny"), css_class='small-3')
            )
        )
    )

    class Meta:
        model = Format
        fields = ("name",)


class ModifyFormatForm(forms.ModelForm):
    streams = forms.CharField(max_length=255, required=False)

    helper = FormHelper()
    helper.form_method = "POST"
    helper.layout = Layout(
        Fieldset(
            "Modify format",
            "name", "streams", "splitter_type", "splitter_args"
        ),
        ButtonHolder(Submit('submit', 'Update', css_class="small"))
    )

    class Meta:
        model = Format
        fields = ("name", "splitter_type", "splitter_args")


class TestFormatDataForm(forms.Form):
    input = forms.CharField(max_length=2048)

    def __init__(self, *args, **kwargs):
        format_id = kwargs.pop("format_id")
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                "Enter test data",
                Row(
                    Column('input', css_class='small-7 medium-9'),
                    Column(
                        Row(
                            Column(HTML("<label>&nbsp;</label>"),
                                   HTML("""<a class='button tiny secondary' id='refresh_button' data-formatid=%s>
                                            <i class='fi-refresh large'></i></a>""" % format_id),
                                   css_class='small-3'),
                            Column(HTML("<label>&nbsp;</label>"),
                                   Submit('submit', 'Submit', css_class="tiny"),
                                   css_class='small-9')
                        ),
                        css_class="small-5 medium-3"
                    )
                )
            ),
        )


        super(TestFormatDataForm, self).__init__(*args, **kwargs)




class FieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                'Add Field',
                "name", "type", "source_template"
            ),
            ButtonHolder(Submit('submit', 'Submit', css_class="small"))
        )

        if "instance" in kwargs and kwargs["instance"]:
            self.helper.layout.fields[0].legend = "Modify Field"
        super(FieldForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Field
        fields = ("name", "type", "source_template")


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


class FormatStreamsForm(forms.Form):
    streams = forms.CharField(max_length=1024)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Fieldset(
                'Edit Files',
                "streams"
            ),
            ButtonHolder(Submit('submit', 'Submit', css_class="small"))
        )
        super(FormatStreamsForm, self).__init__(*args, **kwargs)