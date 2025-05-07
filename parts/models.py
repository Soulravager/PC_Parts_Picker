from django.db import models
# parts/models.py


from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/stock.png', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class CPU(models.Model):
    model = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    cores = models.IntegerField()
    threads = models.IntegerField()
    tdp = models.CharField(max_length=10, null=True, blank=True)  # Can store string values like "65W"
    clock_speed = models.CharField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='parts/cpus/', null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    CPU_socket = models.CharField(max_length=100, null=True, blank=True)
    watt = models.IntegerField(null=True, blank=True)  # Numeric field for watts
    product_link = models.URLField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Sync watt and tdp fields
        if self.watt and not self.tdp:
            self.tdp = f"{self.watt}W"  # Convert watt to string format
        elif self.tdp and not self.watt:
            try:
                self.watt = int(self.tdp.replace("W", "").strip())  # Extract number from "XXW"
            except ValueError:
                pass  # In case tdp contains unexpected text
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.model


class GPU(models.Model):
    model = models.CharField(max_length=100, null=True, blank=True,unique=True)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    memory = models.IntegerField()  # in GB
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='parts/gpus/', null=True, blank=True)  # Add image field
    rop = models.CharField(null=True,blank=True)#GPU POINT/ROPs/TMUS/Shaders
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)  # Rating from 1 to 5    
    oem = models.CharField(max_length=100, null=True, blank=True)  # OEM Field
    watt = models.IntegerField(null=True, blank=True)
    product_link = models.URLField(max_length=500, null=True, blank=True)  # Link to product

    def __str__(self):
        return self.model

class Motherboard(models.Model):
    model = models.CharField(max_length=100, null=True, blank=True,unique=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    socket_type = models.CharField(max_length=100)  # e.g., LGA 1151, AM4
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compatible_cpu = models.ManyToManyField(CPU)
    image = models.ImageField(upload_to='parts/motherboards/', null=True, blank=True)  # Add image field
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)  # Rating from 1 to 5
    description = models.TextField( null=True, blank=True)
    watt = models.IntegerField(null=True, blank=True)
    RAM_Type = models.CharField(max_length=50,null= True,blank=True)
    product_link = models.URLField(max_length=500, null=True, blank=True)  # Link to product

    def __str__(self):
        return self.model

class RAM(models.Model):
    model = models.CharField(max_length=100, null=True, blank=True,unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  # Allow the field to be empty
    capacity = models.IntegerField()  # in GB
    brand = models.CharField(max_length=100)
    speed = models.IntegerField()  # in MHz
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10)  # e.g., DDR4, DDR5
    image = models.ImageField(upload_to='parts/rams/', null=True, blank=True)  # Add image field
    description = models.TextField( null=True, blank=True)
    watt = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)  # Rating from 1 to 5
    product_link = models.URLField(max_length=500, null=True, blank=True)  # Link to product

    def __str__(self):
        return f"{self.brand} {self.model} ({self.capacity}GB)"


class SSD(models.Model):
    model = models.CharField(max_length=100, null=True, blank=True,unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  # Allow the field to be empty
    size = models.IntegerField()  # in GB
    read_speed = models.IntegerField()  # in MB/s
    write_speed = models.IntegerField()  # in MB/s
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    generation = models.IntegerField(null=True,blank=True)  # e.g., 3, 4, 5 for PCIe generation
    description = models.TextField( null=True, blank=True)
    watt = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='parts/ssds/', null=True, blank=True)  # Add image field
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)  # Rating from 1 to 5
    product_link = models.URLField(max_length=500, null=True, blank=True)  # Link to product

    def __str__(self):
        return f"{self.brand} {self.model} ({self.size}GB)"


class PSU(models.Model):    
    model = models.CharField(max_length=100, null=True, blank=True,unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)  # Allow the field to be empty
    brand = models.CharField(max_length=100)
    watt = models.IntegerField()  # e.g., 550W, 750W
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField( null=True, blank=True)
    image = models.ImageField(upload_to='parts/psus/', null=True, blank=True)  # Add image field
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)  # Rating from 1 to 5
    product_link = models.URLField(max_length=500, null=True, blank=True)  # Link to product

    def __str__(self):
        return f"{self.brand} {self.model} ({self.watt}W)"



class Build(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE, default=1)
    ssd = models.ForeignKey(SSD, on_delete=models.CASCADE, default=1)
    psu = models.ForeignKey(PSU, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    shareable = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.model} - {self.user.username}'
    
from django.db import models
from django.contrib.auth.models import User
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU  # Import the relevant models

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    build_name = models.CharField(max_length=255)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    ssd = models.ForeignKey(SSD, on_delete=models.CASCADE)
    psu = models.ForeignKey(PSU, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase by {self.user.username} on {self.purchase_date}"


class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    part_model = models.CharField(max_length=255,null=True, blank=True)
    category = models.CharField(max_length=50,null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.part_model}"


from django.db import models
from django.contrib.auth.models import User
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU  # Adjust based on available models

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part_model = models.CharField(max_length=255,null=True, blank=True)
    part_name = models.CharField(max_length=255, null=True, blank=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
         return f"{self.user.username} - {self.part_name if self.part_name else 'Deleted Item'}"

from django.db import models
from django.contrib.auth.models import User

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part_model = models.CharField(max_length=255)
    category = models.CharField(max_length=50,null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} by {self.user.username} on {self.part_model}"


from django.db import models
from django.contrib.auth.models import User
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU  # Adjust based on available models

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part_model = models.CharField(max_length=255, null=True, blank=True)
    part_name = models.CharField(max_length=255, null=True, blank=True)
    is_cart = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.part_name if self.part_name else 'Deleted Item'}"


    
class Part_sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    part_model = models.CharField(max_length=255)
    part_name = models.CharField(max_length=255)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.part_name} on {self.purchased_at}"
    






