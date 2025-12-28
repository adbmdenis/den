#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion de la base de donnees SQLite - Plateforme IPTV Complete
"""

import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from contextlib import contextmanager

from config import (DATABASE_PATH, SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD, 
                   SUPER_ADMIN_EMAIL, DEFAULT_SUBSCRIPTION_TYPES)

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return secrets.token_urlsafe(32)

def init_database():
    """Initialise la base de donnees complete"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Table des admins/vendeurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                is_super_admin INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                login_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES admins(id)
            )
        """)
        
        # Table des quotas admin (types d'abonnements autorises par admin)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_quotas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                subscription_type_id INTEGER NOT NULL,
                max_quantity INTEGER DEFAULT 100,
                sold_quantity INTEGER DEFAULT 0,
                allowed_price REAL,
                valid_until TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (admin_id) REFERENCES admins(id),
                FOREIGN KEY (subscription_type_id) REFERENCES subscription_types(id)
            )
        """)
        
        # Table des types d'abonnements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscription_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                duration_days INTEGER NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                description TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des lignes IPTV (stock)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iptv_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                line_type TEXT NOT NULL,
                username TEXT,
                password TEXT,
                mac_address TEXT,
                m3u_url TEXT,
                server_url TEXT,
                port INTEGER,
                is_assigned INTEGER DEFAULT 0,
                assigned_to INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_to) REFERENCES clients(id)
            )
        """)
        
        # Table des clients
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                full_name TEXT,
                token TEXT UNIQUE,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                notes TEXT,
                FOREIGN KEY (created_by) REFERENCES admins(id)
            )
        """)
        
        # Table des abonnements clients
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                subscription_type_id INTEGER NOT NULL,
                iptv_line_id INTEGER,
                sold_by INTEGER NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'active',
                max_connections INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (subscription_type_id) REFERENCES subscription_types(id),
                FOREIGN KEY (iptv_line_id) REFERENCES iptv_lines(id),
                FOREIGN KEY (sold_by) REFERENCES admins(id)
            )
        """)
        
        # Table des ventes/paiements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscription_id INTEGER NOT NULL,
                admin_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT DEFAULT 'cash',
                payment_status TEXT DEFAULT 'pending',
                transaction_ref TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_at TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (subscription_id) REFERENCES subscriptions(id),
                FOREIGN KEY (admin_id) REFERENCES admins(id),
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        """)
        
        # Table des connexions actives
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        """)
        
        # Table des logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_type TEXT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table du cache VAVOO
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vavoo_cache (
                id INTEGER PRIMARY KEY,
                token TEXT,
                token_updated_at TIMESTAMP,
                channels_json TEXT,
                channels_updated_at TIMESTAMP
            )
        """)
        
        # Creer le super admin
        cursor.execute("SELECT id FROM admins WHERE is_super_admin = 1")
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO admins (username, password, email, is_super_admin)
                VALUES (?, ?, ?, 1)
            """, (SUPER_ADMIN_USERNAME, hash_password(SUPER_ADMIN_PASSWORD), SUPER_ADMIN_EMAIL))
            print(f"[DB] Super admin cree: {SUPER_ADMIN_USERNAME}")
        
        # Creer les types d'abonnements par defaut
        for sub_type in DEFAULT_SUBSCRIPTION_TYPES:
            cursor.execute("SELECT id FROM subscription_types WHERE name = ?", (sub_type['name'],))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO subscription_types (name, duration_days, price, stock)
                    VALUES (?, ?, ?, ?)
                """, (sub_type['name'], sub_type['duration_days'], sub_type['price'], sub_type['stock']))
        
        # Initialiser le cache VAVOO
        cursor.execute("SELECT id FROM vavoo_cache WHERE id = 1")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO vavoo_cache (id) VALUES (1)")
        
        print("[DB] Base de donnees initialisee")


# ============== ADMINS ==============

