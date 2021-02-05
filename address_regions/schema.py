from graphene import relay, ObjectType

from graphene_django import DjangoObjectType
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

from address_regions.models import Region

class RegionNode(DjangoObjectType):
    class Meta:
        model = Region
        fields = ("zipcode", "district", "city", "province")
        filter_fields = ["zipcode", "district", "city", "province", "language_code"]
        interfaces = (relay.Node, )


class RegionQueries(ObjectType):
    region = relay.Node.Field(RegionNode)
    regions = DjangoFilterConnectionField(RegionNode)
