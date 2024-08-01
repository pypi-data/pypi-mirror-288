import importlib
import zlib

from confluent_kafka import Consumer, KafkaException, KafkaError


class ProtobufKafkaConsumer:
    def __init__(self, bootstrap_servers, group_id, topics, auto_offset_reset='earliest', enable_auto_commit=True):
        self.conf = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': auto_offset_reset,
            'enable.auto.commit': enable_auto_commit
        }
        self.consumer = Consumer(self.conf)
        if isinstance(topics, str):
            topics = [topics]  # Ensure topics is a list
        self.consumer.subscribe(topics)

    def load_proto_module(self, proto_module_name):
        return importlib.import_module(proto_module_name)

    def create_message(self, proto_module, message_type):
        return getattr(proto_module, message_type)()

    def deserialize_message(self, proto_module, message_type, binary_data):
        message = self.create_message(proto_module, message_type)
        message.ParseFromString(zlib.decompress(binary_data))
        return message

    def consume_messages(self, proto_module_name, message_type):
        try:
            while True:
                msg_batch = self.consumer.consume(num_messages=1, timeout=0.5)
                if not msg_batch:
                    print('No message....count....!!!')
                    continue
                for msg in msg_batch:
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            print('%% %s [%d] reached end at offset %d\n' %
                                  (msg.topic(), msg.partition(), msg.offset()))
                        elif msg.error():
                            raise KafkaException(msg.error())
                    else:
                        try:
                            msg_val = msg.value()

                            # Decompress the message
                            decompressed_msg_val = zlib.decompress(msg_val)
                            message = self.deserialize_message(proto_module_name, message_type, decompressed_msg_val)
                            # Process your message here
                            print(message)
                        except Exception as e:
                            print(e)
                            continue
        except Exception as e:
            print(e)
        finally:
            self.consumer.close()
