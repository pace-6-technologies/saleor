import graphene
from django.core.exceptions import ValidationError

from saleor.core.permissions import ProductPermissions
from saleor.product import models
from saleor.product.error_codes import ProductErrorCode
from saleor.graphql.channel import ChannelContext
from saleor.graphql.core.mutations import BaseMutation, ModelMutation
from saleor.graphql.core.types import Upload
from saleor.graphql.core.types.common import UploadError
from saleor.graphql.decorators import permission_required
from saleor.graphql.decorators import staff_member_or_app_required

from saleor.core.permissions import ProductPermissions, ProductTypePermissions

from .types import ImportFile

from csv_import.enum import ImportTypeEnum
from csv_import.models import ImportFile as ImportFileModel

class CSVUpload(BaseMutation):
    import_file = graphene.Field(ImportFile)

    class Arguments:
        file = Upload(
            required=True, description="Represents a file in a multipart request."
        )
        import_type = ImportTypeEnum(description="Type of import file.", required=True)

    class Meta:
        description = (
            "Upload a csv file. This mutation must be sent as a `multipart` "
            "request. More detailed specs of the upload format can be found here: "
            "https://github.com/jaydenseric/graphql-multipart-request-spec"
        )
        permissions = (ProductPermissions.MANAGE_PRODUCTS,)
        error_type_class = UploadError
        error_type_field = "upload_errors"

    @classmethod
    @staff_member_or_app_required
    def perform_mutation(cls, _root, info, **data):
        content_file = info.context.FILES.get(data["file"])
        import_file = ImportFileModel(
            content_file=content_file,
            import_type=data["import_type"],
            user=info.context.user
        )
        import_file.save()
        return CSVUpload(import_file=import_file)
