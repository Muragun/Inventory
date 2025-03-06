from rest_framework import serializers
from .models import ItemType, InventoryItem, Location, ItemLocationAssignment, ItemAssociation

# Сериализаторы для уже существующих моделей ...
class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    # Вместо числового item_type – вернём его название
    item_type_name = serializers.ReadOnlyField(source='item_type.name')
    
    # Вернём название текущей локации, если назначение активно
    current_location = serializers.SerializerMethodField()

    def get_current_location(self, obj):
        active_assignment = obj.assignments.filter(removed_at__isnull=True).first()
        if active_assignment:
            return active_assignment.location.name
        return None

    class Meta:
        model = InventoryItem
        # Включаем нужные поля. 'item_type_name' и 'current_location' – виртуальные
        fields = [
            'id',
            'name',
            'serial_number',
            'inventory_number',
            'item_type',       # чтобы при создании/редактировании мы могли указывать тип
            'item_type_name',  # чтобы в ответе видеть название типа
            'description',
            'purchase_date',
            'cost',
            'is_active',
            'current_location' # чтобы в ответе видеть текущую локацию
        ]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ItemLocationAssignmentSerializer(serializers.ModelSerializer):
    location_name = serializers.ReadOnlyField(source='location.name')
    class Meta:
        model = ItemLocationAssignment
        fields = '__all__'

# Новый сериализатор для связей между предметами
class ItemAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAssociation
        fields = '__all__'

# Сериализатор для регистрации пользователей (без изменений)
from django.contrib.auth.models import User
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user



