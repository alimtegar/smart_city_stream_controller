from functools import lru_cache
import logging


log = logging.getLogger(__name__)

class AppEvent:
    event = ""
    def get_event_name(self) -> str:
        return self.event


class EventsEmitter:
    @staticmethod
    @lru_cache
    def instance():
        return EventsEmitter()

    handlers = {}

    def emit(self, event: AppEvent):
        event_name = event.get_event_name()
        log.info("New event:", event_name)
        if self.handlers.get(event_name) is not None:
            for handler in self.handlers[event_name]:
                handler(event)


    def on(self, event_name: str, handler):
        log.info("Registering event handler:", event_name)
        if self.handlers.get(event_name) is None:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)



def events_on(event_name: str):
    def decorator(func):
        EventsEmitter.instance().on(event_name, func)

    return decorator
