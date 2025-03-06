from rest_framework.decorators import action
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ItemType, InventoryItem, Location, ItemLocationAssignment, ItemAssociation
from .serializers import (
    ItemTypeSerializer,
    InventoryItemSerializer,
    LocationSerializer,
    ItemLocationAssignmentSerializer,
    ItemAssociationSerializer,
    UserRegisterSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework import permissions
from django.utils.timezone import now
import csv
from django.http import HttpResponse
from django.db.models import Count, Sum, Q

class InventoryStatsView(APIView):
    """
    Отчет по статистике инвентаря:
    - Общее число предметов
    - Число активных предметов
    - Статистика по типам предметов (количество и суммарная стоимость)
    - Статистика по локациям (число активных назначений)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        # Общее число предметов
        total_items = InventoryItem.objects.count()
        # Число активных предметов: имеющих хотя бы одно активное назначение
        active_items = InventoryItem.objects.filter(assignments__removed_at__isnull=True).distinct().count()
        
        # Статистика по типам: фильтруем только активные предметы, группируем по типу
        items_by_type = list(
            InventoryItem.objects.filter(is_active=True)
            .values('item_type__name')
            .annotate(
                count=Count('id'),
                total_cost=Sum('cost')
            )
        )
        
        # Статистика по локациям: для каждой локации считаем число активных назначений
        items_by_location = list(
            Location.objects.annotate(
                active_items_count=Count('assignments', filter=Q(assignments__removed_at__isnull=True))
            ).values('name', 'active_items_count')
        )
        
        data = {
            'total_items': total_items,
            'active_items': active_items,
            'items_by_type': items_by_type,
            'items_by_location': items_by_location,
        }
        return Response(data)

class IsInventoryManagerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ на чтение для аутентифицированных пользователей,
    а на изменение – только для пользователей, входящих в группу 'inventory_manager'.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.groups.filter(name='inventory_manager').exists()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []  # доступ открыт для всех

class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'serial_number']
    permission_classes = [IsInventoryManagerOrReadOnly]

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """
        Возвращает историю перемещений данного предмета.
        Для каждого назначения возвращаются данные о локации, дате назначения и, если применимо, дате снятия.
        """
        item = self.get_object()
        # Получаем все назначения (и активные, и снятые) для данного предмета, сортируя по дате назначения (новейшие первыми)
        assignments = item.assignments.all().order_by('-assigned_at')
        serializer = ItemLocationAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        try:
            item = self.get_object()
            new_location_id = request.data.get('location_id')
            if not new_location_id:
                return Response({"error": "Необходимо указать location_id."}, status=400)
            try:
                new_location = Location.objects.get(id=new_location_id)
            except Location.DoesNotExist:
                return Response({"error": "Локация не найдена."}, status=404)
            
            # Ищем любую запись для данной пары (активную или снятую)
            existing_assignment = item.assignments.filter(location=new_location).first()
            
            if existing_assignment:
                if existing_assignment.removed_at is None:
                    # Если уже активна для новой локации, снимаем все остальные активные назначения и возвращаем сообщение
                    active_assignments = item.assignments.filter(removed_at__isnull=True).exclude(id=existing_assignment.id)
                    for assignment in active_assignments:
                        assignment.remove_from_location()
                    return Response({"message": "Предмет уже находится в данной локации."}, status=200)
                else:
                    # Если запись существует, но не активна, обновляем её
                    existing_assignment.removed_at = None
                    existing_assignment.assigned_at = now()
                    existing_assignment.save()
                    # Снимаем все остальные активные назначения
                    active_assignments = item.assignments.filter(removed_at__isnull=True).exclude(id=existing_assignment.id)
                    for assignment in active_assignments:
                        assignment.remove_from_location()
                    serializer = ItemLocationAssignmentSerializer(existing_assignment)
                    return Response(serializer.data)
            else:
                # Если для новой локации записи нет, снимаем все активные назначения
                active_assignments = item.assignments.filter(removed_at__isnull=True)
                for assignment in active_assignments:
                    assignment.remove_from_location()
                # Создаем новое назначение
                new_assignment = ItemLocationAssignment.objects.create(item=item, location=new_location)
                serializer = ItemLocationAssignmentSerializer(new_assignment)
                return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)





# Новый класс для экспорта инвентаря в CSV
class InventoryExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        # Получаем все предметы инвентаря
        items = InventoryItem.objects.all()
        
        # Создаем HTTP-ответ с типом контента CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory_export.csv"'
        
        writer = csv.writer(response)
        # Записываем заголовок CSV
        writer.writerow(['ID', 'Название', 'Серийный номер', 'Тип предмета', 'Текущее местоположение', 'Дата назначения'])
        
        for item in items:
            # Определяем активное назначение (если существует)
            active_assignment = item.assignments.filter(removed_at__isnull=True).first()
            if active_assignment:
                current_location = active_assignment.location.name
                assigned_at = active_assignment.assigned_at
            else:
                current_location = ''
                assigned_at = ''
            writer.writerow([
                item.id,
                item.name,
                item.serial_number or '',
                item.item_type.name,
                current_location,
                assigned_at,
            ])
        return response


    



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

class ItemLocationAssignmentViewSet(viewsets.ModelViewSet):
    queryset = ItemLocationAssignment.objects.all()
    serializer_class = ItemLocationAssignmentSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        """
        Кастомное действие для "снятия" привязки предмета от локации.
        Вызывает метод remove_from_location у модели, если привязка активна.
        """
        assignment = self.get_object()
        if assignment.removed_at is None:
            assignment.remove_from_location()
            return Response({
                "status": "removed",
                "removed_at": assignment.removed_at,
            })
        return Response({
            "status": "already removed"
        }, status=400)

class ItemAssociationViewSet(viewsets.ModelViewSet):
    queryset = ItemAssociation.objects.all()
    serializer_class = ItemAssociationSerializer
    permission_classes = [IsInventoryManagerOrReadOnly]

# Отчёты по локациям остаются без изменений
class LocationReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        report_data = []
        locations = Location.objects.all()
        for loc in locations:
            assignments = loc.assignments.filter(removed_at__isnull=True)
            items = []
            for assignment in assignments:
                item = assignment.item
                items.append({
                    "id": item.id,
                    "name": item.name,
                    "serial_number": item.serial_number,
                    "item_type": item.item_type.name,
                })
            report_data.append({
                "location": loc.name,
                "description": loc.description,
                "items": items
            })
        return Response(report_data)

class FullLocationReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        report_data = []
        locations = Location.objects.all()
        for loc in locations:
            active_assignments = loc.assignments.filter(removed_at__isnull=True)
            removed_assignments = loc.assignments.filter(removed_at__isnull=False)
            active_items = []
            for assignment in active_assignments:
                item = assignment.item
                active_items.append({
                    "id": item.id,
                    "name": item.name,
                    "serial_number": item.serial_number,
                    "item_type": item.item_type.name,
                    "assigned_at": assignment.assigned_at,
                })
            removed_items = []
            for assignment in removed_assignments:
                item = assignment.item
                removed_items.append({
                    "id": item.id,
                    "name": item.name,
                    "serial_number": item.serial_number,
                    "item_type": item.item_type.name,
                    "assigned_at": assignment.assigned_at,
                    "removed_at": assignment.removed_at,
                })
            report_data.append({
                "location": loc.name,
                "description": loc.description,
                "active_items": active_items,
                "removed_items": removed_items,
                "active_count": active_assignments.count(),
                "removed_count": removed_assignments.count(),
            })
        return Response(report_data)

class InventoryImportView(APIView):
    """
    API для массового импорта инвентарных предметов из CSV-файла.
    Ожидается, что CSV-файл содержит заголовки:
    name, serial_number, item_type, description, purchase_date, cost, is_active
    """
    permission_classes = [IsInventoryManagerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "Файл не найден в запросе"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
        except Exception as e:
            return Response({"error": f"Ошибка обработки файла: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        errors = []
        created_items = []
        for i, row in enumerate(reader):
            try:
                # Обязательное поле item_type: ищем по названию
                item_type_name = row.get('item_type')
                if not item_type_name:
                    raise ValueError("Отсутствует значение item_type")
                item_type = ItemType.objects.filter(name=item_type_name).first()
                if not item_type:
                    raise ValueError(f"Тип '{item_type_name}' не найден")
                
                # Создаем предмет; поля purchase_date и cost могут потребовать дополнительной обработки
                item = InventoryItem.objects.create(
                    name=row.get('name'),
                    serial_number=row.get('serial_number'),
                    inventory_number=row.get('inventory_number'),
                    item_type=item_type,
                    description=row.get('description', ''),
                    purchase_date=row.get('purchase_date') or None,
                    cost=row.get('cost') or None,
                    is_active=str(row.get('is_active', 'True')).lower() == 'true'
                )
                created_items.append(item.id)
            except Exception as e:
                print("Ошибка при обработке CSV:", e)
                errors.append({"row": i+1, "error": str(e)})
        
        data = {
            "created_items": created_items,
            "errors": errors
        }
        # Если есть ошибки, возвращаем статус 207 (Multi-Status), иначе 201 Created
        return Response(data, status=status.HTTP_201_CREATED if not errors else status.HTTP_207_MULTI_STATUS)

from django.utils.timezone import now

class BulkTransferView(APIView):
    permission_classes = [IsInventoryManagerOrReadOnly]

    def post(self, request, format=None):
        item_ids = request.data.get("item_ids")
        location_id = request.data.get("location_id")

        if not item_ids or not isinstance(item_ids, list) or not location_id:
            return Response({"error": "Нужно указать список item_ids и location_id."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            new_location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return Response({"error": "Локация не найдена."}, status=status.HTTP_404_NOT_FOUND)

        transferred = []
        errors = []
        for item_id in item_ids:
            try:
                item = InventoryItem.objects.get(id=item_id)
                
                # Найдем активное назначение для новой локации (если оно есть)
                existing_assignment = item.assignments.filter(location=new_location).first()
                if existing_assignment:
                    if existing_assignment.removed_at is None:
                        # Уже активное назначение для новой локации
                        # При этом снимем все остальные активные назначения
                        item.assignments.filter(removed_at__isnull=True).exclude(id=existing_assignment.id).update(removed_at=now())
                        transferred.append(item_id)
                        continue
                    else:
                        # Если запись существует, но неактивна – обновляем её
                        existing_assignment.removed_at = None
                        existing_assignment.assigned_at = now()
                        existing_assignment.save()
                        # Снимаем все остальные активные назначения
                        item.assignments.filter(removed_at__isnull=True).exclude(id=existing_assignment.id).update(removed_at=now())
                        transferred.append(item_id)
                        continue

                # Если записи для новой локации нет, снимаем все активные назначения
                active_assignments = item.assignments.filter(removed_at__isnull=True)
                if active_assignments.exists():
                    active_assignments.update(removed_at=now())
                
                # Создаем новое назначение для новой локации
                new_assignment = ItemLocationAssignment.objects.create(item=item, location=new_location)
                transferred.append(item_id)
            except InventoryItem.DoesNotExist:
                errors.append({"item_id": item_id, "error": "Предмет не найден"})
            except Exception as e:
                errors.append({"item_id": item_id, "error": str(e)})
        data = {
            "transferred": transferred,
            "errors": errors
        }
        return Response(data, status=status.HTTP_200_OK)
