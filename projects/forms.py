from django import forms

from projects.models import Project


class CreateProjectForm(forms.ModelForm):
    name = forms.CharField(max_length=256, required=True,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control form-control-user'}))

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Название проекта"

    class Meta:
        model = Project
        fields = ['name']