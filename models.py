from pydantic import BaseModel, ValidationInfo, Field, model_validator, ConfigDict
from typing import Annotated, List, Dict, Union
from pydantic.v1.typing import is_none_type

TypeStr = Annotated[str | None, Field(default=None)]
TypeBool = Annotated[bool | None, Field(default=None)]
TypeInt = Annotated[int | None, Field(default=None)]

class Objects(BaseModel):
    total: Union[int, None] = Field(default=0, ge=0)
    objectIDs: Union[List[int], None] = Field(default=[])


    @model_validator(mode="after")
    def check_length_of_object(self, info: ValidationInfo):
        context = str(info.context)
        if (is_none_type(self.total) + is_none_type(self.objectIDs)) > 0:
            return self
        if "search" in context:
            index_limit = context.find("limit")
            if index_limit == -1:
                count_1 = 100
            else:
                count_1 = ""
                first_symbol_is_alpha = True
                for i in range(0, 4):
                    if (len(context) > (index_limit + 6 + i)) and (context[index_limit + 6 + i].isdigit()):
                        if i == 0:
                            first_symbol_is_alpha = False
                        count_1 += context[index_limit + 6 + i]
                count_1 = int("0" + count_1)
                if count_1 > 500:
                    count_1 = 500
                if (count_1 == 0) or first_symbol_is_alpha:
                    count_1 = 100
            if (self.total == len(self.objectIDs)) or (self.total >= count_1):
                return self
        else:
            if self.total == len(self.objectIDs):
                return self
        raise ValueError("Количество общедоступных объектов не совпадает с фактическим количеством")

class DepartmentsPart(BaseModel):
    departmentId: TypeInt
    displayName: TypeStr

class Departments(BaseModel):
    departments: Union[List[DepartmentsPart], None] = Field(default=None)

class Message(BaseModel):
    message: TypeStr

class ObjectDimensionsParsed:
    element: TypeStr
    dimensionType: TypeStr
    dimension: Union[float, int, None] = Field(default=None)

class ObjectTags(BaseModel):
    term: TypeStr
    AAT_URL: TypeStr
    Wikidata_URL: TypeStr

class ObjectConstituents(BaseModel):
    constituentID: TypeInt
    role: TypeStr
    name: TypeStr
    constituentULAN_URL: TypeStr
    constituentWikidata_URL: TypeStr
    gender: TypeStr

class ObjectMeasurements(BaseModel):
    elementName: TypeStr
    elementDescription: TypeStr
    elementMeasurements: Union[Dict[str, Union[int, float, None]], None] = Field(default=None)

class Object(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    objectID: int = Field(gt=0) #Не может быть None
    isHighlight: TypeBool
    accessionNumber: TypeStr
    accessionYear: TypeStr
    isPublicDomain: TypeBool
    primaryImage: TypeStr
    primaryImageSmall: TypeStr
    additionalImages: Union[List[str], None] = Field(default=None)
    constituents: Union[List[ObjectConstituents], None] = Field(default=None)
    department: TypeStr
    objectName: TypeStr
    title: TypeStr
    culture: TypeStr
    period: TypeStr
    dynasty: TypeStr
    reign: TypeStr
    portfolio: TypeStr
    artistRole: TypeStr
    artistPrefix: TypeStr
    artistDisplayName: TypeStr
    artistDisplayBio: TypeStr
    artistSuffix: TypeStr
    artistAlphaSort: TypeStr
    artistNationality: TypeStr
    artistBeginDate: TypeStr
    artistEndDate: TypeStr
    artistGender: TypeStr
    artistWikidata_URL: TypeStr
    artistULAN_URL: TypeStr
    objectDate: TypeStr
    objectBeginDate: TypeInt
    objectEndDate: TypeInt
    medium: TypeStr
    dimensions: TypeStr
    dimensionsParsed: Union[List[ObjectDimensionsParsed], None] = Field(default=None)
    measurements: Union[List[ObjectMeasurements], None] = Field(default=None)
    creditLine: TypeStr
    geographyType: TypeStr
    city: TypeStr
    state: TypeStr
    county: TypeStr
    country: TypeStr
    region: TypeStr
    subregion: TypeStr
    locale: TypeStr
    locus: TypeStr
    excavation: TypeStr
    river: TypeStr
    classification: TypeStr
    rightsAndReproduction: TypeStr
    linkResource: TypeStr
    metadataDate: TypeStr
    repository: TypeStr
    objectURL: TypeStr
    tags: Union[List[ObjectTags], None] = Field(default=None)
    objectWikidata_URL: TypeStr
    isTimelineWork: TypeBool
    GalleryNumber: TypeStr

    @model_validator(mode="after")
    def check_begin_end_date(self):
        if (is_none_type(self.artistEndDate) + is_none_type(self.artistBeginDate) + is_none_type(self.objectEndDate) + is_none_type(self.objectBeginDate)) > 0:
            return self
        if (int(self.artistEndDate + "0") - int(self.artistBeginDate + "0")) >= 0 and (int(self.objectEndDate) - int(self.objectBeginDate)) >= 0:
            return self
        elif self.artistEndDate == "":
            return self
        raise ValueError("Год окончания не может быть меньше года начала")
