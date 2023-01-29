from django.db import models
from django.forms import FileField

class gujrati_files(models.Model):
    # email = models.EmailField(max_length=254)
    image = models.FileField(upload_to='Uploaded_Data')
    