"""
...
"""

from typing import TYPE_CHECKING, Any, Optional

from sqlmodel import Session, select

if TYPE_CHECKING:
    from .models import BaseModel


class BaseManager:
    """..."""
    
    model: Optional["BaseModel"]

    def __init__(
        self,
        database: Any,
        model: Optional["BaseModel"]=None
    ) -> None:
        """..."""

        if model:
            self.model = model
        
        if not database:
            raise Exception("session should be set")

        self.session: Session = Session(database)


    def filter(
        self,
        data: dict[Any, Any]={},
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> "BaseModel":
        """..."""

        result = self.get().all()
        self.session.close()

        return result
        

    def create(
        self,
        data: dict[Any, Any],
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ) -> "BaseModel":
        """..."""
 
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        self.session.close()

        return instance

    
    def create_bulk(
        self,
        ids: list[int],
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """ ... """
        
        raise NotImplementedError()


    def get(
        self,
        pk: int|None = None,
        data: dict[Any, Any]={},
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """..."""

        statement = select(self.model)
        if pk:
            statement = statement.where(self.model.id == pk)

        result = self.session.exec(statement)

        return result
    
    def read(
        self,
        pk: int,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """..."""

        result = self.get(pk).one()
        self.session.close()

        return result


    def update(
        self,
        pk: int,
        data: dict[Any, Any],
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """..."""

        result = self.get(pk).one()

        for key, value in data.items():
            setattr(result, key, value)
        
        self.session.commit()
        self.session.refresh(result)
        self.session.close()

        return result
    
    def update_bulk(
        self,
        ids: list[int],
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """ ... """

        raise NotImplementedError()


    def delete(
        self, pk: int,
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """..."""

        result = self.get(pk).one()

        self.session.delete(result)
        self.session.commit()
        self.session.close()


    def delete_bulk(
        self,
        ids: list[int],
        *args: tuple[Any],
        **kwargs: dict[Any, Any]
    ):
        """ ... """

        raise NotImplementedError()