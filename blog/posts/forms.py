from django import forms
from .models import Post,Comment
# from tinymce import TinyMCEWidget

# class TinyMCEWidget(TinyMCEWidget):
#     def use_required_attribute(self,*args):
#         return False
from ckeditor.fields import RichTextField
class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=20,
    # widget=forms.TextInput(attrs={
    #     'class':'form-control',
    #     'placeholder':'Enter you title',
    #     'id':"title",
    #     }
    #     ))
    # overview = forms.CharField(max_length=50,
    # widget=forms.TextInput(attrs={
    #     'class':'form-control',
    #     'placeholder':'Enter the overview of your post here',
    #     'id':"overview",
    #     }
    #     )
    # )
    # content = RichTextField(blank='True',null=True,
    
    # )
 
    class Meta:
        model = Post
        fields = ['title','overview','content','thumbnail','categories','featured','previous_post','next_post']

class CommentForm(forms.ModelForm):
    content = forms.CharField( widget=forms.Textarea( attrs={
        'class':'form-control',
        'placeholder':'Type your comment',
        "id":'usercomment',
        'rows':'4',
    }))
    class Meta:
        model = Comment
        fields = ('content',)