#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Panel d'administration HTML complet"""

from config import SERVER_PORT, PAYMENT_STATUS, PAYMENT_METHODS

CSS = """<style>
*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',Arial,sans-serif;background:#0f0f1a;color:#eee}
.sidebar{position:fixed;left:0;top:0;width:260px;height:100vh;background:#1a1a2e;padding:20px;overflow-y:auto}
.logo{font-size:1.5em;color:#e94560;font-weight:bold;margin-bottom:30px;text-align:center}
.nav-item{display:block;padding:12px 15px;color:#888;text-decoration:none;border-radius:8px;margin-bottom:5px;cursor:pointer}
.nav-item:hover,.nav-item.active{background:rgba(233,69,96,0.2);color:#e94560}
.nav-section{color:#555;font-size:0.75em;margin:20px 0 10px;text-transform:uppercase}
.main{margin-left:260px;padding:30px;min-height:100vh}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:30px;flex-wrap:wrap;gap:15px}
.header h1{font-size:1.8em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px;margin-bottom:30px}
.stat-card{background:linear-gradient(135deg,#1a1a2e,#16213e);padding:20px;border-radius:12px;border-left:4px solid #e94560}
.stat-card h3{color:#888;font-size:0.85em;margin-bottom:8px}.stat-card .value{font-size:1.8em;color:#e94560;font-weight:bold}
.card{background:#1a1a2e;border-radius:12px;padding:20px;margin-bottom:20px}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px}
.btn{padding:10px 18px;border:none;border-radius:8px;cursor:pointer;font-size:13px;text-decoration:none;display:inline-block}
.btn-primary{background:#e94560;color:white}.btn-secondary{background:#0f3460;color:white}
.btn-danger{background:#dc3545;color:white}.btn-success{background:#28a745;color:white}
.btn-warning{background:#ffc107;color:#000}.btn-info{background:#17a2b8;color:white}
.btn-sm{padding:6px 12px;font-size:12px}.btn-xs{padding:4px 8px;font-size:11px}
table{width:100%;border-collapse:collapse}th,td{padding:12px 10px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.08)}
th{color:#888;font-weight:500;font-size:0.85em}
.status-active,.status-paid{color:#28a745}.status-expired,.status-cancelled{color:#dc3545}.status-inactive,.status-pending{color:#ffc107}
.badge{display:inline-block;padding:4px 10px;border-radius:20px;font-size:0.75em}
.badge-success{background:rgba(40,167,69,0.2);color:#28a745}.badge-danger{background:rgba(220,53,69,0.2);color:#dc3545}
.badge-warning{background:rgba(255,193,7,0.2);color:#ffc107}.badge-info{background:rgba(23,162,184,0.2);color:#17a2b8}
.form-group{margin-bottom:15px}.form-group label{display:block;margin-bottom:6px;color:#aaa;font-size:0.9em}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:10px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:8px;background:rgba(255,255,255,0.05);color:#fff}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:1000;align-items:center;justify-content:center;padding:20px}
.modal.active{display:flex}.modal-content{background:#1a1a2e;padding:25px;border-radius:15px;width:100%;max-width:550px;max-height:90vh;overflow-y:auto}
.modal-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:15px;border-bottom:1px solid rgba(255,255,255,0.1)}
.modal-close{background:none;border:none;color:#888;font-size:28px;cursor:pointer}
.section{display:none}.section.active{display:block}
.url-box{background:#000;padding:12px 15px;border-radius:8px;font-family:monospace;word-break:break-all;margin:10px 0;font-size:0.9em}
code{background:#000;padding:2px 6px;border-radius:4px}
.alert{padding:12px 15px;border-radius:8px;margin-bottom:15px}
.alert-danger{background:rgba(220,53,69,0.15);border:1px solid rgba(220,53,69,0.3);color:#ff6b6b}
.alert-success{background:rgba(40,167,69,0.15);border:1px solid rgba(40,167,69,0.3);color:#5cb85c}
.search-box{display:flex;gap:10px;margin-bottom:15px}
.search-box input{flex:1;padding:10px 15px;border:1px solid rgba(255,255,255,0.1);border-radius:8px;background:rgba(255,255,255,0.05);color:#fff}
.search-box select{padding:10px;border-radius:8px;background:rgba(255,255,255,0.05);color:#fff;border:1px solid rgba(255,255,255,0.1)}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.info-item{padding:10px;background:rgba(0,0,0,0.2);border-radius:8px}
.info-item label{color:#888;font-size:0.8em;display:block;margin-bottom:3px}.info-item span{color:#fff;font-weight:500}
.action-btns{display:flex;gap:5px;flex-wrap:wrap}
.quota-info{background:rgba(233,69,96,0.1);padding:15px;border-radius:8px;margin-top:10px}
.quota-bar{background:#333;border-radius:10px;height:8px;overflow:hidden;margin-top:8px}
.quota-fill{background:linear-gradient(90deg,#e94560,#ff6b6b);height:100%}
</style>"""

