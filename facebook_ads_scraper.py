#!/usr/bin/env python3
"""
Script pour récupérer les données de la bibliothèque publicitaire Facebook en JSON.
Supporte deux méthodes : API officielle ou scraping avec Playwright.

Analyse les angles créatifs : textes, images, CTAs, formats publicitaires.
"""

import json
import urllib.parse
import re
from datetime import datetime
from dateutil import parser as date_parser
from typing import Dict, List, Optional
import argparse


class FacebookAdsLibraryAPI:
    """Utilise l'API officielle de Facebook Ads Library"""

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0/ads_archive"

    def search_ads(
        self,
        page_id: str,
        search_term: str,
        start_date: str,
        end_date: str,
        country: str = "FR",
        limit: int = 500
    ) -> Dict:
        """
        Recherche des publicités via l'API Facebook

        Args:
            page_id: ID de la page Facebook
            search_term: Terme de recherche
            start_date: Date de début (YYYY-MM-DD)
            end_date: Date de fin (YYYY-MM-DD)
            country: Code pays (FR par défaut)
            limit: Nombre max de résultats par page

        Returns:
            Dict contenant les données des publicités
        """
        import requests

        params = {
            "access_token": self.access_token,
            "search_page_ids": page_id,
            "search_terms": search_term,
            "ad_reached_countries": country,
            "ad_active_status": "ALL",
            "fields": ",".join([
                "id",
                "ad_creation_time",
                "ad_creative_bodies",
                "ad_creative_link_captions",
                "ad_creative_link_descriptions",
                "ad_creative_link_titles",
                "ad_delivery_start_time",
                "ad_delivery_stop_time",
                "ad_snapshot_url",
                "age_country_gender_reach_breakdown",
                "beneficiary_payers",
                "bylines",
                "currency",
                "delivery_by_region",
                "demographic_distribution",
                "estimated_audience_size",
                "eu_total_reach",
                "impressions",
                "languages",
                "page_id",
                "page_name",
                "publisher_platforms",
                "spend",
                "target_ages",
                "target_gender",
            ]),
            "limit": limit,
        }

        all_ads = []
        url = self.base_url

        try:
            while url:
                response = requests.get(url, params=params if url == self.base_url else None)
                response.raise_for_status()
                data = response.json()

                if "data" in data:
                    all_ads.extend(data["data"])
                    print(f"Récupéré {len(all_ads)} publicités...")

                # Pagination
                url = data.get("paging", {}).get("next")
                params = None  # Les paramètres sont dans l'URL next

            return {
                "success": True,
                "total_ads": len(all_ads),
                "ads": all_ads,
                "query": {
                    "page_id": page_id,
                    "search_term": search_term,
                    "start_date": start_date,
                    "end_date": end_date,
                    "country": country
                }
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erreur lors de la requête à l'API Facebook"
            }


