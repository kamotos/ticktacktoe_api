from test_plus.test import TestCase

from .factories import GameFactory, ActionFactory


class GameAction(TestCase):
    def test__get_last_player_returns_none_if_no_actions(self):
        assert GameFactory().get_last_player() is None

    def test__get_last_player_returns_none_if_no_actions(self):
        action = ActionFactory()
        assert action.game.get_last_player() == action.player

