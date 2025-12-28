#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service VAVOO - Gestion des tokens et chaines (Version Haute Performance)
"""

import json
import time
import threading
from random import choice
from datetime import datetime
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor

import requests

from config import TOKEN_REFRESH_INTERVAL, SERVER_PORT
import database as db

# Variable globale pour l'IP du serveur
SERVER_IP = "127.0.0.1"

def set_server_ip(ip):
    global SERVER_IP
    SERVER_IP = ip


class VavooService:
    """Service de gestion VAVOO - Haute Performance"""
    
    def __init__(self):
        self.token = None
        self.token_timestamp = 0
        self.channels = None
        self.channels_timestamp = 0
        self.lock = threading.RLock()
        self.initialized = False
        
        # Cache des URLs par stream_id
        self.url_cache = {}
        self.url_cache_timestamp = 0
        
        # Pool de vecteurs pour les tokens
        self.vec_list = []
        self.vec_timestamp = 0
    
    def initialize(self):
        """Initialise le service"""
        if self.initialized:
            return
        
        self._load_from_cache()
        
        # Thread de rafraichissement du token (toutes les 10 min)
        self.token_thread = threading.Thread(target=self._token_refresh_loop, daemon=True)
        self.token_thread.start()
        
        # Thread de rafraichissement des chaines (toutes les 30 min)
        self.channels_thread = threading.Thread(target=self._channels_refresh_loop, daemon=True)
        self.channels_thread.start()
        
        self.initialized = True
    
    def _load_from_cache(self):
        """Charge les donnees depuis le cache DB"""
        try:
            cache = db.get_vavoo_cache()
            if cache:
                if cache.get('token'):
                    self.token = cache['token']
                    if cache.get('token_updated_at'):
                        try:
                            self.token_timestamp = datetime.fromisoformat(cache['token_updated_at']).timestamp()
                        except:
                            self.token_timestamp = 0
                
                if cache.get('channels_json'):
                    try:
                        self.channels = json.loads(cache['channels_json'])
                        if cache.get('channels_updated_at'):
                            self.channels_timestamp = datetime.fromisoformat(cache['channels_updated_at']).timestamp()
                    except:
                        pass
        except Exception as e:
            self.log(f"Cache non disponible: {e}")
    
    def _token_refresh_loop(self):
        """Boucle de rafraichissement du token toutes les 10 minutes"""
        while True:
            time.sleep(600)  # 10 minutes
            self.log("Rafraichissement automatique du token...")
            self.get_token(force=True)
    
    def _channels_refresh_loop(self):
        """Boucle de rafraichissement des chaines toutes les 30 minutes"""
        while True:
            time.sleep(1800)  # 30 minutes
            self.log("Rafraichissement automatique des chaines...")
            self.get_channels(force=True)
            self._rebuild_url_cache()
    
    def log(self, msg):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [VAVOO] {msg}")
    
    def _get_vec_list(self):
        """Recupere la liste des vecteurs (cache 1 heure)"""
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
        """Obtient un token valide"""
        with self.lock:
            # Verifier si le token est encore valide (10 min)
            if not force and self.token and (time.time() - self.token_timestamp) < 600:
                return self.token
            
            self.log("Obtention d'un nouveau token...")
            
            try:
                vec_list = self._get_vec_list()
                if not vec_list:
                    self.log("ERREUR: Pas de vecteurs disponibles")
                    return self.token
                
                # Essayer plusieurs fois
                for i in range(30):
                    try:
                        vec = {"vec": choice(vec_list)}
                        r = requests.post(
                            'https://www.vavoo.tv/api/box/ping2',
                            data=vec,
                            timeout=15,
                            headers={'User-Agent': 'VAVOO/2.6'}
                        )
                        data = r.json()
                        response = data.get('response', {})
                        sig = response.get('signed')
                        
                        if sig:
                            self.token = sig
                            self.token_timestamp = time.time()
                            db.update_vavoo_token(sig)
                            self.log(f"Token obtenu (tentative {i+1})")
                            # Reconstruire le cache des URLs
                            self._rebuild_url_cache()
                            return sig
                    except Exception as e:
                        continue
                
                self.log("ERREUR: Impossible d'obtenir un token apres 30 tentatives")
                return self.token
                
            except Exception as e:
                self.log(f"ERREUR: {e}")
                return self.token
    
    def get_channels(self, force=False):
        """Recupere la liste des chaines"""
        with self.lock:
            # Cache de 30 minutes
            if not force and self.channels and (time.time() - self.channels_timestamp) < 1800:
                return self.channels
            
            self.log("Recuperation des chaines...")
            
            try:
                r = requests.get(
                    "https://www2.vavoo.to/live2/index?countries=all&output=json",
                    timeout=30
                )
                self.channels = r.json()
                self.channels_timestamp = time.time()
                db.update_vavoo_channels(json.dumps(self.channels))
                self.log(f"{len(self.channels)} chaines recuperees")
                return self.channels
            except Exception as e:
                self.log(f"ERREUR: {e}")
                return self.channels or []
    
    def _rebuild_url_cache(self):
        """Reconstruit le cache des URLs"""
        if not self.channels or not self.token:
            return
        
        self.log("Reconstruction du cache des URLs...")
        new_cache = {}
        current_id = 1
        
        organized = self._get_organized_channels_internal()
        
        for country in sorted(organized.keys()):
            for category in sorted(organized[country].keys()):
                for ch in organized[country][category]:
                    base_url = ch.get("url", "")
                    if base_url:
                        new_cache[current_id] = f"{base_url}?n=1&b=5&vavoo_auth={self.token}"
                        current_id += 1
        
        self.url_cache = new_cache
        self.url_cache_timestamp = time.time()
        self.log(f"Cache reconstruit: {len(new_cache)} URLs")
    
    def _get_organized_channels_internal(self):
        """Version interne sans lock"""
        channels = self.channels or []
        organized = {}
        
        for ch in channels:
            group = unquote(ch.get("group", "Other")).strip()
            name = unquote(ch.get("name", "")).strip()
            
            if " _ " in group:
                parts = group.split(" _ ", 1)
                country = parts[0].strip()
                category = parts[1].strip()
            else:
                country = group
                category = "General"
            
            if country not in organized:
                organized[country] = {}
            if category not in organized[country]:
                organized[country][category] = []
            
            organized[country][category].append({
                "name": name,
                "url": ch.get("url", ""),
                "logo": ch.get("logo", ""),
                "tvg_id": ch.get("tvg_id", "")
            })
        
        return organized
    
    def get_organized_channels(self):
        """Retourne les chaines organisees par pays/categorie"""
        self.get_channels()
        return self._get_organized_channels_internal()

    def generate_m3u(self, filter_country=None, filter_category=None):
        """Genere le contenu M3U avec URLs proxy"""
        organized = self.get_organized_channels()
        
        lines = ["#EXTM3U"]
        stream_id = 0
        
        for country in sorted(organized.keys()):
            if filter_country and country.lower() != filter_country.lower():
                continue
            
            for category in sorted(organized[country].keys()):
                if filter_category and category.lower() != filter_category.lower():
                    continue
                
                chans = organized[country][category]
                group_title = country if category == "General" else f"{country} | {category}"
                
                for ch in sorted(chans, key=lambda x: x["name"]):
                    if not ch["url"]:
                        continue
                    
                    stream_id += 1
                    url = f"http://{SERVER_IP}:{SERVER_PORT}/stream/{stream_id}.ts"
                    
                    lines.append(f'#EXTINF:-1 tvg-id="{ch["tvg_id"] or ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{group_title}",{ch["name"]}')
                    lines.append(url)
        
        return "\n".join(lines)
    
    def get_countries_list(self):
        """Retourne la liste des pays avec stats"""
        organized = self.get_organized_channels()
        
        result = []
        for country in sorted(organized.keys()):
            categories = list(organized[country].keys())
            total = sum(len(organized[country][cat]) for cat in categories)
            result.append({
                "name": country,
                "categories": categories,
                "total_channels": total
            })
        
        return result
    
    def get_xtream_categories(self):
        """Retourne les categories au format Xtream Codes"""
        organized = self.get_organized_channels()
        categories = []
        cat_id = 1
        
        for country in sorted(organized.keys()):
            for category in sorted(organized[country].keys()):
                cat_name = country if category == "General" else f"{country} | {category}"
                categories.append({
                    "category_id": str(cat_id),
                    "category_name": cat_name,
                    "parent_id": 0
                })
                cat_id += 1
        
        return categories
    
    def get_xtream_streams(self, category_id=None):
        """Retourne les streams au format Xtream Codes"""
        organized = self.get_organized_channels()
        streams = []
        stream_id = 1
        cat_id = 1
        
        for country in sorted(organized.keys()):
            for category in sorted(organized[country].keys()):
                current_cat_id = str(cat_id)
                
                if category_id and current_cat_id != category_id:
                    cat_id += 1
                    continue
                
                cat_name = country if category == "General" else f"{country} | {category}"
                
                for ch in organized[country][category]:
                    if not ch.get("url"):
                        continue
                    
                    proxy_url = f"http://{SERVER_IP}:{SERVER_PORT}/stream/{stream_id}.ts"
                    
                    streams.append({
                        "num": stream_id,
                        "name": ch["name"],
                        "stream_type": "live",
                        "stream_id": stream_id,
                        "stream_icon": ch.get("logo", ""),
                        "epg_channel_id": ch.get("tvg_id") or ch["name"],
                        "added": "1609459200",
                        "category_id": current_cat_id,
                        "category_name": cat_name,
                        "custom_sid": "",
                        "tv_archive": 0,
                        "direct_source": proxy_url,
                        "tv_archive_duration": 0
                    })
                    stream_id += 1
                
                cat_id += 1
        
        return streams
    
    def get_stream_url_by_id(self, stream_id):
        """Retourne l'URL VAVOO reelle pour un stream_id (utilise le cache)"""
        # Verifier si le cache est valide (moins de 10 min)
        if self.url_cache and (time.time() - self.url_cache_timestamp) < 600:
            url = self.url_cache.get(stream_id)
            if url:
                return url
        
        # Sinon reconstruire
        token = self.get_token()
        if not token:
            return None
        
        # Reconstruire le cache si necessaire
        if not self.url_cache or (time.time() - self.url_cache_timestamp) >= 600:
            self._rebuild_url_cache()
        
        return self.url_cache.get(stream_id)


# Instance globale
vavoo_service = VavooService()
