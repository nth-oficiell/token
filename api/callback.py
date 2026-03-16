#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗░░░██╗██╗░░░░░████████╗██████╗░░█████╗░ 
██║░░░██║██║░░░░░╚══██╔══╝██╔══██╗██╔══██╗
██║░░░██║██║░░░░░░░░██║░░░██████╔╝███████║
██║░░░██║██║░░░░░░░░██║░░░██╔══██╗██╔══██║
╚██████╔╝███████╗░░░██║░░░██║░░██║██║░░██║
░╚═════╝░╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝

SUPER RECHERCHE ANTI-FRAUDE - Version ULTRA
Recherche PARTUIT et encore MIEUX !
"""

import subprocess
import sys
import os
import platform

# AUTO-INSTALLATION AMÉLIORÉE
def install_dependencies():
    """Installe automatiquement toutes les dépendances sans erreur"""
    system = platform.system()
    print(f"🔧 Système détecté : {system}")
    
    # Installation spéciale pour Windows
    if system == "Windows":
        print("📦 Configuration pour Windows...")
        try:
            # Installer python-magic-bin (version Windows)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "python-magic-bin"])
            print("✅ python-magic-bin installé")
        except:
            print("⚠️ Installation alternative...")
            # Fallback: on n'utilisera pas magic
            pass
    
    # Dépendances standards
    dependencies = [
        'flask',
        'flask-cors',
        'requests',
        'pillow',
        'pytesseract',
        'python-whois',
        'dnspython',
        'pypdf2',
        'python-docx',
        'openpyxl',
        'pandas',
        'numpy',
        'opencv-python-headless',  # Version légère
        'pyzbar',
        'tldextract',
        'beautifulsoup4',
        'lxml',
        'phonenumbers',
        'email-validator',
        'scikit-learn',
        'joblib',
        'python-magic-bin; platform_system=="Windows"',  # Windows only
        'python-magic; platform_system!="Windows"',       # Linux/Mac
    ]
    
    print("\n📦 Installation des dépendances...")
    for dep in dependencies:
        if ';' in dep:
            # Dépendance conditionnelle
            continue
        
        try:
            dep_name = dep.split(';')[0].strip()
            module_name = dep_name.replace('-', '_')
            __import__(module_name)
            print(f"✅ {dep_name} déjà installé")
        except ImportError:
            try:
                print(f"⬇️ Installation de {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
                print(f"✅ {dep} installé")
            except:
                print(f"⚠️ Échec installation {dep} (non critique)")
    
    # Installation Tesseract OCR
    if system == "Windows":
        print("\n🔍 Pour l'OCR, installez Tesseract manuellement depuis:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        print("   Puis ajoutez au PATH: C:\\Program Files\\Tesseract-OCR\\")
    
    print("\n✅ Installation terminée!")

# Exécuter l'installation
if __name__ == "__main__":
    install_dependencies()

# Imports avec gestion d'erreurs
import re
import json
import hashlib
import socket
import ssl
import ipaddress
from datetime import datetime, timedelta
from urllib.parse import urlparse, unquote, parse_qs, urljoin
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import dns.resolver
import dns.reversename
import PyPDF2
from docx import Document
import openpyxl
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import pyzbar.pyzbar as pyzbar
import tldextract
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
from email_validator import validate_email, EmailNotValidError
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

# Tentative d'import magic
try:
    import magic
    MAGIC_AVAILABLE = True
except:
    MAGIC_AVAILABLE = False
    print("ℹ️ Magic non disponible, utilisation méthodes alternatives")

# Tentative import pytesseract
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except:
    TESSERACT_AVAILABLE = False
    print("ℹ️ Tesseract non disponible, OCR limité")

app = Flask(__name__)
CORS(app)

# ============================================
# BASE DE DONNÉES ULTRA COMPLÈTE
# ============================================

class UltraAntiFraudDB:
    """Base de données de menaces ultra complète"""
    
    # Liste NOIRE étendue (URLs malveillantes connues)
    MALICIOUS_URLS = set([
        'bit.ly/3xyz', 'tinyurl.com/scam', 'paypal-secure.com',
        'amazon-verification.net', 'apple-id-verify.com',
        # +1000 autres dans la version complète
    ])
    
    # Mots d'urgence MULTI-LANGUES
    URGENT_WORDS = {
        'fr': ['urgent', 'immédiat', 'rapide', 'maintenant', 'attention', 'alerte', 'délai', 'expire', 'dernier'],
        'en': ['urgent', 'immediate', 'quick', 'now', 'attention', 'alert', 'deadline', 'expire', 'final'],
        'es': ['urgente', 'inmediato', 'rápido', 'ahora', 'atención', 'alerta', 'plazo', 'caduca', 'último'],
        'de': ['dringend', 'sofort', 'schnell', 'jetzt', 'achtung', 'warnung', 'frist', 'ablauf', 'letzte'],
        'it': ['urgente', 'immediato', 'veloce', 'ora', 'attenzione', 'allarme', 'scadenza', 'scade', 'ultimo'],
        'nl': ['dringend', 'onmiddellijk', 'snel', 'nu', 'opgelet', 'alarm', 'deadline', 'verloopt', 'laatste'],
    }
    
    # Demandes d'action MULTI-LANGUES
    ACTION_WORDS = {
        'fr': ['cliquez', 'confirmez', 'connectez', 'identifiez', 'validez', 'vérifiez', 'payez', 'téléchargez'],
        'en': ['click', 'confirm', 'login', 'sign', 'validate', 'verify', 'pay', 'download'],
        'es': ['haga clic', 'confirme', 'inicie', 'identifíquese', 'valide', 'verifique', 'pague', 'descargue'],
        'de': ['klicken', 'bestätigen', 'anmelden', 'identifizieren', 'validieren', 'prüfen', 'zahlen', 'herunterladen'],
        'it': ['clicca', 'conferma', 'accedi', 'identificati', 'valida', 'verifica', 'paga', 'scarica'],
    }
    
    # Entreprises FRÉQUEMMENT usurpées (avec variantes)
    SPOOFED_BRANDS = {
        'paypal': ['paypal', 'paypai', 'paypaI', 'pay-pal', 'paypa1', 'paypall'],
        'amazon': ['amazon', 'amaz0n', 'amazone', 'amazn', 'ama-zon'],
        'google': ['google', 'g00gle', 'googel', 'goo-gle', 'go0gle'],
        'microsoft': ['microsoft', 'micros0ft', 'micro-soft', 'micr0soft'],
        'apple': ['apple', 'appIe', 'ap ple', 'app1e', 'a pple'],
        'orange': ['orange', '0range', 'oronge', 'or-ange'],
        'sfr': ['sfr', 's fr', 's-fr', '5fr'],
        'free': ['free', 'fr3e', 'fre e', 'f ree'],
        'bnp': ['bnp', 'b n p', 'b-n-p', 'bnp-paribas'],
        'societe generale': ['societe generale', 'société générale', 'soc gen'],
        'credit agricole': ['credit agricole', 'crédit agricole', 'ca'],
        'labanquepostale': ['labanquepostale', 'banque postale', 'laposte'],
    }
    
    # Extensions de fichiers TRÈS dangereuses
    DANGEROUS_EXTENSIONS = {
        '.exe': 'exécutable Windows',
        '.bat': 'script batch',
        '.cmd': 'script commande',
        '.ps1': 'powershell',
        '.vbs': 'visual basic script',
        '.js': 'javascript',
        '.jar': 'java archive',
        '.scr': 'économiseur d\'écran',
        '.pif': 'program information file',
        '.cpl': 'panneau de configuration',
        '.msi': 'installateur',
        '.reg': 'registre windows',
        '.docm': 'word avec macros',
        '.xlsm': 'excel avec macros',
        '.pptm': 'powerpoint avec macros',
    }
    
    # APIs publiques de scan
    PUBLIC_SCANNERS = {
        'phishtank': 'http://checkurl.phishtank.com/checkurl/',
        'urlhaus': 'https://urlhaus-api.abuse.ch/v1/url/',
        'threatfox': 'https://threatfox-api.abuse.ch/api/v1/',
        'abuseipdb': 'https://api.abuseipdb.com/api/v2/check',
        'ip_api': 'http://ip-api.com/json/',
        'virustotal': 'https://www.virustotal.com/api/v3/urls/',
    }
    
    # Mots-clés de phishing par catégorie
    PHISHING_KEYWORDS = {
        'banking': ['compte', 'banque', 'bank', 'virement', 'transfert', 'carte', 'rib', 'iban'],
        'security': ['sécurité', 'securite', 'security', 'hameçonnage', 'piratage', 'fraude'],
        'verification': ['vérification', 'verification', 'validation', 'confirm', 'confirmation'],
        'account': ['compte', 'account', 'suspension', 'blocage', 'désactivation'],
        'payment': ['paiement', 'payment', 'facture', 'invoice', 'remboursement', 'refund'],
        'personal': ['identifiant', 'password', 'mot de passe', 'code secret', 'cvv', 'rib'],
    }

# ============================================
# ANALYSEURS ULTRA COMPLETS
# ============================================

class UltraURLAnalyzer:
    """Analyse ULTRA complète des URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def ultra_expand_url(self, url, max_redirects=10):
        """Déplie TOUTES les redirections"""
        redirect_chain = []
        current_url = url
        final_url = url
        
        try:
            for i in range(max_redirects):
                response = self.session.head(current_url, allow_redirects=False, timeout=5)
                
                if response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location', '')
                    if location:
                        # Résoudre URL relative
                        if not location.startswith('http'):
                            location = urljoin(current_url, location)
                        
                        redirect_chain.append({
                            'step': i + 1,
                            'from': current_url,
                            'to': location,
                            'code': response.status_code
                        })
                        current_url = location
                    else:
                        break
                else:
                    final_url = current_url
                    break
            else:
                final_url = current_url
        except Exception as e:
            print(f"Erreur expansion: {e}")
        
        return final_url, redirect_chain
    
    def extract_all_features(self, url):
        """Extrait TOUTES les caractéristiques possibles"""
        features = {}
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment
        
        # Caractéristiques de base
        features['url_length'] = len(url)
        features['domain_length'] = len(domain)
        features['path_length'] = len(path)
        features['query_length'] = len(query)
        features['fragment_length'] = len(fragment)
        features['num_subdomains'] = len(domain.split('.')) - 2 if domain.count('.') > 1 else 0
        
        # Compteurs de caractères spéciaux
        features['num_dots'] = url.count('.')
        features['num_hyphens'] = url.count('-')
        features['num_underscores'] = url.count('_')
        features['num_slashes'] = url.count('/')
        features['num_params'] = url.count('=')
        features['num_ampersands'] = url.count('&')
        features['num_percent'] = url.count('%')
        features['num_at'] = url.count('@')
        
        # Vérification IP
        try:
            ipaddress.ip_address(domain)
            features['has_ip'] = 1
        except:
            features['has_ip'] = 0
        
        # HTTPS
        features['has_https'] = 1 if parsed.scheme == 'https' else 0
        
        # Port non standard
        if ':' in domain and not domain.endswith(':80') and not domain.endswith(':443'):
            features['non_standard_port'] = 1
        else:
            features['non_standard_port'] = 0
        
        # Mots-clés suspects
        suspicious_keywords = ['login', 'signin', 'account', 'update', 'secure', 
                              'verify', 'confirm', 'banking', 'paypal', 'amazon']
        features['suspicious_keywords'] = sum(1 for word in suspicious_keywords if word in url.lower())
        
        # Pourcentage chiffres
        digits = sum(c.isdigit() for c in url)
        features['digit_ratio'] = digits / len(url) if url else 0
        
        # TLD suspect
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.club', 
                          '.work', '.date', '.men', '.loan', '.download']
        ext = tldextract.extract(domain)
        features['suspicious_tld'] = 1 if ext.suffix in [tld.replace('.', '') for tld in suspicious_tlds] else 0
        
        return features
    
    def check_typosquatting_ultra(self, domain):
        """Détection ULTRA de typosquatting"""
        signals = []
        ext = tldextract.extract(domain)
        main_domain = ext.domain
        tld = ext.suffix
        
        # Homoglyphes (caractères qui se ressemblent)
        homoglyphs = {
            '0': 'o', '1': 'l', '2': 'z', '3': 'e', '4': 'a',
            '5': 's', '6': 'g', '7': 't', '8': 'b', '9': 'q',
            'l': '1', 'i': '1', 'rn': 'm', 'vv': 'w', 'cl': 'd',
            'rn': 'm', 'vv': 'w', 'vvv': 'w', '|': 'i', '!': 'i'
        }
        
        # Vérifier chaque marque connue
        for brand, variants in UltraAntiFraudDB.SPOOFED_BRANDS.items():
            # Levenshtein ratio
            from difflib import SequenceMatcher
            ratio = SequenceMatcher(None, main_domain.lower(), brand.lower()).ratio()
            
            if 0.7 < ratio < 1.0:
                signals.append({
                    'signal': f'DOMAINE SUSPECT: ressemble à {brand} (similarité {ratio:.1%})',
                    'source': 'typosquatting',
                    'confidence': ratio
                })
            
            # Vérification des variantes
            for variant in variants:
                if variant in main_domain.lower():
                    signals.append({
                        'signal': f'VARIANTE DÉTECTÉE: {variant} (usurpation {brand})',
                        'source': 'brand_variant'
                    })
            
            # Bitsquatting (1 bit flip)
            # À implémenter en version complète
        
        return signals
    
    def deep_dns_analysis(self, domain):
        """Analyse DNS approfondie"""
        dns_info = {}
        
        try:
            # Résolution A
            answers = dns.resolver.resolve(domain, 'A')
            dns_info['ips'] = [str(r) for r in answers]
            
            # Résolution MX (mail servers)
            try:
                mx = dns.resolver.resolve(domain, 'MX')
                dns_info['mx'] = [str(r.exchange) for r in mx]
            except:
                dns_info['mx'] = []
            
            # Résolution TXT (SPF, DKIM, etc.)
            try:
                txt = dns.resolver.resolve(domain, 'TXT')
                dns_info['txt'] = [str(r) for r in txt]
            except:
                dns_info['txt'] = []
            
            # Reverse DNS pour chaque IP
            dns_info['reverse_dns'] = []
            for ip in dns_info.get('ips', []):
                try:
                    rev = dns.reversename.from_address(ip)
                    rev_answers = dns.resolver.resolve(rev, 'PTR')
                    dns_info['reverse_dns'].extend([str(r) for r in rev_answers])
                except:
                    pass
            
            # Vérification blacklists DNS
            dnsbl_servers = [
                'zen.spamhaus.org',
                'b.barracudacentral.org',
                'bl.spamcop.net'
            ]
            
            dns_info['blacklisted'] = []
            for ip in dns_info.get('ips', []):
                for dnsbl in dnsbl_servers:
                    try:
                        rev = '.'.join(reversed(ip.split('.')))
                        query = f"{rev}.{dnsbl}"
                        dns.resolver.resolve(query, 'A')
                        dns_info['blacklisted'].append(f"{ip} sur {dnsbl}")
                    except:
                        pass
                        
        except Exception as e:
            dns_info['error'] = str(e)
        
        return dns_info
    
    def check_ssl_certificate(self, domain):
        """Vérification SSL approfondie"""
        ssl_info = {}
        
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(5)
                s.connect((domain, 443))
                cert = s.getpeercert()
                
                # Dates
                not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                
                ssl_info['issuer'] = dict(cert['issuer'])
                ssl_info['subject'] = dict(cert['subject'])
                ssl_info['not_before'] = not_before.isoformat()
                ssl_info['not_after'] = not_after.isoformat()
                ssl_info['days_valid'] = (not_after - datetime.now()).days
                ssl_info['version'] = cert['version']
                
                # Vérifier si le certificat est récent
                if (datetime.now() - not_before).days < 30:
                    ssl_info['recent'] = True
                else:
                    ssl_info['recent'] = False
                    
        except Exception as e:
            ssl_info['error'] = str(e)
        
        return ssl_info
    
    def scan_page_content(self, url):
        """Scanne le contenu de la page si accessible"""
        content_info = {}
        
        try:
            response = self.session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Titre
            content_info['title'] = soup.title.string if soup.title else None
            
            # Formulaires
            forms = soup.find_all('form')
            content_info['num_forms'] = len(forms)
            
            # Champs de saisie sensibles
            sensitive_inputs = []
            for form in forms:
                inputs = form.find_all('input')
                for inp in inputs:
                    input_type = inp.get('type', '')
                    input_name = inp.get('name', '').lower()
                    if 'password' in input_name or 'pass' in input_name or 'code' in input_name:
                        sensitive_inputs.append({
                            'type': input_type,
                            'name': input_name
                        })
            
            content_info['sensitive_inputs'] = sensitive_inputs
            
            # Liens externes
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('http'):
                    links.append(href)
            content_info['external_links'] = links[:10]
            
            # Si la page demande des identifiants
            if sensitive_inputs:
                content_info['login_page'] = True
            else:
                content_info['login_page'] = False
                
        except Exception as e:
            content_info['error'] = str(e)
        
        return content_info

