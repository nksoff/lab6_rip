from django.db import models


class Tutor(models.Model):
    lastname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)
    sex = models.BooleanField(default=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    tutor = models.ForeignKey(Tutor)
