import graphene
from saleor.graphql.core.enums import to_enum

from .import ImportTypes, FileTypes, ImportEvents

ImportEventEnum = to_enum(ImportEvents)
ImportTypeEnum = to_enum(ImportTypes)
FileTypeEnum = to_enum(FileTypes)

