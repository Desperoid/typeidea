from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        max_length=50, label='昵称', widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style':'width:60%;'}
        )
    )

    email = forms.CharField(
        label='email', max_length=50, widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style':'width: 60%;'}
        )
    )

    website = forms.CharField(
        label='网站', max_length=100, widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )

    content = forms.CharField(
        label='内容', max_length=500, widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'row':6, 'column':60}
        )
    )

    def clean_context(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么能这么短呢!!')
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']