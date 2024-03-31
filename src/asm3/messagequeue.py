import threading

from kombu import Connection, Exchange, Queue, Producer

from asm3.typehints import Database
import asm3.configuration


class MessageQueue:
    """
    Singleton class for sending messages to a message queue.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """
        Override __new__ method to implement singleton pattern.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def send_message(self, dbo: Database, messagebody, logtype):
        """
        Send a message to the message queue.

        Args:
            dbo (Database): Database object.
            messagebody: The body of the message to send.
            logtype: Type of log message.

        Returns:
            None
        """
        try:
            if asm3.configuration.amqp_enabled(dbo):
                if not hasattr(self, '_is_initialized'):
                    # Initialize Kombu connection here
                    conn_string = f"amqp://{asm3.configuration.amqp_username(dbo)}:{asm3.configuration.ampq_password(dbo)}@{asm3.configuration.amqp_host(dbo)}/"
                    self.connection = Connection(conn_string)
                    self.exchange = Exchange(asm3.configuration.amqp_exchange(dbo), type="direct")
                    self.queue = Queue(name=asm3.configuration.amqp_queue(dbo), exchange=self.exchange, routing_key="audit")

                    if not self.connection.connected:
                        raise ConnectionError("Unable to establish connection")

                    self._is_initialized = True
        except Exception as e:
            print("Error initializing message queue:", e)
            return

        try:
            # Construct the message including the type
            formatted_message = {
                "LogType": logtype,
                "Message": messagebody
            }

            # Ensure the connection is open
            with self.connection as conn:
                producer = Producer(conn)
                producer.publish(
                    body=formatted_message,
                    exchange=self.exchange,
                    routing_key="audit",
                    declare=[self.queue],
                    serializer='json'
                )
        except Exception as e:
            print("Error sending message:", e)
            self._is_initialized = False

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of MessageQueue.

        Returns:
            MessageQueue: The singleton instance of MessageQueue.
        """
        return MessageQueue()
