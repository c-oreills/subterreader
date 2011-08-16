from django import forms
from subterreader.models import Document

class AddDocumentForm(forms.Form):
    urls = forms.CharField(max_length=1024)
    
    def create_documents(self):
        documents, errors = [], []
        for url in self.data['urls'].split(' '):
            document = Document()
            document.url = url
            try:
                document.full_clean(exclude=('user',))
            except ValidationError, e:
                errors.append(e)
            else:
                documents.append(document)
        return documents, errors
