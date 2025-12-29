from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Location(BaseModel):

    TYPES = {
        ("M", "Male"),
        ("F", "Female"),
        ("PWD", "PWD"),
        ("U", "Unisex"),
    }

    name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    stall_type = models.CharField(max_length=50, choices=TYPES, default="U")
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.address}"