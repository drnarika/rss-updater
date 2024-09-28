from bs4 import BeautifulSoup as BS
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
        title_node = self.document.new_tag('title')
        title_node.string = self.SOURCE.TITLE
        self.channel_node.append(title_node)
        
        link_node = self.document.new_tag('link')
        link_node.string = self.SOURCE.LINK
        self.channel_node.append(link_node)
        
        author_node = self.document.new_tag('author')
        author_node.string = self.SOURCE.AUTHOR
        self.channel_node.append(author_node)
        
        items = iter(self.SOURCE)
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
            item_description.insert(0,item.CONTENT)
            item_description.replace_with

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
        doc = BS(unescape(doc_unicode),features='xml').prettify('utf-8').decode(errors='ignore')
        with open(desPath,'w+')as w:
            w.write(doc)
        print(f'Export completed. Exported {len(self.SOURCE.items)} items.')
        