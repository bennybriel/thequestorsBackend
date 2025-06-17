# views/base_viewset.py
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.response import Response
from rest_framework import status
from typing import Type
from ..services.base_service import BaseService

class BaseViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
):
    service_class: Type[BaseService]
    serializer_class = None

    def get_queryset(self):
        return self.service_class().get_all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.service_class().create(serializer.validated_data)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.service_class().get_by_id(kwargs['pk'])
        if not instance:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.service_class().get_by_id(kwargs['pk'])
        if not instance:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get current data for PUT requests
        if request.method == 'PUT':
            current_data = self.get_serializer(instance).data
            request_data = {**current_data, **request.data}
            serializer = self.get_serializer(instance, data=request_data, partial=False)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        
        try:
            updated_instance = self.service_class().update(
                kwargs['pk'],
                serializer.validated_data,
                partial=(request.method != 'PUT')
            )
            return Response(self.get_serializer(updated_instance).data)
        except ValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.service_class().get_by_id(kwargs['pk'])
        if not instance:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = self.service_class().update(kwargs['pk'], serializer.validated_data)
        return Response(self.get_serializer(updated_instance).data)

    def destroy(self, request, *args, **kwargs):
        if self.service_class().delete(kwargs['pk']):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)