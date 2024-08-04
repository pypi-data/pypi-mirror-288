class HandlerError(Exception):
    pass


class KafkaProducerInitError(HandlerError):
    pass


class KafkaProducerParsingError(HandlerError):
    pass


class KafkaProducerProduceError(HandlerError):
    pass
