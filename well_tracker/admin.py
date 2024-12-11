from django.contrib import admin

# Register your models here.

from .models import PreSessionMetrics, PostSessionMetrics

# Register your models here
admin.site.register(PreSessionMetrics)
admin.site.register(PostSessionMetrics)