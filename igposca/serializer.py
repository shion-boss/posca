from rest_framework import serializers
from .models import taged_data


class taged_data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = taged_data
        fields = ('igname', 'top_img_url','main_img_url','text','page_url')
