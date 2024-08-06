from plexflow.core.torrents.providers.tpb.tpb import TPB
from plexflow.core.torrents.providers.yts.yts import YTS
from typing import List
from plexflow.core.torrents.results.torrent import Torrent

class AutoTorrents:
    @staticmethod
    def movie(imdb_id: str = None, source: str = 'yts') -> List[Torrent]:
        if source == 'tpb':
            return TPB().search(query=imdb_id)
        elif source == 'yts':
            return YTS().search(query=imdb_id)
        else:
            raise ValueError(f"Invalid source: {source}")
