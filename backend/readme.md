# Django rest framework backend 
## with key files only
1. model 
- item (product)
- importfile(to import items)
2. admin 
- item(add action delete all)
- importfile(override save_model to call importcsv)
- importcsv(read csv in mem and add to cloud sql)
3. view
- serializer(form result to JSON)
- Rest Framework API(response requests)
