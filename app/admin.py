from django.contrib import admin
from app.models import CustomUser,IPRequestLog
# IPRequestLog


admin.site.register(CustomUser)

admin.site.register(IPRequestLog)
