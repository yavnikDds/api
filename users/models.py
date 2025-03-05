from django.db import models

class User(models.Model):
    fullname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128) #store hashed password
    # confirm_password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.password != self.confirm_password:
    #         raise ValueError("Password did not matched.")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.email