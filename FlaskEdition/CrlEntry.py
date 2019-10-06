from CrlWWS import searchItem as searchWWS 
from SrchCOLES import searchItemInDB as searchColes 


def MainSearchItem(word):
    #price collect 
    products_list = [] 
    print('START search：',word) 
    try:       
        # wws 
        searchWWS(word, products_list) 
        # coles 
        searchColes(word, products_list)
    except Exception as e:
        print(e)

    '''
    f = open('dataEntry\\result_{0}.txt'.format(word),'w',encoding = 'utf-8')
    for i in products_list:
        f.write(str(i)+'\n')
    f.close()   
    ''' 

    #print('sorting') 
                
    products_list = sorted(products_list, key=lambda item: float(item['price']), reverse=False) 
    
    #print("sorting done")
    
        
    return products_list 

if __name__ == '__main__':
    word = input('Please input product:') 
    MainSearchItem(word) 
    word = input('input to quit:') 



