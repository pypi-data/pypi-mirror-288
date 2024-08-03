from plexflow.core.torrents.results.torrent import Torrent
from plexflow.utils.imdb.imdb_codes import IMDbCode, extract_imdb_code
import requests
import logging

class TorrentReport:
    def __init__(self, **kwargs) -> None:
        self._torrent: Torrent = kwargs.get("torrent")
        self.extracted_imdb_code = kwargs.get("extracted_imdb_code")
        self.hardcoded = kwargs.get("hardcoded")
        self.korsub = kwargs.get("korsub")
    
    @property
    def torrent(self) -> Torrent:
        return self._torrent
    
    @property
    def imdb_code_matched(self) -> bool:
        return IMDbCode(self.torrent.imdb_code) == IMDbCode(self.extracted_imdb_code)

    @property
    def acceptable_quality(self) -> bool:
        return self.torrent.parsed_release_name.get("quality", "").upper() not in [
            "CAM", "TS", "TC", "SCR", "DVDSCR",
            "SCREENER", "TELESYNC", "TELECINE", "DVDSCREENER",
            "BDSCR", "WEBSCREENER", "HDCAM",
        ]
    @property
    def has_hardcoded_subtitles(self) -> bool:
        return self.torrent.parsed_release_name.get("hardcoded", False) or self.hardcoded
    
    @property
    def has_korsub_subtitles(self) -> bool:
        return self.korsub

class TorrentInspector:
    def __init__(self, torrent: Torrent) -> None:
        self.torrent = torrent
    
    def inspect(self) -> None:
        report = {
            "torrent": self.torrent,
        }
        
        logging.info(f"Inspecting torrent: {self.torrent}")
        logging.info(f"Inspecting release name: {self.torrent.release_name}")
        logging.info(f"Inspecting IMDb code: {self.torrent.imdb_code}")
        logging.info(f"Inspecting URL: {self.torrent.url}")
        
        try:
            url = self.torrent.url
            if isinstance(url, str) and len(url) > 0:
                response = requests.get(url)
                response.raise_for_status()

                logging.info(f"URL status code: {response.status_code}")
                logging.info(f"URL response: {response.text}")
                
                extracted_imdb_id = extract_imdb_code(response.text)
                logging.info(f"Extracted IMDb code: {extracted_imdb_id}")
                
                report["extracted_imdb_code"] = extracted_imdb_id

                # check if torrent has hardcoded subtitles using various alternatives for the word
                # hardcoded
                hardcoded = any([
                    "hardcoded" in self.torrent.release_name.lower(),
                    "hardsub" in self.torrent.release_name.lower(),
                    "hardcoded" in response.text.lower(),
                    "hardsub" in response.text.lower(),
                ])
                
                logging.info(f"Hardcoded subtitles: {hardcoded}")
                
                # check if torrent has korsub subtitles
                korsub = any([
                    "korsub" in self.torrent.release_name.lower(),
                    "korsub" in response.text.lower(),
                ])
                
                logging.info(f"Korsub subtitles: {korsub}")
                
                report["hardcoded"] = hardcoded
                report["korsub"] = korsub
            else:
                logging.info("No URL provided for torrent")
        except Exception as e:
            logging.error(f"Error while inspecting torrent: {e}")

        return TorrentReport(**report)
