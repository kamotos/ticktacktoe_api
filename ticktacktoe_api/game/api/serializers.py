# from rest_framework import serializers
from rest_framework_json_api import serializers

from rest_framework.exceptions import ValidationError

from ticktacktoe_api.game.models import Game, Action, PLAYER


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'created', 'modified', 'winner', 'next_player',
                  'game_state', 'game_log')
        read_only_fields = ('id', 'created', 'modified', 'winner')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('__str__', 'game', 'box', 'player', 'is_winning_move')
        read_only_fields = ('is_winning_move', )

    def validate(self, attrs):
        self.validate_player_turn(attrs)
        return super().validate(attrs)

    def validate_player_turn(self, attrs):
        player = attrs['game'].get_last_player()
        if player == attrs['player'] and player is not None:
            player_turn = 'a' if attrs['player'] == 'b' else 'b'
            raise ValidationError("It's player's '%s' turn" % player_turn)

    def validate_game(self, game):
        if game and game.winner in PLAYER:
            raise ValidationError('game has ended')
        return game