def render_home_page(local_ip, port):
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>IPTV Server</title>{CSS}</head>
<body style="display:flex;align-items:center;justify-content:center;min-height:100vh;">
<div style="text-align:center;max-width:900px;padding:40px;">
<h1 style="font-size:3em;color:#e94560;margin-bottom:10px;">IPTV Server</h1>
<p style="color:#888;font-size:1.1em;margin-bottom:40px;">Plateforme de vente d abonnements IPTV</p>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:40px;max-width:500px;margin-left:auto;margin-right:auto;">
<a href="/admin" class="btn btn-primary" style="padding:20px;font-size:1.1em;text-align:center;">Panel Admin</a>
<a href="/client" class="btn btn-secondary" style="padding:20px;font-size:1.1em;text-align:center;">Espace Client</a>
</div>
<div class="card" style="text-align:left;">
<h3 style="margin-bottom:20px;color:#e94560;">Configuration IPTV Smarters Pro</h3>
<div class="info-grid">
<div class="info-item"><label>Type</label><span>Xtream Codes API</span></div>
<div class="info-item"><label>Server URL</label><span>http://{local_ip}:{port}</span></div>
<div class="info-item"><label>Username</label><span>Votre identifiant</span></div>
<div class="info-item"><label>Password</label><span>Votre mot de passe</span></div>
</div>
<p style="margin-top:15px;color:#888;">URL M3U:</p>
<div class="url-box">http://{local_ip}:{port}/get.php?username=USER&amp;password=PASS</div>
</div></div></body></html>"""

def render_login_page():
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Login</title>{CSS}</head>
<body style="display:flex;align-items:center;justify-content:center;min-height:100vh;">
<div class="card" style="width:100%;max-width:400px;">
<h1 style="text-align:center;color:#e94560;margin-bottom:30px;">IPTV Admin</h1>
<div class="alert alert-danger" id="error" style="display:none;"></div>
<form id="loginForm">
<div class="form-group"><label>Username</label><input type="text" id="username" required></div>
<div class="form-group"><label>Password</label><input type="password" id="password" required></div>
<button type="submit" class="btn btn-primary" style="width:100%;padding:12px;">Connexion</button>
</form></div>
<script>
document.getElementById("loginForm").onsubmit=function(e){{e.preventDefault();
fetch("/api/login",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{username:document.getElementById("username").value,password:document.getElementById("password").value}})
}}).then(r=>r.json()).then(d=>{{if(d.success){{localStorage.setItem("admin_token",d.token);localStorage.setItem("admin_info",JSON.stringify(d.admin));window.location.href="/admin";}}else{{document.getElementById("error").textContent=d.error;document.getElementById("error").style.display="block";}}}});}};
</script></body></html>"""


def render_admin_panel(local_ip, port):
    pm = "".join([f'<option value="{k}">{v}</option>' for k,v in PAYMENT_METHODS.items()])
    ps = "".join([f'<option value="{k}">{v}</option>' for k,v in PAYMENT_STATUS.items()])
    
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>IPTV Admin</title>{CSS}</head><body>
<div class="sidebar">
<div class="logo">IPTV Admin</div>
<div class="nav-section">Tableau de bord</div>
<a class="nav-item active" data-section="dashboard">Dashboard</a>
<div class="nav-section">Gestion</div>
<a class="nav-item" data-section="clients">Clients</a>
<a class="nav-item" data-section="sales">Ventes</a>
<div class="nav-section super-only">Administration</div>
<a class="nav-item super-only" data-section="admins">Vendeurs</a>
<a class="nav-item super-only" data-section="subtypes">Abonnements</a>
<div class="nav-section">Systeme</div>
<a class="nav-item super-only" data-section="logs">Logs</a>
<a class="nav-item" data-section="settings">Parametres</a>
</div>

<div class="main">
<div class="header"><h1 id="page-title">Dashboard</h1>
<div style="display:flex;gap:10px;align-items:center;">
<span id="admin-name" style="color:#888;"></span>
<span id="admin-role" class="badge badge-info"></span>
<button class="btn btn-danger btn-sm" onclick="logout()">Deconnexion</button>
</div></div>

<!-- DASHBOARD -->
<div class="section active" id="dashboard">
<div class="stats" id="stats-box"></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
<div class="card"><h3 style="margin-bottom:15px;">Serveur</h3>
<div class="info-grid">
<div class="info-item"><label>IP</label><span>{local_ip}</span></div>
<div class="info-item"><label>Port</label><span>{port}</span></div>
</div>
<p style="margin-top:15px;color:#888;">URL Playlist:</p>
<div class="url-box" style="font-size:0.85em;">http://{local_ip}:{port}/get.php?username=USER&amp;password=PASS</div>
</div>
<div class="card"><h3 style="margin-bottom:15px;">Actions rapides</h3>
<div style="display:flex;flex-direction:column;gap:10px;">
<button class="btn btn-primary" onclick="showModal('newClientModal')">+ Nouveau client</button>
<button class="btn btn-success" onclick="showSection('clients')">Voir les clients</button>
<button class="btn btn-secondary" onclick="showSection('sales')">Historique ventes</button>
<button class="btn super-only" style="background:#ff6b35;" onclick="refreshChannels()">🔄 Rafraîchir chaînes</button>
</div></div></div>
<div class="card" style="margin-top:20px;"><div class="card-header"><h3>Derniers clients</h3></div>
<table><thead><tr><th>Client</th><th>Expiration</th><th>Status</th><th>Actions</th></tr></thead>
<tbody id="recent-clients"></tbody></table></div>
</div>

<!-- CLIENTS -->
<div class="section" id="clients">
<div class="card"><div class="card-header"><h2>Clients</h2>
<div style="display:flex;gap:10px;"><button class="btn btn-primary" onclick="showModal('newClientModal')">+ Nouveau</button>
<button class="btn btn-secondary" onclick="loadClients()">Actualiser</button></div></div>
<div class="search-box">
<input type="text" id="search-client" placeholder="Rechercher..." onkeyup="filterClients()">
<select id="filter-status" onchange="filterClients()"><option value="">Tous</option><option value="active">Actifs</option><option value="expired">Expires</option><option value="inactive">Inactifs</option></select>
</div>
<table><thead><tr><th>Username</th><th>Nom</th><th>Contact</th><th>Expiration</th><th>Status</th><th>Actions</th></tr></thead>
<tbody id="clients-table"></tbody></table>
</div></div>

<!-- SALES -->
<div class="section" id="sales">
<div class="card"><div class="card-header"><h2>Ventes</h2><button class="btn btn-secondary" onclick="loadSales()">Actualiser</button></div>
<table><thead><tr><th>Date</th><th>Client</th><th>Vendeur</th><th>Type</th><th>Montant</th><th>Status</th><th>Actions</th></tr></thead>
<tbody id="sales-table"></tbody></table>
</div></div>

<!-- ADMINS -->
<div class="section" id="admins">
<div class="card"><div class="card-header"><h2>Vendeurs</h2>
<button class="btn btn-primary" onclick="showModal('newAdminModal')">+ Nouveau</button></div>
<table><thead><tr><th>Username</th><th>Email</th><th>Clients</th><th>Ventes</th><th>Status</th><th>Actions</th></tr></thead>
<tbody id="admins-table"></tbody></table>
</div></div>

