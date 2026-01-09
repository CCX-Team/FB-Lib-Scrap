# 🚀 Démarrage Rapide

## Installation en 2 minutes

```bash
# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Installer le navigateur Chromium pour Playwright
playwright install chromium
```

## Utilisation Simple

### Option 1 : Script automatique (Recommandé)

```bash
# Utiliser le script d'exemple pré-configuré
bash exemple_usage.sh
```

### Option 2 : Commande directe avec votre URL

```bash
python facebook_ads_scraper.py \
  --url "VOTRE_URL_FACEBOOK_ADS_LIBRARY" \
  --output mes_resultats.json
```

### Option 3 : Paramètres manuels

```bash
python facebook_ads_scraper.py \
  --page-id 2179133842361365 \
  --search-term "votre produit" \
  --start-date 2025-01-01 \
  --end-date 2026-01-01 \
  --country FR \
  --output mes_resultats.json
```

## Analyser les Résultats

```bash
# Afficher un rapport détaillé
python analyze_results.py mes_resultats.json

# Exporter un résumé
python analyze_results.py mes_resultats.json --export summary.json
```

## Mode Debug

Si ça ne marche pas, utilisez le mode avec interface graphique :

```bash
python facebook_ads_scraper.py --url "..." --no-headless
```

Vous verrez le navigateur en action et pourrez identifier le problème.

## Exemple Complet

```bash
# 1. Scraper les pubs
python facebook_ads_scraper.py \
  --url "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=FR&q=probiotiques&search_type=page&start_date[min]=2025-01-01&start_date[max]=2026-01-01&view_all_page_id=2179133842361365" \
  --output probiotiques_2025.json

# 2. Analyser les résultats
python analyze_results.py probiotiques_2025.json

# 3. Exploiter les données en Python
python
>>> import json
>>> with open('probiotiques_2025.json', 'r') as f:
...     data = json.load(f)
>>>
>>> # Voir tous les headlines testés
>>> for headline in data['creative_angles']['unique_headlines']:
...     print(headline)
>>>
>>> # Voir les CTAs
>>> print(data['creative_angles']['unique_ctas'])
```

## Ce que vous obtenez

Le JSON contient :

- ✅ **Toutes les publicités** avec dates, textes, images, vidéos
- ✅ **Tous les headlines uniques** testés
- ✅ **Tous les body texts** différents
- ✅ **Tous les CTAs** (boutons)
- ✅ **Formats utilisés** (image/vidéo/carrousel)
- ✅ **Plateformes** (Facebook/Instagram/Messenger)
- ✅ **Thèmes récurrents** (mots-clés les plus fréquents)
- ✅ **Timeline** (quand les pubs ont été lancées)

## Problèmes Courants

### "Playwright non installé"
```bash
pip install playwright
playwright install chromium
```

### "Aucune pub trouvée"
- Vérifiez que le `page_id` est correct
- Vérifiez les dates (format YYYY-MM-DD)
- Essayez avec `--no-headless` pour voir ce qui se passe

### Script trop lent
- Réduisez `--max-scroll` (défaut: 50)
- Le script s'arrête automatiquement quand il trouve des pubs hors période

### Facebook détecte le bot
- Ajoutez des pauses : modifiez `scroll_pause` dans le code
- Utilisez `--no-headless` de temps en temps
- Considérez l'API officielle (nécessite token Facebook)

## Prochaines Étapes

1. **Lancer votre premier scraping** : `bash exemple_usage.sh`
2. **Analyser les résultats** : `python analyze_results.py indispensable_probiotiques_ads.json`
3. **Explorer le JSON** : Ouvrir le fichier dans un éditeur ou avec `jq`
4. **Identifier les patterns** : Quels angles créatifs reviennent le plus ?
5. **Optimiser votre stratégie** : S'inspirer des approches qui durent

## Support

- Lisez le README complet : `README_facebook_ads.md`
- Testez en mode debug : `--no-headless`
- Vérifiez la structure HTML de Facebook (peut changer)