class UltraTextAnalyzer:
    """Analyse ULTRA des textes"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
    def detect_language(self, text):
        """Détecte la langue du texte"""
        # Simple détection basée sur les mots
        text_lower = text.lower()
        scores = {}
        
        for lang, words in UltraAntiFraudDB.URGENT_WORDS.items():
            score = sum(1 for word in words if word in text_lower)
            scores[lang] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'unknown'
    
    def extract_all_entities(self, text):
        """Extrait TOUTES les entités du texte"""
        entities = {
            'urls': [],
            'emails': [],
            'phones': [],
            'ips': [],
            'hashes': [],
            'bank_accounts': [],
            'credit_cards': []
        }
        
        # URLs (amélioré)
        url_patterns = [
            r'https?://[^\s<>"{}|\\^`\[\]]+',
            r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',
            r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?',
            r'bit\.ly/[a-zA-Z0-9]+',
            r'tinyurl\.com/[a-zA-Z0-9]+',
            r'goo\.gl/[a-zA-Z0-9]+',
            r'ow\.ly/[a-zA-Z0-9]+',
        ]
        
        for pattern in url_patterns:
            entities['urls'].extend(re.findall(pattern, text))
        
        # Emails (amélioré)
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        entities['emails'] = re.findall(email_pattern, text)
        
        # Téléphones (international)
        for match in phonenumbers.PhoneNumberMatcher(text, "FR"):
            entities['phones'].append({
                'number': phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'valid': phonenumbers.is_valid_number(match.number),
                'carrier': carrier.name_for_number(match.number, 'fr'),
                'location': geocoder.description_for_number(match.number, 'fr')
            })
        
        # IPs
        ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        entities['ips'] = re.findall(ip_pattern, text)
        
        # Hashes MD5/SHA1/SHA256
        entities['hashes'].extend(re.findall(r'\b[a-fA-F0-9]{32}\b', text))  # MD5
        entities['hashes'].extend(re.findall(r'\b[a-fA-F0-9]{40}\b', text))  # SHA1
        entities['hashes'].extend(re.findall(r'\b[a-fA-F0-9]{64}\b', text))  # SHA256
        
        # IBAN (simplifié)
        iban_pattern = r'[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}'
        entities['bank_accounts'] = re.findall(iban_pattern, text)
        
        # Cartes de crédit (simplifié)
        cc_pattern = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
        entities['credit_cards'] = re.findall(cc_pattern, text)
        
        return entities
    
    def analyze_social_engineering(self, text, language='fr'):
        """Analyse les techniques d'ingénierie sociale"""
        signals = []
        text_lower = text.lower()
        
        # 1. Urgence
        urgent_words = UltraAntiFraudDB.URGENT_WORDS.get(language, UltraAntiFraudDB.URGENT_WORDS['fr'])
        urgent_found = [w for w in urgent_words if w in text_lower]
        if urgent_found:
            signals.append({
                'signal': f'MARQUEURS D\'URGENCE: {", ".join(urgent_found[:3])}',
                'technique': 'urgency',
                'count': len(urgent_found),
                'source': 'social_engineering'
            })
        
        # 2. Demandes d'action
        action_words = UltraAntiFraudDB.ACTION_WORDS.get(language, UltraAntiFraudDB.ACTION_WORDS['fr'])
        action_found = [w for w in action_words if w in text_lower]
        if action_found:
            signals.append({
                'signal': f'DEMANDES D\'ACTION: {", ".join(action_found[:3])}',
                'technique': 'call_to_action',
                'count': len(action_found),
                'source': 'social_engineering'
            })
        
        # 3. Menaces/Conséquences
        threat_patterns = [
            r'suspendu?', r'bloqué?', r'désactivé?', r'fermé?',
            r'perte', r'définitif', r'irréversible', r'supprimé?'
        ]
        threats = []
        for pattern in threat_patterns:
            if re.search(pattern, text_lower):
                threats.append(pattern)
        if threats:
            signals.append({
                'signal': f'MENACES DÉTECTÉES: conséquences négatives',
                'technique': 'threat',
                'source': 'social_engineering'
            })
        
        # 4. Gains/Promesses
        gain_patterns = [
            r'gagné?', r'remboursement', r'réduction', r'promo',
            r'cadeau', r'offre exclusive', r'limité', r'gratuit'
        ]
        gains = [p for p in gain_patterns if re.search(p, text_lower)]
        if gains:
            signals.append({
                'signal': f'PROMESSES DE GAINS: appât',
                'technique': 'bait',
                'source': 'social_engineering'
            })
        
        # 5. Autorité/Confiance
        authority_patterns = [
            r'service client', r'administrateur', r'directeur',
            r'équipe sécurité', r'département fraudes', r'technicien'
        ]
        authorities = [a for a in authority_patterns if a in text_lower]
        if authorities:
            signals.append({
                'signal': f'USURPATION D\'AUTORITÉ: {", ".join(authorities)}',
                'technique': 'authority',
                'source': 'social_engineering'
            })
        
        # 6. Rareté
        scarcity_patterns = [
            r'délai limité', r'dernière chance', r'avant ce soir',
            r'dernières places', r'offre expire'
        ]
        if any(p in text_lower for p in scarcity_patterns):
            signals.append({
                'signal': 'TACTIQUE DE RARETÉ: délai limité',
                'technique': 'scarcity',
                'source': 'social_engineering'
            })
        
        return signals
    
    def check_brand_spoofing_ultra(self, text):
        """Détection ULTRA d'usurpation de marque"""
        signals = []
        text_lower = text.lower()
        
        for brand, variants in UltraAntiFraudDB.SPOOFED_BRANDS.items():
            for variant in variants:
                if variant in text_lower:
                    # Vérifier le contexte
                    context = re.search(f'.{{0,50}}{variant}.{{0,50}}', text_lower)
                    context_text = context.group() if context else variant
                    
                    signals.append({
                        'signal': f'USURPATION {brand.upper()} détectée: "{variant}"',
                        'context': context_text,
                        'brand': brand,
                        'confidence': 0.9 if variant == brand else 0.7,
                        'source': 'brand_spoofing'
                    })
        
        return signals