<!-- SUBTYPES -->
<div class="section" id="subtypes">
<div class="card"><div class="card-header"><h2>Types d abonnements</h2>
<button class="btn btn-primary" onclick="showModal('newTypeModal')">+ Nouveau</button></div>
<table><thead><tr><th>Nom</th><th>Duree</th><th>Prix</th><th>Stock</th><th>Actions</th></tr></thead>
<tbody id="types-table"></tbody></table>
</div></div>

<!-- LOGS -->
<div class="section" id="logs">
<div class="card"><div class="card-header"><h2>Logs</h2><button class="btn btn-secondary" onclick="loadLogs()">Actualiser</button></div>
<table><thead><tr><th>Date</th><th>Action</th><th>Details</th><th>IP</th></tr></thead>
<tbody id="logs-table"></tbody></table>
</div></div>

<!-- SETTINGS -->
<div class="section" id="settings">
<div class="card"><h2 style="margin-bottom:20px;">Changer mot de passe</h2>
<form id="pwdForm" style="max-width:400px;">
<div class="form-group"><label>Ancien</label><input type="password" name="old_password" required></div>
<div class="form-group"><label>Nouveau</label><input type="password" name="new_password" required></div>
<button type="submit" class="btn btn-primary">Changer</button>
</form></div></div>
</div>

<!-- MODALS -->
<div class="modal" id="newClientModal"><div class="modal-content"><div class="modal-header"><h2>Nouveau client</h2><button class="modal-close" onclick="hideModal('newClientModal')">&times;</button></div>
<form id="newClientForm">
<div class="form-row"><div class="form-group"><label>Username *</label><input type="text" name="username" required></div>
<div class="form-group"><label>Password *</label><input type="text" name="password" required></div></div>
<div class="form-row"><div class="form-group"><label>Nom</label><input type="text" name="full_name"></div>
<div class="form-group"><label>Email</label><input type="email" name="email"></div></div>
<div class="form-group"><label>Telephone</label><input type="text" name="phone"></div>
<div class="form-group"><label>Notes</label><textarea name="notes" rows="2"></textarea></div>
<div style="display:flex;gap:10px;"><button type="submit" class="btn btn-primary" style="flex:1;">Creer</button>
<button type="button" class="btn btn-success" onclick="createAndSell()">Creer + Vendre</button></div>
</form></div></div>

<div class="modal" id="sellModal"><div class="modal-content"><div class="modal-header"><h2>Vendre abonnement</h2><button class="modal-close" onclick="hideModal('sellModal')">&times;</button></div>
<div id="sell-info" style="background:rgba(233,69,96,0.1);padding:15px;border-radius:8px;margin-bottom:20px;"></div>
<form id="sellForm"><input type="hidden" name="client_id" id="sell_cid">
<div class="form-group"><label>Type *</label><select name="subscription_type_id" id="sell_type" required></select></div>
<div class="form-row"><div class="form-group"><label>Connexions max</label><input type="number" name="max_connections" value="1" min="1" max="5"></div>
<div class="form-group"><label>Montant</label><input type="number" name="amount" step="0.01" id="sell_amt"></div></div>
<div class="form-row"><div class="form-group"><label>Paiement</label><select name="payment_method">{pm}</select></div>
<div class="form-group"><label>Status</label><select name="payment_status">{ps}</select></div></div>
<button type="submit" class="btn btn-success" style="width:100%;">Valider</button>
</form></div></div>

<div class="modal" id="clientInfoModal"><div class="modal-content" style="max-width:650px;"><div class="modal-header"><h2>Info client</h2><button class="modal-close" onclick="hideModal('clientInfoModal')">&times;</button></div>
<div id="clientInfoContent"></div></div></div>

<div class="modal" id="editClientModal"><div class="modal-content"><div class="modal-header"><h2>Modifier client</h2><button class="modal-close" onclick="hideModal('editClientModal')">&times;</button></div>
<form id="editClientForm"><input type="hidden" name="client_id" id="edit_cid">
<div class="form-row"><div class="form-group"><label>Nom</label><input type="text" name="full_name" id="edit_name"></div>
<div class="form-group"><label>Email</label><input type="email" name="email" id="edit_email"></div></div>
<div class="form-row"><div class="form-group"><label>Tel</label><input type="text" name="phone" id="edit_phone"></div>
<div class="form-group"><label>Nouveau mdp</label><input type="text" name="password" placeholder="Laisser vide"></div></div>
<div class="form-group"><label>Status</label><select name="is_active" id="edit_active"><option value="1">Actif</option><option value="0">Inactif</option></select></div>
<button type="submit" class="btn btn-primary" style="width:100%;">Enregistrer</button>
</form></div></div>

<div class="modal" id="extendModal"><div class="modal-content"><div class="modal-header"><h2>Prolonger</h2><button class="modal-close" onclick="hideModal('extendModal')">&times;</button></div>
<form id="extendForm"><input type="hidden" name="client_id" id="extend_cid">
<p id="extend_info" style="margin-bottom:20px;color:#888;"></p>
<div class="form-group"><label>Jours a ajouter</label>
<select name="days"><option value="1">1 jour</option><option value="7">7 jours</option><option value="30" selected>30 jours</option><option value="90">90 jours</option><option value="180">180 jours</option><option value="365">365 jours</option></select></div>
<button type="submit" class="btn btn-success" style="width:100%;">Prolonger</button>
</form></div></div>

<div class="modal" id="newAdminModal"><div class="modal-content"><div class="modal-header"><h2>Nouveau vendeur</h2><button class="modal-close" onclick="hideModal('newAdminModal')">&times;</button></div>
<form id="newAdminForm">
<div class="form-row"><div class="form-group"><label>Username *</label><input type="text" name="username" required></div>
<div class="form-group"><label>Password *</label><input type="text" name="password" required></div></div>
<div class="form-group"><label>Email</label><input type="email" name="email"></div>
<button type="submit" class="btn btn-primary" style="width:100%;">Creer</button>
</form></div></div>

