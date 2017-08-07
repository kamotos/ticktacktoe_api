from django.contrib.postgres.fields import JSONField
from django.db import models
# Create your models here.
from django.utils.functional import cached_property
from model_utils import Choices
from model_utils.models import TimeStampedModel

from ticktacktoe_api.game.defaults import get_default_state

PLAYER = Choices(
    ('a', 'Player A'),
    ('b', 'Player B'),
)

NEXT_PLAYER = {
    'a': 'b',
    'b': 'a',
}

WINNING_ACTIONS = (
    {1, 2, 3}, {4, 5, 6}, {7, 8, 9},  # Horizontal wins
    {1, 4, 7}, {2, 5, 8}, {3, 6, 9},  # Vertical wins
    {1, 5, 9}, {3, 5, 7}  # Diagonal wins
)


def get_player_actions(game, player):
    """
    Returns player's actions for a game.

    :param game: game.models.Game
    :param player: string
    :rtype: set
    """
    qs = game.action_set.filter(player=player)
    return set(list(qs.values_list('box', flat=True)))


class Game(TimeStampedModel):
    current_state = JSONField(default=get_default_state)
    winner = models.CharField(choices=PLAYER, null=True, blank=True, max_length=1)

    class JSONAPIMeta:
        resource_name = "games/"

    def next_player(self):
        if self.winner:
            return
        last_action = self.action_set.last()
        if not last_action:
            return PLAYER.a
        return NEXT_PLAYER[last_action.player]

    def get_last_player(self):
        return getattr(self.action_set.last(), 'player', None)

    @cached_property
    def game_state(self):
        state = get_default_state()
        for action in self.action_set.all():
            state[action.box] = action.player
        return state

    def game_log(self):
        return map(str, self.action_set.all())


class Action(TimeStampedModel):
    game = models.ForeignKey(Game)
    box = models.SmallIntegerField(choices=Choices(*range(1, 10)))
    player = models.CharField(choices=PLAYER, db_index=True, max_length=1)
    is_winning_move = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('game', 'box'),
        )

    class JSONAPIMeta:
        resource_name = "actions/"

    def __str__(self):
        if self.is_winning_move:
            return "Player {0.player} won by playing the box {0.box}".format(self)
        return "Player {0.player} played the box {0.box}".format(self)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.decide_winner()
        return instance

    def decide_winner(self):
        """
        :rtype: bool
        """
        if self.game.winner is not None:
            return False
        player_actions = get_player_actions(self.game, self.player)
        if any((player_actions.issuperset(winning_action)
                for winning_action in WINNING_ACTIONS)):
            self.game.winner = self.player
            self.game.save(update_fields=['winner'])
            self.is_winning_move = True
            self.save()
            return True
        return False
