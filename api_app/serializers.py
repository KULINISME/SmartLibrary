from rest_framework import serializers
from .models import Buku, Anggota

class BukuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buku
        fields = ['id', 'judul', 'penulis', 'isbn', 'stok_tersedia']

class AnggotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anggota
        fields = ['nim', 'nama', 'status_aktif']