def get_admin_by_id(admin_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE id = ?", (admin_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_admin_by_username(username):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

def verify_admin(username, password):
    admin = get_admin_by_username(username)
    if not admin:
        return None
    if not admin['is_active']:
        return None
    if admin['locked_until']:
        if datetime.fromisoformat(admin['locked_until']) > datetime.now():
            return None
    if admin['password'] == hash_password(password):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE admins SET login_attempts = 0, last_login = CURRENT_TIMESTAMP WHERE id = ?
            """, (admin['id'],))
        return admin
    else:
        with get_db() as conn:
            cursor = conn.cursor()
            attempts = admin['login_attempts'] + 1
            locked = None
            if attempts >= 5:
                locked = (datetime.now() + timedelta(minutes=15)).isoformat()
            cursor.execute("""
                UPDATE admins SET login_attempts = ?, locked_until = ? WHERE id = ?
            """, (attempts, locked, admin['id']))
        return None

def create_admin(username, password, email, created_by):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO admins (username, password, email, created_by)
                VALUES (?, ?, ?, ?)
            """, (username, hash_password(password), email, created_by))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

def update_admin(admin_id, **kwargs):
    allowed = ['email', 'is_active', 'password']
    updates, values = [], []
    for k, v in kwargs.items():
        if k in allowed:
            if k == 'password':
                v = hash_password(v)
            updates.append(f"{k} = ?")
            values.append(v)
    if not updates:
        return False
    values.append(admin_id)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE admins SET {', '.join(updates)} WHERE id = ?", values)
        return cursor.rowcount > 0

