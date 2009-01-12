from django import forms
from models import Listing

class ListingForm(forms.ModelForm):
    """
    Listing form
    """

    class Meta:
        model = Listing
        fields = (
                  'title', 
                  'description', 
                  )
                  
#TODO: Not sure if we can do without the next two                        
class ListingInactivateForm(forms.Form):
    """
    Inactivates listing
    """
    
    delete = forms.BooleanField(initial = True, widget=forms.HiddenInput())
    
class ListingFlagForm(forms.Form):
    """
    Flags listing
    """
    
    flag = forms.BooleanField(initial = True, widget=forms.HiddenInput())
    