<div class="modal" id="quotaModal"><div class="modal-content"><div class="modal-header"><h2>Quotas</h2><button class="modal-close" onclick="hideModal('quotaModal')">&times;</button></div>
<div id="quota-info" style="background:rgba(233,69,96,0.1);padding:15px;border-radius:8px;margin-bottom:20px;"></div>
<form id="quotaForm"><input type="hidden" name="admin_id" id="quota_aid">
<div class="form-group"><label>Type</label><select name="subscription_type_id" id="quota_type"></select></div>
<div class="form-row"><div class="form-group"><label>Quantite max</label><input type="number" name="max_quantity" value="100"></div>
<div class="form-group"><label>Prix autorise</label><input type="number" name="allowed_price" step="0.01" value="5"></div></div>
<div class="form-group"><label>Validite (jours)</label><input type="number" name="valid_days" value="365"></div>
<button type="submit" class="btn btn-primary" style="width:100%;">Definir</button>
</form><div id="current-quotas" style="margin-top:20px;"></div></div></div>

<div class="modal" id="newTypeModal"><div class="modal-content"><div class="modal-header"><h2>Nouveau type</h2><button class="modal-close" onclick="hideModal('newTypeModal')">&times;</button></div>
<form id="newTypeForm">
<div class="form-group"><label>Nom *</label><input type="text" name="name" required placeholder="ex: 1_mois"></div>
<div class="form-row"><div class="form-group"><label>Duree (jours)</label><input type="number" name="duration_days" value="30"></div>
<div class="form-group"><label>Prix</label><input type="number" name="price" step="0.01" value="5"></div></div>
<div class="form-group"><label>Stock</label><input type="number" name="stock" value="1000"></div>
<button type="submit" class="btn btn-primary" style="width:100%;">Creer</button>
</form></div></div>

<div class="modal" id="connectionsModal"><div class="modal-content"><div class="modal-header"><h2>Modifier connexions max</h2><button class="modal-close" onclick="hideModal('connectionsModal')">&times;</button></div>
<form id="connectionsForm"><input type="hidden" name="client_id" id="conn_cid">
<p id="conn_info" style="margin-bottom:20px;color:#888;"></p>
<div class="form-group"><label>Connexions simultanées max</label>
<select name="max_connections" id="conn_max"><option value="1">1 connexion</option><option value="2">2 connexions</option><option value="3">3 connexions</option><option value="4">4 connexions</option><option value="5">5 connexions</option></select></div>
<button type="submit" class="btn btn-primary" style="width:100%;">Modifier</button>
</form></div></div>

<script>
var token=localStorage.getItem("admin_token"),info=JSON.parse(localStorage.getItem("admin_info")||"{{}}"),subTypes=[],allClients=[],allSales=[];
if(!token)window.location.href="/login";
var IP="{local_ip}",PORT="{port}";
function H(){{return{{"Content-Type":"application/json","Authorization":"Bearer "+token}};}}

document.addEventListener("DOMContentLoaded",function(){{
document.getElementById("admin-name").textContent=info.username||"Admin";
document.getElementById("admin-role").textContent=info.is_super_admin?"Super Admin":"Vendeur";
if(!info.is_super_admin)document.querySelectorAll(".super-only").forEach(e=>e.style.display="none");
loadStats();loadClients();loadTypes();
if(info.is_super_admin)loadAdmins();
document.querySelectorAll(".nav-item").forEach(n=>n.onclick=function(e){{e.preventDefault();var s=this.getAttribute("data-section");if(s)showSection(s);}});
document.getElementById("newClientForm").onsubmit=createClient;
document.getElementById("sellForm").onsubmit=sell;
document.getElementById("editClientForm").onsubmit=updateClient;
document.getElementById("extendForm").onsubmit=extendSub;
document.getElementById("connectionsForm").onsubmit=updateConnections;
document.getElementById("newAdminForm").onsubmit=createAdmin;
document.getElementById("quotaForm").onsubmit=setQuota;
document.getElementById("newTypeForm").onsubmit=createType;
document.getElementById("pwdForm").onsubmit=changePwd;
document.getElementById("sell_type").onchange=function(){{document.getElementById("sell_amt").value=this.options[this.selectedIndex].getAttribute("data-price");}};
}});

function showSection(id){{
document.querySelectorAll(".section").forEach(s=>s.classList.remove("active"));
document.querySelectorAll(".nav-item").forEach(n=>n.classList.remove("active"));
document.getElementById(id).classList.add("active");
var nav=document.querySelector("[data-section="+id+"]");if(nav)nav.classList.add("active");
var t={{dashboard:"Dashboard",clients:"Clients",sales:"Ventes",admins:"Vendeurs",subtypes:"Abonnements",logs:"Logs",settings:"Parametres"}};
document.getElementById("page-title").textContent=t[id]||id;
if(id==="logs")loadLogs();if(id==="sales")loadSales();
}}

