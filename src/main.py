from crawl import Source
from rss import RSSConstructer, OPMLConstructer
import sys, os

cwd = os.path.split(sys.argv[0])[0]

if not os.path.exists(os.path.join(cwd,'../sources')):
    os.mkdir(os.path.join(cwd,'../sources'))
if not os.path.exists(os.path.join(cwd,'../dist')):
    os.mkdir(os.path.join(cwd,'../dist'))

OPML = OPMLConstructer()
for root,dirs,files in os.walk(os.path.join(cwd,'../sources')):
    for file in files:
        source = Source(os.path.join(root,file))
        if not source.ENABLED:
            continue
        source.update()

        RSS = RSSConstructer(source)
        RSS.parse()

        desPath = os.path.join(cwd,f'../dist/{file.split(".")[0]}.xml')
        RSS.export(desPath)

        OPML.appendSource(source,file)
        
opmlPath = os.path.join(cwd,f'../dist/summary.opml')
OPML.export(opmlPath)