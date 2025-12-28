#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Service IPTV - Vavoo uniquement
Version simplifiée avec chaînes Vavoo seulement
"""

import os
import json
import time
import threading
from random import choice
from datetime import datetime
from urllib.parse import unquote
import requests

from config import SERVER_PORT

# IP du serveur
SERVER_IP = "127.0.0.1"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def set_server_ip(ip):
    global SERVER_IP
    SERVER_IP = ip


class MultiService:
    """Service IPTV Vavoo uniquement"""
    
    def __init__(self):
        self.token = None
        self.token_timestamp = 0
        self.vec_list = []
        self.vec_timestamp = 0
        self.lock = threading.RLock()
        self.initialized = False
        
        # Stockage des chaînes
        self.channels = []
        self.stream_map = {}
        self.category_map = {}
        
        # VOD
        self.movies = []
        self.series = []
        self.vod_map = {}
        self.series_map = {}
        
        # Stats par source
        self.stats_sources = {"vavoo": 0}

    def initialize(self):
        """Initialise le service"""
        if self.initialized:
            return
        
        # Thread de rafraîchissement des tokens (toutes les 10 min)
        self.token_thread = threading.Thread(target=self._token_refresh_loop, daemon=True)
        self.token_thread.start()
        
        self.initialized = True
    
    def _token_refresh_loop(self):
        """Rafraîchit le token Vavoo toutes les 10 minutes"""
        while True:
            time.sleep(600)
            self.log("Rafraîchissement automatique du token Vavoo...")
            self.get_token(force=True)
    
    def log(self, msg):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [IPTV] {msg}")
    
    def _get_vec_list(self):
        """Récupère la liste des vecteurs pour l'authentification Vavoo"""
        if self.vec_list and (time.time() - self.vec_timestamp) < 3600:
            return self.vec_list
        try:
            r = requests.get(
                "https://raw.githubusercontent.com/Belfagor2005/vavoo/main/data.json",
                timeout=10
            )
            self.vec_list = r.json()
            self.vec_timestamp = time.time()
            return self.vec_list
        except:
            return self.vec_list or []
    
    def get_token(self, force=False):
        """Obtient un token Vavoo valide"""
        with self.lock:
            if not force and self.token and (time.time() - self.token_timestamp) < 600:
                return self.token
            
            self.log("Obtention d'un nouveau token Vavoo...")
            try:
                vec_list = self._get_vec_list()
                if not vec_list:
                    return self.token
                
                for i in range(30):
                    try:
                        vec = {"vec": choice(vec_list)}
                        r = requests.post(
                            'https://www.vavoo.tv/api/box/ping2',
                            data=vec, timeout=15,
                            headers={'User-Agent': 'VAVOO/2.6'}
                        )
                        data = r.json()
                        sig = data.get('response', {}).get('signed')
                        if sig:
                            self.token = sig
                            self.token_timestamp = time.time()
                            self.log(f"Token Vavoo obtenu (tentative {i+1})")
                            return sig
                    except:
                        continue
                return self.token
            except Exception as e:
                self.log(f"ERREUR token: {e}")
                return self.token

    def load_all_sources(self, force=False):
        """Charge les chaînes Vavoo"""
        if not force and self.stream_map:
            return
        
        self.log("=" * 50)
        self.log("CHARGEMENT DES CHAÎNES VAVOO")
        self.log("=" * 50)
        
        self.channels = []
        self.stream_map = {}
        self.category_map = {}
        self.stats_sources = {"vavoo": 0}
        
        # Charger Vavoo
        self._load_vavoo_channels()
        
        # Charger VOD
        self._load_vod_content()
        
        # Construire le cache
        self._build_cache()
        
        self.log("=" * 50)
        self.log(f"TOTAL: {len(self.stream_map)} chaînes Vavoo")
        self.log("=" * 50)
    
    def _load_vavoo_channels(self):
        """Charge les chaînes Vavoo"""
        self.log("Chargement des chaînes Vavoo...")
        try:
            r = requests.get(
                "https://www2.vavoo.to/live2/index?countries=all&output=json",
                timeout=30, headers={'User-Agent': 'VAVOO/2.6'}
            )
            channels = r.json()
            
            count = 0
            for ch in channels:
                group = unquote(ch.get("group", "Other")).strip()
                name = unquote(ch.get("name", "")).strip()
                
                self.channels.append({
                    "name": name,
                    "url": ch.get("url", ""),
                    "logo": ch.get("logo", ""),
                    "tvg_id": ch.get("tvg_id", ""),
                    "group": group,
                    "source": "vavoo"
                })
                count += 1
            
            self.stats_sources["vavoo"] = count
            self.log(f"✓ Vavoo: {count} chaînes")
        except Exception as e:
            self.log(f"✗ Erreur Vavoo: {e}")

    def _load_vod_content(self):
        """Charge les films et séries depuis l'API VOD Vavoo"""
        self.log("Chargement du contenu VOD...")
        
        headers = {'User-Agent': 'VAVOO/2.6'}
        movies = []
        series = []
        
        vod_endpoints = {
            "movies": [
                ("Populaires", "https://vavoo.to/web-vod/api/list?id=movie.popular"),
                ("Tendances", "https://vavoo.to/web-vod/api/list?id=movie.trending"),
            ],
            "series": [
                ("Populaires", "https://vavoo.to/web-vod/api/list?id=series.popular"),
                ("Tendances", "https://vavoo.to/web-vod/api/list?id=series.trending"),
            ]
        }
        
        for cat_name, url in vod_endpoints["movies"]:
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    items = data.get("data", [])
                    for item in items:
                        item['_category'] = cat_name
                    movies.extend(items)
                    self.log(f"✓ Films {cat_name}: {len(items)}")
            except Exception as e:
                self.log(f"✗ Films {cat_name}: {e}")
        
        for cat_name, url in vod_endpoints["series"]:
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    items = data.get("data", [])
                    for item in items:
                        item['_category'] = cat_name
                    series.extend(items)
                    self.log(f"✓ Séries {cat_name}: {len(items)}")
            except Exception as e:
                self.log(f"✗ Séries {cat_name}: {e}")
        
        # Dédupliquer
        seen = set()
        self.movies = []
        for m in movies:
            mid = m.get('id', '')
            if mid and mid not in seen:
                seen.add(mid)
                self.movies.append(m)
        
        seen = set()
        self.series = []
        for s in series:
            sid = s.get('id', '')
            if sid and sid not in seen:
                seen.add(sid)
                self.series.append(s)
        
        self._build_vod_cache()
        self.log(f"VOD Total: {len(self.movies)} films, {len(self.series)} séries")
    
    def _build_vod_cache(self):
        """Construit le cache VOD"""
        self.vod_map = {}
        self.series_map = {}
        
        for idx, movie in enumerate(self.movies, 1):
            cat = movie.get('_category', 'Populaires')
            cat_id = "1" if cat == "Populaires" else "2"
            self.vod_map[idx] = {
                "vod_id": idx,
                "original_id": movie.get('id', ''),
                "title": movie.get('title', movie.get('name', f'Film {idx}')),
                "poster": movie.get('poster', movie.get('image', '')),
                "year": movie.get('year', ''),
                "rating": movie.get('rating', movie.get('vote_average', 0)),
                "plot": movie.get('overview', movie.get('description', '')),
                "category_id": cat_id
            }
        
        for idx, serie in enumerate(self.series, 1):
            cat = serie.get('_category', 'Populaires')
            cat_id = "101" if cat == "Populaires" else "102"
            year = serie.get('year', '')
            if not year and serie.get('first_air_date'):
                year = serie.get('first_air_date', '')[:4]
            self.series_map[idx] = {
                "series_id": idx,
                "original_id": serie.get('id', ''),
                "title": serie.get('title', serie.get('name', f'Série {idx}')),
                "poster": serie.get('poster', serie.get('image', '')),
                "year": year,
                "rating": serie.get('rating', serie.get('vote_average', 0)),
                "plot": serie.get('overview', serie.get('description', '')),
                "category_id": cat_id
            }
    
    def _build_cache(self):
        """Construit le cache avec IDs séquentiels - ORDRE ORIGINAL"""
        self.log("Construction du cache...")
        
        self.stream_map = {}
        self.category_map = {}
        
        # Collecter les groupes dans l'ordre d'apparition
        group_order = []
        groups = {}
        for ch in self.channels:
            group = ch.get("group", "Other")
            if group not in groups:
                groups[group] = []
                group_order.append(group)
            groups[group].append(ch)
        
        stream_id = 1
        cat_id = 1
        
        # Parcourir les groupes dans l'ordre d'apparition (pas de tri)
        for group in group_order:
            channels = groups[group]
            if not channels:
                continue
            
            self.category_map[cat_id] = {
                "category_id": str(cat_id),
                "category_name": group,
                "parent_id": 0
            }
            
            # Garder l'ordre original des chaînes (pas de tri)
            for ch in channels:
                if not ch.get("url"):
                    continue
                
                self.stream_map[stream_id] = {
                    "stream_id": stream_id,
                    "name": ch["name"],
                    "url": ch.get("url", ""),
                    "logo": ch.get("logo", ""),
                    "tvg_id": ch.get("tvg_id", ""),
                    "category_id": str(cat_id),
                    "category_name": group,
                    "source": "vavoo"
                }
                stream_id += 1
            
            cat_id += 1
        
        self.log(f"Cache: {len(self.stream_map)} chaînes, {len(self.category_map)} catégories")

    def get_stream_url_by_id(self, stream_id):
        """Retourne l'URL pour un stream_id"""
        stream = self.stream_map.get(stream_id)
        if not stream:
            return None
        
        url = stream.get("url", "")
        if not url:
            return None
        
        if not self.token:
            self.get_token()
        if self.token:
            return f"{url}?n=1&b=5&vavoo_auth={self.token}"
        
        return url
    
    def get_channels(self):
        """Retourne toutes les chaînes"""
        return list(self.stream_map.values())
    
    def get_xtream_categories(self):
        """Retourne les catégories au format Xtream Codes"""
        if not self.category_map:
            self.load_all_sources()
        return list(self.category_map.values())
    
    def get_xtream_streams(self, category_id=None):
        """Retourne les streams au format Xtream Codes"""
        if not self.stream_map:
            self.load_all_sources()
        
        streams = []
        for stream_id, data in self.stream_map.items():
            if category_id and str(data["category_id"]) != str(category_id):
                continue
            
            streams.append({
                "num": stream_id,
                "name": data["name"],
                "stream_type": "live",
                "stream_id": stream_id,
                "stream_icon": data["logo"],
                "epg_channel_id": data["tvg_id"] or data["name"],
                "added": "0",
                "category_id": data["category_id"],
                "custom_sid": "",
                "tv_archive": 0,
                "direct_source": "",
                "tv_archive_duration": 0
            })
        
        return streams
    
    def get_vod_categories(self):
        """Retourne les catégories VOD"""
        return [
            {"category_id": "1", "category_name": "Films Populaires", "parent_id": 0},
            {"category_id": "2", "category_name": "Films Tendances", "parent_id": 0},
        ]
    
    def get_vod_streams(self, category_id=None):
        """Retourne les films au format Xtream Codes"""
        if not self.vod_map:
            self._load_vod_content()
        
        streams = []
        for vod_id, data in self.vod_map.items():
            if category_id and str(data["category_id"]) != str(category_id):
                continue
            
            rating = data.get("rating", 0)
            try:
                rating_float = float(rating) if rating else 0
            except:
                rating_float = 0
            
            streams.append({
                "num": vod_id,
                "name": data["title"],
                "stream_type": "movie",
                "stream_id": vod_id,
                "stream_icon": data["poster"],
                "rating": str(rating),
                "rating_5based": rating_float / 2,
                "added": "0",
                "category_id": data["category_id"],
                "container_extension": "mp4",
                "custom_sid": "",
                "direct_source": data["original_id"],
                "plot": data["plot"],
                "year": str(data["year"]) if data["year"] else "",
            })
        
        return streams
    
    def get_vod_info(self, vod_id):
        """Retourne les infos d'un film"""
        try:
            vod_id = int(vod_id)
        except:
            pass
        
        data = self.vod_map.get(vod_id)
        if data:
            return {
                "info": {
                    "name": data["title"],
                    "plot": data["plot"],
                    "cast": "", "director": "", "genre": "",
                    "releasedate": str(data["year"]) if data["year"] else "",
                    "rating": data["rating"],
                    "duration": "",
                    "backdrop_path": [data["poster"]],
                },
                "movie_data": {
                    "stream_id": vod_id,
                    "name": data["title"],
                    "container_extension": "mp4",
                }
            }
        return {"info": {}, "movie_data": {}}
    
    def get_series_categories(self):
        """Retourne les catégories de séries"""
        return [
            {"category_id": "101", "category_name": "Séries Populaires", "parent_id": 0},
            {"category_id": "102", "category_name": "Séries Tendances", "parent_id": 0},
        ]
    
    def get_series(self, category_id=None):
        """Retourne les séries au format Xtream Codes"""
        if not self.series_map:
            self._load_vod_content()
        
        series_list = []
        for series_id, data in self.series_map.items():
            if category_id and str(data["category_id"]) != str(category_id):
                continue
            
            rating = data.get("rating", 0)
            try:
                rating_float = float(rating) if rating else 0
            except:
                rating_float = 0
            
            series_list.append({
                "num": series_id,
                "name": data["title"],
                "series_id": series_id,
                "cover": data["poster"],
                "plot": data["plot"],
                "cast": "", "director": "", "genre": "",
                "releaseDate": str(data["year"]) if data["year"] else "",
                "rating": str(rating),
                "rating_5based": rating_float / 2,
                "category_id": data["category_id"],
                "last_modified": "0",
                "backdrop_path": [data["poster"]],
            })
        
        return series_list
    
    def get_series_info(self, series_id):
        """Retourne les infos d'une série"""
        try:
            series_id = int(series_id)
        except:
            pass
        
        data = self.series_map.get(series_id)
        if data:
            return {
                "info": {
                    "name": data["title"],
                    "plot": data["plot"],
                    "cast": "", "director": "", "genre": "",
                    "releaseDate": str(data["year"]) if data["year"] else "",
                    "rating": data["rating"],
                    "backdrop_path": [data["poster"]],
                },
                "episodes": {},
                "seasons": []
            }
        return {"info": {}, "episodes": {}, "seasons": []}

    def generate_m3u(self, filter_country=None, filter_category=None):
        """Génère le contenu M3U"""
        if not self.stream_map:
            self.load_all_sources()
        
        lines = ["#EXTM3U"]
        
        for stream_id in sorted(self.stream_map.keys()):
            data = self.stream_map[stream_id]
            
            if filter_country:
                if filter_country.lower() not in data["category_name"].lower():
                    continue
            
            url = f"http://{SERVER_IP}:{SERVER_PORT}/stream/{stream_id}.ts"
            
            lines.append(f'#EXTINF:-1 tvg-id="{data["tvg_id"] or data["name"]}" tvg-name="{data["name"]}" tvg-logo="{data["logo"]}" group-title="{data["category_name"]}",{data["name"]}')
            lines.append(url)
        
        return "\n".join(lines)
    
    def get_countries_list(self):
        """Retourne la liste des catégories/pays"""
        if not self.category_map:
            self.load_all_sources()
        
        countries = []
        for cat_id, cat in self.category_map.items():
            count = sum(1 for s in self.stream_map.values() if s["category_id"] == str(cat_id))
            countries.append({
                "name": cat["category_name"],
                "total_channels": count
            })
        return countries
    
    def get_stats(self):
        """Retourne les statistiques du service"""
        return {
            "total_channels": len(self.stream_map),
            "total_movies": len(self.movies),
            "total_series": len(self.series),
            "token_valid": self.token is not None,
            "sources": self.stats_sources
        }


# Instance globale
multi_service = MultiService()
