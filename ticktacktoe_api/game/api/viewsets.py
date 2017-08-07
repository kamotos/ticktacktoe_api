from rest_framework import mixins, viewsets

from ticktacktoe_api.game.api.serializers import GameSerializer, ActionSerializer
from ticktacktoe_api.game.models import Game, Action


class GameViewSet(mixins.CreateModelMixin,
                  viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class ActionViewSet(mixins.CreateModelMixin,
                    viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
