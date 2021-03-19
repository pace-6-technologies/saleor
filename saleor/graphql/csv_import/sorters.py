import graphene

from ..core.types import SortInputObjectType


class ImportFileSortField(graphene.Enum):
    STATUS = ["status"]
    CREATED_AT = ["created_at"]
    UPDATED_AT = ["updated_at"]

    @property
    def description(self):
        if self.name in ImportFileSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort export file by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class ImportFileSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = ImportFileSortField
        type_name = "export file"
