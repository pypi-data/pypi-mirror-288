import json
from abc import ABC
from datetime import datetime

from aws_lambda_powertools import Logger

from .Database import Database
from .Events import OrganizationEventBus
from .Repository import ModelRepository


class PlatformService(ABC):
    def __init__(self,
                 service_name: str,
                 event_bus: OrganizationEventBus,
                 logger: Logger,
                 tracer=None,
                 metrics=None
                 ):
        self.service_name: str = service_name
        self.current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self._event_bus = event_bus
        self._logger = logger
        self._tracer = tracer
        self._metrics = metrics

    @property
    def logger(self) -> Logger:
        return self._logger

    @logger.setter
    def logger(self, logger: Logger):
        self._logger = logger
        self._event_bus.logger = logger

    @property
    def event_bus(self) -> OrganizationEventBus:
        return self._event_bus

    @event_bus.setter
    def event_bus(self, event_bus: OrganizationEventBus):
        self._event_bus = event_bus

    @property
    def tracer(self):
        return self._tracer

    @tracer.setter
    def tracer(self, tracer):
        self._tracer = tracer

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        self._metrics = metrics


class OrganizationService(PlatformService):

    def __init__(self,
                 service_name: str,
                 event_bus: OrganizationEventBus,
                 logger: Logger,
                 tracer=None,
                 metrics=None
                 ):
        super().__init__(service_name, event_bus, logger, tracer, metrics)
        self._context = None
        self._organization = None
        self._username = None
        self._user_groups = None
        self.user_applications = None
        self.user_branches = None
        self.user_zoneinfo = None
        self.user_locale = None
        self.user_env = None

    @property
    def organization(self):
        if self._organization is None:
            raise ValueError("Organization not set")
        return self._organization

    @organization.setter
    def organization(self, organization):
        self._organization = organization

    @property
    def username(self):
        if self._username is None:
            raise ValueError("Username not set")
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def user_groups(self):
        return self._user_groups

    @user_groups.setter
    def user_groups(self, user_groups):
        self._user_groups = user_groups

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context
        self.organization = context.get('organization')
        self.username = context.get('username')
        self.user_email = context.get('user_email')
        self.user_groups = context.get('user_groups')
        self.user_applications = context.get('user_applications')
        self.user_branches = context.get('user_branches')
        self.user_zoneinfo = context.get('user_zoneinfo')
        self.user_locale = context.get('user_locale')
        self.user_env = context.get('user_env')

    @staticmethod
    def validate_platform_admin(func):
        def wrapper(*args, **kwargs):
            instance = args[0]
            # if not any(group in instance.user_groups for group in Organization.superadmins()):
            #     raise ValueError(
            #         f"Validation failed: User does not have access to this method, {Organization.superadmins()}")

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def validate_organization_admin(func):
        def wrapper(*args, **kwargs):
            instance = args[0]
            # if not any(group in instance.user_groups for group in Organization.admins()):
            #     raise ValueError(
            #         f"Validation failed: User does not have access to this method, {Organization.admins()}")

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def validate_organization_user(func):
        def wrapper(*args, **kwargs):
            instance = args[0]
            # if not any(group in instance.user_groups for group in Organization.members()):
            #     raise ValueError(
            #         f"Validation failed: User does not have access to this method, {Organization.members()}")

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def validate_organization_external(func):
        def wrapper(*args, **kwargs):
            instance = args[0]
            # if not any(group in instance.user_groups for group in Organization.externals()):
            #     raise ValueError(
            #         f"Validation failed: User does not have access to this method, {Organization.externals()}")

            return func(*args, **kwargs)

        return wrapper

class DbOrganizationService(OrganizationService):
    def __init__(self,
                 service_name: str,
                 database: Database,
                 repository: ModelRepository,
                 event_bus: OrganizationEventBus,
                 logger: Logger,
                 tracer=None,
                 metrics=None
                 ):
        super().__init__(service_name, event_bus, logger, tracer, metrics)
        self.database = database
        self.repository = repository

    def filter(self, filter_json=None):
        with self.database.connect() as session:
            with session.begin():
                self.repository.session = session
                if isinstance(filter_json, str):
                    filter_json = json.loads(filter_json)

                page = filter_json.pop("page", 1) if filter_json else 1
                limit = filter_json.pop("limit", 200) if filter_json else 200

                if filter_json is None:
                    filter_json = {}
                filter_json.update({
                    "organization": self.organization,
                    "is_deleted": False
                })

                filter_response = self.repository.filter(filter_json=filter_json, page=page, limit=limit)
                return filter_response

