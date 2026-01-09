# FB Lib Scrap - Facebook Ads Library Scraper

Scraper Python pour récupérer et analyser les publicités de la bibliothèque publicitaire Facebook (Meta Ad Library).

## 🎯 Fonctionnalités

- ✅ Scraping automatique avec détection intelligente de dates
- ✅ Support API officielle Facebook ou scraping Playwright
- ✅ Extraction complète : textes, images, vidéos, CTAs, plateformes
- ✅ Analyse des angles créatifs automatique
- ✅ Export JSON structuré
- ✅ Arrêt automatique quand hors période
- ✅ Détection des thèmes et patterns

## 📦 Installation Rapide

```bash
# Cloner le repo
git clone https://github.com/VOTRE_USERNAME/FB-Lib-Scrap.git
cd FB-Lib-Scrap

# Installer les dépendances
pip install -r requirements.txt

# Installer le navigateur Playwright
playwright install chromium
```

## 🚀 Utilisation

### Scraping Simple

```bash
python facebook_ads_scraper_v2.py "VOTRE_URL_FACEBOOK_ADS_LIBRARY"
```

### Avec paramètres

```bash
python facebook_ads_scraper.py \
  --url "https://www.facebook.com/ads/library/..." \
  --output mes_pubs.json
```

### Analyser les résultats

```bash
# Analyse spécifique pour probiotiques/DIJO
python analyze_dijo_ads.py facebook_ads_v2.json

# Analyse générique
python analyze_results.py facebook_ads_v2.json
```

## 📚 Documentation

- **[Guide de démarrage rapide](QUICKSTART.md)** - Commencez en 2 minutes
- **[Documentation complète](README_facebook_ads.md)** - Toutes les options et troubleshooting

## 📊 Exemple de Résultats

Le scraper extrait pour chaque publicité :

```json
{
  "id": "123456789",
  "date_start": "15 jan 2025",
  "date_end": "20 jan 2025",
  "platforms": ["Facebook", "Instagram"],
  "text_preview": "Découvrez notre produit...",
  "text_lines": ["Headline", "Body text", "CTA"]
}
```

L'analyse identifie automatiquement :

- 🎯 Angles promotionnels (-30%, -50%, offres spéciales)
- 📦 Mix produits (produits mis en avant)
- 💊 Bénéfices santé / arguments de vente
- 📅 Chronologie et saisonnalité
- ✍️ Headlines et CTAs uniques testés

## 🎨 Cas d'Usage

1. **Veille concurrentielle** - Analyser les stratégies publicitaires de vos concurrents
2. **Recherche de produits** - Identifier les produits gagnants et leurs angles
3. **Analyse créative** - Comprendre quels messages sont testés
4. **Tendances marché** - Observer les patterns saisonniers

## 📁 Structure du Projet

```
FB-Lib-Scrap/
├── facebook_ads_scraper.py       # Scraper complet (API + Playwright)
├── facebook_ads_scraper_v2.py    # Version simplifiée et robuste
├── analyze_dijo_ads.py           # Analyseur spécifique probiotiques
├── analyze_results.py            # Analyseur générique
├── debug_facebook.py             # Outil de debug
├── requirements.txt              # Dépendances Python
├── README.md                     # Ce fichier
├── QUICKSTART.md                 # Guide rapide
├── README_facebook_ads.md        # Doc complète
└── examples/                     # Exemples de résultats
    ├── facebook_ads_v2.json      # 157 pubs DIJO
    └── dijo_angles_summary.json  # Analyse des angles
```

## ⚙️ Configuration

Copiez `config.example.json` et ajustez selon vos besoins :

```json
{
  "method": "scraper",
  "search_params": {
    "page_id": "VOTRE_PAGE_ID",
    "search_term": "votre recherche",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31"
  }
}
```

## 🛠️ Troubleshooting

### Aucune pub trouvée
- Vérifiez le `page_id` sur Facebook
- Vérifiez les dates (format YYYY-MM-DD)
- Essayez avec `--no-headless` pour voir le navigateur

### Facebook détecte le bot
- Ajoutez des pauses plus longues
- Utilisez l'API officielle (nécessite token)

### Playwright non installé
```bash
pip install playwright
playwright install chromium
```

## ⚖️ Légalité et Éthique

- ✅ Utilise uniquement des données publiques de la bibliothèque Meta Ad Library
- ✅ Respecte le Terms of Service de Meta
- ⚠️ N'abusez pas du scraping (rate limiting)
- ⚠️ À usage d'analyse de marché et veille concurrentielle uniquement

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Ouvrir une issue pour signaler un bug
- Proposer des améliorations
- Soumettre une pull request

## 📝 Licence

MIT License - Libre d'utilisation pour vos projets.

## 🙏 Crédits

Créé pour analyser les angles créatifs et stratégies publicitaires sur Facebook/Instagram.

---

⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !
