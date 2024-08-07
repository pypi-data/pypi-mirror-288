"""
...
"""

import json

from typing import TYPE_CHECKING, Any, Awaitable

from tornado.web import RequestHandler

if TYPE_CHECKING:
    pass


class BaseViewset(RequestHandler):
    """..."""
    
    arguments = None
    query_arguments = None

    def _parse_value(
        self,
        value: Any,
        blanks: bool=False
    ) -> "str|int|float|bool|None":
        """..."""

        if value == "" or value is None:
            if blanks:
                return value
            return None

        if value.isdigit():
            value = int(value)
        else:
            if value.replace(".", "").isdecimal():
                value = float(value)
            elif value.lower() in ["true", "false"]:
                value = True if value.lower() == "true" else False
            elif value.isalnum():
                value = str(value)
            else:
                raise Exception

        return value


    def _parse_arguments(
        self,
        arguments: dict[Any, Any],
        blanks: bool=False
    ) -> dict[Any, str|int|float|bool]:
        """..."""

        parse_arguments: dict[Any, Any] = {}

        if arguments:
            for key, value in arguments.items():
                if isinstance(value, list):
                    if len(value) > 1:
                        parse_arguments[key] = []
                        for val in value:
                            parsed_value = self._parse_value(val.decode(), blanks)
                            if blanks or parsed_value:
                                parse_arguments[key].append(parsed_value)
                    else:
                        parsed_value = self._parse_value(value[0].decode(), blanks)
                        if blanks or parsed_value:
                            parse_arguments[key] = self._parse_value(value[0].decode(), blanks)
                else:
                    parsed_value = self._parse_value(value, blanks)
                    if blanks or parsed_value:
                        parse_arguments[key] = parsed_value 
                
        return parse_arguments


    def _get_arguments( # type: ignore
        self,
        blanks: bool=False
    ):
        """..."""
        
        arguments = self._parse_arguments(json.loads(self.request.body), blanks=blanks)

        return arguments


    def _get_argument(self, name: str): # type: ignore
        """..."""

        return self.arguments[name] if name in self.arguments else None


    def _get_query_arguments(
        self,
        blanks: bool=False
    ):
        """..."""

        query_arguments = self._parse_arguments(self.request.query_arguments, blanks=blanks)

        return query_arguments


    def _get_query_argument(self, name: str):
        """..."""
        
        return self.query_arguments[name] if name in self.query_arguments else None


    def initialize(self, **kwargs: dict[Any, Any]):
        """..."""

        if "manager" in kwargs:
            self.manager = kwargs["manager"]()
        
        # TODO implement serializers
        #if "serializer" in kwargs:
        #    self.serializer = kwargs["serializer"]
        
        if "method_map" in kwargs:
            
            for method, action in kwargs["method_map"].items():
                handler = getattr(self, action)
                setattr(self, method, handler)


    def prepare(self, **kwargs: dict[Any, Any]) -> Awaitable[None] | None:
        """..."""
        
        try:
            self.arguments = self._get_arguments()
        except:
            pass
        try:
            self.query_arguments = self._get_query_arguments()
        except:
            pass
    

    def list(self, pk: Any=None, *args: tuple[Any], **kwargs: dict[Any, Any]):
        """..."""
                
        elements = self.manager.filter()

        response_data = {
            "status_code": None,
            "content": [element.model_dump() for element in elements]
        }

        self.write(response_data)
            

    def create(self, *args: tuple[Any], **kwargs: dict[Any, Any]):
        """..."""
        
        element = self.manager.create(self.arguments)

        response_data = {
            "status_code": None,
            "content": element.model_dump()
        }

        self.write(response_data)


    def retrieve(self, pk: Any=None, *args: tuple[Any], **kwargs: dict[Any, Any]):
        """..."""
        
        element = self.manager.read(pk)

        response_data = {
            "status_code": None,
            "content": element.model_dump()
        }

        self.write(response_data)


    def partial_update(self, pk: Any=None, *args: tuple[Any], **kwargs: dict[Any, Any]):
        """..."""

        element = self.manager.update(pk, self.arguments)

        response_data = {
            "status_code": None,
            "content": element.model_dump()
        }

        self.write(response_data)


    def destroy(self, pk: Any=None, *args: tuple[Any], **kwargs: dict[Any, Any]):
        """..."""

        self.manager.delete(pk)

        response_data = {
            "status_code": None,
            "content": None
        }

        self.write(response_data)