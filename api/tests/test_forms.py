from django.test import TestCase


from api.forms import SignupForm,UploadImageForm


class SignupFormTest(TestCase):
    def test_signup_form_labels(self):
        form = SignupForm()
        self.assertTrue(form.fields['username'].label == "Username" or form.fields['username'].label is None)
        self.assertTrue(form.fields['first_name'].label == "First name" or form.fields['first_name'].label is None)
        self.assertTrue(form.fields['last_name'].label == "Last name" or form.fields['last_name'].label is None)
        self.assertTrue(form.fields['email'].label == "Email" or form.fields['email'].label is None)
        self.assertTrue(form.fields['password1'].label == "Password" or form.fields['password'].label is None)
        self.assertTrue(form.fields['password2'].label == "Password confirmation" or form.fields['password_confirmation'].label is None)
    
    def test_signup_form_invalid_username(self):
        username = "ab1.c+g/qsd0dsf-q" # the / is invalid
        form = SignupForm(data={'username': username})
        self.assertFalse(form.is_valid())

    def test_signup_form_invalid_email(self):
        email = "mohamed.gmail.com" 
        form = SignupForm(data={'email': email})
        self.assertFalse(form.is_valid())

    def test_signup_form_invalid_password(self):
        password1 = "1234" # less then 8 char / entirely numeric
        form = SignupForm(data={'password1': password1})
        self.assertFalse(form.is_valid())

    def test_signup_form_invalid_password_confirmation(self):
        password1 = "1234abcde" # valid password
        password2 = "1234hhhhh" # not equal
        form = SignupForm(data={'password1': password1, "password2" : password2})
        self.assertFalse(form.is_valid())

class UploadImageFormTest(TestCase):
    def test_uploadimage_form_labels(self):
        form = UploadImageForm()
        self.assertTrue(form.fields['tags'].label == "Tags" or form.fields['tags'].label is None)
        self.assertTrue(form.fields['description'].label == "Description" or form.fields['description'].label is None)
        self.assertTrue(form.fields['photo'].label == "Photo" or form.fields['photo'].label is None)
        self.assertTrue(form.fields['location'].label == "Location" or form.fields['location'].label is None)

    def test_uploadimage_form_invalid_tags(self):
        tags = "abc-4df,gfgsd,  ,dfkh"
        form = UploadImageForm(data={'tags': tags})
        self.assertFalse(form.is_valid())
    
    def test_uploadimage_form_invalid_photo(self):
        photo = "abc" #not a file
        form = UploadImageForm(data={'photo': photo})
        self.assertFalse(form.is_valid())

