from .models import item 
import csv
from io import TextIOWrapper

#Csv structure
#['l1name','l1id','l2name','l2id',
#'ImgAddr','Title','PartID','ItemID',
#'Link','Brand','Name','OrgPrice','Size','UnitPrice',
#'DscType','DscPrice','DscText','PrcSav']
#database structure
#['category_level_1','category_level_1_ID','category_level_2','category_level_2_ID',
# 'item_image_url','item_title','item_partID','item_itemID',
# 'item_url','item_brand','item_name','item_original_price','item_size','item_unit_price',
# 'item_discount_type','item_discount_price','item_discount_text','item_discount_save']

def import_data_csv(request,obj):
    try:
        sqllist = []
        f = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
        reader = csv.DictReader(f)
        for row in reader:
            if row['Name'] == '' or row['Name'] == 'Name': 
                break
            newitem = item(
                category_level_1 = row['l1name'],
                category_level_1_ID = row['l1id'],
                category_level_2 = row['l2name'],
                category_level_2_ID = row['l2id'],
                item_image_url = row['ImgAddr'],
                item_title = row['Title'],
                item_partID = row['PartID'],
                item_itemID = row['ItemID'],
                item_url = row['Link'],
                item_brand = row['Brand'],
                item_name = row['Name'],
                item_original_price = row['OrgPrice'] or None,
                item_size = row['Size'],
                item_unit_price = row['UnitPrice'],
                item_discount_type = row['DscType'],
                item_discount_price = row['DscPrice'] or None,
                item_discount_text = row['DscText'],
                item_discount_save = row['PrcSav'],
                item_dataset = obj or None,
                item_source = obj.file_name or None
            )
            #newitem.save()
            sqllist.append(newitem)
        item.objects.bulk_create(sqllist)
        return True
    except Exception as e:
        print(str(e))
        return False

