from abc import abstractmethod
from aws_lambda_powertools.metrics import MetricUnit

import os
import json
import datetime


# from aws_embedded_metrics.unit import MetricUnit


class OrganizationEvent:
    def __init__(self, application, service):
        self.application = application
        self.service = service
        self._event = None
        self._context = None
        self._username = None
        self._organization = None

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, event):
        self._event = event
        self.request_context = event.get('requestContext').get('authorizer')
        self.user = self.request_context.get('claims', {})
        self.organization = self.user.get('custom:organization')
        self.username = self.user.get('cognito:username')
        self.email = self.user.get('cognito:email')
        self.user_groups = self.user.get('cognito:groups')
        self.env = os.environ.get('STAGE', 'dev')

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, organization):
        self._organization = organization

    def logger_metadata(self):
        return {
            "env": self.env,
            "organization": self.organization,
            "username": self.username,
            "email": self.email,
            "user_groups": self.user_groups,
            "method": self.event.get('httpMethod'),
            "resource": self.event.get('resource'),
            "query_params": self.event.get('queryStringParameters', {}),
        }

    def metrics_dimensions(self):
        return {
            "env": self.env,
            "organization": self.organization,
            "read_only": self.event.get('httpMethod') in ['GET', 'OPTIONS'],
        }

    def log_metrics(self):
        return {
            "raise_on_empty_metrics": False,
            # "default_dimensions": self.metrics_dimensions, # Organization and method are not available until the event is set
            "capture_cold_start_metric": True
        }

    def init_metrics(self, metrics):
        for _name, _val in self.metrics_dimensions().items():
            metrics.add_dimension(name=_name, value=_val)

        metrics.add_metric(name="api_request", unit=MetricUnit.Count, value=1)

        for _key, _val in self.logger_metadata().items():
            metrics.add_metadata(key=_key, value=_val)

    def init_tracer(self, tracer):
        for _name, _val in self.metrics_dimensions().items():
            tracer.put_annotation(key=_name, value=_val)

        for _key, _val in self.logger_metadata().items():
            tracer.put_metadata(key=_key, value=_val)

    def init_logger(self, logger):
        logger.append_keys(**self.logger_metadata())

    @abstractmethod
    def print_event(self):
        pass


class EventBridgeHandler(OrganizationEvent):
    def logger_metadata(self):
        return {
            "application": self.application,
            "env": os.environ.get('STAGE', 'dev'),
            "source": self.event.source,
            "detail_type": self.event.detail_type,
            "detail": self.event.detail,
            "organization": self.event.detail.get('organization'),
            "username": self.event.detail.get('username'),
        }

    def metrics_dimensions(self):
        return {
            "env": self.env,
            "organization": self.organization,
            "read_only": False,
        }

    def print_event(self):
        print("#" * 88)
        print(f"==================================== {self.service} Event ====================================")
        print("-" * 88)
        print(f"======================> Source: {self.event.source}")
        print(f"=====================> Detail Type: {self.event.detail_type}")
        print(f"======================> Detail: {self.event.detail}")
        print("#" * 88)


class ApiRequestHandler(OrganizationEvent):
    def inspect(self, response, metrics=None, tracer=None):
        if type(response) is str:
            response = json.loads(response)
        statusCode = response.get('statusCode', '')
        response_result = self.get_response_result(statusCode)

        if metrics and tracer:
            metrics.add_metric(name=response_result, unit=MetricUnit.Count, value=1)
            # for _key, _val in response.items():
            #     metrics.add_metadata(key=_key, value=_val)
            #     tracer.put_metadata(key=_key, value=_val)

        body = response.get('body', {}) if response.get('body', {}) is dict else json.loads(response.get('body', {}))
        response_keys = body.keys() if body is dict else []

        print("#" * 120)
        print(
            f"==================================== API RESPONSE: {self.event.get('httpMethod')} | Resource: {self.event.get('resource')} ? {self.event.get('queryStringParameters', {})} ====================================")
        print("-" * 120)

        print(
            f"------------------------------------- statusCode: {response.get('statusCode', '')} | Response keys{response_keys}---------------------------------------------------")

        try:
            message = body.get('message', '')
            message_detail = body.get('message_detail', '')
            count = body.get('count', 'NA')
            data = body.get('data', "")
            print(f"======================> Body Message: {message} | {message_detail}  <======================")
            print(f"======================> Body Count: {count} <======================")
            print(data)
            print("#" * 120)
        except Exception:
            print(
                f"<===&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&===# Full Response #===&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&===>")
            print(response)
            print("#" * 120)
            pass

    def get_user_context(self):
        return {
            "organization": self.organization,
            "username": self.username,
            "user_email": self.email,
            "user_groups": self.user_groups,
            "user_env": self.env,
            "user_applications": self.user.get('custom:applications'),
            "user_branches": self.user.get('custom:branches'),
            "user_locale": self.user.get('custom:locale'),
            "user_zoneinfo": self.user.get('zoneinfo'),
        }

    def get_response_result(self, statusCode):
        _status = int(statusCode) if statusCode else 0
        _response_result = 'unknown_api_responses'
        if _status >= 500:
            _response_result = 'error_api_responses'
        elif _status >= 400:
            _response_result = 'bad_request_api_responses'
        elif _status >= 200:
            _response_result = 'success_api_responses'
        return _response_result

    def body_data(self, data):
        return json.dumps({
            "data": data
        }, default=self.datetime_str_converter)

    def plain_body(self, data):
        return json.dumps(data, default=self.datetime_str_converter)

    def paginated(self, data):
        if isinstance(data, list):
            data = {
                "data": data
            }
        return json.dumps({
            "total_items": data.get('total_items'),
            "page": data.get('page'),
            "limit": data.get('limit'),
            "total_pages": data.get('total_pages'),
            "next_page": data.get('next_page'),
            "previous_page": data.get('previous_page'),
            "count": data.get('count'),
            "data": data.get('data', []),
            "items": data.get('data', []),
        }, default=self.datetime_str_converter)

    def message(self, message, data=None, status="Success"):
        return json.dumps({
            "message": status,
            "show_toast": False,
            "message_detail": message,
            "data": data
        })

    def toast_message(self, message, data=None, status="Success"):
        return json.dumps({
            "message": status,
            "show_toast": True,
            "message_detail": message,
            "data": data
        })

    def datetime_str_converter(self, _datetime):
        if isinstance(_datetime, datetime.datetime):
            return _datetime.isoformat()
        return str(_datetime)

    def print_event(self, ):
        print("#" * 120)
        print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ API REQUEST: {self.service} API @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("-" * 120)
        print(
            f"======================> HTTP Method: {self.event.get('httpMethod')} | Resource: {self.event.get('resource')} | Path: {self.event.get('path')}")
        print(f"=====================> Query Params: {self.event.get('queryStringParameters', {})}")
        print(f"======================> Body Params: {self.event.body}")
        print("#" * 120)
