import requests 
#from selenium import webdriver 
from lxml import html 
import json
import time
import csv
def numb_only(text):
    #find styles: $2.0,$2.0kg,$ 2,$ 2.0
    strlist = text.replace("$ ","$").split(' ')
    for s in strlist:
        if ('$' in s and len(s) > 1) or '.' in s or '%' in s:
            return ''.join(list(filter(lambda ch: ch in '0123456789.',s)))         
    

def PLfromJson(dictctgr,jsonList,product_list):
    #list
    # All in Json Type
    n = 0
    jsondata = json.loads(jsonList)
    pr_list = jsondata["Bundles"]
    #get info 
    m=len(pr_list)
    categoryl1 = dictctgr['l1name']
    categoryl1id = dictctgr['l1id']
    categoryl2 = dictctgr['l2name']
    categoryl2id = dictctgr['l2id']

    for bk in pr_list:
        pName = bk['Name']
        #Mostly Under Product
        ProductL = bk['Products']
        for ProductNode in ProductL:
            n = n + 1
            try:            
                #Name   
                pInStock = ProductNode['IsInStock'] #check Stock,directly pass
                if pInStock == False:
                    #print('record {0},{1} No Stock,(╯‵□′)╯︵┻━┻'.format(n,pName))
                    continue

                pPartID = str(ProductNode['Stockcode']) 
                pItemID = ProductNode['Barcode']
                pImgAddr = ProductNode['LargeImageFile'] #in addr,switch small,medium,large
                pTitle  = ProductNode['Description']#Brand+name+size,often has <br>
                pTitle = pTitle.replace('<br>',' ') 
                pTitle = pTitle.replace('...',' ') 
                pLink = 'https://www.woolworths.com.au/shop/productdetails/{0}/'.format(pPartID)+ProductNode['UrlFriendlyName'] #not sure its working
                pBrand = ProductNode['Brand']
                pSize = ProductNode['PackageSize']
                pUnitPrice = ProductNode['CupString']
                pBrand = ProductNode['Brand']
                #price and disount
                pDscPrice = ProductNode['Price']
                pOrgPrice = ProductNode['WasPrice']

                #find special
                pDscType = "None"
                pDscText = ""
                pPrcSav = "0.00%"

                #Save directly
                if (pDscPrice != pOrgPrice):
                    pPrcSav = '{:.2%}'.format(1-float(pDscPrice)/float(pOrgPrice))

                    if (ProductNode['IsOnSpecial'] == True) and (ProductNode['InstoreIsOnSpecial'] == False):
                        pDscType = "SaveX OL"#Online Only
                        pDscText = pPrcSav+' off(Online Only)'
                    if (ProductNode['IsOnSpecial'] == True) and (ProductNode['InstoreIsOnSpecial'] == True):
                        pDscType = "SaveX"#
                        pDscText = pPrcSav+' off'
                pDscPrice = str(pDscPrice)
                pOrgPrice = str(pOrgPrice)
                #check centre tage
                centretag = ProductNode['CentreTag']['TagContent']
                if centretag != None:
                    selector =  html.fromstring(centretag)
                    pDscText = selector.xpath('//span/text()')[0].strip()
                    #Buy N for X  Example:4 for $20.00         
                    if "for" in pDscText:
                        pDscType = "buyNforN"
                        words = pDscText.split(' ')
                        tDscNumber = int(words[0])
                        tDscSum = float(numb_only(pDscText))
                        pDscPrice = str(tDscSum/tDscNumber)                   
                        pPrcSav = '{:.2%}'.format(1-float(pDscPrice)/float(pOrgPrice))
                    #X% off for N Example:25% off any 6 or more bottles
                    elif "off any" in pDscText:
                        pDscType = "XoffforN"
                        tDscpercent = float(numb_only(pDscText))/100.0
                        pDscPrice = str(float(pDscPrice)*(1.0-tDscpercent))                   
                        pPrcSav = '{:.2%}'.format(1.0-float(pDscPrice)/float(pOrgPrice))
                    #Dropped Example:Was $19.99 04/08/16     
                    elif "Was" in pDscText:
                        pDscType = "Dropped"
                        pOrgPrice = numb_only(pDscText)
                        if float(pOrgPrice)+0.1 > float(pDscPrice):               
                            pPrcSav = '{:.2%}'.format(1.0-float(pDscPrice)/float(pOrgPrice))
                        else:
                            #CupPrice reason
                            tCup = ProductNode['CupPrice']
                            pOrgPrice = float(pOrgPrice)*float(pDscPrice)/float(tCup)
                            pPrcSav = '{:.2%}'.format(1.0-float(pDscPrice)/float(pOrgPrice))
                    else:
                        #As known: 
                        knowntag = "Variety may vary,\
                                Designs may vary,\
                                No further discounts,\
                                Offer Details Here,\
                                Limit of 3 per order"

                        if pDscText not in knowntag:
                            print("Unexpected tag:{0}--{1}".format(pName,pDscText))
                        pDscText = ""

                    if float(pDscPrice) > float(pOrgPrice):
                        print("Unexpected save:{0}--{1}--{2}".format(pName,pDscPrice,pOrgPrice))          

                dictitem = {'l1name': categoryl1,
                            'l1id':categoryl1id,
                            'l2name':categoryl2,
                            'l2id':categoryl2id,
                            'ImgAddr':pImgAddr,
                            'Title':pTitle,
                            'PartID':pPartID,
                            'ItemID':pItemID,
                            'Link':pLink,
                            'Brand':pBrand,
                            'Name':pName,
                            'OrgPrice':pOrgPrice,
                            'Size':pSize,
                            'UnitPrice':pUnitPrice,
                            'DscType':pDscType,
                            'DscPrice':pDscPrice,
                            'DscText':pDscText,
                            'PrcSav':pPrcSav}    
                
                product_list.append(dictitem)                 
            except Exception as e:
                print(pName,pDscText)
                print('record {0},error:{1},(╯‵□′)╯︵┻━┻'.format(n,e))
            
            print(' '*80,end='\r') 
            print(categoryl2,':','☺'*n,end='\r')   
    #print('----Done List') 
    return n


