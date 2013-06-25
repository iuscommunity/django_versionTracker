from django.db import models
from django.contrib.auth.models import User

class Release(models.Model):
    label = models.CharField(max_length=1)
    display_name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.label
    
class Status(models.Model):
    label = models.CharField(max_length=100, unique=True)
    html_color_code = models.CharField(max_length=15)
    
    class Meta:
        verbose_name_plural = "Statues"
    
    def __unicode__(self):
        return self.label
    
class Software(models.Model):
    label = models.CharField(max_length=100)
    enabled = models.BooleanField()
    url = models.CharField(max_length=500, blank=True, null=True)
    pattern = models.CharField(max_length=250, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    post_data = models.CharField(max_length=100, blank=True, null=True)
    post_value = models.CharField(max_length=100, blank=True, null=True)
    assigned = models.ForeignKey(User, blank=True, null=True)
    ticket = models.CharField(max_length=500, blank=True, null=True)
    vcs = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    releases = models.ManyToManyField(Release)
    notes = models.TextField(blank=True, null=True)
    logs = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.label
    
class OurVersion(models.Model):
    label = models.CharField(max_length=100)
    stable_version = models.CharField(max_length=50, blank=True, null=True)
    testing_version = models.CharField(max_length=50, blank=True, null=True)
    development_version = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    software = models.ForeignKey(Software)
    release = models.ForeignKey(Release)
    status = models.ForeignKey(Status, blank=True, null=True)
    logs = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ("label", "release")
    
    def __unicode__(self):
        return self.label
