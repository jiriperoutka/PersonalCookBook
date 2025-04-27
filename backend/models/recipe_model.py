# --- Importy ---

# Pydantic pro datové modely s validací a serializací (např. při práci s FastAPI)
from pydantic import BaseModel, Field

# Typování: List, Optional, atd. pro jasné definování typů dat ve třídách
from typing import List, Optional, Literal

# BSON ObjectId – specifický typ ID používaný v MongoDB (např. _id v dokumentech)
from bson import ObjectId

# BaseModel je základní třída pro datové modely, která:
# 	•	Zajišťuje validaci dat
# 	•	Automaticky řeší převod mezi Python typy a JSON (serializace)
# 	•	Umožňuje použít typování (např. str, int, List[str], atd.)
# 	•	Hodí se výborně pro FastAPI – používá Pydantic modely jako vstup

# Helper to work with ObjectId in Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Ingredient(BaseModel):
    name: str
    amount: str

class Step(BaseModel):
    text: str
    type: Literal["regular", "important", "info"] = "regular" #může nabývat pouze těchto hodnot, default je Regular
    order: int

class RecipeModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    title: str
    description: Optional[str]
    ingredients: List[Ingredient]
    steps: List[Step]
    tags: Optional[List[str]] = []
    created_by: Optional[PyObjectId] = None
    created_at: Optional[str] = None
    image_data: Optional[str] = None  # base64 encoded image

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}