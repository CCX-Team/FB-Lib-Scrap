# Facebook Ads Library Scraper

Script Python pour récupérer et analyser les publicités de la bibliothèque publicitaire Facebook en JSON.

## Fonctionnalités

- **Scraping intelligent avec Playwright** : Scroll automatique avec détection de dates
- **Arrêt automatique** : S'arrête quand il détecte trop de pubs hors période
- **Extraction complète** : Titres, textes, images, vidéos, CTAs, liens, plateformes
- **Analyse des angles créatifs** : Identifie les différentes approches marketing testées
- **Export JSON** : Données structurées pour analyse ultérieure

## Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Installer les navigateurs Playwright
playwright install chromium
```

## Utilisation

### Méthode 1 : Avec URL complète (Recommandé)

```bash
python facebook_ads_scraper.py \
  --url "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=FR&q=l%27indispensable%20probiotiques&search_type=page&start_date[min]=2025-01-01&start_date[max]=2026-01-01&view_all_page_id=2179133842361365" \
  --output mes_pubs.json
```

### Méthode 2 : Avec paramètres séparés

```bash
python facebook_ads_scraper.py \
  --method scraper \
  --page-id 2179133842361365 \
  --search-term "l'indispensable probiotiques" \
  --start-date 2025-01-01 \
  --end-date 2026-01-01 \
  --country FR \
  --output mes_pubs.json
```

### Options supplémentaires

```bash
# Voir le navigateur pendant le scraping (mode debug)
python facebook_ads_scraper.py --url "..." --no-headless

# Utiliser l'API officielle (nécessite un token Facebook)
python facebook_ads_scraper.py \
  --method api \
  --page-id 2179133842361365 \
  --search-term "probiotiques" \
  --start-date 2025-01-01 \
  --end-date 2026-01-01 \
  --token "VOTRE_TOKEN_FACEBOOK" \
  --output mes_pubs.json
```

## Structure du JSON de sortie

```json
{
  "success": true,
  "total_ads": 15,
  "ads": [
    {
      "id": "abc123",
      "date_started": "January 15, 2025",
      "headlines": ["Probiotiques révolutionnaires"],
      "body_texts": ["Découvrez notre formule..."],
      "images": [
        {
          "src": "https://...",
          "width": 1080,
          "height": 1080
        }
      ],
      "videos": [],
      "call_to_actions": ["Acheter maintenant", "En savoir plus"],
      "external_links": ["https://example.com"],
      "platforms": ["Facebook", "Instagram"],
      "ad_library_url": "https://facebook.com/ads/library/...",
      "full_text": "..."
    }
  ],
  "creative_angles": {
    "total_unique_headlines": 10,
    "total_unique_body_texts": 12,
    "total_unique_ctas": 5,
    "unique_headlines": ["Headline 1", "Headline 2", ...],
    "unique_body_texts": ["Text 1", "Text 2", ...],
    "unique_ctas": ["Acheter", "Découvrir", ...],
    "formats": {
      "image_only": 3,
      "video_only": 2,
      "image_and_text": 8,
      "video_and_text": 2
    },
    "platforms": {
      "Facebook": 12,
      "Instagram": 10
    },
    "common_themes": [
      {"word": "santé", "count": 15},
      {"word": "naturel", "count": 12}
    ]
  },
  "stats": {
    "ads_in_range": 15,
    "ads_out_of_range": 3,
    "scrolls_performed": 8
  },
  "scraped_at": "2025-01-09T10:30:00"
}
```

## Analyse des angles créatifs

Le script identifie automatiquement :

1. **Headlines uniques** : Tous les titres différents testés
2. **Body texts** : Tous les textes de corps uniques
3. **CTAs** : Tous les appels à l'action ("Acheter", "En savoir plus", etc.)
4. **Formats** : Distribution image/vidéo/texte
5. **Plateformes** : Facebook, Instagram, Messenger, etc.
6. **Thèmes communs** : Mots-clés les plus fréquents

## Gestion intelligente du scroll

Le script s'arrête automatiquement dans ces cas :

- **Pubs hors période** : Si 5+ publicités consécutives sont avant la date de début
- **Pas de nouvelles pubs** : Si 3 scrolls consécutifs ne chargent rien de nouveau
- **Limite atteinte** : Après max_scroll scrolls (défaut: 50)

Cela évite de descendre trop loin et de récupérer des pubs de 2024 alors qu'on cherche 2025.

## Limitations

### Scraping avec Playwright
- Facebook peut détecter et bloquer le scraping intensif
- Nécessite un navigateur Chromium installé
- Plus lent que l'API officielle
- Structure HTML peut changer

### API officielle
- Nécessite un token d'accès Facebook
- Requiert une validation d'identité
- Fonctionne uniquement pour : pubs EU, Brésil, ou pubs politiques
- Limites de taux (rate limits)

## Troubleshooting

### Erreur "Playwright non installé"
```bash
pip install playwright
playwright install chromium
```

### Le script ne trouve aucune pub
- Vérifiez que le page_id est correct
- Vérifiez les dates (format YYYY-MM-DD)
- Essayez avec --no-headless pour voir ce qui se passe
- Augmentez le temps d'attente (scroll_pause)

### Facebook bloque le scraping
- Ajoutez des pauses plus longues entre les scrolls
- Utilisez --no-headless occasionnellement
- Considérez l'utilisation de l'API officielle

## Exemples d'analyse

Une fois les données récupérées, vous pouvez les analyser :

```python
import json

# Charger les données
with open('mes_pubs.json', 'r') as f:
    data = json.load(f)

# Analyser les angles
angles = data['creative_angles']

print(f"Total de publicités : {data['total_ads']}")
print(f"Headlines uniques testés : {angles['total_unique_headlines']}")
print(f"CTAs uniques : {angles['total_unique_ctas']}")
print(f"\nFormats les plus utilisés :")
for format_type, count in angles['formats'].items():
    print(f"  {format_type}: {count}")

print(f"\nThèmes principaux :")
for theme in angles['common_themes'][:5]:
    print(f"  {theme['word']}: {theme['count']} occurrences")
```

## Conformité

- Ce script utilise uniquement des données publiques de la bibliothèque Facebook Ads
- Respectez les conditions d'utilisation de Facebook
- N'utilisez pas ce script de manière abusive (rate limiting)
- Les données sont à usage d'analyse de marché et veille concurrentielle

## Support

Pour des questions ou problèmes :
- Vérifiez d'abord la section Troubleshooting
- Consultez la documentation de Playwright
- Testez d'abord avec --no-headless pour débugger
