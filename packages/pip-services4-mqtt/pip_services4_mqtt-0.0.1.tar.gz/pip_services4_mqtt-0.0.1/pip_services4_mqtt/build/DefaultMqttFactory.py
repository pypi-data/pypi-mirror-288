# -*- coding: utf-8 -*-
from pip_services4_components.build import Factory
from pip_services4_components.refer import Descriptor

from pip_services4_mqtt.build import MqttMessageQueueFactory
from pip_services4_mqtt.connect import MqttConnection
from pip_services4_mqtt.queues import MqttMessageQueue


class DefaultMqttFactory(Factory):
    """
    Creates :class:`MqttMessageQueue <pip_services4_mqtt.queues.MqttMessageQueue.MqttMessageQueue>`, components by their descriptors.

    See: :class:`MqttMessageQueue <pip_services4_mqtt.queues.MqttMessageQueue.MqttMessageQueue>`

    """

    __MqttQueueDescriptor: Descriptor = Descriptor("pip-services", "message-queue", "mqtt", "*", "1.0")
    __MqttConnectionDescriptor: Descriptor = Descriptor("pip-services", "connection", "mqtt", "*", "1.0")
    __MqttQueueFactoryDescriptor: Descriptor = Descriptor("pip-services", "queue-factory", "mqtt", "*", "1.0")

    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super().__init__()

        def factory_inner(locator: Descriptor):
            name = None if not hasattr(locator, 'get_name') else locator.get_name()
            return MqttMessageQueue(name)

        self.register(DefaultMqttFactory.__MqttQueueDescriptor, factory_inner)
        self.register_as_type(DefaultMqttFactory.__MqttConnectionDescriptor, MqttConnection)
        self.register_as_type(DefaultMqttFactory.__MqttQueueFactoryDescriptor, MqttMessageQueueFactory)
