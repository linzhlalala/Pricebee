from rest_framework import serializers
from .models import item
 
class itemSerializer(serializers.ModelSerializer):
     class Meta:
        model = item
        fields = ('category_level_1', 'category_level_1_ID',
            'category_level_2','category_level_2_ID','item_image_url','item_title',
            'item_partID','item_itemID','item_url','item_brand','item_name',
            'item_original_price','item_size','item_unit_price','item_discount_type',
            'item_discount_price','item_discount_text','item_discount_save','item_source')