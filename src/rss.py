from bs4 import BeautifulSoup as BS
from bs4.formatter import XMLFormatter
from html import unescape
import yaml,os
from crawl import Source, Category, Item

class RSSConstructer:
    
    def __init__(self,source:Source) -> None:
        self.SOURCE = source
        self.document = BS(features='xml')
        self.initRSSRootNode()
        
    def initRSSRootNode(self):
        rss = self.document.new_tag('rss',attrs={'version':'2.0'})
        self.document.append(rss)
        channel = self.document.new_tag('channel')
        rss.append(channel)
        self.root_node = rss
        self.channel_node = channel
        
    def parse(self):
        items = self.SOURCE.items
        print('Serializing content into RSSXml...\n')
        for item in items:
            item_node = self.document.new_tag('item')

            item_title = self.document.new_tag('title')
            item_title.string = item.TITLE

            item_link = self.document.new_tag('link')
            item_link.string = item.LINK

            item_category = self.document.new_tag('category')
            item_category.string = item.PARENT.TITLE

            item_description = self.document.new_tag('description')
            item_description.append(item.CONTENT)
            # if self.SOURCE.CONTENT_PREF['viewRaw']:
            #     item_description.append(BS('<br><div style="text-align: left;"> \
            #                 <a herf="{self.LINK}">View Raw</a></div>'))

            item_pubDate = self.document.new_tag('pubDate')
            item_pubDate.string = item.PUBDATE

            
            item_node.append(item_title)
            item_node.append(item_link)
            item_node.append(item_category)
            item_node.append(item_description)
            item_node.append(item_pubDate)
            
            self.channel_node.append(item_node)
            print(f'Serializing {item.TITLE} completed.\r')
    
    def export(self,desPath:str):
        print(f'Export result to {desPath}...')
        doc_unicode = self.document.prettify('utf-8').decode(errors='ignore')
        # doc = BS(unescape(doc_unicode),features='lxml').prettify('utf-8',None).decode(errors='ignore')
        # doc = doc.replace('\n </body>\n</html>','')
        # doc = doc.replace('\n<html>\n <body>\n  ','')
        with open(desPath,'w+')as w:
            w.write(doc_unicode)
        print(f'Export completed. Exported {len(self.SOURCE.items)} items.')