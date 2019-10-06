import requests
from lxml import html 
import json
import time

def searchItem(word,product_list):
    
    totaltimestart = time.time()
    totalitem = 0
    
    #start search
    
    #flog = open('datawws\\{0}_log.txt'.format(word),'w',encoding='utf-8')
    flog = ''

    mSession = requests.Session()

    
    #go page1
    time_start = time.time()
    searchurl = 'https://www.woolworths.com.au/shop/search/products?searchTerm={0}'.format(word)
    res1 = mSession.get(searchurl)    
    #wait
    if res1.status_code != 200 :
        #flog.write('Get Main page fail---RES.CODE：{0}\n'.format(res1.status_code))
        #print('WWS:Get Main page fail---RES.CODE：{0}\n'.format(res1.status_code))
        return

    time_end = time.time()
    costtime = time_end-time_start
    #flog.write('Get Main page done---Spend:{0}s\n'.format(costtime))
    #print('WWS:Get Main page done---Spend:{0}s\n'.format(costtime))
    '''
    hdoc = res1.text
    fpage = open('datawws\\{0}_MainPage.txt'.format(word),'w',encoding='utf-8')
    fpage.write(hdoc)
    fpage.close()
    '''
    '''
    #PieCategory
    
    time_start = time.time()
    CategoryUrl = 'https://www.woolworths.com.au/apis/ui/PiesCategoriesWithSpecials/'
    res2 = mSession.get(CategoryUrl) 

    if res2.status_code != 200 :
        flog.write('Get Category fail RES.CODE：{0}'.format(res2.status_code))
        flog.write('\n')
        return

    time_end = time.time()
    costtime = time_end-time_start
    flog.write('Category: Loading time cost:{0}s\n'.format(costtime))  
    flog.write('\n') 
    flog.write(str(mSession.cookies))
    flog.write('\n')

    hdoc = res2.text
    fpage = open('datawws\\{0}_getCategory.txt'.format(word),'w',encoding='utf-8')
    fpage.write(hdoc)
    fpage.close()
    '''
    #count,get TOTAL,to calculate page number,not essential
    time_start = time.time()
    params = (
        ('SearchTerm', word),
    )

    res3 = mSession.get('https://www.woolworths.com.au/apis/ui/Search/count',params=params)

    if res3.status_code != 200 :
        #flog.write('Get count fail---RES.CODE：{0}\n'.format(res3.status_code))
        #print('WWS:Get count fail---RES.CODE：{0}\n'.format(res3.status_code))
        return

    time_end = time.time()
    costtime = time_end-time_start
    #flog.write('Get Count done---Spend:{0}s\n'.format(costtime))
    #print('WWS:Get Count done---Spend:{0}s\n'.format(costtime))
    

    hdoc = res3.text
    '''
    fpage = open('datawws\\{0}_Getcount.txt'.format(word),'w',encoding='utf-8')
    fpage.write(hdoc)
    fpage.close()
    '''
    #load Json
    jsonCount = json.loads(hdoc)
    TotalCount = jsonCount["SearchCount"]["ProductCount"]
    SpcCount = jsonCount["SearchCount"]["SpecialProductCount"]

    #flog.write('Count result---{0} items,{1} in special\n'.format(TotalCount,SpcCount))
    #print('Count result---{0} items,{1} in special\n'.format(TotalCount,SpcCount))
    #SEARCH OPTION
    oPageSize = 36 #max 36 in test, wws use 24 as default
    oIsSpecial = "false" #use true to get special only

    pageMax = int((TotalCount-1)/oPageSize) + 1

    def PLfromJson(jsonList,product_list,flog):
        #list
        # All in Json Type
        time_start = time.time()
        n = 0

        jsondata = json.loads(jsonList)
        pr_list = jsondata["Products"]
        #get info 
        m=len(pr_list)
        
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
                        #flog.write('@@@@@@@@record {0},{1} No Stock,(╯‵□′)╯︵┻━┻\n'.format(n,pName))
                        continue

                    pPartID = ProductNode['Barcode'] #int
                    pItemID = ProductNode['Stockcode']
                    pImgAddr = ProductNode['LargeImageFile'] #in addr,switch small,medium,large
                    pTitle  = ProductNode['Description']#Brand+name+size,often has <br>
                    pTitle = pTitle.replace('<br>',' ') 
                    pTitle = pTitle.replace('...',' ') 
                    pLink = 'https://www.woolworths.com.au/shop/productdetails/{0}/'.format(pItemID)+ProductNode['UrlFriendlyName'] #not sure its working
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
                            pDscType = "SaveX"#Online Only
                            pDscText = pPrcSav+' off'
                    pDscPrice = str(pDscPrice)
                    pOrgPrice = str(pOrgPrice)
                    #Buy N for X
                    if ProductNode['ImageTag']['FallbackText'] == 'Buy More Save More':
                        pDscType = "buyNforN"
                        strTagContent = ProductNode['CentreTag']['TagContent']
                        selector =  html.fromstring(strTagContent)
                        pDscText = selector.xpath('@title')[0]
                        pDscNumber = int(pDscText.split(' ')[0])
                        pDscSum = float(pDscText.split(' ')[2])
                        pDscPrice = str(pDscSum/pDscNumber)                   
                        pPrcSav = '{:.2%}'.format(1-float(pDscPrice)/float(pOrgPrice))
                    '''
                    flog.write('--------record {0}:{1},{2},{3},{4},{5},{6},{7},{8}\n'
                        .format(n,pTitle,pPartID,pItemID,pBrand,pName,pDscPrice,pSize,pUnitPrice))
                        #+pImgAddr+','+pLink+'\n')
                    '''
                    if pDscType != 'None':
                        '''
                        flog.write('(✪ω✪)Discount:{0},{1},{2},(Save {3})\n'
                            .format(pDscText,pDscPrice,pOrgPrice,pPrcSav))
                        '''
                        
                    
                    product_list.append({ 
                        'title': pTitle, 
                        'price': pDscPrice, 
                        'link': pDscText, 
                        'store': pUnitPrice, 
                        'referer': 'woolworths'})
                        
                except Exception as e:
                    #flog.write('@@@@@@@@record {0},error:{1},(╯‵□′)╯︵┻━┻\n'.format(n,e))
                    print('WWS:@@@@@@@@record {0},error:{1},(╯‵□′)╯︵┻━┻\n'.format(n,e))
        
        time_end = time.time()
        costtime = time_end-time_start
        #flog.write('----Done List time cost:{0} s\n'.format(costtime)) 
        #print('WWS:----Done List time cost:{0} s\n'.format(costtime)) 
        return n

    for pageNum in range(1,pageMax+1):# link and parse
        time_start = time.time()
        #linking
        dataPack = {"SearchTerm":word,
            "PageSize":oPageSize,
            "PageNumber":pageNum,
            "SortType":"TraderRelevance",
            "IsSpecial":oIsSpecial,
            "Filters":"[]",
            "Location":"/shop/search/products?searchTerm="+word
            #"Passes":"[27]" #Unknown but appear in 2-end pages
        }
        res4 = mSession.post('https://www.woolworths.com.au/apis/ui/Search/products', data= dataPack)
        if res4.status_code != 200 :
            #flog.write('Get list {0} fail RES.CODE：{1}\n'.format(pageNum,res4.status_code))
            #print('WWS:Get list {0} fail RES.CODE：{1}\n'.format(pageNum,res4.status_code))
            continue

        time_end = time.time()
        costtime = time_end-time_start
        #flog.write('List{0}: Loading time cost:{1}s\n'.format(pageNum,costtime))
        #print('WWS:List{0}: Loading time cost:{1}s\n'.format(pageNum,costtime))
        hdoc = res4.text
        '''
        fpage = open('datawws\\{0}_getlist{1}.txt'.format(word,pageNum),'w',encoding='utf-8')
        fpage.write(hdoc)
        fpage.close()
        '''
        #parse
        totalitem += PLfromJson(hdoc,product_list,flog)
        
    
    totaltimeend = time.time()
    costtime = totaltimeend - totaltimestart

    #flog.write('SUM ITEM:{0} , TIME:{1}s\n'.format(totalitem,costtime)) 
    print('WWS:SUM ITEM:{0} , TIME:{1}s'.format(totalitem,costtime)) 
    #flog.close()    
    
    return


if __name__ == '__main__':
    a = []
    word1 = input('input search item:')
    searchItem(word1, a)
    input('wait for quit:')

