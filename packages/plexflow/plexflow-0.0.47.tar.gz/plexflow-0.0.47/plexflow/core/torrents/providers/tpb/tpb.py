from plexflow.utils.api.rest.restful import Restful
from plexflow.core.torrents.providers.tpb.utils import TPBSearchResult

class TPB(Restful):
    def __init__(self, base_url: str = 'https://apibay.org'):
        super().__init__(base_url=base_url)
    
    def search(self, query: str):
        response = self.get('/q.php', query_params={
            'q': query,
        })
        
        response.raise_for_status()
        
        print(response.content)
        
        data = response.json()
        
        return list(map(lambda x: TPBSearchResult(**x), data))
