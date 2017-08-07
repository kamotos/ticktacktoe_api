from rest_framework import routers

from ticktacktoe_api.game.api.viewsets import ActionViewSet, GameViewSet

router = routers.SimpleRouter()
router.register(r'games', GameViewSet)
router.register(r'actions', ActionViewSet)
urlpatterns = router.urls
