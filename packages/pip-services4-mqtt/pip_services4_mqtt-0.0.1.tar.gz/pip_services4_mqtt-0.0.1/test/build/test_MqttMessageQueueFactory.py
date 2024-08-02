# -*- coding: utf-8 -*-
from pip_services4_components.refer import Descriptor

from pip_services4_mqtt.build import MqttMessageQueueFactory


class TestMqttMessageQueueFactory:

    def test_create_message_queue(self):
        factory = MqttMessageQueueFactory()
        descriptor = Descriptor("pip-services", "message-queue", "mqtt", "test", "1.0")

        can_result = factory.can_create(descriptor)
        assert can_result is not None

        queue = factory.create(descriptor)
        assert queue is not None
        assert 'test' == queue.get_name()
