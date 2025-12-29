#!/usr/bin/env python3
"""
nCore Torrent Downloader
Downloads torrents from ncore.pro based on selected category
"""

import requests
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

class NcoreDownloader:
    def __init__(self, config_file='ncore.cfg'):
        self.config_file = config_file
        self.site_url = 'https://ncore.pro'
        self.cookies_file = 'cookies.txt'
        self.state_file = 'download_state.json'
        self.history_file = 'download_history.json'
        self.session = requests.Session()
        
        # Available categories
        self.categories = {
            'Film SD/HU': 'xvid_hun',
            'Film SD/EN': 'xvid',
            'Film DVDR/HU': 'dvd_hun',
            'Film DVDR/EN': 'dvd',
            'Film DVD9/HU': 'dvd9_hun',
            'Film DVD9/EN': 'dvd9',
            'Film HD/HU': 'hd_hun',
            'Film HD/EN': 'hd',
            'Sorozat SD/HU': 'xvidser_hun',
            'Sorozat SD/EN': 'xvidser',
            'Sorozat DVDR/HU': 'dvdser_hun',
            'Sorozat DVDR/EN': 'dvdser',
            'Sorozat HD/HU': 'hdser_hun',
            'Sorozat HD/EN': 'hdser',
            'Játék PC/ISO': 'game_iso',
            'Játék PC/RIP': 'game_rip',
            'Játék Konzol': 'console',
            'Program PROG/ISO': 'iso',
            'Program PROG/RIP': 'misc',
            'Program PROG/Mobil': 'mobil',
            'Könyv eBook/HU': 'ebook_hun',
            'Könyv eBook/EN': 'ebook',
            'Zene MP3/HU': 'mp3_hun',
            'Zene MP3/EN': 'mp3',
            'Zene LOSSLESS/HU': 'lossless_hun',
            'Zene LOSSLESS/EN': 'lossless',
            'Zene Klip': 'clip',
            'XXX SD': 'xxx_xvid',
            'XXX DVDR': 'xxx_dvd',
            'XXX Imageset': 'xxx_imageset',
            'XXX HD': 'xxx_hd'
        }
        
        self.config = {}
        self.download_path = None
        
    def create_config_interactive(self):
        """Create config interactively by asking user"""
        print("\nConfig fájl nem található!")
        print("=" * 50)
        
        # Ask for username
        while True:
            username = input("Felhasználónév: ").strip()
            if username:
                break
            print("A felhasználónév nem lehet üres!")
        
        # Ask for password
        while True:
            password = input("Jelszó: ").strip()
            if password:
                break
            print("A jelszó nem lehet üres!")
        
        # Ask for download path (optional)
        print("\nLetöltési mappa (Enter = aktuális mappa):")
        download_path = input("Útvonal: ").strip()
        
        # Store in config
        self.config['username'] = username
        self.config['password'] = password
        if download_path:
            self.config['download_path'] = download_path
        
        # Ask if user wants to save
        print("\n" + "=" * 50)
        save_choice = input("El akarod menteni ezeket az adatokat a config fájlba? (i/n): ").strip().lower()
        
        if save_choice == 'i':
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    f.write(f"username={username}\n")
                    f.write(f"password={password}\n")
                    if download_path:
                        f.write(f"download_path={download_path}\n")
                print(f"✓ Config fájl elmentve: {self.config_file}")
            except Exception as e:
                print(f"FIGYELEM: Config fájl mentése sikertelen: {e}")
                print("A program az adatokat csak erre a futásra használja.")
        else:
            print("Config fájl nem lett elmentve. Az adatokat csak erre a futásra használjuk.")
    
    def load_config(self):
        """Load configuration from cfg file"""
        if not os.path.exists(self.config_file):
            self.create_config_interactive()
        else:
            # Load existing config
            with open(self.config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
            
            if 'username' not in self.config or 'password' not in self.config:
                print("ERROR: username és password kötelező a config fájlban!")
                sys.exit(1)
        
        # Set download path
        if 'download_path' in self.config and self.config['download_path']:
            self.download_path = Path(self.config['download_path'])
        else:
            # No download path in config, ask user
            print("\nLetöltési útvonal nincs megadva a config fájlban.")
            choice = input("Meg szeretnél adni egy letöltési útvonalat? (i/n): ").strip().lower()
            
            if choice == 'i':
                download_path = input("Letöltési útvonal: ").strip()
                if download_path:
                    self.download_path = Path(download_path)
                    
                    # Ask if user wants to save it to config
                    save_choice = input("El akarod menteni ezt az útvonalat a config fájlba? (i/n): ").strip().lower()
                    if save_choice == 'i':
                        try:
                            # Append to config file
                            with open(self.config_file, 'a', encoding='utf-8') as f:
                                f.write(f"\ndownload_path={download_path}\n")
                            self.config['download_path'] = download_path
                            print(f"✓ Letöltési útvonal elmentve a config fájlba.")
                        except Exception as e:
                            print(f"FIGYELEM: Config fájl frissítése sikertelen: {e}")
                else:
                    self.download_path = Path.cwd()
                    print(f"✓ Aktuális mappa használata: {self.download_path}")
            else:
                self.download_path = Path.cwd()
                print(f"✓ Aktuális mappa használata: {self.download_path}")
        
        # Create download directory if it doesn't exist
        self.download_path.mkdir(parents=True, exist_ok=True)
        
    def load_cookies(self):
        """Load cookies from file"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies_dict = json.load(f)
                    self.session.cookies.update(cookies_dict)
                return True
            except:
                return False
        return False
    
    def save_cookies(self):
        """Save cookies to file"""
        cookies_dict = dict(self.session.cookies)
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies_dict, f)
    
    def check_login(self):
        """Check if currently logged in"""
        try:
            response = self.session.get(self.site_url, timeout=10)
            return response.status_code == 200 and 'login.php' not in response.url
        except:
            return False
    
    def login(self):
        """Login to ncore"""
        print("Bejelentkezés...")
        
        # Try loading existing cookies
        if self.load_cookies():
            if self.check_login():
                print("Cookies OK, bejelentkezve.")
                return True
            else:
                print("Cookies érvénytelenek, újra bejelentkezés...")
        
        # Perform login
        login_url = urljoin(self.site_url, '/login.php')
        login_data = {
            'nev': self.config['username'],
            'pass': self.config['password'],
            'ne_leptessen_ki': '1'
        }
        
        try:
            response = self.session.post(login_url, data=login_data, timeout=10)
            
            if self.check_login():
                print("Sikeres bejelentkezés!")
                self.save_cookies()
                return True
            else:
                print("ERROR: Bejelentkezés sikertelen!")
                if os.path.exists(self.cookies_file):
                    os.remove(self.cookies_file)
                return False
        except Exception as e:
            print(f"ERROR: Bejelentkezési hiba: {e}")
            return False
    
    def select_category(self):
        """Display categories and let user select one"""
        print("\nElérhető kategóriák:")
        print("-" * 50)
        
        category_list = list(self.categories.items())
        for idx, (name, code) in enumerate(category_list, 1):
            print(f"{idx:2}. {name}")
        
        print("-" * 50)
        
        while True:
            try:
                choice = input("\nVálassz egy kategóriát (szám): ").strip()
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(category_list):
                    selected_name, selected_code = category_list[choice_idx]
                    print(f"Kiválasztva: {selected_name} ({selected_code})")
                    return selected_code
                else:
                    print("Érvénytelen választás!")
            except ValueError:
                print("Kérlek számot adj meg!")
            except KeyboardInterrupt:
                print("\nMegszakítva.")
                sys.exit(0)
    
    def fetch_torrents(self, category, page=1):
        """Fetch torrents from a specific category and page"""
        # Sort by creation time ascending (oldest first) for consistent ordering
        url = f"{self.site_url}/torrents.php?miszerint=ctime&hogyan=ASC&tipus={category}&oldal={page}&jsons=true"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"ERROR: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    def get_unique_filename(self, base_path, filename):
        """Get unique filename by adding number if file exists"""
        file_path = base_path / filename
        
        if not file_path.exists():
            return file_path
        
        # File exists, add number
        name_parts = filename.rsplit('.', 1)
        if len(name_parts) == 2:
            name, ext = name_parts
        else:
            name = filename
            ext = ''
        
        counter = 2
        while True:
            if ext:
                new_filename = f"{name}_{counter}.{ext}"
            else:
                new_filename = f"{name}_{counter}"
            
            file_path = base_path / new_filename
            if not file_path.exists():
                return file_path
            counter += 1
    
    def download_torrent(self, torrent_data):
        """Download a single torrent file"""
        download_url = torrent_data['download_url']
        release_name = self.sanitize_filename(torrent_data['release_name'])
        
        # Ensure .torrent extension
        if not release_name.endswith('.torrent'):
            release_name += '.torrent'
        
        # Get unique filename
        file_path = self.get_unique_filename(self.download_path, release_name)
        
        try:
            response = self.session.get(download_url, timeout=30)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                return True, file_path.name
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def load_state(self):
        """Load download state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def save_state(self, state):
        """Save download state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def clear_state(self):
        """Clear download state file"""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
    
    def load_history(self):
        """Load download history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_history(self, category, last_torrent_id):
        """Save download history to file"""
        history = self.load_history()
        
        from datetime import datetime
        history[category] = {
            'last_torrent_id': last_torrent_id,
            'last_download': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def get_category_history(self, category):
        """Get last downloaded torrent ID for a category"""
        history = self.load_history()
        if category in history:
            return history[category].get('last_torrent_id')
        return None
    
    def download_all(self, category):
        """Download all torrents from selected category"""
        # Check for existing state
        state = self.load_state()
        start_page = 1
        downloaded_count = 0
        max_downloads = None
        last_torrent_id = None
        
        # Check history for this category
        history_last_id = self.get_category_history(category)
        if history_last_id:
            print(f"\nTalálható korábbi letöltés ebben a kategóriában: {category}")
            print(f"Utolsó letöltött torrent ID: {history_last_id}")
            choice = input("Csak az új torrenteket töltöd le (utolsó ID után)? (i/n): ").strip().lower()
            
            if choice == 'i':
                last_torrent_id = history_last_id
                print(f"✓ Folytatás az ID {history_last_id} után...")
            else:
                print("✓ Minden torrent letöltése (újrakezdés)...")
        
        if state and state.get('category') == category:
            print(f"\nTalálható félbehagyott letöltés: {state['category']}")
            print(f"Oldal: {state['current_page']}, Letöltve: {state['downloaded_count']}")
            if 'max_downloads' in state:
                print(f"Maximum letöltések: {state['max_downloads']}")
            if 'last_torrent_id' in state:
                print(f"Utolsó letöltött torrent ID: {state['last_torrent_id']}")
            print("\nFIGYELEM: A letöltés a legrégebbi torrentektől folytatódik!")
            print("(A torrentek feltöltési idő szerint növekvő sorrendben vannak)")
            choice = input("\nFolytatod a félbehagyott letöltést? (i/n): ").strip().lower()
            
            if choice == 'i':
                downloaded_count = state['downloaded_count']
                max_downloads = state.get('max_downloads')
                last_torrent_id = state.get('last_torrent_id')
                
                # Safety: go back 5 pages from saved position
                saved_page = state['current_page']
                start_page = max(1, saved_page - 5)
                
                if start_page < saved_page:
                    print(f"Biztonsági okokból az oldal {saved_page} helyett {start_page}-tól indul.")
                    print(f"(A már letöltött torrenteket ID alapján kihagyja)")
                
                print("Folytatás...")
            else:
                print("Új letöltés indul...")
                self.clear_state()
                # Keep history-based last_torrent_id if it was set
        
        # Fetch first page to get total count
        print(f"\nKategória lekérdezése: {category}")
        data = self.fetch_torrents(category, start_page)
        
        if not data or 'results' not in data:
            print("ERROR: Nem sikerült lekérdezni a torrenteket!")
            return
        
        total_results = int(data['total_results'])
        per_page = int(data['perpage'])
        total_pages = (total_results + per_page - 1) // per_page
        
        print(f"\nÖsszesen {total_results} torrent található.")
        print(f"Oldalak: {total_pages}")
        print("\nINFO: A torrentek a legrégebbiek felől haladnak az újabbak felé.")
        print("(Rendezés: feltöltési idő szerint növekvő sorrend)")
        
        # Ask how many torrents to download (only for new downloads)
        if max_downloads is None:
            if last_torrent_id is not None:
                print("\nHány ÚJ torrentet szeretnél letölteni (az utolsó ID után)?")
            else:
                print("\nHány torrentet szeretnél letölteni?")
            
            print("  - Írd be a számot (pl: 50)")
            print("  - vagy írd: 'összes' az összes letöltéséhez")
            
            while True:
                choice = input("\nMennyiség: ").strip().lower()
                
                if choice in ['összes', 'osszes', 'all', 'mind']:
                    max_downloads = total_results
                    if last_torrent_id is not None:
                        print(f"✓ Az összes új torrent letöltése.")
                    else:
                        print(f"✓ Mind a {total_results} torrent letöltésre kerül.")
                    break
                else:
                    try:
                        max_downloads = int(choice)
                        if max_downloads <= 0:
                            print("Kérlek pozitív számot adj meg!")
                            continue
                        if max_downloads > total_results:
                            print(f"Figyelem: Maximum {total_results} torrent érhető el.")
                            max_downloads = total_results
                        if last_torrent_id is not None:
                            print(f"✓ {max_downloads} új torrent letöltése (ID > {last_torrent_id}).")
                        else:
                            print(f"✓ {max_downloads} torrent letöltése.")
                        break
                    except ValueError:
                        print("Érvénytelen bemenet! Adj meg egy számot vagy az 'összes' szót.")
                        continue
        
        # Calculate estimated time
        if max_downloads:
            # Calculate how many torrents still need to be downloaded
            if state and downloaded_count > 0:
                # Continuing from a paused download
                downloads_to_do = max_downloads - downloaded_count
            else:
                # New download (might skip some if history-based)
                downloads_to_do = max_downloads
            
            # Ensure positive value
            if downloads_to_do <= 0:
                downloads_to_do = max_downloads
            
            # Estimate: ~8 seconds per 25 torrents (includes download + 2 sec pause)
            estimated_seconds = int((downloads_to_do / 25.0) * 8)
            
            hours = estimated_seconds // 3600
            minutes = (estimated_seconds % 3600) // 60
            seconds = estimated_seconds % 60
            
            time_parts = []
            if hours > 0:
                time_parts.append(f"{hours} óra")
            if minutes > 0:
                time_parts.append(f"{minutes} perc")
            if seconds > 0 or not time_parts:
                time_parts.append(f"{seconds} másodperc")
            
            time_str = ", ".join(time_parts)
            
            print(f"\n{'='*50}")
            print(f"Becsült letöltési idő: ~{time_str}")
            print(f"  • {downloads_to_do} torrent letöltése")
            print(f"  • ~{downloads_to_do // 25} x 2 mp várakozás (25 torrentenként)")
            print(f"  • Számítás: ~8 mp / 25 torrent")
            print(f"{'='*50}")
            
            confirm = input("\nIndítod a letöltést? (i/n): ").strip().lower()
            if confirm != 'i':
                print("Letöltés megszakítva.")
                return
        
        print(f"\nLetöltés indítása... (Mentés helye: {self.download_path})")
        if max_downloads:
            print(f"Letöltendő: max {max_downloads} torrent")
        if last_torrent_id:
            print(f"Kihagyva: ID <= {last_torrent_id}")
        print("(Ctrl+C a megszakításhoz)")
        
        torrents_since_wait = 0
        current_page = start_page
        actual_downloads = 0  # Track actual new downloads
        skipped_count = 0  # Track skipped torrents
        
        try:
            for page in range(start_page, total_pages + 1):
                # Check if we've reached the download limit
                if actual_downloads >= (max_downloads - (downloaded_count if state else 0)):
                    print(f"\n✓ Elérte a megadott limitet: {max_downloads} torrent letöltve összesen.")
                    break
                
                current_page = page
                print(f"\n--- Oldal {page}/{total_pages} ---")
                
                # Fetch page if not the first one (already fetched)
                if page != start_page:
                    data = self.fetch_torrents(category, page)
                    if not data or 'results' not in data:
                        print(f"ERROR: Oldal {page} lekérdezése sikertelen!")
                        continue
                
                # Download torrents from this page
                for torrent in data['results']:
                    torrent_id = int(torrent['torrent_id'])
                    
                    # Skip if already downloaded (ID is less than or equal to last downloaded ID)
                    if last_torrent_id is not None and torrent_id <= last_torrent_id:
                        skipped_count += 1
                        print(f"  ↷ Kihagyva (már letöltve): {torrent['release_name']} (ID: {torrent_id})")
                        continue
                    
                    # Check if we've reached the download limit
                    if actual_downloads >= (max_downloads - (downloaded_count if state else 0)):
                        print(f"\n✓ Elérte a megadott limitet.")
                        break
                    
                    success, result = self.download_torrent(torrent)
                    
                    if success:
                        downloaded_count += 1
                        actual_downloads += 1
                        torrents_since_wait += 1
                        last_torrent_id = torrent_id
                        
                        print(f"[{actual_downloads}/{max_downloads - (downloaded_count - actual_downloads if state else 0)}] ✓ {result} (ID: {torrent_id})")
                        
                        # Wait after every 25 downloads, but only if we haven't reached the limit
                        if torrents_since_wait >= 25 and actual_downloads < (max_downloads - (downloaded_count - actual_downloads if state else 0)):
                            print("  → 25 letöltés megtörtént, várakozás 2 másodperc...")
                            time.sleep(2)
                            torrents_since_wait = 0
                    else:
                        print(f"✗ Hiba: {result} (ID: {torrent_id})")
                    
                    # Save state after each download or skip
                    self.save_state({
                        'category': category,
                        'current_page': current_page,
                        'downloaded_count': downloaded_count,
                        'max_downloads': max_downloads,
                        'last_torrent_id': last_torrent_id
                    })
        
        except KeyboardInterrupt:
            print("\n\nLetöltés megszakítva!")
            print(f"Eddig letöltve: {actual_downloads} új torrent")
            if last_torrent_id:
                print(f"Utolsó letöltött torrent ID: {last_torrent_id}")
            print(f"Állomány mentve: {self.state_file}")
            print("A letöltést később folytathatod.")
            sys.exit(0)
        
        print(f"\n✓ Kész! Összesen {actual_downloads} új torrent letöltve.")
        
        # Save to history
        if last_torrent_id:
            self.save_history(category, last_torrent_id)
            print(f"✓ Előzmények mentve: {self.history_file}")
        
        # Clear state after successful completion
        self.clear_state()
    
    def run(self):
        """Main execution flow"""
        print("=" * 50)
        print("nCore Torrent Downloader")
        print("=" * 50)
        
        # Load configuration
        self.load_config()
        
        # Login
        if not self.login():
            sys.exit(1)
        
        # Select category
        category = self.select_category()
        
        # Download all torrents
        self.download_all(category)


if __name__ == '__main__':
    downloader = NcoreDownloader()
    downloader.run()
