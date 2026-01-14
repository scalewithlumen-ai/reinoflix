#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script v2 para restaurar carrosséis - método mais robusto
"""

import os
import re

def extract_carousel_v2(content, carousel_id):
    """Extrai carousel procurando pelo próximo data-id"""
    # Encontrar início
    pattern_start = rf'(<div[^>]*elementor-element-{carousel_id}[^>]*data-id="{carousel_id}"[^>]*>)'

    match_start = re.search(pattern_start, content)
    if not match_start:
        return None

    start_pos = match_start.start()

    # Encontrar o próximo elemento com data-id (que marca o início do próximo widget)
    pattern_next = r'<div[^>]*data-id="[^"]+?"[^>]*data-element_type='

    # Procurar a partir da posição logo após o início do carousel
    search_from = start_pos + 100  # Pular o próprio carousel

    match_next = re.search(pattern_next, content[search_from:])

    if match_next:
        end_pos = search_from + match_next.start()
    else:
        # Se não encontrar próximo, pegar até o fim da seção
        end_pos = len(content)

    # Extrair o conteúdo
    carousel_html = content[start_pos:end_pos]

    # Garantir que fechamos todos os divs abertos
    # Contar divs
    open_divs = carousel_html.count('<div')
    close_divs = carousel_html.count('</div>')

    if close_divs < open_divs:
        # Adicionar </div>s faltantes
        missing = open_divs - close_divs
        carousel_html += '</div>' * missing

    return carousel_html.strip()

def fix_carousel_content(carousel_html):
    """Remove WebP e corrige URLs"""
    # 1. Remover <picture> e </picture>
    carousel_html = re.sub(r'<picture>', '', carousel_html)
    carousel_html = re.sub(r'</picture>', '', carousel_html)

    # 2. Remover <source> tags
    carousel_html = re.sub(r'<source[^>]*>', '', carousel_html)

    # 3. Corrigir URLs
    carousel_html = re.sub(
        r'https://reinoflix\.com/wp-content/webp-express/webp-images/uploads/',
        '/wp-content/uploads/',
        carousel_html
    )

    carousel_html = re.sub(
        r'https://reinoflix\.com/',
        '/',
        carousel_html
    )

    # 4. Corrigir src sem barra
    carousel_html = re.sub(r'src="wp-content/', r'src="/wp-content/', carousel_html)
    carousel_html = re.sub(r'href="wp-content/', r'href="/wp-content/', carousel_html)

    # 5. Remover classes webpexpress
    carousel_html = re.sub(r'\s*webpexpress-processed', '', carousel_html)

    return carousel_html

def main():
    """Função principal"""
    print("=" * 70)
    print("RESTAURAÇÃO DE CARROSSÉIS V2")
    print("=" * 70)
    print()

    current_file = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html"
    backup_file = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html.backup"

    # Ler arquivos
    with open(current_file, 'r', encoding='utf-8') as f:
        current_content = f.read()

    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()

    carousel_ids = ['7c702e79', '54cf0fe6']

    for carousel_id in carousel_ids:
        print(f"\nProcessando carousel {carousel_id}...")

        # Extrair do backup
        backup_carousel = extract_carousel_v2(backup_content, carousel_id)

        if not backup_carousel:
            print(f"  [ERRO] Não encontrado no backup")
            continue

        print(f"  Extraído: {len(backup_carousel)} chars")
        print(f"  Divs: {backup_carousel.count('<div')} opens, {backup_carousel.count('</div>')} closes")
        print(f"  Slides: {backup_carousel.count('swiper-slide-inner')}")

        # Corrigir
        fixed_carousel = fix_carousel_content(backup_carousel)
        print(f"  Corrigido: {len(fixed_carousel)} chars")

        # Extrair carousel atual (para substituir)
        current_carousel = extract_carousel_v2(current_content, carousel_id)

        if not current_carousel:
            print(f"  [ERRO] Não encontrado no arquivo atual")
            continue

        print(f"  Atual (antes): {len(current_carousel)} chars, {current_carousel.count('swiper-slide-inner')} slides")

        # Substituir
        current_content = current_content.replace(current_carousel, fixed_carousel)
        print(f"  [OK] Substituído")

    # Verificar se houve mudanças
    with open(current_file, 'r', encoding='utf-8') as f:
        original = f.read()

    if current_content != original:
        # Backup
        backup_path = current_file + '.before-v2-carousel'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)

        # Salvar
        with open(current_file, 'w', encoding='utf-8') as f:
            f.write(current_content)

        # Verificar resultado
        print("\n" + "=" * 70)
        print("[SUCESSO] Arquivo salvo!")

        # Contar slides no resultado final
        slide_count = current_content.count('swiper-slide-inner')
        print(f"Total de swiper-slide-inner no resultado: {slide_count}")
        print(f"Backup: {backup_path}")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("[INFO] Nenhuma alteração")
        print("=" * 70)

if __name__ == "__main__":
    main()
