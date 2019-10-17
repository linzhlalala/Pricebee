from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.

#Csv structure
#['l1name','l1id','l2name','l2id','ImgAddr','Title','PartID','ItemID',
# 'Link','Brand','Name','OrgPrice','Size','UnitPrice',
# 'DscType','DscPrice','DscText','PrcSav']
class ImportFile(models.Model):
    
    file = models.FileField(null=True)
    file_name = models.CharField(verbose_name = 'source',max_length=50)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DATA_FILE'

    def __str__(self):
        return self.file_name
    

class item(models.Model):
    category_level_1 = models.CharField(max_length = 50,blank=True)
    category_level_1_ID = models.CharField(max_length = 50,blank=True)
    category_level_2 = models.CharField(max_length = 50,blank=True)
    category_level_2_ID = models.CharField(max_length = 50,blank=True)
    item_image_url = models.CharField(max_length = 255,blank=True)
    item_title = models.CharField(max_length=255)
    item_partID = models.CharField(max_length=50,blank=True)
    item_itemID = models.CharField(max_length = 50,blank=True)
    item_url = models.CharField(max_length = 255)
    item_brand = models.CharField(max_length=50)
    item_name = models.CharField(max_length=255)
    item_original_price = models.FloatField(null=True)
    item_size = models.CharField(max_length=50,null=True,blank=True)
    item_unit_price = models.CharField(max_length=50,null=True,blank=True)
    item_discount_type = models.CharField(max_length=50,null=True,blank=True)
    item_discount_price = models.FloatField(null=True)
    item_discount_text = models.CharField(max_length=50,null=True,blank=True)
    item_discount_save = models.CharField(max_length=50,null=True,blank=True)
    item_dataset = models.ForeignKey(ImportFile,
        on_delete=models.CASCADE,blank=True,null=True,default=None)
    item_source = models.CharField(max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = 'ITEM'#coles only now
    def __str__(self):
        return self.item_brand + self.item_name+ self.item_size

'''
@receiver(pre_delete, sender=ImportFile)
def delete_file(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.file:
        instance.file.delete(False)
'''
