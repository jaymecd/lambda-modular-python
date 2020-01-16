from typing import Callable


class IocContainer(object):
    """
    IoC container to automatic dependency orchestration.
    """

    PARAM_PREFIX = '_p.'

    class Error(Exception):
        pass

    @staticmethod
    def required():
        raise ValueError("mandatory parameter is not provided")

    @classmethod
    def param(cls: str, attr: str):
        return f"{cls.PARAM_PREFIX}{attr}"

    @classmethod
    def decode_attr(cls: str, attr: str) -> tuple:
        if attr.startswith(cls.PARAM_PREFIX):
            return ('param', attr[len(cls.PARAM_PREFIX):])

        return ('service', attr)

    def __init__(self, parameters: dict, services: tuple, **defaults: dict):
        """
        Initializes container with parameter and service definitions.
        Order of services definition matters.
        """

        merged = dict(defaults)
        merged.update(parameters)

        configuration = tuple([(f"{self.PARAM_PREFIX}{key}", val, None) for key, val in merged.items()]) + services

        for attr, value, args in configuration:
            if not isinstance(value, type) and not callable(value):
                self.__dict__[attr] = value
                continue

            args = [self.__getattr__(arg) for arg in (args or [])]

            try:
                self.__dict__[attr] = value(*args)
            except Exception as ex:
                [kind, name] = self.decode_attr(attr)
                raise self.Error(f"IoC: {kind} '{name}' error: {ex}").with_traceback(ex.__traceback__) from None

    def __delattr__(self, attr: str):
        [kind, name] = self.decode_attr(attr)
        raise self.Error(f"IoC: {kind} '{name}' could not be deleted")

    def __setattr__(self, attr: str, value):
        [kind, name] = self.decode_attr(attr)
        raise self.Error(f"IoC: {kind} '{name}' is immutable")

    def __getattr__(self, attr: str):
        try:
            return self.__dict__[attr]
        except KeyError:
            [kind, name] = self.decode_attr(attr)
            raise self.Error(f"IoC: {kind} '{name}' is not declared") from None


class LambdaContext(object):
    """
    Within DI it keeps native context object to avoid props drilling.
    """

    class ContextIsNotSet(Exception):
        pass

    class InvalidContextAttribute(Exception):
        pass

    def use(self, context):
        self._context = context

    def __getattr__(self, attribute: str):
        if not self._context:
            raise self.ContextIsNotSet()

        if not hasattr(self._context, attribute):
            raise self.InvalidContextAttribute(attribute)

        return getattr(self._context, attribute)
