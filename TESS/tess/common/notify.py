import logging
LOGGER = logging.getLogger()

class Notify:
    def __init__(self, name, type, topic, qos):
        self.name = name
        self.type = type
        self.topic = topic
        self.qos = qos

    @staticmethod
    def create_notifications(notifications):
        return [Notify(**notification) for notification in notifications]

    def __repr__(self):
        return '<Notification name={} topic={}>'.format(self.namne, self.topic)
