# **************************************************************
# START dongilay
# **************************************************************
from django.db import models
from workforce.models import Department
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

# TODO: Add Viewer Counter
class Tutorial(models.Model):
    title = models.CharField(max_length=250)
    desc = models.TextField()
    video_link = models.URLField(max_length=250)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    department = models.ManyToManyField(Department, related_name="tutorials")

    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def department_str(self):
        return ",\n".join(s.name for s in self.department.all())

    def tags_str(self):
        return ",\n".join(s.name for s in self.tags.all())

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(self.title)
        # else:
        #     self.slug
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tutorial"
        verbose_name_plural = "Video Tutorials"

# class VideoTutorial(models.Model):
#     title = models.CharField(max_length=250)
#     desc = models.TextField()
#     video_link = models.URLField(max_length=250)
#     slug = models.SlugField(unique=True, max_length=100)
#     tags = TaggableManager()

#     department = models.ManyToManyField(Department, related_name="tutorials")

#     create_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

#     def department_str(self):
#         return ",\n".join(s.name for s in self.department.all())

#     def tags_str(self):
#         return ",\n".join(s.name for s in self.tags.all())

#     def save(self, *args, **kwargs):
#         # if not self.slug:
#         self.slug = slugify(self.title)
#         # else:
#         #     self.slug
#         return super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = "Video Tutorial"
#         verbose_name_plural = "Video Tutorials"

# **************************************************************
# END dongilay
# **************************************************************

