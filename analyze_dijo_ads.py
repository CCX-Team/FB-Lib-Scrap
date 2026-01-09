#!/usr/bin/env python3
"""
Analyseur spécifique pour les publicités DIJO / probiotiques
Avec exemples de créa pour chaque angle identifié
"""

import json
import re
from collections import Counter
from typing import Dict, List

def load_data(filename="facebook_ads_v2.json"):
    """Charge les données"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_ad_example(ad: Dict, indent="    ") -> str:
    """Formate un exemple de publicité"""
    lines = []
    lines.append(f"{indent}📅 Période: {ad.get('date_start', 'N/A')} → {ad.get('date_end', 'N/A')}")
    lines.append(f"{indent}🆔 ID: {ad.get('id', 'N/A')}")

    if ad.get('platforms'):
        lines.append(f"{indent}📱 Plateformes: {', '.join(ad['platforms'])}")

    text_lines = ad.get('text_lines', [])
    if text_lines:
        lines.append(f"{indent}📝 Contenu:")
        for i, line in enumerate(text_lines[:5], 1):
            if line and len(line) > 3:
                lines.append(f"{indent}   {i}. {line[:80]}{'...' if len(line) > 80 else ''}")

    return "\n".join(lines)

def analyze_creative_angles(data: Dict):
    """Analyse approfondie des angles créatifs avec exemples"""

    ads = data.get('ads', [])

    print(f"\n{'='*70}")
    print(f"  ANALYSE DES ANGLES CRÉATIFS - DIJO PROBIOTIQUES")
    print(f"{'='*70}\n")

    print(f"📊 Vue d'ensemble")
    print(f"  Total de publicités : {len(ads)}")
    print(f"  Attendues : {data.get('expected_total', 'N/A')}")

    # Extraction des angles avec exemples
    promotional_angles = []
    product_angles = []
    benefit_angles = []
    all_ctas = []

    # Dictionnaires pour stocker les exemples par angle
    promo_examples = {}
    product_examples = {}
    benefit_examples = {}

    for ad in ads:
        text_lines = ad.get('text_lines', [])
        full_text = ' '.join(text_lines).lower()

        # Angles promotionnels
        if '-' in full_text and '%' in full_text:
            promo_match = re.search(r'(-\d+%)', ' '.join(text_lines))
            if promo_match:
                promo_key = promo_match.group(1)
                promotional_angles.append(promo_key)
                if promo_key not in promo_examples:
                    promo_examples[promo_key] = ad

        # Angles produit
        if 'probiotiques' in full_text and 'indispensable' in full_text:
            product_angles.append("Focus Probiotiques")
            if "Focus Probiotiques" not in product_examples:
                product_examples["Focus Probiotiques"] = ad

        if 'glutamine' in full_text:
            product_angles.append("Focus Glutamine")
            if "Focus Glutamine" not in product_examples:
                product_examples["Focus Glutamine"] = ad

        if 'reset' in full_text:
            product_angles.append("DIJO RESET")
            if "DIJO RESET" not in product_examples:
                product_examples["DIJO RESET"] = ad

        if ('pack' in full_text or 'associez' in full_text) and not 'pack' in product_examples:
            product_angles.append("Pack/Bundle")
            if "Pack/Bundle" not in product_examples:
                product_examples["Pack/Bundle"] = ad

        # Bénéfices mentionnés
        if 'microbiote' in full_text:
            benefit_angles.append("Équilibre microbiote")
            if "Équilibre microbiote" not in benefit_examples:
                benefit_examples["Équilibre microbiote"] = ad

        if 'flore intestinale' in full_text:
            benefit_angles.append("Flore intestinale")
            if "Flore intestinale" not in benefit_examples:
                benefit_examples["Flore intestinale"] = ad

        if 'ventre gonflé' in full_text or 'ballonnement' in full_text:
            benefit_angles.append("Anti-ballonnements")
            if "Anti-ballonnements" not in benefit_examples:
                benefit_examples["Anti-ballonnements"] = ad

        if 'poids' in full_text or 'minceur' in full_text or 'métabolisme' in full_text:
            benefit_angles.append("Perte de poids / Métabolisme")
            if "Perte de poids / Métabolisme" not in benefit_examples:
                benefit_examples["Perte de poids / Métabolisme"] = ad

        if 'stress' in full_text or 'anxiété' in full_text:
            benefit_angles.append("Anti-stress")
            if "Anti-stress" not in benefit_examples:
                benefit_examples["Anti-stress"] = ad

        # CTAs
        for line in text_lines:
            if any(word in line.lower() for word in ['learn more', 'découvrez', 'profitez', 'prenez soin']):
                if 5 < len(line) < 60:
                    all_ctas.append(line)

    # Compteurs
    promo_counter = Counter(promotional_angles)
    product_counter = Counter(product_angles)
    benefit_counter = Counter(benefit_angles)

    # === ANGLES PROMOTIONNELS ===
    print(f"\n{'='*70}")
    print(f"  🎯 ANGLES PROMOTIONNELS")
    print(f"{'='*70}\n")

    if promo_counter:
        for promo, count in promo_counter.most_common(5):
            bar = '█' * (count // 2)
            print(f"  {promo:30s} : {count:3d} {bar}")

            if promo in promo_examples:
                print(f"\n  💡 Exemple de créa typique:")
                print(format_ad_example(promo_examples[promo]))
                print()
    else:
        print("  Aucun angle promotionnel identifié")

    # === ANGLES PRODUITS ===
    print(f"\n{'='*70}")
    print(f"  📦 ANGLES PRODUITS")
    print(f"{'='*70}\n")

    if product_counter:
        for product, count in product_counter.most_common():
            percentage = (count / len(ads)) * 100
            bar = '█' * int(percentage / 5)
            print(f"  {product:30s} : {count:3d} ({percentage:5.1f}%) {bar}")

            if product in product_examples:
                print(f"\n  💡 Exemple de créa typique:")
                print(format_ad_example(product_examples[product]))
                print()
    else:
        print("  Aucun angle produit identifié")

    # === BÉNÉFICES SANTÉ ===
    print(f"\n{'='*70}")
    print(f"  💊 BÉNÉFICES SANTÉ MIS EN AVANT")
    print(f"{'='*70}\n")

    if benefit_counter:
        for benefit, count in benefit_counter.most_common():
            percentage = (count / len(ads)) * 100
            bar = '█' * int(percentage / 5)
            print(f"  {benefit:30s} : {count:3d} ({percentage:5.1f}%) {bar}")

            if benefit in benefit_examples:
                print(f"\n  💡 Exemple de créa typique:")
                print(format_ad_example(benefit_examples[benefit]))
                print()
    else:
        print("  Aucun bénéfice identifié")

    # === TIMELINE ===
    print(f"\n{'='*70}")
    print(f"  📅 CHRONOLOGIE DES CAMPAGNES")
    print(f"{'='*70}\n")

    months = {}
    for ad in ads:
        date_start = ad.get('date_start', '')
        if date_start:
            try:
                month_match = re.search(r'(\w+)\s+\d{4}', date_start)
                if month_match:
                    month = month_match.group(1)
                    months[month] = months.get(month, 0) + 1
            except:
                pass

    for month_name, count in sorted(months.items(), key=lambda x: x[1], reverse=True):
        bar = '█' * count
        print(f"  {month_name:15s} : {count:3d} {bar}")

    # === EXEMPLES DE COPY ===
    print(f"\n{'='*70}")
    print(f"  ✍️  EXEMPLES DE COPY (HEADLINES)")
    print(f"{'='*70}\n")

    unique_headlines = set()
    for ad in ads:
        lines = ad.get('text_lines', [])
        if lines:
            headline = lines[0]
            if 10 < len(headline) < 150:
                unique_headlines.add(headline)

    for i, headline in enumerate(sorted(unique_headlines)[:15], 1):
        print(f"  {i:2d}. {headline}")

    # === CTAs ===
    print(f"\n{'='*70}")
    print(f"  🎬 CALL-TO-ACTIONS UTILISÉS")
    print(f"{'='*70}\n")

    unique_ctas = set(all_ctas)
    for i, cta in enumerate(sorted(unique_ctas)[:10], 1):
        print(f"  {i:2d}. {cta}")

    # === INSIGHTS ===
    print(f"\n{'='*70}")
    print(f"  💡 INSIGHTS STRATÉGIQUES")
    print(f"{'='*70}\n")

    if promo_counter:
        most_common_promo = promo_counter.most_common(1)[0]
        print(f"✓ Angle promotionnel principal : {most_common_promo[0]}")
        print(f"  Utilisé dans {most_common_promo[1]} publicités")

    if product_counter:
        print(f"\n✓ Mix produits :")
        for product, count in product_counter.most_common(3):
            print(f"  - {product} : {count} mentions")

    if benefit_counter:
        top_benefit = benefit_counter.most_common(1)[0]
        print(f"\n✓ Bénéfice le plus mis en avant : {top_benefit[0]}")
        print(f"  Utilisé dans {(top_benefit[1]/len(ads)*100):.0f}% des pubs")

    if months:
        print(f"\n✓ Mois les plus actifs : {', '.join(list(months.keys())[:3])}")

    print(f"\n{'='*70}\n")

    # Export summary avec exemples
    summary = {
        "total_ads": len(ads),
        "promotional_angles": {
            "counts": dict(promo_counter),
            "examples": {k: v for k, v in promo_examples.items()}
        },
        "product_angles": {
            "counts": dict(product_counter),
            "examples": {k: v for k, v in product_examples.items()}
        },
        "benefit_angles": {
            "counts": dict(benefit_counter),
            "examples": {k: v for k, v in benefit_examples.items()}
        },
        "monthly_distribution": months,
        "unique_headlines": list(unique_headlines),
        "unique_ctas": list(unique_ctas)
    }

    return summary


def export_summary(summary: Dict, filename="dijo_angles_summary.json"):
    """Exporte le résumé en JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"📄 Résumé exporté : {filename}")


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "examples/facebook_ads_v2.json"

    data = load_data(input_file)
    summary = analyze_creative_angles(data)
    export_summary(summary)
