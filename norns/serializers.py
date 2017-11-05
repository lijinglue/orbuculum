from rest_framework import serializers
from .models import *


class CharacterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    avatar = models.CharField()

    class Meta:
        model = Character
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class DialogueSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model = Dialogue
        fields = '__all__'


class CharacterRelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterRel
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    characterRels = CharacterRelSerializer(many=True)
    class Meta:
        model = Player
        fields = '__all__'


