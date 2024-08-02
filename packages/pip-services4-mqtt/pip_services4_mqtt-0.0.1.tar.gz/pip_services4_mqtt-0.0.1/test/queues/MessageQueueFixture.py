# -*- coding: utf-8 -*-
import time

from pip_services4_components.context import Context
from pip_services4_messaging.queues import IMessageQueue, MessageEnvelope
from pip_services4_messaging.test.TestMessageReceiver import TestMessageReceiver


class MessageQueueFixture:

    def __init__(self, queue: IMessageQueue):
        self._queue = queue

    def test_send_receive_message(self):
        ctx = Context.from_trace_id("123")

        envelope1: MessageEnvelope = MessageEnvelope(ctx, "Test", "Test message")
        self._queue.send(ctx, envelope1)

        envelope2 = self._queue.receive(ctx, 10000)
        assert envelope2
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

    def test_receive_send_message(self):
        ctx = Context.from_trace_id("123")
        envelope1 = MessageEnvelope(ctx, "Test", "Test message")

        time.sleep(0.5)
        self._queue.send(ctx, envelope1)

        envelope2 = self._queue.receive(ctx, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

    def test_receive_complete_message(self):
        ctx = Context.from_trace_id("123")
        envelope1 = MessageEnvelope(ctx, "Test", "Test message")

        self._queue.send(ctx, envelope1)

        count = self._queue.read_message_count()
        assert count > 0

        envelope2 = self._queue.receive(ctx, 10000)
        assert envelope2
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

        self._queue.complete(envelope2)
        assert envelope2.get_reference() is None

    def test_receive_abandon_message(self):
        ctx = Context.from_trace_id("123")
        envelope1: MessageEnvelope = MessageEnvelope(ctx, "Test", "Test message")
        self._queue.send(ctx, envelope1)

        envelope2 = self._queue.receive(ctx, 10000)
        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

        self._queue.abandon(envelope2)

        envelope2 = self._queue.receive(None, 10000)

        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

    def test_send_peek_message(self):
        ctx = Context.from_trace_id("123")
        envelope1: MessageEnvelope = MessageEnvelope(ctx, "Test", "Test message")

        self._queue.send(ctx, envelope1)

        # Delay until the message is received
        time.sleep(0.5)

        envelope2 = self._queue.peek(ctx)

        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

    def test_peek_no_message(self):
        envelope = self._queue.peek(None)
        assert envelope is None

    def test_move_to_dead_message(self):
        ctx = Context.from_trace_id("123")
        envelope1: MessageEnvelope = MessageEnvelope(ctx, "Test", "Test message")

        self._queue.send(ctx, envelope1)

        envelope2 = self._queue.receive(ctx, 10000)

        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

        self._queue.move_to_dead_letter(envelope2)

    def test_on_message(self):
        ctx = Context.from_trace_id("123")
        message_receiver = TestMessageReceiver()
        self._queue.begin_listen(ctx, message_receiver)

        time.sleep(1)

        envelope1: MessageEnvelope = MessageEnvelope(ctx, "Test", "Test message")
        self._queue.send(ctx, envelope1)

        time.sleep(1)

        envelope2 = message_receiver.messages[0]

        assert envelope2 is not None
        assert envelope1.message_type == envelope2.message_type
        assert envelope1.message.decode('utf-8') == envelope2.message.decode('utf-8')
        assert envelope1.trace_id == envelope2.trace_id

        self._queue.end_listen(ctx)
