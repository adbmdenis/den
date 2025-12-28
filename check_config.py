#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification de la configuration avant déploiement
"""

import os
import sys

def check_env_vars():
    """Vérifie que les variables d'environnement importantes sont définies"""
    print("🔍 Vérification des variables d'environnement...")
    
    required_vars = {
        "PORT": "8888",
        "SECRET_KEY": None,
        "SUPER_ADMIN_USERNAME": "superadmin",
        "SUPER_ADMIN_PASSWORD": None,
        "SUPER_ADMIN_EMAIL": "admin@iptv.local"
    }
    
    warnings = []
    errors = []
    
    for var, default in required_vars.items():
        value = os.getenv(var)
        if value:
            if var in ["SECRET_KEY", "SUPER_ADMIN_PASSWORD"]:
                print(f"  ✅ {var}: ****** (défini)")
            else:
                print(f"  ✅ {var}: {value}")
        else:
            if default:
                print(f"  ⚠️  {var}: Non défini (utilisera la valeur par défaut: {default})")
                warnings.append(var)
            else:
                print(f"  ❌ {var}: Non défini (REQUIS)")
                errors.append(var)
    
    return warnings, errors

def check_files():
    """Vérifie que tous les fichiers nécessaires existent"""
    print("\n📁 Vérification des fichiers...")
    
    required_files = [
        "server.py",
        "config.py",
        "database.py",
        "multi_service.py",
        "admin_panel.py",
        "vavoo_service.py",
        "requirements.txt",
        "render.yaml",
        "Procfile",
        "runtime.txt",
        ".gitignore"
    ]
    
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (MANQUANT)")
            missing.append(file)
    
    return missing

def check_requirements():
    """Vérifie le fichier requirements.txt"""
    print("\n📦 Vérification des dépendances...")
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            
        required_packages = ["requests", "gunicorn"]
        missing = []
        
        for package in required_packages:
            if package in content:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ {package} (MANQUANT)")
                missing.append(package)
        
        return missing
    except FileNotFoundError:
        print("  ❌ requirements.txt non trouvé")
        return ["requirements.txt"]

def check_gitignore():
    """Vérifie que les fichiers sensibles sont dans .gitignore"""
    print("\n🔒 Vérification de la sécurité (.gitignore)...")
    
    try:
        with open(".gitignore", "r") as f:
            content = f.read()
        
        sensitive_patterns = [
            "*.db",
            ".env",
            "__pycache__"
        ]
        
        missing = []
        
        for pattern in sensitive_patterns:
            if pattern in content:
                print(f"  ✅ {pattern}")
            else:
                print(f"  ⚠️  {pattern} (recommandé)")
                missing.append(pattern)
        
        return missing
    except FileNotFoundError:
        print("  ❌ .gitignore non trouvé")
        return [".gitignore"]

def check_render_yaml():
    """Vérifie la configuration render.yaml"""
    print("\n⚙️  Vérification de render.yaml...")
    
    try:
        with open("render.yaml", "r") as f:
            content = f.read()
        
        required_keys = [
            "services:",
            "type: web",
            "env: python",
            "buildCommand:",
            "startCommand:",
            "envVars:"
        ]
        
        missing = []
        
        for key in required_keys:
            if key in content:
                print(f"  ✅ {key}")
            else:
                print(f"  ❌ {key} (MANQUANT)")
                missing.append(key)
        
        return missing
    except FileNotFoundError:
        print("  ❌ render.yaml non trouvé")
        return ["render.yaml"]

def main():
    """Fonction principale"""
    print("=" * 60)
    print("  VÉRIFICATION DE LA CONFIGURATION POUR RENDER")
    print("=" * 60)
    print()
    
    # Vérifications
    env_warnings, env_errors = check_env_vars()
    missing_files = check_files()
    missing_packages = check_requirements()
    missing_gitignore = check_gitignore()
    missing_render = check_render_yaml()
    
    # Résumé
    print("\n" + "=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    
    total_errors = len(env_errors) + len(missing_files) + len(missing_packages) + len(missing_render)
    total_warnings = len(env_warnings) + len(missing_gitignore)
    
    if total_errors == 0 and total_warnings == 0:
        print("\n✅ Tout est prêt pour le déploiement sur Render !")
        print("\n📝 Prochaines étapes :")
        print("  1. Poussez votre code sur GitHub")
        print("  2. Connectez votre dépôt à Render")
        print("  3. Render détectera automatiquement render.yaml")
        print("  4. Configurez les variables d'environnement sensibles")
        print("\n📖 Voir DEPLOY.md pour plus de détails")
        return 0
    
    if total_errors > 0:
        print(f"\n❌ {total_errors} erreur(s) trouvée(s) :")
        if env_errors:
            print(f"  - Variables d'environnement manquantes : {', '.join(env_errors)}")
        if missing_files:
            print(f"  - Fichiers manquants : {', '.join(missing_files)}")
        if missing_packages:
            print(f"  - Packages manquants : {', '.join(missing_packages)}")
        if missing_render:
            print(f"  - Configuration render.yaml incomplète")
    
    if total_warnings > 0:
        print(f"\n⚠️  {total_warnings} avertissement(s) :")
        if env_warnings:
            print(f"  - Variables d'environnement non définies (valeurs par défaut utilisées)")
        if missing_gitignore:
            print(f"  - Patterns .gitignore recommandés manquants")
    
    if total_errors > 0:
        print("\n❌ Corrigez les erreurs avant de déployer")
        return 1
    else:
        print("\n⚠️  Vous pouvez déployer, mais vérifiez les avertissements")
        return 0

if __name__ == "__main__":
    sys.exit(main())
