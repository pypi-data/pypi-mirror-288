"""
Exception related classes and functions
"""

from ._client_error import *
from ._handler import handle_microservice_exception
from ._microservice_exception import MicroserviceException
from ._rabbitmq_exception import RabbitMQException
from ._redirection_error import *

# disable redefining built-in function
# because of NotImplemented
from ._server_error import *  # pylint: disable=W0622
from ._severity import Severity
