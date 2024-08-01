import inspect
import typing
from typing import Any, Callable
from types import UnionType
from kisa_utils.response import Response

class Value:
    def __init__(self, valueType:Any, validator:Callable,/):
        '''
        create a value definition to be used by `kisa_utils.structures.validator.validate`

        @param `valueType:Any`: The type of the value eg `int` or `int|float`
        @param `validator:Callable`: Callable, the function to call for each value instance. 
                the function should
                - take a single argument; this will be the instance value
                - return a standard KISA response object
        '''

        if not (isinstance(valueType, UnionType) or type(valueType)==type(type)):
            raise TypeError(f'Invalid `valueType` given expected Type|UnionType')

        if not validator:
            raise TypeError(f'invalid/no `validator` given')

        if not (inspect.isfunction(validator) or inspect.ismethod(validator)):
            raise TypeError('Invalid `validator` given. Expected function|method')
        

        if 1 != len(inspect.signature(validator).parameters):
            raise TypeError(f'validator should take only 1 argument (not counting `self` for methods)')
        
        reply = validator(
            valueType() if type(valueType)==type(type) else list(typing.get_args(valueType))[0]()
        )

        if not isinstance(reply, Response):
            raise TypeError(f'`validator` must return kutils.response.Response object')

        self._valueType = valueType
        self._validator = validator
    
    def validate(self, valueInstance:Any, /) -> Response:
        '''
        attempt to validate the `valueInstance` against the value `validator` passed to the constructor
        '''
        return self._validator(valueInstance)
