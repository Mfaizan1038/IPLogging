from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from app.middleware import LoggingAndRateLimitMiddleware
from app.models import CustomUser, IPRequestLog
from app.rolechoices import RoleChoice


class LoggingAndRateLimitMiddlewareTests(TestCase):

    def setUp(self):
        
        self.factory = RequestFactory()
        self.middleware = LoggingAndRateLimitMiddleware(lambda req: None)
        self.ip = "192.168.2.2"

        
        self.gold_user = CustomUser.objects.create_user(
            email="gold@test.com",
            password="12345",
            role=RoleChoice.Gold_user,
            
        )

    def make_request(self, user=None, path="/"):
        
        request = self.factory.get(path)
        request.META["REMOTE_ADDR"] = self.ip
        request.user = user
        return request

    def test_allows_requests_within_limit_gold(self):
        
        limit = self.middleware.role_limits[RoleChoice.Gold_user]
        for _ in range(limit):
            
            req = self.make_request(user=self.gold_user)
            response = self.middleware.process_request(req)
            self.assertIsNone(
                response,)

    def test_blocks_after_limit_exceeded(self):
        
        limit = self.middleware.role_limits[RoleChoice.Gold_user]
        for _ in range(limit):
            req = self.make_request(user=self.gold_user)
            self.middleware.process_request(req)

        req = self.make_request(user=self.gold_user)
        response = self.middleware.process_request(req)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 429)
        

    def test_unauthenticated_user_limited(self):
        
        limit = self.middleware.role_limits[RoleChoice.Unauthenticated_user]
        for _ in range(limit):
            req = self.make_request(user=None)
            response = self.middleware.process_request(req)
            self.assertIsNone(response)

        req = self.make_request(user=None)
        response = self.middleware.process_request(req)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 429)

    def test_request_log_reset_after_time_window(self):
        
        old_time = timezone.now() - timedelta(minutes=5)
        IPRequestLog.objects.create(
            ip_address=self.ip,
            count=10,
            start_time=old_time,
        )

        req = self.make_request(user=self.gold_user)
        response = self.middleware.process_request(req)

        log = IPRequestLog.objects.get(ip_address=self.ip)
        self.assertEqual(log.count, 1)
        self.assertIsNone(response)
