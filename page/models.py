from django.db import models

# Create your models here.
# hard coded passwords
regular_user = {"username": "User", "pw": "nicepwd4$"}
admin_user = {"username": "Victor", "pw": "adminpwd4$"}

class comments(models.Model):
    user = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)