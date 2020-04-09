# from django import forms

# class ProfileForm(forms.Form):
    
    # NOT ENOUGH TIME TO IMPLEMENT WELL STRUCTURED FORM CLASSES
    # TO VALIDATE USERS IN... 


from django import forms

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()