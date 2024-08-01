import importlib
import json
import zlib

from confluent_kafka import Producer
from google.protobuf.descriptor import FieldDescriptor


class ProtobufKafka:
    def __init__(self, broker):
        self.broker = broker

    def load_proto_module(self, proto_module_name):
        return importlib.import_module(proto_module_name)

    def create_message(self, proto_module, message_type):
        return getattr(proto_module, message_type)()

    def set_message_fields(self, message, data):
        for key, value in data.items():
            if not hasattr(message, key):
                print(f"Warning: {key} is not a valid field of {message.DESCRIPTOR.name}")
                continue

            field_descriptor = message.DESCRIPTOR.fields_by_name[key]

            if field_descriptor.label == FieldDescriptor.LABEL_REPEATED:
                field = getattr(message, key)
                if not isinstance(value, list):
                    print(f"Error: Field {key} is a repeated field, but a non-list value was provided")
                    continue
                for item in value:
                    if field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
                        if isinstance(item, str):
                            item = json.loads(item)
                        sub_message = field.add()
                        self.set_message_fields(sub_message, item)
                    else:
                        field.append(item)
            elif field_descriptor.type == FieldDescriptor.TYPE_MESSAGE:
                field = getattr(message, key)
                if isinstance(value, str):
                    value = json.loads(value)
                if isinstance(value, dict):
                    self.set_message_fields(field, value)
                else:
                    print(f"Error: Field {key} is a message type, but a non-dict value was provided")
            else:
                if value is None:
                    setattr(message, key, "")
                    continue
                setattr(message, key, value)

        return message

    def serialize_message(self, message):
        return zlib.compress(message.SerializeToString())

    def deserialize_message(self, proto_module, message_type, binary_data):
        message = self.create_message(proto_module, message_type)
        message.ParseFromString(zlib.decompress(binary_data))
        return message

    def produce_message(self, proto_module_name, message_type, data, topic, version, key=None):
        proto_module = self.load_proto_module(proto_module_name)
        message = self.create_message(proto_module, message_type)
        self.set_message_fields(message, data)
        serialized_message = self.serialize_message(message)
        headers = [('version', version.encode('utf-8'))]

        producer_conf = {'bootstrap.servers': self.broker}
        producer = Producer(producer_conf)

        try:
            producer.produce(topic, value=serialized_message, key=key, headers=headers)
            producer.poll(1)
        except BufferError:
            producer.flush()
            producer.poll(5)
            producer.produce(topic, value=serialized_message, key=key, headers=headers)
        except Exception as e:
            print(e)
