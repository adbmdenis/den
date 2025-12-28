#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPTV Server - Serveur Haute Performance Multi-Thread Multi-Sources
Supporte 500+ utilisateurs simultanes
Sources: Vavoo, Oha, Kool, Huhu + VOD (Films & Séries)
"""

import os
import sys
import json
import socket
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs, unquote
import threading
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SERVER_HOST, SERVER_PORT, SECRET_KEY
import database as db
from multi_service import multi_service, set_server_ip

# Pool de threads pour le streaming (max 1000 connexions simultanees)
STREAM_POOL = ThreadPoolExecutor(max_workers=1000)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Serveur HTTP multi-thread pour haute performance"""
    daemon_threads = True
    request_queue_size = 500
    allow_reuse_address = True


class IPTVHandler(BaseHTTPRequestHandler):
    # Timeout plus court pour liberer les connexions
    timeout = 300
    
    def log_message(self, format, *args):
        pass  # Silencieux
    
    def get_client_ip(self):
        return self.client_address[0]
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str, ensure_ascii=False).encode('utf-8'))
    
    def send_html(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def send_m3u(self, content, filename="playlist.m3u"):
        self.send_response(200)
        self.send_header("Content-Type", "application/x-mpegurl; charset=utf-8")
        self.send_header("Content-Disposition", f"attachment; filename={filename}")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def parse_post_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            return json.loads(post_data)
        except:
            result = {}
            for pair in post_data.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    result[unquote(key)] = unquote(value)
            return result
    
    def get_auth_admin(self):
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth[7:]
            try:
                admin_id, key = token.split(':')
                if key == SECRET_KEY:
                    return db.get_admin_by_id(int(admin_id))
            except:
                pass
        return None
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # ============== PAGES ==============
        if path == "/" or path == "/index.html":
            from admin_panel import render_home_page
            self.send_html(render_home_page(LOCAL_IP, SERVER_PORT))
            return
        
        if path == "/login":
            from admin_panel import render_login_page
            self.send_html(render_login_page())
            return
        
        if path == "/admin":
            from admin_panel import render_admin_panel
            self.send_html(render_admin_panel(LOCAL_IP, SERVER_PORT))
            return
        
        if path == "/client":
            from admin_panel import render_client_portal
            self.send_html(render_client_portal(LOCAL_IP, SERVER_PORT))
            return
        
        # ============== XTREAM CODES API (pour IPTV Smarters Pro) ==============
        if path == "/player_api.php":
            self.handle_xtream_api(params)
            return
        
        # ============== STREAM PROXY ==============
        if path.startswith("/stream/"):
            self.handle_stream_proxy(path)
            return
        
        # ============== STREAM LIVE (Xtream Codes format) ==============
        if path.startswith("/live/") or path.endswith(".ts") or path.endswith(".m3u8"):
            self.handle_live_stream(path, params)
            return
        
        # ============== IPTV PLAYLIST ==============
        if path in ["/get.php", "/playlist.m3u", "/get"]:
            self.handle_playlist(params)
            return
        
        # ============== API PUBLIQUE ==============
        if path == "/api/status":
            self.send_json({
                "status": "online",
                "channels": len(multi_service.get_channels()),
                "server": LOCAL_IP,
                "port": SERVER_PORT
            })
            return
        
        if path == "/api/subscription-types":
            types = db.get_subscription_types()
            self.send_json(types)
            return
        
        # ============== API ADMIN ==============
        if path.startswith("/api/admin/"):
            admin = self.get_auth_admin()
            if not admin:
                self.send_json({"error": "Non autorise"}, 401)
                return
            self.handle_admin_get(path, params, admin)
            return
        
        # ============== API CLIENT ==============
        if path.startswith("/api/client/"):
            self.handle_client_get(path, params)
            return
        
        self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        data = self.parse_post_data()
        
        # Login Admin
        if path == "/api/login":
            username = data.get("username")
            password = data.get("password")
            admin = db.verify_admin(username, password)
            if admin:
                token = f"{admin['id']}:{SECRET_KEY}"
                db.add_log("login", f"Admin: {username}", "admin", admin['id'], self.get_client_ip())
                self.send_json({
                    "success": True,
                    "token": token,
                    "admin": {
                        "id": admin['id'],
                        "username": admin['username'],
                        "is_super_admin": admin['is_super_admin']
                    }
                })
            else:
                self.send_json({"error": "Identifiants invalides"}, 401)
            return
        
        # Login Client
        if path == "/api/client/login":
            username = data.get("username")
            password = data.get("password")
            client = db.verify_client(username, password)
            if client:
                db.add_log("login", f"Client: {username}", "client", client['id'], self.get_client_ip())
                self.send_json({
                    "success": True,
                    "token": client['token'],
                    "client": {
                        "id": client['id'],
                        "username": client['username'],
                        "full_name": client['full_name']
                    }
                })
            else:
                self.send_json({"error": "Identifiants invalides"}, 401)
            return
        
        # API Admin POST
        if path.startswith("/api/admin/"):
            admin = self.get_auth_admin()
            if not admin:
                self.send_json({"error": "Non autorise"}, 401)
                return
            self.handle_admin_post(path, data, admin)
            return
        
        self.send_json({"error": "Not found"}, 404)

    
    def verify_iptv_client(self, params):
        """Verifie les identifiants client pour IPTV"""
        username = params.get("username", [None])[0]
        password = params.get("password", [None])[0]
        token = params.get("token", [None])[0]
        
        client = None
        if token:
            client = db.get_client_by_token(token)
        elif username and password:
            client = db.verify_client(username, password)
        
        if not client:
            return None, "Identifiants invalides"
        if not client['is_active']:
            return None, "Compte desactive"
        if not db.is_client_subscription_valid(client['id']):
            return None, "Abonnement expire"
        
        return client, None
    
    def handle_live_stream(self, path, params):
        """Gere le streaming live au format Xtream Codes /live/username/password/stream_id.ts"""
        import re
        
        # Format: /live/username/password/stream_id.ts ou .m3u8
        match = re.match(r'/live/([^/]+)/([^/]+)/(\d+)\.(ts|m3u8)', path)
        if match:
            username, password, stream_id, ext = match.groups()
            params['username'] = [username]
            params['password'] = [password]
        
        client, error = self.verify_iptv_client(params)
        if not client:
            self.send_json({"error": error}, 401)
            return
        
        # Trouver le stream par ID et rediriger vers le proxy avec authentification
        if match:
            stream_id = int(stream_id)
            self.send_response(302)
            self.send_header("Location", f"/stream/{stream_id}.ts?username={username}&token={client['token']}")
            self.end_headers()
        else:
            self.send_json({"error": "Invalid stream URL"}, 400)
    
    def handle_stream_proxy(self, path):
        """Proxy de streaming Vavoo"""
        import re
        import requests
        
        # Extraire l'ID du stream
        match = re.match(r'/stream/(\d+)\.(ts|m3u8)', path)
        if not match:
            self.send_json({"error": "Invalid stream URL"}, 400)
            return
        
        stream_id = int(match.group(1))
        
        # TODO: Ajouter contrôle des connexions ici
        # Pour l'instant, on laisse passer pour tester
        
        # S'assurer que les sources sont chargées
        if not multi_service.stream_map:
            multi_service.load_all_sources()
        
        # Obtenir les infos du stream
        stream_info = multi_service.stream_map.get(stream_id)
        if not stream_info:
            self.send_json({"error": f"Stream {stream_id} not found"}, 404)
            return
            return
            return
        
        # Obtenir l'URL avec token
        stream_url = multi_service.get_stream_url_by_id(stream_id)
        if not stream_url:
            self.send_json({"error": "Stream URL not available"}, 404)
            return
        
        # Déterminer le User-Agent (Vavoo uniquement)
        user_agent = 'VAVOO/2.6'
        
        try:
            session = requests.Session()
            headers = {
                'User-Agent': user_agent,
                'Accept': '*/*',
                'Connection': 'keep-alive',
            }
            
            resp = session.get(stream_url, headers=headers, stream=True, timeout=30, allow_redirects=True)
            
            # Si erreur 403, rafraîchir le token
            if resp.status_code == 403:
                multi_service.get_token(force=True)
                stream_url = multi_service.get_stream_url_by_id(stream_id)
                if stream_url:
                    resp = session.get(stream_url, headers=headers, stream=True, timeout=30)
            
            if resp.status_code != 200:
                self.send_json({"error": f"Stream error: {resp.status_code}"}, resp.status_code)
                return
            
            # Envoyer la reponse au client
            self.send_response(200)
            content_type = resp.headers.get("Content-Type", "video/mp2t")
            if ".m3u8" in stream_url:
                content_type = "application/vnd.apple.mpegurl"
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            
            # Streamer les donnees
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError):
                        break
                    except Exception:
                        break
            
            session.close()
                        
        except requests.exceptions.Timeout:
            self.send_json({"error": "Timeout"}, 504)
        except Exception as e:
            pass  # Silencieux pour les deconnexions normales
    
    def handle_xtream_api(self, params):
        """Gere l'API Xtream Codes pour IPTV Smarters Pro"""
        client, error = self.verify_iptv_client(params)
        if not client:
            self.send_json({"user_info": {"auth": 0, "message": error}})
            return
        
        action = params.get("action", [None])[0]
        username = params.get("username", [None])[0]
        password = params.get("password", [None])[0]
        
        # Obtenir l'abonnement actif
        sub = db.get_active_subscription(client['id'])
        exp_date = ""
        if sub and sub.get('end_date'):
            try:
                from datetime import datetime
                end_dt = datetime.fromisoformat(sub['end_date'].replace('Z', '+00:00'))
                exp_date = str(int(end_dt.timestamp()))
            except:
                exp_date = str(int(datetime.now().timestamp()) + 30*24*3600)
        
        # Info utilisateur de base (format Xtream Codes)
        user_info = {
            "username": client['username'],
            "password": password or "***",
            "message": "Welcome",
            "auth": 1,
            "status": "Active",
            "exp_date": exp_date,
            "is_trial": "0",
            "active_cons": "0",
            "created_at": str(int(datetime.fromisoformat(client['created_at']).timestamp())) if client.get('created_at') else "",
            "max_connections": str(sub['max_connections']) if sub else "1",
            "allowed_output_formats": ["m3u8", "ts"]
        }
        
        server_info = {
            "url": LOCAL_IP,
            "port": str(SERVER_PORT),
            "https_port": str(SERVER_PORT),
            "server_protocol": "http",
            "rtmp_port": "1935",
            "timezone": "Europe/Paris",
            "timestamp_now": int(datetime.now().timestamp()),
            "time_now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Sans action = authentification simple
        if not action:
            self.send_json({
                "user_info": user_info,
                "server_info": server_info
            })
            return
        
        # Action: get_live_categories
        if action == "get_live_categories":
            categories = multi_service.get_xtream_categories()
            self.send_json(categories)
            return
        
        # Action: get_live_streams
        if action == "get_live_streams":
            category_id = params.get("category_id", [None])[0]
            streams = multi_service.get_xtream_streams(category_id)
            self.send_json(streams)
            return
        
        # Action: get_vod_categories
        if action == "get_vod_categories":
            categories = multi_service.get_vod_categories()
            self.send_json(categories)
            return
        
        # Action: get_vod_streams
        if action == "get_vod_streams":
            category_id = params.get("category_id", [None])[0]
            streams = multi_service.get_vod_streams(category_id)
            self.send_json(streams)
            return
        
        # Action: get_series_categories
        if action == "get_series_categories":
            categories = multi_service.get_series_categories()
            self.send_json(categories)
            return
        
        # Action: get_series
        if action == "get_series":
            category_id = params.get("category_id", [None])[0]
            series = multi_service.get_series(category_id)
            self.send_json(series)
            return
        
        # Action par defaut
        self.send_json({
            "user_info": user_info,
            "server_info": server_info
        })
    
    def handle_playlist(self, params):
        """Gere les requetes de playlist IPTV"""
        client, error = self.verify_iptv_client(params)
        if not client:
            self.send_json({"error": error}, 401)
            return
        
        # Ajouter connexion (sans verifier le max pour la playlist)
        db.add_connection(client['id'], self.get_client_ip(), self.headers.get('User-Agent', ''))
        
        # Generer playlist avec URLs authentifiées
        filter_country = params.get("country", [None])[0]
        filter_category = params.get("category", [None])[0]
        
        content = self.generate_authenticated_m3u(client, filter_country, filter_category)
        self.send_m3u(content)
        
        db.add_log("playlist_access", None, "client", client['id'], self.get_client_ip())
    
    def generate_authenticated_m3u(self, client, filter_country=None, filter_category=None):
        """Génère une playlist M3U avec URLs authentifiées"""
        if not multi_service.stream_map:
            multi_service.load_all_sources()
        
        lines = ["#EXTM3U"]
        
        for stream_id in sorted(multi_service.stream_map.keys()):
            data = multi_service.stream_map[stream_id]
            
            if filter_country:
                if filter_country.lower() not in data["category_name"].lower():
                    continue
            
            # URL avec authentification
            url = f"http://{LOCAL_IP}:{SERVER_PORT}/stream/{stream_id}.ts?username={client['username']}&token={client['token']}"
            
            lines.append(f'#EXTINF:-1 tvg-id="{data["tvg_id"] or data["name"]}" tvg-name="{data["name"]}" tvg-logo="{data["logo"]}" group-title="{data["category_name"]}",{data["name"]}')
            lines.append(url)
        
        return "\n".join(lines)
    
    def handle_admin_get(self, path, params, admin):
        """Gere les GET de l'API admin"""
        
        # Stats globales (super admin) ou personnelles
        if path == "/api/admin/stats":
            if admin['is_super_admin']:
                stats = db.get_global_stats()
                stats['channels'] = len(multi_service.get_channels())
            else:
                stats = db.get_admin_stats(admin['id'])
            self.send_json(stats)
            return
        
        # Liste des admins (super admin only)
        if path == "/api/admin/admins":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            admins = db.get_all_admins()
            self.send_json(admins)
            return
        
        # Quotas d'un admin
        if path == "/api/admin/quotas":
            admin_id = params.get("admin_id", [admin['id']])[0]
            if not admin['is_super_admin'] and int(admin_id) != admin['id']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            quotas = db.get_admin_quotas(int(admin_id))
            self.send_json(quotas)
            return
        
        # Liste des clients
        if path == "/api/admin/clients":
            if admin['is_super_admin']:
                clients = db.get_all_clients()
            else:
                clients = db.get_clients_by_admin(admin['id'])
            self.send_json(clients)
            return
        
        # Types d'abonnements
        if path == "/api/admin/subscription-types":
            types = db.get_subscription_types()
            self.send_json(types)
            return
        
        # Ventes
        if path == "/api/admin/sales":
            if admin['is_super_admin']:
                admin_filter = params.get("admin_id", [None])[0]
                admin_filter = int(admin_filter) if admin_filter else None
            else:
                admin_filter = admin['id']
            
            sales = db.get_sales(admin_id=admin_filter, limit=200)
            self.send_json(sales)
            return
        
        # Logs
        if path == "/api/admin/logs":
            limit = int(params.get("limit", [100])[0])
            logs = db.get_logs(limit=limit)
            self.send_json(logs)
            return
        
        # Stats lignes IPTV
        if path == "/api/admin/iptv-lines":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            stats = db.get_iptv_lines_stats()
            self.send_json(stats)
            return
        
        # Pays disponibles
        if path == "/api/admin/countries":
            countries = multi_service.get_countries_list()
            self.send_json(countries)
            return
        
        # Stats des chaînes
        if path == "/api/admin/channels/stats":
            stats = multi_service.get_stats()
            self.send_json(stats)
            return
        
        self.send_json({"error": "Not found"}, 404)
    
    def handle_admin_post(self, path, data, admin):
        """Gere les POST de l'API admin"""
        
        # ============== GESTION ADMINS (Super Admin) ==============
        
        if path == "/api/admin/admins/create":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            username = data.get("username")
            password = data.get("password")
            email = data.get("email", "")
            
            if not username or not password:
                self.send_json({"error": "Username et password requis"}, 400)
                return
            
            admin_id = db.create_admin(username, password, email, admin['id'])
            if admin_id:
                db.add_log("admin_created", f"Admin: {username}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True, "admin_id": admin_id})
            else:
                self.send_json({"error": "Username deja utilise"}, 400)
            return
        
        if path == "/api/admin/admins/update":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            admin_id = int(data.get("admin_id", 0))
            updates = {}
            if "is_active" in data:
                updates["is_active"] = int(data["is_active"])
            if "password" in data and data["password"]:
                updates["password"] = data["password"]
            if "email" in data:
                updates["email"] = data["email"]
            
            if db.update_admin(admin_id, **updates):
                db.add_log("admin_updated", f"Admin ID: {admin_id}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec mise a jour"}, 500)
            return
        
        if path == "/api/admin/admins/delete":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            admin_id = int(data.get("admin_id", 0))
            if db.delete_admin(admin_id):
                db.add_log("admin_deleted", f"Admin ID: {admin_id}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec suppression"}, 500)
            return
        
        # ============== GESTION QUOTAS (Super Admin) ==============
        
        if path == "/api/admin/quotas/set":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            target_admin_id = int(data.get("admin_id", 0))
            sub_type_id = int(data.get("subscription_type_id", 0))
            max_qty = int(data.get("max_quantity", 100))
            price = float(data.get("allowed_price", 0))
            valid_days = int(data.get("valid_days", 365))
            
            quota_id = db.set_admin_quota(target_admin_id, sub_type_id, max_qty, price, valid_days)
            if quota_id:
                db.add_log("quota_set", f"Admin: {target_admin_id}, Type: {sub_type_id}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True, "quota_id": quota_id})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        # ============== GESTION TYPES ABONNEMENTS (Super Admin) ==============
        
        if path == "/api/admin/subscription-types/create":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            name = data.get("name")
            duration = int(data.get("duration_days", 30))
            price = float(data.get("price", 0))
            stock = int(data.get("stock", 100))
            desc = data.get("description", "")
            
            type_id = db.create_subscription_type(name, duration, price, stock, desc)
            if type_id:
                self.send_json({"success": True, "type_id": type_id})
            else:
                self.send_json({"error": "Nom deja utilise"}, 400)
            return
        
        if path == "/api/admin/subscription-types/update":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            type_id = int(data.get("type_id", 0))
            updates = {k: v for k, v in data.items() if k != "type_id"}
            
            if db.update_subscription_type(type_id, **updates):
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec"}, 500)
            return

        
        # ============== GESTION CLIENTS ==============
        
        if path == "/api/admin/clients/create":
            username = data.get("username")
            password = data.get("password")
            email = data.get("email", "")
            phone = data.get("phone", "")
            full_name = data.get("full_name", "")
            notes = data.get("notes", "")
            
            if not username or not password:
                self.send_json({"error": "Username et password requis"}, 400)
                return
            
            result = db.create_client(username, password, email, phone, full_name, admin['id'], notes)
            if result:
                db.add_log("client_created", f"Client: {username}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True, "client": result})
            else:
                self.send_json({"error": "Username deja utilise"}, 400)
            return
        
        if path == "/api/admin/clients/update":
            client_id = int(data.get("client_id", 0))
            client = db.get_client_by_id(client_id)
            
            if not client:
                self.send_json({"error": "Client non trouve"}, 404)
                return
            
            if not admin['is_super_admin'] and client['created_by'] != admin['id']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            updates = {}
            for k in ['email', 'phone', 'full_name', 'is_active', 'notes', 'password']:
                if k in data and data[k]:
                    updates[k] = data[k] if k != 'is_active' else int(data[k])
            
            if db.update_client(client_id, **updates):
                db.add_log("client_updated", f"Client: {client['username']}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        # ============== VENTE D'ABONNEMENT ==============
        
        if path == "/api/admin/sell":
            client_id = int(data.get("client_id", 0))
            sub_type_id = int(data.get("subscription_type_id", 0))
            max_connections = int(data.get("max_connections", 1))
            payment_method = data.get("payment_method", "cash")
            payment_status = data.get("payment_status", "paid")
            amount = data.get("amount")
            
            client = db.get_client_by_id(client_id)
            if not client:
                self.send_json({"error": "Client non trouve"}, 404)
                return
            
            if not admin['is_super_admin'] and client['created_by'] != admin['id']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            # Verifier quota (sauf super admin)
            if not admin['is_super_admin']:
                can_sell, result = db.check_admin_can_sell(admin['id'], sub_type_id)
                if not can_sell:
                    self.send_json({"error": result}, 403)
                    return
                if amount is None:
                    amount = result['allowed_price']
            else:
                if amount is None:
                    sub_type = db.get_subscription_type(sub_type_id)
                    amount = sub_type['price'] if sub_type else 0
            
            # Creer l'abonnement
            subscription = db.create_subscription(client_id, sub_type_id, admin['id'], max_connections)
            if not subscription:
                self.send_json({"error": "Echec creation abonnement"}, 500)
                return
            
            # Creer la vente
            sale_id = db.create_sale(subscription['id'], admin['id'], client_id, float(amount), payment_method, payment_status)
            
            # Incrementer quota admin
            if not admin['is_super_admin']:
                db.increment_admin_sold(admin['id'], sub_type_id)
            
            db.add_log("sale", f"Client: {client['username']}, Type: {subscription['type']}", "admin", admin['id'], self.get_client_ip())
            
            self.send_json({
                "success": True,
                "subscription": subscription,
                "sale_id": sale_id,
                "playlist_url": f"http://{LOCAL_IP}:{SERVER_PORT}/get.php?username={client['username']}&password=***"
            })
            return
        
        # ============== PROLONGER ABONNEMENT ==============
        
        if path == "/api/admin/extend":
            client_id = int(data.get("client_id", 0))
            days = int(data.get("days", 30))
            
            client = db.get_client_by_id(client_id)
            if not client:
                self.send_json({"error": "Client non trouve"}, 404)
                return
            
            if not admin['is_super_admin'] and client['created_by'] != admin['id']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            # Trouver l'abonnement actif
            sub = db.get_active_subscription(client_id)
            if not sub:
                self.send_json({"error": "Pas d'abonnement actif"}, 400)
                return
            
            new_end = db.extend_subscription(sub['id'], days)
            if new_end:
                db.add_log("subscription_extended", f"Client: {client['username']}, +{days} jours", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True, "new_end_date": new_end})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        # ============== MODIFIER CONNEXIONS MAX ==============
        
        if path == "/api/admin/update-connections":
            client_id = int(data.get("client_id", 0))
            max_connections = int(data.get("max_connections", 1))
            
            client = db.get_client_by_id(client_id)
            if not client:
                self.send_json({"error": "Client non trouve"}, 404)
                return
            
            if not admin['is_super_admin'] and client['created_by'] != admin['id']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            # Trouver l'abonnement actif
            sub = db.get_active_subscription(client_id)
            if not sub:
                self.send_json({"error": "Pas d'abonnement actif"}, 400)
                return
            
            if db.update_subscription_max_connections(sub['id'], max_connections):
                db.add_log("connections_updated", f"Client: {client['username']}, Connexions: {max_connections}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        # ============== ANNULER/SUSPENDRE ABONNEMENT ==============
        
        if path == "/api/admin/subscription/cancel":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            sub_id = int(data.get("subscription_id", 0))
            if db.update_subscription_status(sub_id, "cancelled"):
                db.add_log("subscription_cancelled", f"Sub ID: {sub_id}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        # ============== RAFRAICHIR LES CHAINES ==============
        
        if path == "/api/admin/channels/refresh":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse - Super admin uniquement"}, 403)
                return
            
            try:
                log("Rafraichissement manuel des chaînes demandé...")
                
                # Forcer le rechargement
                multi_service.load_all_sources(force=True)
                
                # Obtenir les nouvelles stats
                stats = multi_service.get_stats()
                
                db.add_log("channels_refreshed", f"Chaînes: {stats['total_channels']}, Films: {stats['total_movies']}, Séries: {stats['total_series']}", "admin", admin['id'], self.get_client_ip())
                
                self.send_json({
                    "success": True,
                    "message": "Chaînes mises à jour avec succès",
                    "stats": stats
                })
            except Exception as e:
                log(f"Erreur lors du rafraîchissement: {e}")
                self.send_json({"error": f"Erreur: {str(e)}"}, 500)
            return
        
        # ============== MISE A JOUR PAIEMENT ==============
        
        if path == "/api/admin/sales/update":
            sale_id = int(data.get("sale_id", 0))
            status = data.get("status", "paid")
            
            if db.update_sale_status(sale_id, status):
                db.add_log("sale_updated", f"Sale ID: {sale_id}, Status: {status}", "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        # ============== IMPORT LIGNES IPTV (Super Admin) ==============
        
        if path == "/api/admin/iptv-lines/import":
            if not admin['is_super_admin']:
                self.send_json({"error": "Acces refuse"}, 403)
                return
            
            lines = data.get("lines", [])
            if not lines:
                self.send_json({"error": "Aucune ligne fournie"}, 400)
                return
            
            count = db.import_iptv_lines(lines)
            db.add_log("iptv_import", f"{count} lignes importees", "admin", admin['id'], self.get_client_ip())
            self.send_json({"success": True, "imported": count})
            return
        
        # ============== CHANGER MOT DE PASSE ==============
        
        if path == "/api/admin/change-password":
            old_password = data.get("old_password")
            new_password = data.get("new_password")
            
            if not old_password or not new_password:
                self.send_json({"error": "Mots de passe requis"}, 400)
                return
            
            from database import hash_password
            if admin['password'] != hash_password(old_password):
                self.send_json({"error": "Ancien mot de passe incorrect"}, 400)
                return
            
            if db.update_admin(admin['id'], password=new_password):
                db.add_log("password_changed", None, "admin", admin['id'], self.get_client_ip())
                self.send_json({"success": True})
            else:
                self.send_json({"error": "Echec"}, 500)
            return
        
        self.send_json({"error": "Not found"}, 404)
    
    def handle_client_get(self, path, params):
        """Gere les GET de l'API client"""
        token = params.get("token", [None])[0]
        if not token:
            auth = self.headers.get('Authorization', '')
            if auth.startswith('Bearer '):
                token = auth[7:]
        
        if not token:
            self.send_json({"error": "Token requis"}, 401)
            return
        
        client = db.get_client_by_token(token)
        if not client:
            self.send_json({"error": "Token invalide"}, 401)
            return
        
        if path == "/api/client/me":
            sub = db.get_active_subscription(client['id'])
            self.send_json({
                "id": client['id'],
                "username": client['username'],
                "full_name": client['full_name'],
                "email": client['email'],
                "subscription": sub,
                "playlist_url": f"http://{LOCAL_IP}:{SERVER_PORT}/get.php?token={client['token']}"
            })
            return
        
        if path == "/api/client/subscriptions":
            subs = db.get_client_subscriptions(client['id'])
            self.send_json(subs)
            return
        
        self.send_json({"error": "Not found"}, 404)


def main():
    print("=" * 60)
    print("IPTV SERVER - Vavoo uniquement")
    print("Source: Vavoo + VOD (Films & Séries)")
    print("Supporte 500+ utilisateurs simultanes")
    print("=" * 60)
    print()
    
    log("Initialisation de la base de donnees...")
    db.init_database()
    
    log("Initialisation du service Vavoo...")
    
    multi_service.initialize()
    
    # Charger Vavoo
    log("Chargement des chaînes Vavoo...")
    multi_service.load_all_sources()
    
    # Afficher les stats
    stats = multi_service.get_stats()
    
    print()
    print(f"Serveur demarre sur: http://{LOCAL_IP}:{SERVER_PORT}")
    print()
    print("=" * 50)
    print("STATISTIQUES:")
    print(f"  - Chaines Live: {stats['total_channels']}")
    print(f"  - Films: {stats['total_movies']}")
    print(f"  - Series: {stats['total_series']}")
    print(f"  - Token Vavoo: {'OK' if stats['token_valid'] else 'Non'}")
    print("=" * 50)
    print()
    print("URLs importantes:")
    print(f"  - Page d'accueil:    http://{LOCAL_IP}:{SERVER_PORT}/")
    print(f"  - Panel Admin:       http://{LOCAL_IP}:{SERVER_PORT}/admin")
    print(f"  - Portail Client:    http://{LOCAL_IP}:{SERVER_PORT}/client")
    print()
    print("Configuration IPTV Smarters Pro:")
    print(f"  - Server URL: http://{LOCAL_IP}")
    print(f"  - Port: {SERVER_PORT}")
    print(f"  - Username: (votre client)")
    print(f"  - Password: (mot de passe client)")
    print()
    print("Identifiants Super Admin:")
    print(f"  - Username: superadmin")
    print(f"  - Password: Super@2024!")
    print()
    print("Rafraichissement automatique:")
    print("  - Tokens Vavoo: toutes les 10 minutes")
    print()
    print("=" * 60)
    
    # Serveur multi-thread haute performance
    server = ThreadedHTTPServer((SERVER_HOST, SERVER_PORT), IPTVHandler)
    
    log(f"Serveur multi-thread pret (max 500+ connexions)")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArret du serveur...")
        STREAM_POOL.shutdown(wait=False)
        server.shutdown()


if __name__ == "__main__":
    main()
