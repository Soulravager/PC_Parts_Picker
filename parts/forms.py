# your_app/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture','address']


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review here...'})
        }

from django import forms
from .models import UserRating

class RatingForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 stars

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'})
    )

    class Meta:
        model = UserRating
        fields = ['rating']

from django import forms
from .models import CPU, GPU, RAM, SSD, Motherboard, PSU

class CPUForm(forms.ModelForm):
    class Meta:
        model = CPU
        fields = ['brand','name','model',  'cores', 'threads', 'CPU_socket','clock_speed', 'tdp', 'price', 'image','product_link','description']

class GPUForm(forms.ModelForm):
    class Meta:
        model = GPU
        fields = ['brand','name', 'model', 'memory', 'rop', 'price', 'image','oem', 'watt','product_link','description']

class RAMForm(forms.ModelForm):
    class Meta:
        model = RAM
        fields = ['brand','name',  'model', 'capacity', 'speed', 'type', 'price', 'watt', 'image','product_link','description']

class SSDForm(forms.ModelForm):
    class Meta:
        model = SSD
        fields = ['brand','name',  'model', 'size', 'read_speed', 'write_speed', 'watt', 'price', 'image','product_link','description']

class MotherboardForm(forms.ModelForm):
    class Meta:
        model = Motherboard
        fields = ['brand', 'name','model', 'socket_type','RAM_Type', 'watt', 'price', 'image','product_link','description']

class PSUForm(forms.ModelForm):
    class Meta:
        model = PSU
        fields = ['brand','name',  'model', 'watt', 'price', 'image','product_link','description']
