from django import forms
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU

# CPU Form
class CPUForm(forms.ModelForm):
    class Meta:
        model = CPU
        fields = ['name', 'brand', 'price', 'rating', 'image', 'tdp', 'clock_speed']

# GPU Form
class GPUForm(forms.ModelForm):
    class Meta:
        model = GPU
        fields = ['name', 'brand', 'price', 'rating', 'image', 'rop']

# Motherboard Form
class MotherboardForm(forms.ModelForm):
    class Meta:
        model = Motherboard
        fields = ['name', 'brand', 'price', 'rating', 'image']

# RAM Form
class RAMForm(forms.ModelForm):
    class Meta:
        model = RAM
        fields = ['name', 'brand', 'model', 'capacity', 'speed', 'price', 'rating', 'image']

# SSD Form
class SSDForm(forms.ModelForm):
    class Meta:
        model = SSD
        fields = ['name', 'brand', 'model', 'size', 'price', 'rating', 'image']

# PSU Form
class PSUForm(forms.ModelForm):
    class Meta:
        model = PSU
        fields = ['name', 'brand', 'model', 'watt', 'price', 'rating', 'image']
