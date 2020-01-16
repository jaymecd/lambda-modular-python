import boto3

from . import services
from .di import LambdaContext
from .di import IocContainer as DI


def get_container(**parameters: dict) -> DI:
    # Note! definitions order matters
    definitions = (
        ('context', LambdaContext, None),
        # private services
        ('_boto3_session', boto3.Session, None),
        ('_status_requester', services.status_requester, ('_boto3_session', 'context', DI.param('code'))),
        ('_result_builder', services.result_builder, ('_status_requester', DI.param('ns_dict'))),
        # public services
        ('direct_handler', services.direct_handler, ('_result_builder', )),
    )

    return DI(
        services=definitions,
        parameters=parameters,
        # default parameters
        code=lambda: DI.required(),
        ns_dict=lambda: DI.required(),
    )
