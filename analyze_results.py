#!/usr/bin/env python3
"""
Script d'analyse des résultats du scraping Facebook Ads.
Affiche un résumé des angles créatifs testés.
"""

import json
import sys
from typing import Dict, List
from collections import Counter


def load_results(filename: str) -> Dict:
    """Charge le fichier JSON de résultats"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {filename}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Erreur de parsing JSON : {filename}")
        sys.exit(1)


def print_header(title: str):
    """Affiche un header stylisé"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def analyze_ads(data: Dict):
    """Analyse complète des publicités"""

    if not data.get('success'):
        print(f"❌ Erreur dans les données : {data.get('message', 'Inconnu')}")
        return

    total_ads = data.get('total_ads', 0)
    ads = data.get('ads', [])
    angles = data.get('creative_angles', {})
    stats = data.get('stats', {})

    # Vue d'ensemble
    print_header("📊 VUE D'ENSEMBLE")
    print(f"Total de publicités récupérées : {total_ads}")
    print(f"Publicités dans la période     : {stats.get('ads_in_range', 0)}")
    print(f"Publicités hors période        : {stats.get('ads_out_of_range', 0)}")
    print(f"Nombre de scrolls effectués    : {stats.get('scrolls_performed', 0)}")

    query = data.get('query', {})
    print(f"\n🔍 Recherche")
    print(f"  Terme : {query.get('search_term', 'N/A')}")
    print(f"  Période : {query.get('start_date', 'N/A')} → {query.get('end_date', 'N/A')}")
    print(f"  Pays : {query.get('country', 'N/A')}")

    # Angles créatifs
    print_header("🎨 ANGLES CRÉATIFS TESTÉS")

    print(f"📝 Headlines uniques : {angles.get('total_unique_headlines', 0)}")
    headlines = angles.get('unique_headlines', [])
    for i, headline in enumerate(headlines[:10], 1):
        print(f"  {i}. {headline[:80]}{'...' if len(headline) > 80 else ''}")
    if len(headlines) > 10:
        print(f"  ... et {len(headlines) - 10} autres")

    print(f"\n💬 Textes uniques : {angles.get('total_unique_body_texts', 0)}")
    body_texts = angles.get('unique_body_texts', [])
    for i, text in enumerate(body_texts[:5], 1):
        preview = text[:100].replace('\n', ' ')
        print(f"  {i}. {preview}{'...' if len(text) > 100 else ''}")
    if len(body_texts) > 5:
        print(f"  ... et {len(body_texts) - 5} autres")

    print(f"\n🎯 Call-to-Actions uniques : {angles.get('total_unique_ctas', 0)}")
    ctas = angles.get('unique_ctas', [])
    for i, cta in enumerate(ctas, 1):
        print(f"  {i}. {cta}")

    # Formats
    print_header("📹 FORMATS PUBLICITAIRES")
    formats = angles.get('formats', {})
    total_formats = sum(formats.values())

    for format_type, count in sorted(formats.items(), key=lambda x: x[1], reverse=True):
        if total_formats > 0:
            percentage = (count / total_formats) * 100
            bar = '█' * int(percentage / 5)
            print(f"  {format_type:20s} : {count:3d} ({percentage:5.1f}%) {bar}")

    # Plateformes
    print_header("📱 PLATEFORMES")
    platforms = angles.get('platforms', {})
    for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
        bar = '█' * (count // 2)
        print(f"  {platform:20s} : {count:3d} {bar}")

    # Thèmes communs
    print_header("🔤 THÈMES ET MOTS-CLÉS PRINCIPAUX")
    themes = angles.get('common_themes', [])
    print("Mots les plus fréquents dans les publicités :\n")
    for i, theme in enumerate(themes[:15], 1):
        word = theme['word']
        count = theme['count']
        bar = '█' * min(count, 30)
        print(f"  {i:2d}. {word:20s} : {count:3d} {bar}")

    # Timeline
    print_header("📅 CHRONOLOGIE")
    ads_with_dates = [ad for ad in ads if ad.get('date_started')]

    if ads_with_dates:
        from datetime import datetime

        date_counts = Counter()
        for ad in ads_with_dates:
            try:
                date_str = ad['date_started']
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
                month_key = date_obj.strftime("%Y-%m")
                date_counts[month_key] += 1
            except:
                pass

        print("Publicités lancées par mois :\n")
        for month, count in sorted(date_counts.items()):
            bar = '█' * count
            print(f"  {month} : {count:3d} {bar}")
    else:
        print("Aucune information de date disponible")

    # Insights
    print_header("💡 INSIGHTS")

    # Format le plus utilisé
    if formats:
        most_used_format = max(formats.items(), key=lambda x: x[1])
        print(f"✓ Format le plus utilisé : {most_used_format[0]} ({most_used_format[1]} pubs)")

    # CTA le plus fréquent
    if ctas:
        print(f"✓ Nombre de CTAs différents testés : {len(ctas)}")
        if len(ctas) > 5:
            print("  → Grande variété d'approches testées")
        elif len(ctas) <= 2:
            print("  → Approche CTA très ciblée")

    # Diversité des headlines
    if headlines and total_ads > 0:
        headline_ratio = len(headlines) / total_ads
        if headline_ratio > 0.8:
            print(f"✓ Forte diversité des headlines : {len(headlines)} headlines pour {total_ads} pubs")
            print("  → Tests A/B intensifs sur les accroches")
        elif headline_ratio < 0.3:
            print(f"✓ Headlines réutilisés : {len(headlines)} headlines pour {total_ads} pubs")
            print("  → Approche plus conservative, messages éprouvés")

    # Présence multi-plateforme
    if platforms:
        if len(platforms) > 1:
            print(f"✓ Stratégie multi-plateformes : {len(platforms)} plateformes")
            print(f"  → {', '.join(platforms.keys())}")

    print("\n" + "="*70 + "\n")


def export_summary(data: Dict, output_file: str):
    """Exporte un résumé structuré"""
    summary = {
        "total_ads": data.get('total_ads', 0),
        "period": {
            "start": data.get('query', {}).get('start_date'),
            "end": data.get('query', {}).get('end_date')
        },
        "creative_angles": {
            "headlines_count": data.get('creative_angles', {}).get('total_unique_headlines', 0),
            "body_texts_count": data.get('creative_angles', {}).get('total_unique_body_texts', 0),
            "ctas_count": data.get('creative_angles', {}).get('total_unique_ctas', 0),
        },
        "formats": data.get('creative_angles', {}).get('formats', {}),
        "platforms": data.get('creative_angles', {}).get('platforms', {}),
        "top_themes": data.get('creative_angles', {}).get('common_themes', [])[:10]
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"📄 Résumé exporté vers : {output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Analyse des résultats Facebook Ads")
    parser.add_argument(
        'input',
        nargs='?',
        default='facebook_ads.json',
        help='Fichier JSON à analyser (défaut: facebook_ads.json)'
    )
    parser.add_argument(
        '--export',
        help='Exporter un résumé vers un fichier JSON'
    )

    args = parser.parse_args()

    print("\n🎯 Facebook Ads Creative Angles Analyzer")

    data = load_results(args.input)
    analyze_ads(data)

    if args.export:
        export_summary(data, args.export)


if __name__ == "__main__":
    main()
