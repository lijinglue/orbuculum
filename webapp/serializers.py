from rest_framework import serializers
from accounts.serializers import RespUserSerializer
from .models import *
from constance import config


# from django.contrib.auth.models import User


class PositionSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(min_value=config.MINIMUM_POSITION, required=True)
    is_cleared = serializers.BooleanField(read_only=True)
    payoff = serializers.FloatField(read_only=True)

    class Meta:
        model = Position
        fields = ('id', 'amount', 'is_cleared', 'payoff')


class AccountSerializer(serializers.ModelSerializer):
    # positions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    positions = PositionSerializer(many=True)
    owner = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    balance = serializers.FloatField(default=1000.0, read_only=True)
    isActive = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'owner', 'balance', 'isActive', 'positions', 'created')


class TopAccountSerializer(serializers.ModelSerializer):
    owner = RespUserSerializer()
    profit = serializers.FloatField(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'owner', 'profit')


class OptionReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'content')


class OptionRespSerializer(serializers.ModelSerializer):
    option_bucket = serializers.FloatField()

    class Meta:
        model = Option
        fields = ('id', 'content', 'option_bucket')


class PredictionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')
    options = OptionReqSerializer(many=True)

    def create(self, validated_data):
        options_json = validated_data.pop('options')
        prediction = Prediction.objects.create(**validated_data)
        options = [Option.objects.create(content=op['content'], prediction=prediction) for op in options_json]
        return prediction

    class Meta:
        model = Prediction
        fields = ('id', 'owner', 'content', 'start_at', 'created', 'options', 'status')