def delete_admin(admin_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin_quotas WHERE admin_id = ?", (admin_id,))
        cursor.execute("DELETE FROM admins WHERE id = ? AND is_super_admin = 0", (admin_id,))
        return cursor.rowcount > 0

def get_all_admins():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, 
                   (SELECT COUNT(*) FROM clients WHERE created_by = a.id) as client_count,
                   (SELECT COUNT(*) FROM sales WHERE admin_id = a.id AND payment_status = 'paid') as sales_count
            FROM admins a WHERE a.is_super_admin = 0
            ORDER BY a.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

# ============== ADMIN QUOTAS ==============

def set_admin_quota(admin_id, subscription_type_id, max_quantity, allowed_price, valid_days):
    valid_until = (datetime.now() + timedelta(days=valid_days)).isoformat() if valid_days else None
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO admin_quotas 
            (admin_id, subscription_type_id, max_quantity, allowed_price, valid_until, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (admin_id, subscription_type_id, max_quantity, allowed_price, valid_until))
        return cursor.lastrowid

def get_admin_quotas(admin_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT q.*, t.name as type_name, t.duration_days, t.price as default_price
            FROM admin_quotas q
            JOIN subscription_types t ON q.subscription_type_id = t.id
            WHERE q.admin_id = ? AND q.is_active = 1
        """, (admin_id,))
        return [dict(row) for row in cursor.fetchall()]

def check_admin_can_sell(admin_id, subscription_type_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM admin_quotas 
            WHERE admin_id = ? AND subscription_type_id = ? AND is_active = 1
        """, (admin_id, subscription_type_id))
        quota = cursor.fetchone()
        if not quota:
            return False, "Type d'abonnement non autorise"
        if quota['valid_until'] and datetime.fromisoformat(quota['valid_until']) < datetime.now():
            return False, "Autorisation expiree"
        if quota['sold_quantity'] >= quota['max_quantity']:
            return False, "Quota atteint"
        return True, dict(quota)

def increment_admin_sold(admin_id, subscription_type_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE admin_quotas SET sold_quantity = sold_quantity + 1
            WHERE admin_id = ? AND subscription_type_id = ?
        """, (admin_id, subscription_type_id))

# ============== SUBSCRIPTION TYPES ==============

def get_subscription_types():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscription_types WHERE is_active = 1 ORDER BY duration_days")
        return [dict(row) for row in cursor.fetchall()]

def get_subscription_type(type_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscription_types WHERE id = ?", (type_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def create_subscription_type(name, duration_days, price, stock, description=""):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO subscription_types (name, duration_days, price, stock, description)
                VALUES (?, ?, ?, ?, ?)
            """, (name, duration_days, price, stock, description))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

def update_subscription_type(type_id, **kwargs):
    allowed = ['name', 'duration_days', 'price', 'stock', 'description', 'is_active']
    updates, values = [], []
    for k, v in kwargs.items():
        if k in allowed:
            updates.append(f"{k} = ?")
            values.append(v)
    if not updates:
        return False
    values.append(type_id)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE subscription_types SET {', '.join(updates)} WHERE id = ?", values)
        return cursor.rowcount > 0


# ============== IPTV LINES ==============

def import_iptv_lines(lines_data):
    """Importe des lignes IPTV (liste de dicts)"""
    with get_db() as conn:
        cursor = conn.cursor()
        count = 0
        for line in lines_data:
            cursor.execute("""
                INSERT INTO iptv_lines (line_type, username, password, mac_address, m3u_url, server_url, port)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                line.get('type', 'xtream'),
                line.get('username'),
                line.get('password'),
                line.get('mac'),
                line.get('m3u_url'),
                line.get('server'),
                line.get('port')
            ))
            count += 1
        return count

def get_available_iptv_line():
    """Recupere une ligne IPTV disponible"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM iptv_lines WHERE is_assigned = 0 LIMIT 1")
        row = cursor.fetchone()
        return dict(row) if row else None

def assign_iptv_line(line_id, client_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE iptv_lines SET is_assigned = 1, assigned_to = ? WHERE id = ?
        """, (client_id, line_id))
        return cursor.rowcount > 0

def get_iptv_lines_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM iptv_lines")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as assigned FROM iptv_lines WHERE is_assigned = 1")
        assigned = cursor.fetchone()['assigned']
        return {"total": total, "assigned": assigned, "available": total - assigned}

# ============== CLIENTS ==============

def get_client_by_id(client_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_client_by_username(username):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_client_by_token(token):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE token = ?", (token,))
        row = cursor.fetchone()
        return dict(row) if row else None

def verify_client(username, password):
    client = get_client_by_username(username)
    if client and client['is_active'] and client['password'] == hash_password(password):
        return client
    return None

def create_client(username, password, email, phone, full_name, created_by, notes=""):
    token = generate_token()
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clients (username, password, email, phone, full_name, token, created_by, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (username, hash_password(password), email, phone, full_name, token, created_by, notes))
            return {"id": cursor.lastrowid, "username": username, "token": token}
        except sqlite3.IntegrityError:
            return None

def update_client(client_id, **kwargs):
    allowed = ['email', 'phone', 'full_name', 'is_active', 'notes', 'password']
    updates, values = [], []
    for k, v in kwargs.items():
        if k in allowed:
            if k == 'password':
                v = hash_password(v)
            updates.append(f"{k} = ?")
            values.append(v)
    if not updates:
        return False
    values.append(client_id)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE clients SET {', '.join(updates)} WHERE id = ?", values)
        return cursor.rowcount > 0

def get_clients_by_admin(admin_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, 
                   (SELECT COUNT(*) FROM subscriptions WHERE client_id = c.id AND status = 'active') as active_subs,
                   (SELECT end_date FROM subscriptions WHERE client_id = c.id AND status = 'active' ORDER BY end_date DESC LIMIT 1) as expires_at,
                   s.max_connections, s.type_name, s.id as subscription_id
            FROM clients c 
            LEFT JOIN (
                SELECT s.client_id, s.max_connections, st.name as type_name, s.id,
                       ROW_NUMBER() OVER (PARTITION BY s.client_id ORDER BY s.end_date DESC) as rn
                FROM subscriptions s
                JOIN subscription_types st ON s.subscription_type_id = st.id
                WHERE s.status = 'active'
            ) s ON c.id = s.client_id AND s.rn = 1
            WHERE c.created_by = ?
            ORDER BY c.created_at DESC
        """, (admin_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_all_clients():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, a.username as admin_username,
                   (SELECT COUNT(*) FROM subscriptions WHERE client_id = c.id AND status = 'active') as active_subs,
                   (SELECT end_date FROM subscriptions WHERE client_id = c.id AND status = 'active' ORDER BY end_date DESC LIMIT 1) as expires_at,
                   s.max_connections, s.type_name, s.id as subscription_id
            FROM clients c
            LEFT JOIN admins a ON c.created_by = a.id
            LEFT JOIN (
                SELECT s.client_id, s.max_connections, st.name as type_name, s.id,
                       ROW_NUMBER() OVER (PARTITION BY s.client_id ORDER BY s.end_date DESC) as rn
                FROM subscriptions s
                JOIN subscription_types st ON s.subscription_type_id = st.id
                WHERE s.status = 'active'
            ) s ON c.id = s.client_id AND s.rn = 1
            ORDER BY c.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

# ============== SUBSCRIPTIONS ==============

def create_subscription(client_id, subscription_type_id, sold_by, max_connections=1, iptv_line_id=None):
    sub_type = get_subscription_type(subscription_type_id)
    if not sub_type:
        return None
    
    end_date = (datetime.now() + timedelta(days=sub_type['duration_days'])).isoformat()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscriptions (client_id, subscription_type_id, iptv_line_id, sold_by, end_date, max_connections)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (client_id, subscription_type_id, iptv_line_id, sold_by, end_date, max_connections))
        
        # Decrementer le stock
        cursor.execute("UPDATE subscription_types SET stock = stock - 1 WHERE id = ? AND stock > 0", (subscription_type_id,))
        
        return {
            "id": cursor.lastrowid,
            "client_id": client_id,
            "type": sub_type['name'],
            "end_date": end_date
        }

def get_client_subscriptions(client_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, t.name as type_name, t.duration_days
            FROM subscriptions s
            JOIN subscription_types t ON s.subscription_type_id = t.id
            WHERE s.client_id = ?
            ORDER BY s.created_at DESC
        """, (client_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_active_subscription(client_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, t.name as type_name, t.duration_days
            FROM subscriptions s
            JOIN subscription_types t ON s.subscription_type_id = t.id
            WHERE s.client_id = ? AND s.status = 'active' AND s.end_date > datetime('now')
            ORDER BY s.end_date DESC LIMIT 1
        """, (client_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_subscription_status(sub_id, status):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE subscriptions SET status = ? WHERE id = ?", (status, sub_id))
        return cursor.rowcount > 0

def extend_subscription(sub_id, days):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT end_date FROM subscriptions WHERE id = ?", (sub_id,))
        row = cursor.fetchone()
        if row:
            current = datetime.fromisoformat(row['end_date'])
            if current < datetime.now():
                current = datetime.now()
            new_end = (current + timedelta(days=days)).isoformat()
            cursor.execute("UPDATE subscriptions SET end_date = ?, status = 'active' WHERE id = ?", (new_end, sub_id))
            return new_end
    return None

def update_subscription_max_connections(sub_id, max_connections):
    """Met à jour le nombre maximum de connexions d'un abonnement"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE subscriptions SET max_connections = ? WHERE id = ?", (max_connections, sub_id))
        return cursor.rowcount > 0

def is_client_subscription_valid(client_id):
    sub = get_active_subscription(client_id)
    return sub is not None


# ============== SALES ==============

def create_sale(subscription_id, admin_id, client_id, amount, payment_method='cash', payment_status='pending', notes=""):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sales (subscription_id, admin_id, client_id, amount, payment_method, payment_status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (subscription_id, admin_id, client_id, amount, payment_method, payment_status, notes))
        return cursor.lastrowid

def update_sale_status(sale_id, status):
    with get_db() as conn:
        cursor = conn.cursor()
        paid_at = datetime.now().isoformat() if status == 'paid' else None
        cursor.execute("UPDATE sales SET payment_status = ?, paid_at = ? WHERE id = ?", (status, paid_at, sale_id))
        return cursor.rowcount > 0

def get_sales(admin_id=None, start_date=None, end_date=None, subscription_type_id=None, limit=100):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT s.*, c.username as client_username, a.username as admin_username,
                   t.name as subscription_type
            FROM sales s
            JOIN clients c ON s.client_id = c.id
            JOIN admins a ON s.admin_id = a.id
            JOIN subscriptions sub ON s.subscription_id = sub.id
            JOIN subscription_types t ON sub.subscription_type_id = t.id
            WHERE 1=1
        """
        params = []
        
        if admin_id:
            query += " AND s.admin_id = ?"
            params.append(admin_id)
        if start_date:
            query += " AND s.created_at >= ?"
            params.append(start_date)
        if end_date:
            query += " AND s.created_at <= ?"
            params.append(end_date)
        if subscription_type_id:
            query += " AND sub.subscription_type_id = ?"
            params.append(subscription_type_id)
        
        query += " ORDER BY s.created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_admin_sales(admin_id):
    return get_sales(admin_id=admin_id)

# ============== CONNECTIONS ==============

def get_active_connections(client_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM active_connections WHERE last_activity < datetime('now', '-5 minutes')")
        cursor.execute("SELECT * FROM active_connections WHERE client_id = ?", (client_id,))
        return [dict(row) for row in cursor.fetchall()]

def add_connection(client_id, ip_address, user_agent):
    with get_db() as conn:
        cursor = conn.cursor()
        # Nettoyer les connexions expirées (plus de 5 minutes d'inactivité)
        cursor.execute("DELETE FROM active_connections WHERE last_activity < datetime('now', '-5 minutes')")
        cursor.execute("""
            INSERT INTO active_connections (client_id, ip_address, user_agent)
            VALUES (?, ?, ?)
        """, (client_id, ip_address, user_agent))
        return cursor.lastrowid

def remove_connection(connection_id):
    """Supprime une connexion active"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM active_connections WHERE id = ?", (connection_id,))
        return cursor.rowcount > 0

def cleanup_expired_connections():
    """Nettoie les connexions expirées"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM active_connections WHERE last_activity < datetime('now', '-5 minutes')")
        return cursor.rowcount

def can_client_connect(client_id):
    sub = get_active_subscription(client_id)
    if not sub:
        return False, "Pas d'abonnement actif"
    connections = get_active_connections(client_id)
    if len(connections) >= sub['max_connections']:
        return False, "Nombre max de connexions atteint"
    return True, sub

# ============== LOGS ==============

def add_log(action, details=None, user_type=None, user_id=None, ip_address=None):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (user_type, user_id, action, details, ip_address)
            VALUES (?, ?, ?, ?, ?)
        """, (user_type, user_id, action, details, ip_address))

def get_logs(limit=100, user_type=None, user_id=None, action=None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM logs WHERE 1=1"
        params = []
        if user_type:
            query += " AND user_type = ?"
            params.append(user_type)
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if action:
            query += " AND action LIKE ?"
            params.append(f"%{action}%")
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

# ============== STATISTICS ==============

def get_global_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM admins WHERE is_super_admin = 0 AND is_active = 1")
        stats['total_admins'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM clients")
        stats['total_clients'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM clients WHERE is_active = 1")
        stats['active_clients'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE status = 'active' AND end_date > datetime('now')")
        stats['active_subscriptions'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE end_date <= datetime('now')")
        stats['expired_subscriptions'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sales WHERE payment_status = 'paid'")
        stats['total_sales'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM sales WHERE payment_status = 'paid'")
        stats['total_revenue'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM active_connections")
        stats['active_connections'] = cursor.fetchone()[0]
        
        # Ventes par admin
        cursor.execute("""
            SELECT a.username, COUNT(s.id) as sales_count, COALESCE(SUM(s.amount), 0) as revenue
            FROM admins a
            LEFT JOIN sales s ON a.id = s.admin_id AND s.payment_status = 'paid'
            WHERE a.is_super_admin = 0
            GROUP BY a.id
            ORDER BY revenue DESC
        """)
        stats['sales_by_admin'] = [dict(row) for row in cursor.fetchall()]
        
        return stats

def get_admin_stats(admin_id):
    with get_db() as conn:
        cursor = conn.cursor()
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM clients WHERE created_by = ?", (admin_id,))
        stats['total_clients'] = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM subscriptions s
            JOIN clients c ON s.client_id = c.id
            WHERE c.created_by = ? AND s.status = 'active' AND s.end_date > datetime('now')
        """, (admin_id,))
        stats['active_subscriptions'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sales WHERE admin_id = ? AND payment_status = 'paid'", (admin_id,))
        stats['total_sales'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM sales WHERE admin_id = ? AND payment_status = 'paid'", (admin_id,))
        stats['total_revenue'] = cursor.fetchone()[0]
        
        # Quotas
        stats['quotas'] = get_admin_quotas(admin_id)
        
        return stats

# ============== VAVOO CACHE ==============

def get_vavoo_cache():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vavoo_cache WHERE id = 1")
        return cursor.fetchone()

def update_vavoo_token(token):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE vavoo_cache SET token = ?, token_updated_at = CURRENT_TIMESTAMP WHERE id = 1", (token,))

def update_vavoo_channels(channels_json):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE vavoo_cache SET channels_json = ?, channels_updated_at = CURRENT_TIMESTAMP WHERE id = 1", (channels_json,))
