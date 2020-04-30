from django.contrib import admin
from .models import Report, Journal, Author, SummaryReport, Summary

# Register your models here.

admin.site.register(Report)
admin.site.register(Journal)
admin.site.register(Author)
admin.site.register(SummaryReport)
admin.site.register(Summary)