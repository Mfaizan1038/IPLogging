import logging
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin 
from .models import  CustomUser,IPRequestLog
from app.rolechoices import RoleChoice

logger = logging.getLogger('request_logger')


class LoggingAndRateLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.time_window = timedelta(minutes=1) 
        self.role_limits = {
            RoleChoice.Gold_user: 20,
            RoleChoice.Silver_user: 15,
            RoleChoice.Bronze_user: 10,
            RoleChoice.Unauthenticated_user: 5,
        }

    def process_request(self, request):
        
        
        if request.path.startswith("/admin") :
            return None

        ip = self.get_client_ip(request)
        now = timezone.now()

       
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            role = user.role
        else:
            role = RoleChoice.Unauthenticated_user

        limit = self.role_limits.get(role, 1)

       
        log, created = IPRequestLog.objects.get_or_create(ip_address=ip)

        
        if now - log.start_time > self.time_window:
            log.count = 0
            log.start_time = now

        log.count += 1
        log.last_request = now
        log.save()

       
        if log.count > limit:
            logger.warning(f"BLOCKED: {ip} ({role}) exceeded rate limit.")
            return JsonResponse(
                {"error": f"{role} users exceeded rate limit! Try again after 1 minute."},
                status=429,
            )

        
        logger.info(f"IP: {ip}  Role: {role}  Method: {request.method}  Time: {now}")

        
        return None

    def get_client_ip(self, request):
        
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