class FacebookAdsLibraryScraper:
    """Scrape la bibliothèque publicitaire Facebook avec Playwright"""

    def __init__(self):
        try:
            from playwright.sync_api import sync_playwright
            self.playwright_available = True
        except ImportError:
            self.playwright_available = False

    def search_ads(
        self,
        page_id: str,
        search_term: str,
        start_date: str,
        end_date: str,
        country: str = "FR",
        headless: bool = True,
        max_scroll: int = 50,
        scroll_pause: float = 2.5
    ) -> Dict:
        """
        Scrape les publicités avec Playwright - avec détection intelligente de date

        Args:
            page_id: ID de la page Facebook
            search_term: Terme de recherche
            start_date: Date de début (YYYY-MM-DD)
            end_date: Date de fin (YYYY-MM-DD)
            country: Code pays
            headless: Mode sans interface graphique
            max_scroll: Nombre maximum de scrolls
            scroll_pause: Pause entre chaque scroll (secondes)

        Returns:
            Dict contenant les données des publicités avec angles créatifs
        """
        if not self.playwright_available:
            return {
                "success": False,
                "error": "Playwright non installé",
                "message": "Installez Playwright avec: pip install playwright && playwright install"
            }

        from playwright.sync_api import sync_playwright
        import time

        # Conversion des dates
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return {
                "success": False,
                "error": "Format de date invalide",
                "message": "Utilisez le format YYYY-MM-DD"
            }

        # Construction de l'URL
        url = self._build_url(page_id, search_term, start_date, end_date, country)

        all_ads = []
        previous_ad_count = 0
        consecutive_no_new_ads = 0
        out_of_range_count = 0

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                )
                page = context.new_page()

                print(f"Navigation vers: {url}")
                page.goto(url, wait_until="networkidle", timeout=60000)
                time.sleep(4)

                # Scroll intelligent avec vérification des dates
                for scroll_num in range(max_scroll):
                    print(f"\n[Scroll {scroll_num + 1}/{max_scroll}]")

                    # Extraction des publicités actuellement visibles
                    current_ads = self._extract_ads_from_page(page)

                    # Filtrage par date
                    ads_in_range = []
                    ads_out_of_range = 0

                    for ad in current_ads:
                        ad_date = self._parse_ad_date(ad.get("date_started", ""))
                        if ad_date:
                            if start_dt <= ad_date <= end_dt:
                                # Éviter les doublons
                                if not any(existing["id"] == ad["id"] for existing in all_ads):
                                    ads_in_range.append(ad)
                            elif ad_date < start_dt:
                                ads_out_of_range += 1

                    all_ads.extend(ads_in_range)
                    out_of_range_count += ads_out_of_range

                    print(f"  Nouvelles pubs dans période: {len(ads_in_range)}")
                    print(f"  Total récupéré: {len(all_ads)}")
                    print(f"  Pubs hors période: {ads_out_of_range}")

                    # Conditions d'arrêt
                    if len(current_ads) == previous_ad_count:
                        consecutive_no_new_ads += 1
                        if consecutive_no_new_ads >= 3:
                            print("\n⚠ Pas de nouvelles pubs après 3 scrolls - arrêt")
                            break
                    else:
                        consecutive_no_new_ads = 0

                    # Arrêter si on a beaucoup de pubs hors période
                    if ads_out_of_range >= 5:
                        print(f"\n⚠ Trop de pubs hors période ({ads_out_of_range}) - arrêt pour éviter de descendre trop loin")
                        break

                    previous_ad_count = len(current_ads)

                    # Scroll vers le bas
                    page.evaluate("window.scrollBy(0, window.innerHeight)")
                    time.sleep(scroll_pause)

                browser.close()

            # Analyse des angles créatifs
            creative_angles = self._analyze_creative_angles(all_ads)

            return {
                "success": True,
                "total_ads": len(all_ads),
                "ads": all_ads,
                "creative_angles": creative_angles,
                "query": {
                    "page_id": page_id,
                    "search_term": search_term,
                    "start_date": start_date,
                    "end_date": end_date,
                    "country": country,
                    "url": url
                },
                "stats": {
                    "ads_in_range": len(all_ads),
                    "ads_out_of_range": out_of_range_count,
                    "scrolls_performed": scroll_num + 1
                },
                "scraped_at": datetime.now().isoformat()
            }

        except Exception as e:
            import traceback
            return {
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "message": f"Erreur lors du scraping: {str(e)}"
            }

    def _extract_ads_from_page(self, page) -> List[Dict]:
        """Extrait toutes les publicités de la page actuelle"""
        return page.evaluate("""
            () => {
                const ads = [];
                const adCards = document.querySelectorAll('[data-testid="search_result_ad_card"], [role="article"]');

                adCards.forEach((card) => {
                    try {
                        // ID unique basé sur le contenu
                        const cardText = card.innerText.substring(0, 200);
                        const cardHash = btoa(cardText).substring(0, 20);

                        const ad = {
                            id: cardHash,
                            timestamp: Date.now(),
                        };

                        // Date de début (chercher "Started running on")
                        const dateMatch = card.innerText.match(/Started running on ([A-Za-z]+ \\d+, \\d{4})/i);
                        if (dateMatch) {
                            ad.date_started = dateMatch[1];
                        }

                        // Titre/Headline
                        const headlines = [];
                        card.querySelectorAll('[class*="headline"], h3, h4, strong').forEach(el => {
                            const text = el.innerText.trim();
                            if (text && text.length > 5 && !headlines.includes(text)) {
                                headlines.push(text);
                            }
                        });
                        ad.headlines = headlines;

                        // Corps de texte
                        const bodies = [];
                        card.querySelectorAll('[class*="body"], p, div[dir="auto"]').forEach(el => {
                            const text = el.innerText.trim();
                            if (text && text.length > 20 && !bodies.some(b => b.includes(text))) {
                                bodies.push(text);
                            }
                        });
                        ad.body_texts = bodies;

                        // Images
                        const images = [];
                        card.querySelectorAll('img').forEach(img => {
                            if (img.src && !img.src.includes('data:image') && img.width > 50) {
                                images.push({
                                    src: img.src,
                                    alt: img.alt || '',
                                    width: img.width,
                                    height: img.height
                                });
                            }
                        });
                        ad.images = images;

                        // Vidéos
                        const videos = [];
                        card.querySelectorAll('video').forEach(video => {
                            if (video.src) {
                                videos.push({
                                    src: video.src,
                                    poster: video.poster || ''
                                });
                            }
                        });
                        ad.videos = videos;

                        // Call to Action (boutons)
                        const ctas = [];
                        card.querySelectorAll('button, a[role="button"], [class*="cta"]').forEach(btn => {
                            const text = btn.innerText.trim();
                            if (text && text.length < 50) {
                                ctas.push(text);
                            }
                        });
                        ad.call_to_actions = ctas;

                        // Liens
                        const links = [];
                        card.querySelectorAll('a[href]').forEach(link => {
                            if (link.href && !link.href.includes('facebook.com/ads')) {
                                links.push(link.href);
                            }
                        });
                        ad.external_links = links;

                        // Plateformes (Facebook, Instagram, etc.)
                        const platformMatch = card.innerText.match(/(Facebook|Instagram|Messenger|Audience Network)/gi);
                        if (platformMatch) {
                            ad.platforms = [...new Set(platformMatch)];
                        }

                        // Texte complet pour analyse
                        ad.full_text = card.innerText;

                        // URL de la pub
                        const adLink = card.querySelector('a[href*="/ads/library"]');
                        if (adLink) {
                            ad.ad_library_url = adLink.href;
                        }

                        ads.push(ad);
                    } catch (e) {
                        console.error('Erreur extraction pub:', e);
                    }
                });

                return ads;
            }
        """)

    def _parse_ad_date(self, date_str: str) -> Optional[datetime]:
        """Parse la date d'une publicité"""
        if not date_str:
            return None

        try:
            # Format Facebook: "January 1, 2025"
            return datetime.strptime(date_str, "%B %d, %Y")
        except (ValueError, TypeError):
            try:
                # Autres formats possibles
                return date_parser.parse(date_str)
            except:
                return None

    def _analyze_creative_angles(self, ads: List[Dict]) -> Dict:
        """Analyse les différents angles créatifs utilisés"""
        angles = {
            "unique_headlines": [],
            "unique_body_texts": [],
            "unique_ctas": [],
            "formats": {
                "image_only": 0,
                "video_only": 0,
                "image_and_text": 0,
                "video_and_text": 0
            },
            "platforms": {},
            "common_themes": []
        }

        all_text = []

        for ad in ads:
            # Headlines uniques
            for headline in ad.get("headlines", []):
                if headline not in angles["unique_headlines"]:
                    angles["unique_headlines"].append(headline)

            # Body texts uniques
            for body in ad.get("body_texts", []):
                if body not in angles["unique_body_texts"]:
                    angles["unique_body_texts"].append(body)
                all_text.append(body.lower())

            # CTAs uniques
            for cta in ad.get("call_to_actions", []):
                if cta not in angles["unique_ctas"]:
                    angles["unique_ctas"].append(cta)

            # Formats
            has_image = len(ad.get("images", [])) > 0
            has_video = len(ad.get("videos", [])) > 0
            has_text = len(ad.get("body_texts", [])) > 0

            if has_image and not has_video and not has_text:
                angles["formats"]["image_only"] += 1
            elif has_video and not has_image:
                angles["formats"]["video_only"] += 1
            elif has_image and has_text:
                angles["formats"]["image_and_text"] += 1
            elif has_video and has_text:
                angles["formats"]["video_and_text"] += 1

            # Plateformes
            for platform in ad.get("platforms", []):
                angles["platforms"][platform] = angles["platforms"].get(platform, 0) + 1

        # Détection de thèmes communs (mots-clés fréquents)
        from collections import Counter
        words = []
        for text in all_text:
            words.extend(re.findall(r'\b\w{4,}\b', text))

        common_words = Counter(words).most_common(20)
        angles["common_themes"] = [
            {"word": word, "count": count}
            for word, count in common_words
        ]

        angles["total_unique_headlines"] = len(angles["unique_headlines"])
        angles["total_unique_body_texts"] = len(angles["unique_body_texts"])
        angles["total_unique_ctas"] = len(angles["unique_ctas"])

        return angles

    def _build_url(
        self,
        page_id: str,
        search_term: str,
        start_date: str,
        end_date: str,
        country: str
    ) -> str:
        """Construit l'URL de recherche Facebook Ads Library"""
        base_url = "https://www.facebook.com/ads/library/"

        params = {
            "active_status": "all",
            "ad_type": "all",
            "country": country,
            "is_targeted_country": "false",
            "media_type": "all",
            "q": search_term,
            "search_type": "page",
            "start_date[min]": start_date,
            "start_date[max]": end_date,
            "view_all_page_id": page_id
        }

        return base_url + "?" + urllib.parse.urlencode(params)


