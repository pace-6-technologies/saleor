import graphene
from django.utils.translation import gettext as _

from ...core.permissions import ProductPermissions
from ..core.fields import FilterInputConnectionField
from ..decorators import permission_required
from .filters import ImportFileFilterInput

from .mutations import CSVUpload
from .sorters import ImportFileSortingInput
from .types import ImportFile
from .sorters import ImportFileSortingInput

from csv_import import ImportTypes
from csv_import import models


class CsvUploadQueries(graphene.ObjectType):
    csv_upload_file = graphene.Field(
        ImportFile,
        id=graphene.Argument(
            graphene.ID, description="ID of the import file job.", required=True
        ),
        description="Look up a import file by ID.",
    )
    csv_upload_files = FilterInputConnectionField(
        ImportFile,
        filter=ImportFileFilterInput(description="Filtering options for import files."),
        sort_by=ImportFileSortingInput(description="Sort import files."),
        description="List of import files.",
    )

    @permission_required(ProductPermissions.MANAGE_PRODUCTS)
    def resolve_csv_upload_file(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, ImportFile)

    @permission_required(ProductPermissions.MANAGE_PRODUCTS)
    def resolve_csv_upload_files(self, info, query=None, sort_by=None, **kwargs):
        return models.ImportFile.objects.all()

class CsvUploadTypeQueries(graphene.ObjectType):
    csv_import_types = graphene.List(graphene.JSONString)

    @permission_required(ProductPermissions.MANAGE_PRODUCTS)
    def resolve_csv_import_types(self, info): 
        return [(c[0], _(c[1])) for c in ImportTypes.CHOICES]

class CsvUploadMutations(graphene.ObjectType):
    csv_upload = CSVUpload.Field()

