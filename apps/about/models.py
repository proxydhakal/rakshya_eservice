from django.db import models
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"Only one instance of {self.__class__.__name__} is allowed.")
        return super().save(*args, **kwargs)
    
class About(SingletonModel):
    description = CKEditor5Field("Content", config_name="extends")

    def __str__(self):
        return "About Page Content"

class AboutFeature(models.Model):
    about = models.ForeignKey(About, related_name='features', on_delete=models.CASCADE)
    icon = models.CharField(max_length=100, help_text="Font Awesome or Bootstrap icon class")
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


# Mission Singleton Model
class Mission(SingletonModel):
    description = CKEditor5Field("Content", config_name="extends")

    def __str__(self):
        return "Mission Page Content"

class MissionFeature(models.Model):
    mission = models.ForeignKey(Mission, related_name='features', on_delete=models.CASCADE)
    mission_feature = models.CharField(max_length=200)

    def __str__(self):
        return self.mission_feature


# Vision Singleton Model
class Vision(SingletonModel):
    description = CKEditor5Field("Content", config_name="extends")

    def __str__(self):
        return "Vision Page Content"

class VisionFeature(models.Model):
    vision = models.ForeignKey(Vision, related_name='features', on_delete=models.CASCADE)
    vision_feature = models.CharField(max_length=200)


    def __str__(self):
        return self.vision_feature
