from django.contrib import admin
from .models import MyModel, Report, Journal, Author

# Register your models here.

admin.site.register(MyModel)
admin.site.register(Report)
admin.site.register(Journal)
admin.site.register(Author)