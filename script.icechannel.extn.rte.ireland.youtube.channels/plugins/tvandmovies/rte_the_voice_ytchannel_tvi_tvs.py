'''
    RTE The Voice
'''

from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import TVShowSource

#import xbmc

#import re

class rte_the_voice_ytchannel(TVShowIndexer, TVShowSource):
    implements = [TVShowIndexer, TVShowSource]

    name = 'Youtube: RTE The Voice'
    display_name = 'Youtube: RTE The Voice'
    
    img = 'http://yt3.ggpht.com/-ERCE-ZomhtA/AAAAAAAAAAI/AAAAAAAAAAA/r4ny3wK50oQ/s88-c-k-no/photo.jpg'
    default_indexer_enabled = 'true'
    source_enabled_by_default = 'true'

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        num_items_on_a_page = 50

        from entertainment.net import Net
        import json

        net = Net()
        
        if not page or page == '':
            page = '1'

        myUrl = url + '&start-index=%s' % (str((int(page)-1) * num_items_on_a_page + 1))
        
        html = net.http_GET(myUrl).content

        html = json.loads(html)

        if total_pages == '':
            total_items = int(html['data']['totalItems'])
            total_pages = str((total_items/50) + ( 1 if total_items%50 > 0 else 0 ) )

        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
        
        start_index = ( int(page) - 1 ) * num_items_on_a_page
        
        for item in html['data']['items']:
            if section=="playlist_items":
                item = item['video']
                print item
            name = item['title']
            try:
                img = item['thumbnail']['hqDefault']
            except:
                img = ''
            plot = item['description']
            if section == 'uploads' or section=='playlist_items':
                url = item['player']['default']
                self.AddContent(list, indexer, common.mode_File_Hosts, name, '', 'tv_episodes', url=url, name=name, season='0', episode='0', img=img, plot=plot)
            elif section =='playlists':
                url = 'http://gdata.youtube.com/feeds/api/playlists/' + item['id'] + '?&v=2&max-results=50&alt=jsonc'
                self.AddSection(list, indexer, 'playlist_items', name, url, indexer, img=img, plot=plot)

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        if section == 'main':
            self.AddSection(list, indexer, 'uploads', 'Uploads', 'http://gdata.youtube.com/feeds/api/users/RTETheVoice/uploads?&v=2&max-results=50&alt=jsonc', indexer)
            self.AddSection(list, indexer, 'playlists', 'Playlists', 'http://gdata.youtube.com/feeds/api/users/RTETheVoice/playlists?&v=2&max-results=50&alt=jsonc', indexer)
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

    def GetFileHosts(self, url, list, lock, message_queue):
        self.AddFileHost(list, 'SD', url, 'YOUTUBE.COM')
