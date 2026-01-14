#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final para restaurar carrosséis completos do backup original
"""

import os
import re

def extract_carousel_from_backup(backup_content, carousel_id):
    """Extrai um carousel completo do backup usando data-id"""
    # Encontrar início do elemento
    pattern = rf'<div class="elementor-element elementor-element-{carousel_id}[^>]*data-id="{carousel_id}"[^>]*>'

    match = re.search(pattern, backup_content)
    if not match:
        return None

    start = match.start()

    # Encontrar o final procurando pelo fechamento do widget
    # Procurar por </div></div></div> que fecha o carousel widget
    search_from = start
    depth = 0
    pos = start

    while pos < len(backup_content):
        if backup_content[pos:pos+5] == '<div ':
            depth += 1
            pos += 5
        elif backup_content[pos:pos+6] == '</div>':
            if depth == 0:
                # Este é o fechamento do nosso carousel
                return backup_content[start:pos+6]
            depth -= 1
            pos += 6
        else:
            pos += 1

    return None

def fix_webp_in_carousel(carousel_html):
    """Remove referências WebP e corrige URLs"""
    # 1. Remover tags <picture> mantendo o conteúdo
    carousel_html = re.sub(r'<picture>', '', carousel_html)
    carousel_html = re.sub(r'</picture>', '', carousel_html)

    # 2. Remover tags <source> com webp
    carousel_html = re.sub(r'<source[^>]*>', '', carousel_html)

    # 3. Corrigir URLs absolutas
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

    # 4. Corrigir src sem barra inicial
    carousel_html = re.sub(
        r'src="wp-content/',
        r'src="/wp-content/',
        carousel_html
    )

    # 5. Remover classes webpexpress
    carousel_html = re.sub(r'\s*webpexpress-processed', '', carousel_html)

    return carousel_html

def replace_carousel_in_content(content, carousel_id, new_carousel):
    """Substitui um carousel no conteúdo atual"""
    # Encontrar o carousel atual (quebrado)
    pattern = rf'<div class="elementor-element elementor-element-{carousel_id}[^>]*data-id="{carousel_id}"[^>]*>.*?</div></div></div>'

    # Tentar encontrar com DOTALL para pegar múltiplas linhas
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        # Tentar padrão mais simples
        pattern2 = rf'<div[^>]*elementor-element-{carousel_id}[^>]*>.*?</div></div></div>'
        match = re.search(pattern2, content, re.DOTALL)

        if not match:
            return content, False

    # Substituir
    content = content[:match.start()] + new_carousel + content[match.end():]
    return content, True

def main():
    """Função principal"""
    print("=" * 70)
    print("RESTAURAÇÃO FINAL DE CARROSSÉIS")
    print("=" * 70)
    print()

    current_file = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html"
    backup_file = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html.backup"

    if not os.path.exists(backup_file):
        print(f"[ERRO] Backup não encontrado: {backup_file}")
        return

    # Ler arquivos
    with open(current_file, 'r', encoding='utf-8') as f:
        current_content = f.read()

    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_content = f.read()

    original_content = current_content

    # IDs dos carrosséis
    carousel_ids = ['7c702e79', '54cf0fe6']

    for carousel_id in carousel_ids:
        print(f"Processando carousel {carousel_id}...")

        # Extrair do backup
        carousel_from_backup = extract_carousel_from_backup(backup_content, carousel_id)

        if not carousel_from_backup:
            print(f"  [ERRO] Não foi possível extrair carousel {carousel_id} do backup")
            continue

        print(f"  Carousel extraído: {len(carousel_from_backup)} caracteres")

        # Corrigir WebP
        fixed_carousel = fix_webp_in_carousel(carousel_from_backup)
        print(f"  Carousel corrigido: {len(fixed_carousel)} caracteres")

        # Substituir no conteúdo atual
        current_content, success = replace_carousel_in_content(current_content, carousel_id, fixed_carousel)

        if success:
            print(f"  [OK] Carousel {carousel_id} restaurado")
        else:
            print(f"  [AVISO] Não foi possível substituir carousel {carousel_id}")

    if current_content != original_content:
        # Fazer backup
        backup_path = current_file + '.before-final-carousel'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)

        # Salvar
        with open(current_file, 'w', encoding='utf-8') as f:
            f.write(current_content)

        print()
        print("=" * 70)
        print("[SUCESSO] Carrosséis restaurados com sucesso!")
        print(f"Backup criado: {backup_path}")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("[INFO] Nenhuma alteração foi feita")
        print("=" * 70)

if __name__ == "__main__":
    main()