function loadStats(){{
fetch("/api/admin/stats",{{headers:H()}}).then(r=>r.json()).then(s=>{{
var h="";
if(info.is_super_admin){{
h+='<div class="stat-card"><h3>Vendeurs</h3><div class="value">'+(s.total_admins||0)+'</div></div>';
h+='<div class="stat-card"><h3>Clients</h3><div class="value">'+(s.total_clients||0)+'</div></div>';
h+='<div class="stat-card"><h3>Abonnements actifs</h3><div class="value">'+(s.active_subscriptions||0)+'</div></div>';
h+='<div class="stat-card"><h3>Ventes</h3><div class="value">'+(s.total_sales||0)+'</div></div>';
h+='<div class="stat-card"><h3>CA</h3><div class="value">'+(s.total_revenue||0).toFixed(2)+' EUR</div></div>';
}}else{{
h+='<div class="stat-card"><h3>Mes clients</h3><div class="value">'+(s.total_clients||0)+'</div></div>';
h+='<div class="stat-card"><h3>Abonnements</h3><div class="value">'+(s.active_subscriptions||0)+'</div></div>';
h+='<div class="stat-card"><h3>Ventes</h3><div class="value">'+(s.total_sales||0)+'</div></div>';
h+='<div class="stat-card"><h3>CA</h3><div class="value">'+(s.total_revenue||0).toFixed(2)+' EUR</div></div>';
}}
document.getElementById("stats-box").innerHTML=h;
}});
// Charger aussi les stats des chaînes
if(info.is_super_admin){{
fetch("/api/admin/channels/stats",{{headers:H()}}).then(r=>r.json()).then(cs=>{{
var ch='<div class="card" style="margin-top:20px;"><h3 style="margin-bottom:15px;">📺 Statistiques IPTV</h3>';
ch+='<div class="info-grid">';
ch+='<div class="info-item"><label>Chaînes Live</label><span style="color:#e94560;font-weight:bold;">'+(cs.total_channels||0)+'</span></div>';
ch+='<div class="info-item"><label>Films VOD</label><span style="color:#e94560;font-weight:bold;">'+(cs.total_movies||0)+'</span></div>';
ch+='<div class="info-item"><label>Séries</label><span style="color:#e94560;font-weight:bold;">'+(cs.total_series||0)+'</span></div>';
ch+='<div class="info-item"><label>Token Vavoo</label><span style="color:'+(cs.token_valid?'#2ecc71':'#e74c3c')+';">'+(cs.token_valid?'✅ Valide':'❌ Invalide')+'</span></div>';
ch+='</div></div>';
var sb=document.getElementById("stats-box");
if(sb.nextElementSibling)sb.nextElementSibling.insertAdjacentHTML('beforebegin',ch);
}});
}}
}}

function loadTypes(){{
fetch("/api/admin/subscription-types",{{headers:H()}}).then(r=>r.json()).then(types=>{{
subTypes=types;
var opts=types.map(t=>'<option value="'+t.id+'" data-price="'+t.price+'">'+t.name+' ('+t.duration_days+'j) - '+t.price+' EUR</option>').join("");
document.getElementById("sell_type").innerHTML=opts;
document.getElementById("quota_type").innerHTML=opts;
if(types.length>0)document.getElementById("sell_amt").value=types[0].price;
var tbl=types.map(t=>'<tr><td>'+t.name+'</td><td>'+t.duration_days+' jours</td><td>'+t.price.toFixed(2)+' EUR</td><td>'+t.stock+'</td><td><button class="btn btn-xs btn-secondary">Modifier</button></td></tr>').join("");
document.getElementById("types-table").innerHTML=tbl||'<tr><td colspan="5">Aucun</td></tr>';
}});
}}

function loadClients(){{
fetch("/api/admin/clients",{{headers:H()}}).then(r=>r.json()).then(clients=>{{
allClients=clients;renderClients(clients);
var recent=clients.slice(0,5).map(c=>{{
var exp=c.expires_at?new Date(c.expires_at):null,isExp=!exp||exp<new Date();
return'<tr><td>'+c.username+'</td><td>'+(exp?exp.toLocaleDateString():"-")+'</td><td><span class="badge '+(isExp?'badge-danger':'badge-success')+'">'+(isExp?'Expire':'Actif')+'</span></td><td><button class="btn btn-xs btn-info" onclick="showClientInfo('+c.id+')">Info</button> <button class="btn btn-xs btn-success" onclick="showSell('+c.id+')">Vendre</button></td></tr>';
}}).join("");
document.getElementById("recent-clients").innerHTML=recent||'<tr><td colspan="4">Aucun</td></tr>';
}});
}}

function renderClients(clients){{
var h=clients.map(c=>{{
var exp=c.expires_at?new Date(c.expires_at):null,isExp=!exp||exp<new Date();
var st=!c.is_active?"Inactif":(isExp?"Expire":"Actif");
var cls=!c.is_active?"badge-warning":(isExp?"badge-danger":"badge-success");
return'<tr data-u="'+c.username.toLowerCase()+'" data-s="'+(!c.is_active?"inactive":(isExp?"expired":"active"))+'"><td><strong>'+c.username+'</strong></td><td>'+(c.full_name||"-")+'</td><td>'+(c.email||c.phone||"-")+'</td><td>'+(exp?exp.toLocaleDateString():"Aucun")+'</td><td><span class="badge '+cls+'">'+st+'</span></td><td class="action-btns"><button class="btn btn-xs btn-info" onclick="showClientInfo('+c.id+')">Info</button><button class="btn btn-xs btn-success" onclick="showSell('+c.id+')">Vendre</button><button class="btn btn-xs btn-warning" onclick="showExtend('+c.id+')">+</button><button class="btn btn-xs btn-secondary" onclick="showEditClient('+c.id+')">Edit</button></td></tr>';
}}).join("");
document.getElementById("clients-table").innerHTML=h||'<tr><td colspan="6">Aucun client</td></tr>';
}}

function filterClients(){{
var s=document.getElementById("search-client").value.toLowerCase(),st=document.getElementById("filter-status").value;
var f=allClients.filter(c=>{{
var m=c.username.toLowerCase().includes(s)||(c.full_name&&c.full_name.toLowerCase().includes(s));
var exp=c.expires_at?new Date(c.expires_at):null,isExp=!exp||exp<new Date();
var cs=!c.is_active?"inactive":(isExp?"expired":"active");
return m&&(!st||cs===st);
}});
renderClients(f);
}}

function loadAdmins(){{
fetch("/api/admin/admins",{{headers:H()}}).then(r=>r.json()).then(admins=>{{
var h=admins.map(a=>'<tr><td><strong>'+a.username+'</strong></td><td>'+(a.email||"-")+'</td><td>'+(a.client_count||0)+'</td><td>'+(a.sales_count||0)+'</td><td><span class="badge '+(a.is_active?'badge-success':'badge-danger')+'">'+(a.is_active?'Actif':'Inactif')+'</span></td><td class="action-btns"><button class="btn btn-xs btn-info" onclick="showQuota('+a.id+',\\''+a.username+'\\')">Quotas</button><button class="btn btn-xs btn-'+(a.is_active?'warning':'success')+'" onclick="toggleAdmin('+a.id+','+(a.is_active?0:1)+')">'+(a.is_active?'Desactiver':'Activer')+'</button></td></tr>').join("");
document.getElementById("admins-table").innerHTML=h||'<tr><td colspan="6">Aucun</td></tr>';
}});
}}

