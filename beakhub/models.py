from django.db import models

# Create your models here.
class BhAccount(models.Model):
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name    = 'Account'
        verbose_name_plural = 'Accounts'
        ordering        = ['username']
    def __str__(self):
        return self.username

class BhUser(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, null=True)
    whatsapp_phone = models.CharField(max_length=25, null=True)
    phone_number = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to="photo_user/",null=True)
    date_of_birth = models.DateField(max_length=250, null=True)
    account = models.OneToOneField(BhAccount, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name    = 'User'
        verbose_name_plural = 'Users'
        ordering        = ['first_name', 'last_name']
    def __str__(self):
        return self.last_name + ' ' + self.first_name

class BhCategory(models.Model):
    title = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']
    def __str__(self):
        return self.title

class BhJob(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    user = models.ForeignKey(BhUser, on_delete=models.CASCADE)
    category = models.ForeignKey(BhCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['title']
    def __str__(self):
        return self.title

class BhAddress(models.Model):
    title = models.CharField(max_length=150)
    country = models.CharField(max_length=150, null=True)
    town = models.CharField(max_length=150, null=True)
    street = models.CharField(max_length=150, null=True)
    website = models.URLField(max_length=150, null=True)
    phone_number_1 = models.CharField(max_length=150)
    phone_number_2 = models.CharField(max_length=150, null=True)
    job = models.ForeignKey(BhJob, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Address'
        ordering = ['title']
    def __str__(self):
        return self.title

class BhComment(models.Model):
    commentary = models.TextField(max_length=250)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(BhUser, on_delete=models.CASCADE)
    job = models.ForeignKey(BhJob, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']
    def __str__(self):
        return self.commentary