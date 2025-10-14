from typing import Generic, TypeVar

from pydantic import BaseModel

from core.db.base_model import Base


  
DBModel = TypeVar("Model", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)


class BaseDataMapper(Generic[DBModel, Schema]):
    model: type[DBModel]
    schema: type[Schema]
    
    @classmethod
    def map_to_domain_entity(cls, data: DBModel) -> Schema:
        """ Преобразование модели в схему  """
        return cls.schema.model_validate(data)
    
    @classmethod
    def map_to_persistence_entity(cls, data: Schema) -> DBModel:
        """ Преобразование схемы в модель """
        return cls.model(**data.model_dump())
    
    @classmethod
    def map_to_dict(cls, data: Schema, **filters):
        """ Преобразование схемы в словарь """
        return cls.schema.model_dump(data, **filters)