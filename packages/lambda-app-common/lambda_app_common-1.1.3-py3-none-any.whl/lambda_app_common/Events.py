import json
from abc import ABC, abstractmethod


class OrganizationEventBus(ABC):

    def __init__(self, event_bus_name, client, service, logger):
        self.event_bus_name = event_bus_name
        self.client = client
        self.service = service
        self.logger = logger
        self._organization = None
        self._username = None

    @abstractmethod
    def publish(self, event_action, detail_type, payload):
        pass

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, organization):
        self._organization = organization

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    def set_organization(self, organization, username):
        self.organization = organization
        self.username = username


class EventBridge(OrganizationEventBus):

    def publish(self, event_action, detail_type, payload):
        source = f"{self.service}.{event_action}"

        payload.update({
            'organization': self.organization,
            'username': self.username,
        })
        event = {
            'EventBusName': self.event_bus_name,
            'Source': source,
            'DetailType': detail_type,
            'Detail': json.dumps(payload),
        }
        try:
            response = self.client.put_events(
                Entries=[
                    event
                ]
            )
            print(response)

            self.logger.info(f"[EventBus] Event Published", extra={
                "event": event
            })
        except Exception as e:
            self.logger.error(f"[EventBus] Error sending event [{source}]: {e}")
            raise e

    def chunk_list_and_publish(self, event_action, detail_type, records: list):
        for i in range(0, len(records), 300):
            chunk = records[i:i + 300]
            payload = {
                'records': chunk
            }

            response = self.publish(event_action, detail_type, payload)
            print(f"Chunk Event Created [{i}/{len(payload)}]")
            print(f"Chunk Event Response  [{response}]")
