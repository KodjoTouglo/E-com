from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "id":"exampleInputEmail1", "placeholder":"Enter email/username"}))
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=8, widget=forms.TextInput(attrs={"placeholder":"Enter Username"}))
    fisrt_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter First_name"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter Last name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter Email"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"placeholder":"Enter Password"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"placeholder":"Confirm password"}))


    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return self.cleaned_data['password']