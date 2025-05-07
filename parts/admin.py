from django.contrib import admin
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU

class CPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','model', 'price','image','tdp','clock_speed','CPU_socket','product_link')  # Include rating
class GPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','model', 'price','oem','product_link','image')  # Include rating
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand','model', 'price','image','RAM_Type','product_link')  # Include rating
class RAMAdmin(admin.ModelAdmin):
    list_display = ('name','brand', 'model', 'capacity', 'speed', 'price','image','product_link')  # Include rating
class SSDAdmin(admin.ModelAdmin):
    list_display = ('name','brand', 'model', 'size', 'price','image','product_link')  # Include rating
class PSUAdmin(admin.ModelAdmin):
    list_display = ('name','brand', 'model', 'watt', 'price','image','product_link')  # Include rating

admin.site.register(CPU, CPUAdmin)
admin.site.register(GPU, GPUAdmin)
admin.site.register(Motherboard, MotherboardAdmin)
admin.site.register(RAM, RAMAdmin)
admin.site.register(SSD, SSDAdmin)
admin.site.register(PSU, PSUAdmin)
