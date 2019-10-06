import time
import csv

def searchItemInDB(word,product_list):
    '''
    csv database instruction
    ['l1name','l1id','l2name','l2id','ImgAddr','Title','PartID','ItemID',
    'Link','Brand','Name','OrgPrice','Size','UnitPrice','DscType','DscPrice','DscText','PrcSav']
    '''
    totaltimestart = time.time()
    #prepare the word
    keywordset = word.lower().split(' ')
    keywordnum = len(keywordset)

    #get to file
    itemfilename = 'data/clsitem.csv'
    #itemlist = []
    with open(itemfilename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            l1name = row['l1name']
            l2name = row['l2name']
            Brand = row['Brand']
            Name = row['Name']
            Size = row['Size']
            
            matchbox = "{0} {1} {2} {3} {4} \n".format(l1name,l2name,Brand,Name,Size)
            matchbox = matchbox.lower()
            #searching logic every word in keyword must appear
            appearnum = 0
            for sw in keywordset:
                if sw in matchbox:
                    appearnum += 1
            if appearnum == keywordnum:
                '''
                del row['l1name']
                del row['l2name']
                del row['l1id']
                del row['l2id']
                product_list.append(row)
                '''
                product = {'title': row['Title'], 
                        'price': row['DscPrice'], 
                        'link': row['DscText'], 
                        'store': row['UnitPrice'], 
                        'referer': 'coles'}
                if product['price'] != '':
                    product_list.append(product)
                
    totaltimeend= time.time()
    totaltime = totaltimeend-totaltimestart
    print("COLES:SUM ITEM:{0} , TIME:{1}s".format(len(product_list),totaltime))
    return

if __name__ == '__main__':
    keyword = ''
    result = []
    while keyword!= 'quit':
        keyword = input('enter keyword:')
        
        if keyword !='show' :
            result = []
            searchItemInDB(keyword,result)
        else:
            print(result)

#wait 
