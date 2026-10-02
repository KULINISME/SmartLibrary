from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Buku, Anggota
from .serializers import BukuSerializer, AnggotaSerializer

class BukuViewSet(viewsets.ModelViewSet):
    queryset = Buku.objects.all()
    serializer_class = BukuSerializer

    # Custom Endpoint: Fitur pencarian buku berdasarkan judul (OPAC)
    @action(detail=False, methods=['get'])
    def cari(self, request):
        keyword = request.query_params.get('judul', None)
        if keyword:
            # Memanfaatkan B-tree index untuk pencarian cepat
            buku = Buku.objects.filter(judul__icontains=keyword)
            serializer = self.get_serializer(buku, many=True)
            return Response(serializer.data)
        return Response({"error": "Parameter 'judul' harus diisi"}, status=400)

class AnggotaViewSet(viewsets.ModelViewSet):
    queryset = Anggota.objects.all()
    serializer_class = AnggotaSerializer