function loadSales(){{
fetch("/api/admin/sales",{{headers:H()}}).then(r=>r.json()).then(sales=>{{
allSales=sales;
var h=sales.map(s=>'<tr><td>'+new Date(s.created_at).toLocaleString()+'</td><td>'+s.client_username+'</td><td>'+s.admin_username+'</td><td>'+s.subscription_type+'</td><td>'+s.amount.toFixed(2)+' EUR</td><td><span class="badge badge-'+(s.payment_status==="paid"?"success":(s.payment_status==="pending"?"warning":"danger"))+'">'+s.payment_status+'</span></td><td>'+(s.payment_status==="pending"?'<button class="btn btn-xs btn-success" onclick="markPaid('+s.id+')">Paye</button>':'')+'</td></tr>').join("");
document.getElementById("sales-table").innerHTML=h||'<tr><td colspan="7">Aucune</td></tr>';
}});
}}

function loadLogs(){{
fetch("/api/admin/logs?limit=100",{{headers:H()}}).then(r=>r.json()).then(logs=>{{
var h=logs.map(l=>'<tr><td>'+new Date(l.created_at).toLocaleString()+'</td><td>'+l.action+'</td><td>'+(l.details||"-")+'</td><td>'+(l.ip_address||"-")+'</td></tr>').join("");
document.getElementById("logs-table").innerHTML=h||'<tr><td colspan="4">Aucun</td></tr>';
}});
}}
</script>
""" + get_admin_js2(local_ip, port)


def get_admin_js2(local_ip, port):
    return f"""<script>
function createClient(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/clients/create",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("newClientModal");e.target.reset();loadClients();loadStats();showCreatedClient(res.client,d.password);}}
else alert("Erreur: "+(res.error||"Impossible"));
}});}}

function createAndSell(){{var f=document.getElementById("newClientForm"),d={{}};new FormData(f).forEach((v,k)=>d[k]=v);
if(!d.username||!d.password){{alert("Username et password requis");return;}}
fetch("/api/admin/clients/create",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("newClientModal");f.reset();loadClients();showSell(res.client.id);}}
else alert("Erreur: "+res.error);
}});}}

function showCreatedClient(c,pwd){{
var url="http://"+IP+":"+PORT+"/get.php?username="+c.username+"&password="+pwd;
var turl="http://"+IP+":"+PORT+"/get.php?token="+c.token;
var smartersConfig='<div style="background:rgba(23,162,184,0.1);padding:15px;border-radius:8px;margin-top:15px;"><h4 style="color:#17a2b8;margin-bottom:10px;">Configuration IPTV Smarters Pro</h4><div class="info-grid"><div class="info-item"><label>Type</label><span>Xtream Codes API</span></div><div class="info-item"><label>Server URL</label><span>http://'+IP+':'+PORT+'</span></div><div class="info-item"><label>Username</label><span>'+c.username+'</span></div><div class="info-item"><label>Password</label><span>'+pwd+'</span></div></div></div>';
document.getElementById("clientInfoContent").innerHTML='<div class="alert alert-success">Client cree!</div><div class="info-grid"><div class="info-item"><label>Username</label><span>'+c.username+'</span></div><div class="info-item"><label>Password</label><span>'+pwd+'</span></div></div>'+smartersConfig+'<p style="margin-top:15px;color:#888;">Token:</p><div class="url-box" style="font-size:0.8em;">'+c.token+'</div><p style="margin-top:15px;color:#888;">URL Playlist:</p><div class="url-box">'+url+'</div><button class="btn btn-secondary btn-sm" onclick="copyText(\\''+url+'\\')">Copier</button><p style="margin-top:15px;color:#888;">URL Token:</p><div class="url-box">'+turl+'</div><button class="btn btn-secondary btn-sm" onclick="copyText(\\''+turl+'\\')">Copier</button><hr style="margin:20px 0;border-color:rgba(255,255,255,0.1);"><button class="btn btn-success" onclick="hideModal(\\'clientInfoModal\\');showSell('+c.id+');">Vendre maintenant</button>';
showModal("clientInfoModal");
}}

function showSell(cid){{var c=allClients.find(x=>x.id===cid);if(!c)return;
document.getElementById("sell_cid").value=cid;
document.getElementById("sell-info").innerHTML='<strong style="color:#e94560;">'+c.username+'</strong>'+(c.full_name?' - '+c.full_name:'');
if(subTypes.length>0)document.getElementById("sell_amt").value=subTypes[0].price;
showModal("sellModal");
}}

function sell(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/sell",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("sellModal");loadClients();loadStats();alert("Vente OK!\\nExpire: "+new Date(res.subscription.end_date).toLocaleDateString());}}
else alert("Erreur: "+res.error);
}});}}

