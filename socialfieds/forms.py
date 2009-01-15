from django import forms
from models import Listing, Category
from django.utils.translation import ugettext_lazy as _

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
    
class CategoryAdminForm(forms.ModelForm):
    """
    Form for Category Admin
    """
    
    parent_category = forms.ModelChoiceField(Category.objects.all(), required=False)
    
    class Meta:
        model = Category
        fields = (
                  'title', 
                  'parent_category', 
                  )

    def clean_parent_category(self):
    	parent_category = self.cleaned_data['parent_category']
    	if parent_category:
            if parent_category.title == self.cleaned_data['title']: 
                raise forms.ValidationError(_('Parent category can not be current category'))
        return self.cleaned_data['parent_category']