def EntryByPage():
    
    totaltimestart = time.time()
    totalitem = 0
        
    urllines = []
    with open('wwsall\\wwsurll2.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urllines.append(row)
    #start seesion
    urlbase = "https://www.woolworths.com.au"

    timestr = time.strftime("%y%m%d", time.localtime())
    itemfilename = 'wwsall\\wwsitem_{0}.csv'.format(timestr)
    with open(itemfilename, 'w', newline='',encoding='utf-8') as csvfile:
        fieldnames = ['l1name','l1id','l2name','l2id',
                    'ImgAddr','Title','PartID','ItemID',
                    'Link','Brand','Name','OrgPrice','Size','UnitPrice',
                    'DscType','DscPrice','DscText','PrcSav']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for row in urllines:
        productlist = []
        mSession = requests.Session()
        urll2 = urlbase+row["l2url"]
        #into page
        res1 = mSession.get(urll2)
        if res1.status_code != 200 :
            print('Get Main page fail---RES.CODE：{0}'.format(res1.status_code))
            return
        #print("front page pass")
        '''
        #pie category (no essential)
        CategoryUrl = 'https://www.woolworths.com.au/apis/ui/PiesCategoriesWithSpecials/'
        res2 = mSession.get(CategoryUrl) 

        if res2.status_code != 200 :
            print('Get Category fail RES.CODE：{0}'.format(res2.status_code))
            return
        print("pie pass")
        #3 SeoMetatags(not essential)
        params = {
            "FormatObject": "{}",
            "IsSpecial": False,
            "PageType": "Home",
            "UrlPath": row["l2url"],            
        }
        
        res3 = mSession.post('https://www.woolworths.com.au/apis/ui/SeoMetatags',data=params)

        if res3.status_code != 200 :
            print('Get Seo fail---RES.CODE：{0}'.format(res3.status_code))
            return
        print("Seo pass")
        '''
        #products get product. First Page for total number
        #payroll Example
        #post https://www.woolworths.com.au/apis/ui/browse/category
        '''
        categoryId:"1_22C1314"
        filters:[]
        formatObject:"{"name":"Chips & Wedges"}"
        isBundle:false
        isMobile:false
        isSpecial:false
        location:"/shop/browse/freezer/chips-wedges"
        pageNumber:2
        pageSize:36
        sortType:"TraderRelevance"
        url:"/shop/browse/freezer/chips-wedges?pageNumber=2"
        '''
        #SEARCH OPTION
        oPageSize = 36 #max 36 in test, wws use 24 as default

        params = {"categoryId":row["l2id"],
            "pageNumber":1,
            "pageSize":oPageSize,
            "sortType":"TraderRelevance",
            "url":row["l2url"],
            "location":row["l2url"],
            "formatObject":"{\"name\":\""+row["l2name"]+"\"}",
            "isSpecial":False,
            "isBundle":False,
            "isMobile":False,
            "filters":None
        }
        
        res4 = mSession.post('https://www.woolworths.com.au/apis/ui/browse/category',data=params)
        if res4.status_code != 200 :
            print('Get page1 fail---RES.CODE：{0}'.format(res4.status_code))
            return
        #print('Get page1 done')
        hdoc = res4.text
        #load Json Count
        jsonCount = json.loads(hdoc)
        ctCount = jsonCount["TotalRecordCount"]
        if ctCount <= 0:
            continue
        #print('Count result---{0} items'.format(ctCount))
        pageMax = int((ctCount-1)/oPageSize) + 1
        #Parse Productlist
        totalitem += PLfromJson(row,hdoc,productlist)

        for pageNum in range(2,pageMax+1):# link and parse
            #linking
            params = {"categoryId":row["l2id"],
                "pageNumber":pageNum,
                "pageSize":oPageSize,
                "sortType":"TraderRelevance",
                "url":row["l2url"]+"?pageNumber={0}".format(pageNum),
                "location":row["l2url"],
                "formatObject":"{\"name\":\""+row["l2name"]+"\"}",
                "isSpecial":False,
                "isBundle":False,
                "isMobile":False,
                "filters":None
            }
            res5 = mSession.post('https://www.woolworths.com.au/apis/ui/browse/category',data=params)
            if res5.status_code != 200 :
                print('Get {0}list {1} fail RES.CODE：{2}'.format(row["l2name"],pageNum,res5.status_code))
                continue
            #print('List {0}: Done'.format(pageNum))
            hdoc = res5.text            
            #Parse
            totalitem += PLfromJson(row,hdoc,productlist)
        #print('List {0}: Done'.format(row["l2name"]))
        mSession.close() 
        with open(itemfilename, 'a+', newline='',encoding='utf-8') as csvfile:
            fieldnames = ['l1name','l1id','l2name','l2id',
                    'ImgAddr','Title','PartID','ItemID',
                    'Link','Brand','Name','OrgPrice','Size','UnitPrice',
                    'DscType','DscPrice','DscText','PrcSav']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(productlist)     
        
    totaltimeend = time.time()
    costtime = totaltimeend - totaltimestart
    print('SUM ITEM:{0},SPEND：{1}s'.format(totalitem,costtime)) 
    return


if __name__ == '__main__':
    EntryByPage()
    #input('wait for quit:')
