import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Type

import backoff
from pydantic import BaseModel, ValidationError


def backoff_hdlr(details) -> None:
    logging.warning(f"Backing off {details['wait']} seconds after {details['tries']} tries due to {details['target']}.")


class AbstractClientServer(ABC):
    """Abstract base class for client-server communication."""

    def __init__(self, default_model: Type[BaseModel] | None = None) -> None:
        self.default_model = default_model
        self._connect()

    def send_data(self, data: BaseModel) -> None:
        """Send data to the server or client.

        Args:
            data (Any): The data to send.
            model (Optional[Type[BaseModel]]): Optional Pydantic model to use for data serialization.
        """
        self._send_data(data)


    def _connect(self) -> None:  # noqa: B027
        """Abstract method to perform the actual connection."""
        pass


    def _send_data(self, data: Any, **kwargs) -> None:
        """Abstract method to perform the actual data sending."""
        raise NotImplementedError

    @backoff.on_exception(backoff.expo, Exception, max_tries=5, on_backoff=backoff_hdlr)
    def receive_data(self) -> Any:
        """Receive data from the server or client, blocking until the resource is available.

        Returns:
            Any: The received data, optionally validated by a Pydantic model.
        """
        logged = False
        while not self.is_resource_available():
            if not logged:
                logging.info("Waiting for resource to become available...")
                logged = True

        data = self._receive_data()

        if self.default_model:
            try:
                return self.default_model.model_validate_json(data)
            except ValidationError as e:
                logging.error(f"Validation error: {e}")
                raise
        self._reset_resource()
        return data

    @abstractmethod
    def _reset_resource(self) -> None:
        """Abstract method to reset the resource."""
        pass

    def _receive_data(self) -> str:
        """Abstract method to perform the actual data reception.

        Returns:
            str: The received data as a string.
        """
        raise NotImplementedError

    def is_resource_available(self) -> bool:
        """Check if the resource is available for receiving data.

        Returns:
            bool: True if the resource is available, False otherwise.
        """
        raise NotImplementedError

    def handle_request(self, message: Any) -> Any:
        """Process the received message and perform business logic.

        Args:
            message (Any): The received and validated message.

        Returns:
            Any: The result of the business logic.
        """
        raise NotImplementedError

    def respond(self, message: Any) -> None:
        """Send a response to the server or client.

        Args:
            message (Any): The message to send.
        """
        raise NotImplementedError

    def poll(self, fn: Callable[[BaseModel], Any]) -> None:
        """Listen for messages from the client and handle them."""
        while True:
            try:
                request = self.receive_data()
                output = self.handle_request(request)
                fn(output)
                self.respond(output)
            except Exception as e:
                logging.error(f"Error processing request: {e}")
