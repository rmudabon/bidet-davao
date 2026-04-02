from django.contrib.gis.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Location(BaseModel):
    class StallType(models.TextChoices):
        MALE = "M"
        FEMALE = "F"
        PWD = "PWD"
        UNISEX = "U"

    name = models.CharField(max_length=255)
    address = models.TextField()
    point = models.PointField(srid=4326, geography=True, null=False)
    stall_type = models.CharField(max_length=50, choices=StallType.choices, default=StallType.UNISEX)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.address}"