def parse_url(url: str) -> Dict[str, str]:
    """Parse une URL de Facebook Ads Library pour extraire les paramètres"""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)

    return {
        "page_id": params.get("view_all_page_id", [""])[0],
        "search_term": params.get("q", [""])[0],
        "start_date": params.get("start_date[min]", [""])[0],
        "end_date": params.get("start_date[max]", [""])[0],
        "country": params.get("country", ["FR"])[0]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Scraper pour Facebook Ads Library"
    )
    parser.add_argument(
        "--method",
        choices=["api", "scraper"],
        default="scraper",
        help="Méthode: 'api' (nécessite token) ou 'scraper' (Playwright)"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL complète de Facebook Ads Library"
    )
    parser.add_argument(
        "--page-id",
        type=str,
        help="ID de la page Facebook"
    )
    parser.add_argument(
        "--search-term",
        type=str,
        help="Terme de recherche"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        help="Date de début (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        help="Date de fin (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--country",
        type=str,
        default="FR",
        help="Code pays (défaut: FR)"
    )
    parser.add_argument(
        "--token",
        type=str,
        help="Token d'accès Facebook (pour méthode API)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="facebook_ads.json",
        help="Fichier de sortie JSON"
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Afficher le navigateur (scraper seulement)"
    )

    args = parser.parse_args()

    # Parse URL si fournie
    if args.url:
        params = parse_url(args.url)
        page_id = params["page_id"]
        search_term = params["search_term"]
        start_date = params["start_date"]
        end_date = params["end_date"]
        country = params["country"]
        print(f"Paramètres extraits de l'URL:")
        print(f"  Page ID: {page_id}")
        print(f"  Recherche: {search_term}")
        print(f"  Période: {start_date} à {end_date}")
        print(f"  Pays: {country}")
    else:
        page_id = args.page_id
        search_term = args.search_term
        start_date = args.start_date
        end_date = args.end_date
        country = args.country

    # Validation
    if not all([page_id, search_term, start_date, end_date]):
        parser.error("Fournissez soit --url, soit tous les paramètres (page-id, search-term, start-date, end-date)")

    # Exécution
    if args.method == "api":
        if not args.token:
            parser.error("La méthode API nécessite --token")

        print("Utilisation de l'API Facebook...")
        api = FacebookAdsLibraryAPI(args.token)
        result = api.search_ads(page_id, search_term, start_date, end_date, country)

    else:  # scraper
        print("Utilisation du scraper Playwright...")
        scraper = FacebookAdsLibraryScraper()
        result = scraper.search_ads(
            page_id, search_term, start_date, end_date, country,
            headless=not args.no_headless
        )

    # Sauvegarde
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    if result.get("success"):
        print(f"\n✓ Succès ! {result.get('total_ads', 0)} publicités récupérées")
        print(f"✓ Données sauvegardées dans: {args.output}")
    else:
        print(f"\n✗ Erreur: {result.get('message', 'Erreur inconnue')}")
        if "error" in result:
            print(f"  Détails: {result['error']}")


if __name__ == "__main__":
    main()
