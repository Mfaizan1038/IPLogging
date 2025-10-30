from django.contrib import admin
from app.models import CustomUser,IPRequestLog
# IPRequestLog

# Register your models here.
admin.site.register(CustomUser)
# admin.site.register(IPRequestLog)
admin.site.register(IPRequestLog)
