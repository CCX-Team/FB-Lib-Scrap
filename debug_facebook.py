#!/usr/bin/env python3
"""Script de debug pour voir la structure de la page Facebook Ads Library"""

from playwright.sync_api import sync_playwright
import time

url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=FR&is_targeted_country=false&media_type=all&q=l%27indispensable%20probiotiques&search_type=page&start_date[min]=2025-01-01&start_date[max]=2026-01-01&view_all_page_id=2179133842361365"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    )
    page = context.new_page()

    print("Navigation vers la page...")
    page.goto(url, wait_until="networkidle", timeout=60000)
    print("Page chargée, attente de 10 secondes...")
    time.sleep(10)

    # Screenshot
    page.screenshot(path="facebook_page_debug.png", full_page=True)
    print("Screenshot sauvegardée: facebook_page_debug.png")

    # Chercher différents sélecteurs possibles
    selectors_to_try = [
        '[data-testid="search_result_ad_card"]',
        '[role="article"]',
        '[data-pagelet]',
        'div[class*="ad"]',
        'div[class*="card"]',
        'div[class*="result"]'
    ]

    print("\nTest des sélecteurs:")
    for selector in selectors_to_try:
        count = page.locator(selector).count()
        print(f"  {selector}: {count} éléments trouvés")

    # Extraire le HTML de la page
    html_content = page.content()
    with open("facebook_page_debug.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("\nHTML sauvegardé: facebook_page_debug.html")

    # Vérifier s'il y a des messages d'erreur
    page_text = page.locator('body').inner_text()

    if "no results" in page_text.lower() or "aucun résultat" in page_text.lower():
        print("\n⚠️  La page indique qu'il n'y a aucun résultat")

    if "login" in page_text.lower() or "connexion" in page_text.lower():
        print("\n⚠️  La page demande peut-être une connexion")

    # Extraire un extrait du texte de la page
    print(f"\nPremiers 1000 caractères du texte de la page:")
    print(page_text[:1000])

    print("\n\nAttente de 5 secondes avant de fermer...")
    time.sleep(5)

    browser.close()

    print("\n✓ Debug terminé. Vérifiez:")
    print("  - facebook_page_debug.png (screenshot)")
    print("  - facebook_page_debug.html (code source)")
