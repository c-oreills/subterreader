from django import forms
from subterreader.models import Webpage

class AddWebpageForm(forms.Form):
    urls = forms.CharField(max_length=1024)
    
    def create_webpages(self):
        webpages, errors = [], []
        for url in self.data['urls'].split(' '):
            webpage = Webpage()
            webpage.url = url
            try:
                webpage.full_clean(exclude=('user',))
            except ValidationError, e:
                errors.append(e)
            else:
                webpages.append(webpage)
        return webpages, errors
