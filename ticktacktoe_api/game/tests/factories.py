import factory


class GameFactory(factory.django.DjangoModelFactory):
    winner = None

    class Meta:
        model = 'game.Game'


class ActionFactory(factory.django.DjangoModelFactory):
    game = factory.SubFactory(GameFactory)
    box = factory.Iterator(range(1, 10))
    player = factory.Iterator(['a', 'b'])

    class Meta:
        model = 'game.Action'
