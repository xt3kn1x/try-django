from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error("title", f"{title} already exists. Please choose another title")
        return data

class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    # def clean_title(self):
    #     cleaned_data = self.cleaned_data # dictionary
    #     title = cleaned_data.get('title')
    #     if title.lower().strip() == "something":
    #         raise forms.ValidationError("You cannot use that title name")
    #     return title


    def clean(self):
        cleaned_data = self.cleaned_data
        print('all data', cleaned_data)
        title = cleaned_data.get('title')
        if title.lower().strip() == "something":
            self.add_error('title', 'This title is taken.')
            # raise forms.ValidationError("You cannot use that title name")
        return cleaned_data
