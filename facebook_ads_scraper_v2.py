#!/usr/bin/env python3
"""
Version simplifiée et améliorée du scraper Facebook Ads
Se concentre sur l'extraction du texte brut et l'analyse
"""

import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

def scrape_facebook_ads(url, output_file="facebook_ads.json"):
    """Scrape Facebook Ads Library avec une approche robuste"""

    with sync_playwright() as p:
        print("Lancement du navigateur...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        print(f"Navigation vers: {url}")
        page.goto(url, timeout=60000)

        # Attendre que la page soit chargée
        print("Attente du chargement de la page...")
        time.sleep(8)

        # Vérifier combien de résultats sont disponibles
        page_text = page.locator('body').inner_text()

        results_match = re.search(r'(\d+)\s+résultats?', page_text)
        total_expected = int(results_match.group(1)) if results_match else 0
        print(f"Total de résultats annoncés : {total_expected}")

        all_ads = []
        ads_seen = set()
        no_new_ads_count = 0
        max_scrolls = 100

        for scroll_num in range(max_scrolls):
            print(f"\n[Scroll {scroll_num + 1}/{max_scrolls}]")

            # Extraire le texte complet de la page
            current_text = page.inner_text('body')

            # Diviser en sections de publicités basées sur des patterns
            ad_sections = re.split(r'(?=Inactive\s+ID dans la bibliothèque)', current_text)

            new_ads_this_scroll = 0

            for section in ad_sections:
                if 'ID dans la bibliothèque' not in section:
                    continue

                # Extraire l'ID de la pub
                id_match = re.search(r'ID dans la bibliothèque\s*:\s*(\d+)', section)
                if not id_match:
                    continue

                ad_id = id_match.group(1)

                # Éviter les doublons
                if ad_id in ads_seen:
                    continue

                ads_seen.add(ad_id)
                new_ads_this_scroll += 1

                # Extraire la date
                date_match = re.search(r'(\d+\s+\w+\s+\d{4})\s*-\s*(\d+\s+\w+\s+\d{4})', section)
                date_start = date_match.group(1) if date_match else None
                date_end = date_match.group(2) if date_match else None

                # Extraire les plateformes
                platforms = []
                if 'Facebook' in section:
                    platforms.append('Facebook')
                if 'Instagram' in section:
                    platforms.append('Instagram')
                if 'Messenger' in section:
                    platforms.append('Messenger')

                # Extraire le texte de la pub (après "Sponsorisé")
                text_after_sponsored = section.split('Sponsorisé', 1)
                ad_text = text_after_sponsored[1][:500].strip() if len(text_after_sponsored) > 1 else ""

                # Lignes du texte
                lines = [line.strip() for line in ad_text.split('\n') if line.strip()]

                ad_data = {
                    "id": ad_id,
                    "date_start": date_start,
                    "date_end": date_end,
                    "platforms": platforms,
                    "text_preview": ad_text[:200],
                    "text_lines": lines[:10],  # Premières lignes
                    "full_section": section[:1000]  # Échantillon pour debug
                }

                all_ads.append(ad_data)

            print(f"  Nouvelles pubs trouvées: {new_ads_this_scroll}")
            print(f"  Total accumulé: {len(all_ads)}")

            # Conditions d'arrêt
            if new_ads_this_scroll == 0:
                no_new_ads_count += 1
                if no_new_ads_count >= 3:
                    print("\n⚠ Pas de nouvelles pubs après 3 scrolls - arrêt")
                    break
            else:
                no_new_ads_count = 0

            # Arrêter si on a tout récupéré
            if total_expected > 0 and len(all_ads) >= total_expected * 0.9:
                print(f"\n✓ Récupéré ~90% des pubs attendues ({len(all_ads)}/{total_expected})")
                break

            # Scroll
            page.evaluate("window.scrollBy(0, window.innerHeight * 2)")
            time.sleep(3)

        browser.close()

        # Analyse simple des angles
        headlines = []
        all_text_lines = []

        for ad in all_ads:
            for line in ad.get('text_lines', []):
                if 5 < len(line) < 100:
                    if line not in headlines:
                        headlines.append(line)
                    all_text_lines.append(line)

        result = {
            "success": True,
            "total_ads": len(all_ads),
            "expected_total": total_expected,
            "ads": all_ads,
            "analysis": {
                "unique_text_lines": len(headlines),
                "sample_headlines": headlines[:20]
            },
            "scraped_at": datetime.now().isoformat(),
            "url": url
        }

        # Sauvegarder
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n✓ {len(all_ads)} publicités récupérées")
        print(f"✓ Sauvegardé dans: {output_file}")

        return result


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=FR&is_targeted_country=false&media_type=all&q=l%27indispensable%20probiotiques&search_type=page&start_date[min]=2025-01-01&start_date[max]=2026-01-01&view_all_page_id=2179133842361365"

    output = sys.argv[2] if len(sys.argv) > 2 else "facebook_ads_v2.json"

    scrape_facebook_ads(url, output)