function showClientInfo(cid){{var c=allClients.find(x=>x.id===cid);if(!c)return;
var exp=c.expires_at?new Date(c.expires_at):null,isExp=!exp||exp<new Date();
var url="http://"+IP+":"+PORT+"/get.php?token="+c.token;
var smartersConfig='<div style="background:rgba(23,162,184,0.1);padding:15px;border-radius:8px;margin-top:15px;"><h4 style="color:#17a2b8;margin-bottom:10px;">Configuration IPTV Smarters Pro</h4><div class="info-grid"><div class="info-item"><label>Type</label><span>Xtream Codes API</span></div><div class="info-item"><label>Server URL</label><span>http://'+IP+':'+PORT+'</span></div><div class="info-item"><label>Username</label><span>'+c.username+'</span></div><div class="info-item"><label>Password</label><span>Mot de passe client</span></div></div></div>';
var connInfo = c.max_connections ? '<div class="info-item"><label>Connexions max</label><span>'+c.max_connections+'</span></div>' : '';
var hasSubscription = c.max_connections && c.subscription_id;
document.getElementById("clientInfoContent").innerHTML='<div class="info-grid"><div class="info-item"><label>Username</label><span>'+c.username+'</span></div><div class="info-item"><label>Nom</label><span>'+(c.full_name||"-")+'</span></div><div class="info-item"><label>Email</label><span>'+(c.email||"-")+'</span></div><div class="info-item"><label>Tel</label><span>'+(c.phone||"-")+'</span></div><div class="info-item"><label>Status</label><span class="'+(c.is_active?'status-active':'status-inactive')+'">'+(c.is_active?'Actif':'Inactif')+'</span></div><div class="info-item"><label>Abonnement</label><span class="'+(isExp?'status-expired':'status-active')+'">'+(isExp?'Expire':'Actif')+'</span></div>'+connInfo+'<div class="info-item"><label>Expiration</label><span>'+(exp?exp.toLocaleString():"Aucun")+'</span></div><div class="info-item"><label>Cree le</label><span>'+new Date(c.created_at).toLocaleDateString()+'</span></div></div>'+smartersConfig+'<p style="margin-top:15px;color:#888;">Token:</p><div class="url-box" style="font-size:0.75em;">'+c.token+'</div><p style="margin-top:10px;color:#888;">URL Playlist:</p><div class="url-box">'+url+'</div><div style="display:flex;gap:10px;margin-top:15px;flex-wrap:wrap;"><button class="btn btn-secondary btn-sm" onclick="copyText(\\''+url+'\\')">Copier URL</button><button class="btn btn-success btn-sm" onclick="hideModal(\\'clientInfoModal\\');showSell('+c.id+');">Vendre</button><button class="btn btn-warning btn-sm" onclick="hideModal(\\'clientInfoModal\\');showExtend('+c.id+');">Prolonger</button>'+(hasSubscription?'<button class="btn btn-info btn-sm" onclick="hideModal(\\'clientInfoModal\\');showConnections('+c.id+');">Connexions</button>':'')+'<button class="btn btn-info btn-sm" onclick="hideModal(\\'clientInfoModal\\');showEditClient('+c.id+');">Modifier</button></div>';
showModal("clientInfoModal");
}}

function showEditClient(cid){{var c=allClients.find(x=>x.id===cid);if(!c)return;
document.getElementById("edit_cid").value=cid;
document.getElementById("edit_name").value=c.full_name||"";
document.getElementById("edit_email").value=c.email||"";
document.getElementById("edit_phone").value=c.phone||"";
document.getElementById("edit_active").value=c.is_active?"1":"0";
showModal("editClientModal");
}}

function updateClient(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>{{if(v)d[k]=v;}});
fetch("/api/admin/clients/update",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("editClientModal");loadClients();alert("Client mis a jour!");}}
else alert("Erreur: "+res.error);
}});}}

function showExtend(cid){{var c=allClients.find(x=>x.id===cid);if(!c)return;
document.getElementById("extend_cid").value=cid;
var exp=c.expires_at?new Date(c.expires_at).toLocaleDateString():"Aucun";
document.getElementById("extend_info").innerHTML="Client: <strong>"+c.username+"</strong><br>Expiration: "+exp;
showModal("extendModal");
}}

function extendSub(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/extend",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("extendModal");loadClients();alert("Prolonge!\\nNouvelle expiration: "+new Date(res.new_end_date).toLocaleDateString());}}
else alert("Erreur: "+res.error);
}});}}

function showConnections(cid){{var c=allClients.find(x=>x.id===cid);if(!c)return;
document.getElementById("conn_cid").value=cid;
var currentConn = c.max_connections || 1;
document.getElementById("conn_info").innerHTML="Client: <strong>"+c.username+"</strong><br>Connexions actuelles: "+currentConn;
document.getElementById("conn_max").value=currentConn;
showModal("connectionsModal");
}}

function updateConnections(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/update-connections",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("connectionsModal");loadClients();alert("Connexions max modifiees!");}}
else alert("Erreur: "+res.error);
}});}}

function createAdmin(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/admins/create",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("newAdminModal");e.target.reset();loadAdmins();loadStats();alert("Vendeur cree!");}}
else alert("Erreur: "+res.error);
}});}}

function toggleAdmin(aid,st){{
fetch("/api/admin/admins/update",{{method:"POST",headers:H(),body:JSON.stringify({{admin_id:aid,is_active:st}})}}).then(r=>r.json()).then(res=>{{
if(res.success)loadAdmins();else alert("Erreur: "+res.error);
}});}}

function refreshChannels(){{
if(!confirm("Rafraîchir toutes les chaînes depuis Vavoo?\\nCela peut prendre 1-2 minutes."))return;
var btn=event.target;
btn.disabled=true;
btn.textContent="⏳ Rafraîchissement...";
fetch("/api/admin/channels/refresh",{{method:"POST",headers:H()}}).then(r=>r.json()).then(res=>{{
btn.disabled=false;
btn.textContent="🔄 Rafraîchir chaînes";
if(res.success){{
alert("✅ Chaînes mises à jour!\\n\\nChaînes: "+res.stats.total_channels+"\\nFilms: "+res.stats.total_movies+"\\nSéries: "+res.stats.total_series);
loadStats();
}}else alert("❌ Erreur: "+res.error);
}}).catch(e=>{{
btn.disabled=false;
btn.textContent="🔄 Rafraîchir chaînes";
alert("❌ Erreur: "+e);
}});
}}

function showQuota(aid,name){{
document.getElementById("quota_aid").value=aid;
document.getElementById("quota-info").innerHTML="Vendeur: <strong>"+name+"</strong>";
fetch("/api/admin/quotas?admin_id="+aid,{{headers:H()}}).then(r=>r.json()).then(quotas=>{{
if(quotas.length>0){{
var h='<h4 style="margin-bottom:10px;">Quotas actuels:</h4>';
quotas.forEach(q=>{{var pct=Math.round((q.sold_quantity/q.max_quantity)*100);
h+='<div class="quota-info"><strong>'+q.type_name+'</strong> - '+q.sold_quantity+'/'+q.max_quantity+' ('+pct+'%)<div class="quota-bar"><div class="quota-fill" style="width:'+pct+'%"></div></div></div>';
}});
document.getElementById("current-quotas").innerHTML=h;
}}else document.getElementById("current-quotas").innerHTML='<p style="color:#888;">Aucun quota</p>';
}});
showModal("quotaModal");
}}

