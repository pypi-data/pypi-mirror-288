import traceback

from django.http import HttpRequest
from django.utils import timezone
from .helpers import LogSettings
from django.conf import settings
from .apis import post_api_log


class LoggingMiddleware:
    settings: LogSettings

    method = None
    request_body = None
    headers = None

    skip_request_body = False
    skip_request_body_methods = []
    skip_request_headers = False
    skip_request_headers_methods = []
    skip_response_body = False
    skip_response_body_methods = []
    priority_log_methods = []

    _log = {}

    def __init__(self, get_response):
        self.settings = getattr(settings, "LOG_SETTINGS")
        self.get_response = get_response

    def __is_path_excluded__(self, path: str):
        for excluded_path in self.settings.paths_to_exclude:
            if path.startswith(excluded_path):
                return True
        return False

    @property
    def __can_skip_logging__body(self):
        return self.skip_request_body or self.method in self.skip_request_body_methods

    @property
    def __can_skip_logging__headers(self):
        return (
            self.skip_request_headers
            or self.method in self.skip_request_headers_methods
        )

    @property
    def __can_skip_logging__response_body(self):
        return self.skip_response_body or self.method in self.skip_response_body_methods

    @property
    def __is_api_priority_log__(self):
        return self.method in self.priority_log_methods

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
        if self.__is_path_excluded__(request.path) or not self.settings.enabled:
            return None

        self.skip_request_body = getattr(view_func, "cls", None) and getattr(
            view_func.cls, "skip_logging", False
        )
        self.skip_request_body_methods = (
            getattr(view_func, "cls", None)
            and getattr(view_func.cls, "skip_request_body_methods", None)
            or []
        )
        self.skip_request_headers = getattr(view_func, "cls", None) and getattr(
            view_func.cls, "skip_request_headers", False
        )
        self.skip_request_headers_methods = (
            getattr(view_func, "cls", None)
            and getattr(view_func.cls, "skip_request_headers_methods", None)
            or []
        )
        self.skip_response_body = getattr(view_func, "cls", None) and getattr(
            view_func.cls, "skip_response_body", False
        )
        self.priority_log_methods = (
            getattr(view_func, "cls", None)
            and getattr(view_func.cls, "priority_log_methods", None)
            or []
        )

    def update_post_response_data(self, request, response):
        self._log["status_code"] = self.settings.get_status_code(response)
        self._log["headers"] = (
            self.settings.clean_header(dict(request.headers))
            if not self.__can_skip_logging__headers
            else None
        )
        if self.__can_skip_logging__body:
            self._log["body"] = (
                None  # body can't be accessed after response is composed
            )
        self._log["response"] = (
            response.content.decode("utf-8")
            if not self.__can_skip_logging__response_body
            and response.headers.get("Content-Type") == "application/json"
            else None
        )
        self._log["ended_at"] = timezone.now().timestamp()

    def __call__(self, request: HttpRequest):
        if self.__is_path_excluded__(request.path) or not self.settings.enabled:
            return self.get_response(request)

        self._log = {
            "path": request.path,
            "query_params": request.GET.dict(),
            "method": request.method,
            "user": {
                "id": request.user.id if request.user.is_authenticated else None,
                "email": (
                    request.user.email if request.user.is_authenticated else None
                ),
            },
            "started_at": timezone.now().timestamp(),
        }

        self._log["body"] = request.body.decode("utf-8")

        response = self.get_response(request)
        self.update_post_response_data(request, response)
        post_api_log(self._log, self.__is_api_priority_log__)

        return response

    def process_exception(self, request: HttpRequest, e):
        if self.__is_path_excluded__(request.path) or not self.settings.enabled:
            return None

        response = self.settings.app_exception_handler(
            request, e, traceback.format_exc()
        )
        if not self.settings.can_ignore_exception(e):
            self._log["error"] = {
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
        return response
