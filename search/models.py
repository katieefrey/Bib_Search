from django.db import models
from users.models import CustomUser, Bibgroup


# Create your models here.

class Report(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    jnum = models.IntegerField(default=0)
    anum = models.IntegerField(default=0)
    daterange = models.CharField(max_length=250, null=True, blank=True)
    namelist = models.TextField(null=True, blank=True)
    bibgroup = models.ForeignKey(Bibgroup, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.username.first_name}, {self.daterange}"


class Journal(models.Model):
    resultset = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    jname = models.CharField(max_length=250, null=True, blank=True)
    articlenum = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.resultset} {self.jname} {self.articlenum}"


class Author(models.Model):
    resultset = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    aname = models.CharField(max_length=250, null=True, blank=True)
    rart = models.IntegerField(default=0)
    nrart = models.IntegerField(default=0)
    rcite = models.IntegerField(default=0)
    nrcite = models.IntegerField(default=0)
    rfirst = models.IntegerField(default=0)
    nrfirst = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.resultset} {self.aname}"


class SummaryReport(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    bibgroup = models.ForeignKey(Bibgroup, on_delete=models.CASCADE, null=True, blank=True)
    daterange = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.username.first_name}, {self.daterange}"

class Summary(models.Model):
    resultset = models.ForeignKey(SummaryReport, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField(default=0)
    refart = models.IntegerField(default=0)
    refcite = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.resultset} {self.year}"