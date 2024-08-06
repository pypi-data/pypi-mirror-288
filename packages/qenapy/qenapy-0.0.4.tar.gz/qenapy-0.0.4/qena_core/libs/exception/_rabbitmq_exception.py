"""
Exception used specifically for rabbitmq consumers and RPC
"""


class RabbitMQException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        self.args = (str(self),)

    def __str__(self):
        return f"code: [{self.code}], message: [{self.message}]"
