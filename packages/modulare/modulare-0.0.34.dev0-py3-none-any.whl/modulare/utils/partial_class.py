from typing import Optional, Type
from pydantic import BaseModel, create_model

def PartialClass(cls: Type[BaseModel]) -> Type[BaseModel]:
    annotations = cls.__annotations__
    
    fields = {
        name: (Optional[annotation], None)
        for name, annotation in annotations.items()
    }
    
    return create_model(f'Partial{cls.__name__}', **fields)