function setQuota(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/quotas/set",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{alert("Quota defini!");showQuota(d.admin_id,"");}}
else alert("Erreur: "+res.error);
}});}}

function createType(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/subscription-types/create",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{hideModal("newTypeModal");e.target.reset();loadTypes();alert("Type cree!");}}
else alert("Erreur: "+res.error);
}});}}

function markPaid(sid){{
fetch("/api/admin/sales/update",{{method:"POST",headers:H(),body:JSON.stringify({{sale_id:sid,status:"paid"}})}}).then(r=>r.json()).then(res=>{{
if(res.success)loadSales();else alert("Erreur: "+res.error);
}});}}

function changePwd(e){{e.preventDefault();var d={{}};new FormData(e.target).forEach((v,k)=>d[k]=v);
fetch("/api/admin/change-password",{{method:"POST",headers:H(),body:JSON.stringify(d)}}).then(r=>r.json()).then(res=>{{
if(res.success){{e.target.reset();alert("Mot de passe change!");}}
else alert("Erreur: "+res.error);
}});}}

function copyText(t){{navigator.clipboard.writeText(t).then(()=>alert("Copie!"));}}
function showModal(id){{document.getElementById(id).classList.add("active");}}
function hideModal(id){{document.getElementById(id).classList.remove("active");}}
function logout(){{localStorage.removeItem("admin_token");localStorage.removeItem("admin_info");window.location.href="/login";}}
</script></body></html>"""


def render_client_portal(local_ip, port):
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Espace Client</title>{CSS}</head><body>
<div id="login-box" style="display:flex;align-items:center;justify-content:center;min-height:100vh;">
<div class="card" style="width:100%;max-width:400px;">
<h1 style="text-align:center;color:#e94560;margin-bottom:30px;">Espace Client</h1>
<div class="alert alert-danger" id="error" style="display:none;"></div>
<form id="loginForm">
<div class="form-group"><label>Username</label><input type="text" id="username" required></div>
<div class="form-group"><label>Password</label><input type="password" id="password" required></div>
<button type="submit" class="btn btn-primary" style="width:100%;padding:12px;">Connexion</button>
</form><p style="text-align:center;margin-top:20px;"><a href="/" style="color:#888;">Retour</a></p>
</div></div>

<div id="dashboard" style="display:none;max-width:900px;margin:0 auto;padding:40px 20px;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:30px;">
<h1 style="color:#e94560;">Mon Espace IPTV</h1>
<button class="btn btn-secondary" onclick="cLogout()">Deconnexion</button>
</div>
<div class="card"><h2 style="margin-bottom:20px;">Mon Abonnement</h2><div id="sub-info"></div></div>
<div class="card"><h2 style="margin-bottom:20px;">Configuration IPTV Smarters Pro</h2>
<div class="info-grid">
<div class="info-item"><label>Type</label><span>Xtream Codes API</span></div>
<div class="info-item"><label>Server URL</label><span>http://{local_ip}:{port}</span></div>
<div class="info-item"><label>Username</label><span id="cfg-user"></span></div>
<div class="info-item"><label>Password</label><span>Votre mot de passe</span></div>
</div></div>
<div class="card"><h2 style="margin-bottom:20px;">URL M3U</h2>
<div class="url-box" id="m3u-url"></div>
<button class="btn btn-primary" onclick="copyM3U()">Copier</button>
</div></div>

<script>
var cToken=localStorage.getItem("client_token");
if(cToken)showDash();
document.getElementById("loginForm").onsubmit=function(e){{e.preventDefault();
fetch("/api/client/login",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{username:document.getElementById("username").value,password:document.getElementById("password").value}})}}).then(r=>r.json()).then(d=>{{
if(d.success){{localStorage.setItem("client_token",d.token);cToken=d.token;showDash();}}
else{{document.getElementById("error").textContent=d.error;document.getElementById("error").style.display="block";}}
}});
}};
function showDash(){{document.getElementById("login-box").style.display="none";document.getElementById("dashboard").style.display="block";loadInfo();}}
function loadInfo(){{
fetch("/api/client/me?token="+cToken).then(r=>r.json()).then(d=>{{
if(d.error){{cLogout();return;}}
document.getElementById("cfg-user").textContent=d.username;
document.getElementById("m3u-url").textContent=d.playlist_url;
var h="";
if(d.subscription){{
var end=new Date(d.subscription.end_date),exp=end<new Date(),days=Math.ceil((end-new Date())/(1000*60*60*24));
h='<div class="info-grid"><div class="info-item"><label>Type</label><span>'+d.subscription.type_name+'</span></div><div class="info-item"><label>Status</label><span class="'+(exp?'status-expired':'status-active')+'">'+(exp?'Expire':'Actif')+'</span></div><div class="info-item"><label>Expire le</label><span>'+end.toLocaleDateString()+'</span></div><div class="info-item"><label>Jours restants</label><span>'+(exp?'0':days)+'</span></div><div class="info-item"><label>Connexions max</label><span>'+d.subscription.max_connections+'</span></div></div>';
if(exp)h+='<div class="alert alert-danger" style="margin-top:15px;">Abonnement expire. Contactez votre vendeur.</div>';
else if(days<=7)h+='<div class="alert" style="margin-top:15px;background:rgba(255,193,7,0.15);border:1px solid rgba(255,193,7,0.3);color:#ffc107;">Expire bientot!</div>';
}}else h='<div class="alert alert-danger">Aucun abonnement actif.</div>';
document.getElementById("sub-info").innerHTML=h;
}});
}}
function copyM3U(){{navigator.clipboard.writeText(document.getElementById("m3u-url").textContent);alert("Copie!");}}
function cLogout(){{localStorage.removeItem("client_token");window.location.reload();}}
</script></body></html>"""