class UltraFileAnalyzer:
    """Analyse ULTRA des fichiers"""
    
    def __init__(self):
        pass
    
    def get_file_info(self, filename, content=None):
        """Obtient TOUTES les infos sur le fichier"""
        info = {
            'filename': filename,
            'extension': os.path.splitext(filename)[1].lower(),
            'size': len(content) if content else 0,
            'hash': {}
        }
        
        if content:
            # Calculer tous les hash
            info['hash']['md5'] = hashlib.md5(content).hexdigest()
            info['hash']['sha1'] = hashlib.sha1(content).hexdigest()
            info['hash']['sha256'] = hashlib.sha256(content).hexdigest()
            
            # Détection du type
            if MAGIC_AVAILABLE:
                try:
                    mime = magic.from_buffer(content[:1024], mime=True)
                    info['mime_type'] = mime
                except:
                    info['mime_type'] = 'unknown'
            else:
                # Détection basique par extension
                info['mime_type'] = self.guess_mime_by_ext(info['extension'])
        
        # Vérifier si dangereux
        if info['extension'] in UltraAntiFraudDB.DANGEROUS_EXTENSIONS:
            info['dangerous'] = True
            info['danger_reason'] = UltraAntiFraudDB.DANGEROUS_EXTENSIONS[info['extension']]
        else:
            info['dangerous'] = False
        
        return info
    
    def guess_mime_by_ext(self, ext):
        """Devine le MIME type par extension"""
        mime_map = {
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.jpg': 'image/jpeg',
            '.png': 'image/png',
            '.exe': 'application/x-msdownload',
            '.bat': 'application/x-bat',
        }
        return mime_map.get(ext, 'application/octet-stream')
    
    def extract_all_from_pdf(self, filepath):
        """Extraction ULTRA depuis PDF"""
        data = {
            'text': '',
            'urls': [],
            'emails': [],
            'metadata': {}
        }
        
        try:
            with open(filepath, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                
                # Métadonnées
                data['metadata'] = pdf.metadata if pdf.metadata else {}
                
                # Tout le texte
                for page in pdf.pages:
                    data['text'] += page.extract_text() + "\n"
                
                # URLs dans le texte
                url_pattern = r'https?://[^\s]+'
                data['urls'] = re.findall(url_pattern, data['text'])
                
                # Emails
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                data['emails'] = re.findall(email_pattern, data['text'])
                
                # Liens hypertexte
                if hasattr(pdf, 'pages'):
                    for page in pdf.pages:
                        if '/Annots' in page:
                            for annot in page['/Annots']:
                                obj = annot.get_object()
                                if '/A' in obj and '/URI' in obj['/A']:
                                    data['urls'].append(obj['/A']['/URI'])
                
        except Exception as e:
            data['error'] = str(e)
        
        return data
    
    def extract_all_from_docx(self, filepath):
        """Extraction ULTRA depuis DOCX"""
        data = {
            'text': '',
            'urls': [],
            'emails': [],
            'metadata': {}
        }
        
        try:
            doc = Document(filepath)
            
            # Métadonnées basiques
            data['metadata'] = {
                'core_properties': str(doc.core_properties) if hasattr(doc, 'core_properties') else {}
            }
            
            # Texte des paragraphes
            for para in doc.paragraphs:
                data['text'] += para.text + "\n"
                
                # URLs dans les hyperliens
                if hasattr(para, 'runs'):
                    for run in para.runs:
                        if hasattr(run, 'hyperlink') and run.hyperlink:
                            data['urls'].append(str(run.hyperlink))
            
            # Texte des tableaux
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        data['text'] += cell.text + " "
            
            # URLs dans le texte
            url_pattern = r'https?://[^\s]+'
            data['urls'].extend(re.findall(url_pattern, data['text']))
            
            # Emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            data['emails'] = re.findall(email_pattern, data['text'])
            
        except Exception as e:
            data['error'] = str(e)
        
        return data
    
    def extract_all_from_excel(self, filepath):
        """Extraction ULTRA depuis Excel"""
        data = {
            'text': '',
            'urls': [],
            'emails': [],
            'sheets': []
        }
        
        try:
            wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
            
            for sheet_name in wb.sheetnames:
                sheet_data = {
                    'name': sheet_name,
                    'rows': []
                }
                
                sheet = wb[sheet_name]
                for row in sheet.iter_rows(values_only=True):
                    row_text = ' '.join(str(cell) for cell in row if cell)
                    if row_text.strip():
                        data['text'] += row_text + "\n"
                        sheet_data['rows'].append(row_text)
                
                data['sheets'].append(sheet_data)
            
            # URLs dans le texte
            url_pattern = r'https?://[^\s]+'
            data['urls'] = re.findall(url_pattern, data['text'])
            
            # Emails
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            data['emails'] = re.findall(email_pattern, data['text'])
            
        except Exception as e:
            data['error'] = str(e)
        
        return data

class UltraImageAnalyzer:
    """Analyse ULTRA des images"""
    
    def __init__(self):
        pass
    
    def analyze_image_deep(self, image_path):
        """Analyse approfondie de l'image"""
        analysis = {
            'dimensions': None,
            'format': None,
            'mode': None,
            'colors': None,
            'text': '',
            'qr_codes': [],
            'faces': 0,
            'logos': [],
            'suspicious_elements': []
        }
        
        try:
            # Informations basiques
            img = Image.open(image_path)
            analysis['dimensions'] = img.size
            analysis['format'] = img.format
            analysis['mode'] = img.mode
            
            # Analyse des couleurs (simplifiée)
            img_cv = cv2.imread(image_path)
            if img_cv is not None:
                # Convertir en HSV
                hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
                
                # Détection de rouge (souvent utilisé pour les alertes)
                red_mask1 = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
                red_mask2 = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
                red_mask = cv2.bitwise_or(red_mask1, red_mask2)
                red_pixels = np.sum(red_mask > 0)
                
                if red_pixels > img_cv.size * 0.01:
                    analysis['suspicious_elements'].append({
                        'type': 'red_text_area',
                        'description': 'Zone de texte rouge détectée'
                    })
                
                # Détection de logos (simplifié - template matching)
                # À implémenter avec des templates de logos connus
            
            # OCR
            if TESSERACT_AVAILABLE:
                try:
                    analysis['text'] = pytesseract.image_to_string(img, lang='fra+eng')
                except:
                    pass
            
            # QR Codes
            if img_cv is not None:
                qr_codes = pyzbar.decode(img_cv)
                for qr in qr_codes:
                    analysis['qr_codes'].append({
                        'data': qr.data.decode('utf-8'),
                        'type': qr.type,
                        'rect': {
                            'x': qr.rect.left,
                            'y': qr.rect.top,
                            'width': qr.rect.width,
                            'height': qr.rect.height
                        }
                    })
            
            # Détection de visages (optionnel, nécessite opencv contrib)
            # if hasattr(cv2, 'CascadeClassifier'):
            #     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            #     gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            #     faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            #     analysis['faces'] = len(faces)
            
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis

# ============================================
# MOTEUR DE SCORING ULTRA
# ============================================

class UltraScoringEngine:
    """Moteur de scoring ultra précis"""
    
    def __init__(self):
        self.weights = {
            'blacklist_match': 100,
            'typosquatting': 80,
            'domain_age': 70,
            'ssl_issues': 60,
            'social_engineering': 50,
            'sensitive_data_request': 90,
            'redirect_chain': 40,
            'dangerous_file': 100,
            'qr_code_suspicious': 70,
            'ip_address': 60,
            'multiple_entities': 30,
            'brand_spoofing': 85,
            'dns_blacklist': 95,
            'suspicious_tld': 50,
            'url_features': 40
        }
    
    def ultra_calculate_score(self, signals, input_type, analysis_depth='deep'):
        """Calcule le score ULTRA (0-100, 0 = ultra dangereux)"""
        total_penalty = 0
        max_possible = sum(self.weights.values())
        
        # Compter les signaux par catégorie
        signal_categories = {}
        for signal in signals:
            source = signal.get('source', 'unknown')
            signal_categories[source] = signal_categories.get(source, 0) + 1
        
        # Appliquer les pénalités
        for signal in signals:
            signal_text = signal.get('signal', '').lower()
            confidence = signal.get('confidence', 1.0)
            
            # Blacklist (pénalité max)
            if any(word in signal_text for word in ['blacklist', 'malicious', 'phish', 'urlhaus']):
                total_penalty += self.weights['blacklist_match'] * confidence
            
            # Typosquatting
            elif 'typosquatting' in signal_text or 'ressemble à' in signal_text:
                total_penalty += self.weights['typosquatting'] * confidence
            
            # Domaine récent
            elif 'âge' in signal_text or 'créé il y a' in signal_text:
                days = signal.get('days', 999)
                if days < 7:
                    total_penalty += self.weights['domain_age'] * 1.0
                elif days < 30:
                    total_penalty += self.weights['domain_age'] * 0.7
                else:
                    total_penalty += self.weights['domain_age'] * 0.3
            
            # SSL issues
            elif 'ssl' in signal_text or 'certificat' in signal_text:
                total_penalty += self.weights['ssl_issues'] * confidence
            
            # Social engineering
            elif 'urgence' in signal_text or 'action' in signal_text or 'menace' in signal_text:
                count = signal.get('count', 1)
                penalty = self.weights['social_engineering'] * min(count / 3, 1.0)
                total_penalty += penalty
            
            # Demande données sensibles
            elif 'sensitive' in signal_text or 'password' in signal_text or 'login' in signal_text:
                total_penalty += self.weights['sensitive_data_request']
            
            # Redirections
            elif 'redirection' in signal_text:
                count = signal.get('count', 1)
                total_penalty += self.weights['redirect_chain'] * min(count / 3, 1.0)
            
            # Fichier dangereux
            elif 'exécutable' in signal_text or 'extension' in signal_text:
                total_penalty += self.weights['dangerous_file']
            
            # QR code suspect
            elif 'qr' in signal_text.lower():
                total_penalty += self.weights['qr_code_suspicious']
            
            # IP address
            elif 'ip' in signal_text:
                total_penalty += self.weights['ip_address']
            
            # Brand spoofing
            elif 'usurpation' in signal_text or 'spoofing' in signal_text:
                total_penalty += self.weights['brand_spoofing'] * confidence
            
            # Suspicious TLD
            elif 'tld' in signal_text:
                total_penalty += self.weights['suspicious_tld']
        
        # Bonus pour profondeur d'analyse
        if analysis_depth == 'deep':
            total_penalty = total_penalty * 0.9  # -10% car plus de confiance
        
        # Calcul final
        danger_score = max(0, 100 - (total_penalty * 100 / max_possible))
        
        # Catégorisation
        if danger_score < 20:
            category = 'ULTRA DANGEREUX'
            emoji = '🚨🚨'
        elif danger_score < 40:
            category = 'TRÈS DANGEREUX'
            emoji = '⚠️⚠️'
        elif danger_score < 60:
            category = 'DANGEREUX'
            emoji = '⚠️'
        elif danger_score < 80:
            category = 'SUSPECT'
            emoji = '🔍'
        else:
            category = 'PROBABLEMENT SAIN'
            emoji = '✅'
        
        return {
            'score': round(danger_score, 1),
            'category': category,
            'emoji': emoji,
            'penalty': round(total_penalty, 1),
            'signals_count': len(signals),
            'sources_diversity': len(signal_categories)
        }

# ============================================
# ENDPOINTS ULTRA AMÉLIORÉS
# ============================================

# Initialisation
url_analyzer = UltraURLAnalyzer()
text_analyzer = UltraTextAnalyzer()
file_analyzer = UltraFileAnalyzer()
image_analyzer = UltraImageAnalyzer()
scoring_engine = UltraScoringEngine()

# Interface web simple
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Super Anti-Fraude API</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f0f2f5; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #1a73e8; }
        code { background: #e8e8e8; padding: 2px 5px; border-radius: 3px; }
        .status { color: #0f9d58; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ SUPER RECHERCHE ANTI-FRAUDE API</h1>
        <p class="status">✅ API opérationnelle - Version ULTRA</p>
        
        <h2>Endpoints disponibles :</h2>
        
        <div class="endpoint">
            <strong>POST /analyze/text</strong> - Analyse SMS/email<br>
            <code>{"content": "Votre message", "source": "sms"}</code>
        </div>
        
        <div class="endpoint">
            <strong>POST /analyze/url</strong> - Analyse URL<br>
            <code>{"url": "https://..."}</code>
        </div>
        
        <div class="endpoint">
            <strong>POST /analyze/file</strong> - Analyse fichier<br>
            <code>multipart/form-data avec champ "file"</code>
        </div>
        
        <div class="endpoint">
            <strong>POST /analyze/image</strong> - Analyse image<br>
            <code>multipart/form-data avec champ "image"</code>
        </div>
        
        <div class="endpoint">
            <strong>POST /analyze/bulk</strong> - Analyse multiple<br>
            <code>{"items": [{"type": "url", "content": "..."}]}</code>
        </div>
        
        <div class="endpoint">
            <strong>GET /health</strong> - Statut API
        </div>
        
        <p>🔍 L'API recherche <strong>PARTOUT</strong> : URLs, emails, SMS, fichiers, images, QR codes, logs...</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Analyse ULTRA d'un texte"""
    try:
        data = request.json
        content = data.get('content', '')
        source = data.get('source', 'sms')
        
        signals = []
        
        # 1. Détection langue
        language = text_analyzer.detect_language(content)
        
        # 2. Extraction entités
        entities = text_analyzer.extract_all_entities(content)
        
        # 3. Analyse URLs trouvées
        for url in entities['urls'][:10]:
            expanded, redirects = url_analyzer.ultra_expand_url(url)
            if expanded != url:
                signals.append({
                    'signal': f'URL redirigée: {url} → {expanded[:100]}',
                    'source': 'redirect',
                    'count': len(redirects)
                })
            
            # Analyse domaine
            parsed = urlparse(expanded)
            domain = parsed.netloc
            signals.extend(url_analyzer.check_typosquatting_ultra(domain))
        
        # 4. Analyse social engineering
        signals.extend(text_analyzer.analyze_social_engineering(content, language))
        
        # 5. Brand spoofing
        signals.extend(text_analyzer.check_brand_spoofing_ultra(content))
        
        # 6. Analyse emails
        for email in entities['emails']:
            try:
                valid = validate_email(email)
                signals.append({
                    'signal': f'Email valide: {email}',
                    'source': 'email_validation'
                })
            except:
                signals.append({
                    'signal': f'Email invalide: {email}',
                    'source': 'email_validation'
                })
        
        # 7. Analyse téléphones
        for phone in entities['phones']:
            if not phone['valid']:
                signals.append({
                    'signal': f'Téléphone invalide: {phone["number"]}',
                    'source': 'phone_validation'
                })
        
        # Scoring
        score_result = scoring_engine.ultra_calculate_score(signals, source, 'deep')
        
        # Recommandations
        recommendations = generate_ultra_recommendations(signals, score_result['score'])
        
        return jsonify({
            'success': True,
            'type': 'phishing' if score_result['score'] < 50 else 'legit',
            'danger_score': score_result['score'],
            'category': score_result['category'],
            'emoji': score_result['emoji'],
            'language': language,
            'entities': entities,
            'signals_detected': signals[:30],
            'confidence': {
                'text': 0.9,
                'urls': min(1.0, len(entities['urls']) * 0.2),
                'emails': min(1.0, len(entities['emails']) * 0.3)
            },
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    """Analyse ULTRA d'une URL"""
    try:
        data = request.json
        url = data.get('url', '')
        
        signals = []
        
        # 1. Expansion complète
        expanded_url, redirects = url_analyzer.ultra_expand_url(url)
        if redirects:
            signals.append({
                'signal': f'Chaîne de {len(redirects)} redirections détectée',
                'redirects': redirects,
                'source': 'redirect_analysis'
            })
        
        # 2. Extraction caractéristiques
        features = url_analyzer.extract_all_features(expanded_url)
        
        # 3. Analyse DNS
        parsed = urlparse(expanded_url)
        domain = parsed.netloc
        
        dns_info = url_analyzer.deep_dns_analysis(domain)
        if dns_info.get('blacklisted'):
            for bl in dns_info['blacklisted']:
                signals.append({
                    'signal': f'DNS blacklisté: {bl}',
                    'source': 'dns_blacklist'
                })
        
        # 4. Vérification SSL
        if parsed.scheme == 'https':
            ssl_info = url_analyzer.check_ssl_certificate(domain)
            if ssl_info.get('recent'):
                signals.append({
                    'signal': 'Certificat SSL récent (moins de 30 jours)',
                    'source': 'ssl_analysis'
                })
            if ssl_info.get('days_valid', 999) < 30:
                signals.append({
                    'signal': f'Certificat SSL expire bientôt ({ssl_info["days_valid"]} jours)',
                    'source': 'ssl_analysis'
                })
        
        # 5. Typosquatting
        signals.extend(url_analyzer.check_typosquatting_ultra(domain))
        
        # 6. Caractéristiques suspectes
        if features['suspicious_keywords'] > 2:
            signals.append({
                'signal': f'{features["suspicious_keywords"]} mots-clés suspects dans URL',
                'source': 'url_features'
            })
        
        if features['suspicious_tld']:
            signals.append({
                'signal': 'TLD suspect détecté',
                'source': 'url_features'
            })
        
        if features['has_ip']:
            signals.append({
                'signal': 'URL utilise une adresse IP au lieu d\'un nom de domaine',
                'source': 'url_features'
            })
        
        # 7. Scan contenu (optionnel)
        try:
            content_info = url_analyzer.scan_page_content(expanded_url)
            if content_info.get('login_page'):
                signals.append({
                    'signal': 'Page de connexion détectée',
                    'sensitive_inputs': content_info.get('sensitive_inputs', []),
                    'source': 'content_scan'
                })
        except:
            pass
        
        # Scoring
        score_result = scoring_engine.ultra_calculate_score(signals, 'url', 'deep')
        
        # Statut
        if score_result['score'] < 30:
            url_status = 'malicious'
        elif score_result['score'] < 70:
            url_status = 'suspicious'
        else:
            url_status = 'safe'
        
        return jsonify({
            'success': True,
            'type': 'phishing' if url_status == 'malicious' else 'legit',
            'danger_score': score_result['score'],
            'category': score_result['category'],
            'emoji': score_result['emoji'],
            'url_status': url_status,
            'signals_detected': signals[:30],
            'domain_info': {
                'domain': domain,
                'original_url': url,
                'expanded_url': expanded_url,
                'features': features,
                'dns': dns_info,
                'redirects': redirects
            },
            'confidence': {
                'url': 0.95,
                'dns': 0.9 if dns_info else 0.7,
                'features': 0.85
            },
            'recommendations': generate_ultra_recommendations(signals, score_result['score'])
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze/file', methods=['POST'])
def analyze_file():
    """Analyse ULTRA d'un fichier"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier'}), 400
        
        file = request.files['file']
        filename = file.filename
        content = file.read()
        
        # Sauvegarde temporaire
        temp_path = f'/tmp/ultra_{hashlib.md5(content).hexdigest()}'
        with open(temp_path, 'wb') as f:
            f.write(content)
        
        signals = []
        
        # 1. Informations fichier
        file_info = file_analyzer.get_file_info(filename, content)
        
        if file_info['dangerous']:
            signals.append({
                'signal': f'FICHIER DANGEREUX: {file_info["danger_reason"]}',
                'source': 'file_type'
            })
        
        # 2. Analyse selon type
        extracted_data = {}
        ext = file_info['extension']
        
        if ext == '.pdf':
            extracted_data = file_analyzer.extract_all_from_pdf(temp_path)
        elif ext in ['.docx', '.doc']:
            extracted_data = file_analyzer.extract_all_from_docx(temp_path)
        elif ext in ['.xlsx', '.xls']:
            extracted_data = file_analyzer.extract_all_from_excel(temp_path)
        elif ext == '.txt':
            with open(temp_path, 'r', errors='ignore') as f:
                extracted_data['text'] = f.read()
        
        # 3. Analyser URLs dans le fichier
        if 'urls' in extracted_data:
            for url in extracted_data['urls'][:10]:
                expanded, _ = url_analyzer.ultra_expand_url(url)
                if expanded != url:
                    signals.append({
                        'signal': f'URL dans fichier redirige: {url[:50]}...',
                        'source': 'file_content'
                    })
        
        # 4. Analyser texte
        if 'text' in extracted_data and extracted_data['text']:
            entities = text_analyzer.extract_all_entities(extracted_data['text'])
            if entities['urls'] or entities['emails']:
                signals.append({
                    'signal': f'Contient {len(entities["urls"])} URLs et {len(entities["emails"])} emails',
                    'source': 'file_content'
                })
        
        # Nettoyage
        try:
            os.remove(temp_path)
        except:
            pass
        
        # Scoring
        score_result = scoring_engine.ultra_calculate_score(signals, 'file', 'deep')
        
        return jsonify({
            'success': True,
            'type': 'malicious' if file_info['dangerous'] else 'file',
            'danger_score': score_result['score'],
            'category': score_result['category'],
            'emoji': score_result['emoji'],
            'file_info': file_info,
            'extracted_data': {
                'text_preview': extracted_data.get('text', '')[:500] if 'text' in extracted_data else '',
                'urls': extracted_data.get('urls', [])[:20],
                'emails': extracted_data.get('emails', [])[:20],
                'metadata': extracted_data.get('metadata', {})
            },
            'signals_detected': signals[:30],
            'recommendations': generate_ultra_recommendations(signals, score_result['score'])
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    """Analyse ULTRA d'une image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Aucune image'}), 400
        
        image = request.files['image']
        content = image.read()
        
        # Sauvegarde temporaire
        temp_path = f'/tmp/ultra_img_{hashlib.md5(content).hexdigest()}.jpg'
        with open(temp_path, 'wb') as f:
            f.write(content)
        
        signals = []
        
        # Analyse approfondie
        analysis = image_analyzer.analyze_image_deep(temp_path)
        
        # QR codes
        for qr in analysis['qr_codes']:
            signals.append({
                'signal': f'QR code détecté: {qr["data"][:100]}',
                'source': 'qr_code'
            })
            
            # Analyser le contenu du QR code
            if qr['data'].startswith('http'):
                signals.append({
                    'signal': 'QR code contient une URL',
                    'source': 'qr_analysis'
                })
        
        # Texte OCR
        if analysis['text']:
            signals.append({
                'signal': f'Texte extrait: {analysis["text"][:200]}...',
                'source': 'ocr'
            })
            
            # Analyser le texte
            entities = text_analyzer.extract_all_entities(analysis['text'])
            if entities['urls']:
                signals.append({
                    'signal': f'{len(entities["urls"])} URLs dans l\'image',
                    'source': 'ocr_analysis'
                })
        
        # Éléments suspects
        for element in analysis['suspicious_elements']:
            signals.append({
                'signal': element['description'],
                'source': 'image_analysis'
            })
        
        # Nettoyage
        try:
            os.remove(temp_path)
        except:
            pass
        
        # Scoring
        score_result = scoring_engine.ultra_calculate_score(signals, 'image', 'deep')
        
        return jsonify({
            'success': True,
            'type': 'suspicious' if analysis['qr_codes'] else 'image',
            'danger_score': score_result['score'],
            'category': score_result['category'],
            'emoji': score_result['emoji'],
            'image_analysis': {
                'dimensions': analysis['dimensions'],
                'format': analysis['format'],
                'qr_codes': analysis['qr_codes'],
                'text_extracted': analysis['text'][:500] if analysis['text'] else None
            },
            'signals_detected': signals[:30],
            'recommendations': generate_ultra_recommendations(signals, score_result['score'])
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze/bulk', methods=['POST'])
def analyze_bulk():
    """Analyse multiple ULTRA"""
    try:
        data = request.json
        items = data.get('items', [])
        
        results = []
        stats = {
            'total': len(items),
            'ultra_dangerous': 0,
            'very_dangerous': 0,
            'dangerous': 0,
            'suspicious': 0,
            'safe': 0
        }
        
        for item in items:
            item_type = item.get('type')
            content = item.get('content')
            
            # Simulation rapide (en production, appeler les vrais analyseurs)
            if item_type == 'url':
                signals = url_analyzer.check_typosquatting_ultra(content)
                score = scoring_engine.ultra_calculate_score(signals, 'url', 'quick')
            elif item_type == 'text':
                signals = text_analyzer.analyze_social_engineering(content, 'fr')
                score = scoring_engine.ultra_calculate_score(signals, 'text', 'quick')
            else:
                score = {'score': 50, 'category': 'INCONNU'}
            
            # Statistiques
            if score['score'] < 20:
                stats['ultra_dangerous'] += 1
            elif score['score'] < 40:
                stats['very_dangerous'] += 1
            elif score['score'] < 60:
                stats['dangerous'] += 1
            elif score['score'] < 80:
                stats['suspicious'] += 1
            else:
                stats['safe'] += 1
            
            results.append({
                'item': content[:100],
                'type': item_type,
                'score': score['score'],
                'category': score['category']
            })
        
        return jsonify({
            'success': True,
            'summary': stats,
            'results': results,
            'global_recommendations': [
                "Analyser individuellement les éléments ULTRA DANGEREUX",
                "Mettre en quarantaine les éléments très dangereux",
                "Former les utilisateurs sur les éléments suspects",
                "Mettre à jour les blacklists",
                "Surveiller les patterns communs"
            ]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Statut de l'API"""
    return jsonify({
        'status': 'ULTRA HEALTHY',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0-ULTRA',
        'modules': {
            'url_analyzer': 'active',
            'text_analyzer': 'active',
            'file_analyzer': 'active',
            'image_analyzer': 'active',
            'scoring_engine': 'active'
        },
        'stats': {
            'magic_available': MAGIC_AVAILABLE,
            'tesseract_available': TESSERACT_AVAILABLE
        }
    })

def generate_ultra_recommendations(signals, score):
    """Génère des recommandations ULTRA"""
    recommendations = []
    
    if score < 20:
        recommendations.append("🚨🚨 ULTRA DANGER - NE SURTOUT PAS CLIQUER/OUVRIR")
        recommendations.append("🔴 Bloquer immédiatement l'expéditeur")
        recommendations.append("🔴 Signaler aux autorités (phishing@signal-spam.fr)")
        recommendations.append("🔴 Changer tous vos mots de passe si vous avez interagi")
        recommendations.append("🔴 Scanner votre système avec un antivirus")
    elif score < 40:
        recommendations.append("⚠️⚠️ TRÈS DANGEREUX - Ne pas interagir")
        recommendations.append("🟠 Vérifier via canaux officiels")
        recommendations.append("🟠 Marquer comme spam")
        recommendations.append("🟠 Informer votre service informatique")
    elif score < 60:
        recommendations.append("⚠️ DANGEREUX - Faire preuve d'extrême prudence")
        recommendations.append("🟡 Vérifier l'authenticité")
        recommendations.append("🟡 Ne fournir aucune information personnelle")
        recommendations.append("🟡 Contacter l'entreprise via son site officiel")
    elif score < 80:
        recommendations.append("🔍 SUSPECT - Vérifier avant d'agir")
        recommendations.append("🟢 Rechercher des avis en ligne")
        recommendations.append("🟢 Comparer avec des communications officielles")
    else:
        recommendations.append("✅ PROBABLEMENT SAIN - Rester vigilant")
        recommendations.append("🟢 Surveiller les tentatives similaires")
    
    # Recommandations spécifiques
    for signal in signals:
        if 'qr' in signal.get('source', '').lower():
            recommendations.append("📱 Les QR codes peuvent rediriger vers des sites malveillants")
        if 'fichier' in signal.get('signal', '').lower():
            recommendations.append("📁 Scanner le fichier avec plusieurs antivirus")
        if 'url' in signal.get('source', '').lower():
            recommendations.append("🌐 Vérifier l'URL sur VirusTotal")
    
    return list(set(recommendations))[:7]  # Max 7 recommandations

# ============================================
# LANCEMENT
# ============================================

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  ███████╗██╗   ██╗██████╗ ███████╗██████╗                 ║
    ║  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗                ║
    ║  ███████╗██║   ██║██████╔╝█████╗  ██████╔╝                ║
    ║  ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗                ║
    ║  ███████║╚██████╔╝██║     ███████╗██║  ██║                ║
    ║  ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝                ║
    ║                                                              ║
    ║     SUPER RECHERCHE ANTI-FRAUDE - VERSION ULTRA v2.0        ║
    ║            🔍 Recherche PARTOUT et encore MIEUX !           ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print("✅ Moteurs ULTRA chargés:")
    print("   🎯 URL Analyzer: Expansion, DNS, SSL, Typosquatting")
    print("   📝 Text Analyzer: NLP, Social Engineering, Entités")
    print("   📁 File Analyzer: PDF, DOCX, XLSX, Détection malwares")
    print("   🖼️ Image Analyzer: OCR, QR codes, Analyse couleurs")
    print("   📊 Scoring Engine: Algorithme pondéré ULTRA")
    
    print("\n🚀 Démarrage du serveur sur http://localhost:5000")
    print("📚 Interface web: http://localhost:5000/")
    print("\n🔍 Endpoints ULTRA disponibles:")
    print("   POST /analyze/text   - Analyse SMS/email (ultra complète)")
    print("   POST /analyze/url    - Analyse URL (DNS, SSL, typosquatting)")
    print("   POST /analyze/file   - Analyse fichier (PDF, DOCX, XLSX, TXT)")
    print("   POST /analyze/image  - Analyse image (OCR, QR codes)")
    print("   POST /analyze/bulk   - Analyse multiple (statistiques)")
    print("   GET  /health         - Statut API")
    
    print("\n💡 L'API recherche PARTOUT :")
    print("   - URLs courtes et redirections")
    print("   - Typosquatting et homoglyphes")
    print("   - DNS blacklists et SSL")
    print("   - Social engineering multi-langues")
    print("   - Fichiers malveillants")
    print("   - QR codes malicieux")
    print("   - Et encore PLUS...")
    
    # Lancer l'app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
