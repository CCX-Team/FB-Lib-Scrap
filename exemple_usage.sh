#!/bin/bash

# Exemple d'utilisation pour l'indispensable probiotiques
# Page ID: 2179133842361365
# Période: 2025-01-01 à 2026-01-01

echo "🔍 Scraping des publicités Facebook Ads Library..."
echo ""

python facebook_ads_scraper.py \
  --url "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=FR&is_targeted_country=false&media_type=all&q=l%27indispensable%20probiotiques&search_type=page&start_date[min]=2025-01-01&start_date[max]=2026-01-01&view_all_page_id=2179133842361365" \
  --output indispensable_probiotiques_ads.json

echo ""
echo "✅ Scraping terminé !"
echo "📊 Résultats disponibles dans : indispensable_probiotiques_ads.json"
echo ""
echo "Pour analyser les résultats, lancez : python analyze_results.py"
