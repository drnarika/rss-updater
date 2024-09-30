from bs4 import BeautifulSoup as BS
import yaml
import requests

class Source:
    def __init__(self,path: str) -> None:
        self.loadFromYAML(path)
    
    def loadFromYAML(self,path: str):
        with open(path,'r',encoding='utf-8')as r:
            source = yaml.load(r,Loader=yaml.FullLoader)
            if source['enabled'] == False:
                print(f'Source {source["title"]} has been skipped.')
                self.ENABLED = False
                return 0
            else: self.ENABLED = True
            print(f'Start loading source {source["title"]}.')
            for key in source.keys():
                if key == 'title':
                    self.TITLE = source['title']
                elif key == 'link':
                    self.LINK = source['link']
                elif key == 'author':
                    self.AUTHOR = source['author']
                elif key == 'next-page':
                    self.NEXT_PAGE = source['next-page']
                elif key == 'category':
                    self.updateCategories(source['category'])
                elif key == 'item':
                    self.ITEM_PREF = source['item']
                elif key == 'content':
                    self.CONTENT_PREF = source['content']
            print(f'Loading {self.TITLE} completed.\n')
                    
    def updateCategories(self,categories:list):
        t_categories = []
        for c in categories:
            t_c = Category(self, c)
            t_categories.append(t_c)
        self.CATEGORY = t_categories
        del(t_categories)
        
    items = []
    def update(self):
        self.items = []
        for c in self.CATEGORY:
            print(f'Start updating category {c.TITLE}.')
            items_category = c.updateItems()
            self.items.extend(items_category)
            print(f'Updating {c.TITLE} completed.')
            
class Category:
    
    def __init__(self,source:Source,data:list) -> None:
        self.TITLE = data['title']
        self.LINK = f'{source.LINK}{data["link"]}'
        self.SOURCE = source
    
    def updateItems(self):
        t_items = []
        now_link = self.LINK
        while True:
            req = Request(now_link)
            bs = BS(req.ask(),features='lxml')
            for box in bs.select(self.SOURCE.ITEM_PREF['box']):
                t_items.append(Item(self.SOURCE,BS(str(box),features="lxml"),self))
            next = bs.select_one(self.SOURCE.NEXT_PAGE.split('$')[0])
            if next != None:
                now_link = next.attrs[self.SOURCE.NEXT_PAGE.split('$')[1]]
                continue
            else:
                break
        self.ITEM = t_items
        del(t_items)
        self.fetchContent()
        return self.ITEM
    
    def fetchContent(self):
        for item in self.ITEM:
            item.fetchContent()
            
class Item:
    def __init__(self,source:Source,box:BS,parent:Category) -> None:
        if source.ITEM_PREF['title'].split('$')[1] != 'innerText':
            self.TITLE = box.select_one(source.ITEM_PREF['title'].split('$')[0]) \
                .attrs[source.ITEM_PREF['title'].split('$')[1]]
        else:
            self.TITLE = box.select_one(source.ITEM_PREF['title'].split('$')[0]).getText()
        self.LINK = box.select_one(source.ITEM_PREF['link'].split('$')[0]) \
            .attrs[source.ITEM_PREF['link'].split('$')[1]]
        self.PUBDATE = box.select_one(source.ITEM_PREF['pubDate'].split('$')[0]) \
            .attrs[source.ITEM_PREF['pubDate'].split('$')[1]]
        self.SOURCE = source
        self.BOX = box
        self.PARENT = parent
    
    def fetchContent(self):
        req = Request(self.LINK)
        content = BS(req.ask(),features='lxml').select_one(self.SOURCE.CONTENT_PREF['box'])
        self.CONTENT = str(content)
        print(f'Fetching {self.TITLE} completed.\r')
    
class Request:
    USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    
    def __init__(self,link:str) -> None:
        self.LINK = link
        # self.REFERER = referer
    
    def ask(self):
        HEADER = {'User-Agent': self.USER_AGENT,'Referer':self.LINK.encode('latin-1','ignore').decode('latin-1','ignore')}
        try:
            req = requests.get(self.LINK,headers=HEADER)
        except Exception as e:
            print(f'Error when request: {e}')
            return f'<div>Error When Loading Article:<br>{e}</div>'
        return req.text