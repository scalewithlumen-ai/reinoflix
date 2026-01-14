#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir logo srcset e restaurar carrosséis de imagens
"""

import os
import re

def fix_logo_srcset(content):
    """Converte URLs absolutas para relativas no srcset do logo"""
    # Procurar por srcset com URLs absolutas do reinoflix.com
    content = re.sub(
        r'https://reinoflix\.com(/wp-content/[^"\s]+)',
        r'\1',
        content
    )
    return content

def fix_webp_in_carousel(carousel_html):
    """Remove referências WebP de um bloco de carousel HTML"""
    # Remover tags picture e manter apenas img
    # Mas fazemos isso de forma mais cuidadosa para preservar a estrutura do carousel

    # 1. Remover tags <picture> e </picture>, mantendo o conteúdo interno
    carousel_html = re.sub(r'<picture>', '', carousel_html)
    carousel_html = re.sub(r'</picture>', '', carousel_html)

    # 2. Remover tags <source> com webp
    carousel_html = re.sub(r'<source[^>]*webp[^>]*>', '', carousel_html)

    # 3. Corrigir caminhos de imagens
    carousel_html = re.sub(
        r'https://reinoflix\.com/wp-content/webp-express/webp-images/uploads/',
        '/wp-content/uploads/',
        carousel_html
    )
    carousel_html = re.sub(
        r'/wp-content/webp-express/webp-images/uploads/',
        '/wp-content/uploads/',
        carousel_html
    )

    # 4. Converter URLs absolutas para relativas
    carousel_html = re.sub(
        r'https://reinoflix\.com(/wp-content/[^"\s]+)',
        r'\1',
        carousel_html
    )

    # 5. Remover extensões .webp duplicadas
    carousel_html = re.sub(
        r'(/wp-content/uploads/[^"\s]+\.(png|jpg|jpeg))\.webp',
        r'\1',
        carousel_html,
        flags=re.IGNORECASE
    )

    # 6. Remover src= que aponta para webp-express
    carousel_html = re.sub(
        r'src="[^"]*webp-express[^"]*"',
        '',
        carousel_html
    )

    # 7. Corrigir src relativos que ficaram sem a barra inicial
    carousel_html = re.sub(
        r'src="wp-content/',
        r'src="/wp-content/',
        carousel_html
    )

    return carousel_html

def extract_element_block(content, element_id):
    """Extrai um bloco completo de elemento Elementor pelo data-id"""
    # Padrão para encontrar o elemento e todo seu conteúdo até o fechamento
    pattern = rf'(<div[^>]*data-id="{element_id}"[^>]*>)'

    match = re.search(pattern, content)
    if not match:
        return None

    start_pos = match.start()

    # Agora precisamos encontrar o </div> correspondente
    # Contamos os <div> e </div> para encontrar o fechamento correto
    depth = 0
    pos = start_pos
    in_tag = False
    tag_name = ""

    while pos < len(content):
        char = content[pos]

        if char == '<':
            # Início de uma tag
            tag_end = content.find('>', pos)
            if tag_end == -1:
                break

            tag_content = content[pos:tag_end+1]

            if tag_content.startswith('</div>'):
                depth -= 1
                if depth == 0:
                    # Encontramos o fechamento
                    return content[start_pos:tag_end+1]
            elif tag_content.startswith('<div'):
                depth += 1

            pos = tag_end + 1
        else:
            pos += 1

    return None

def restore_carousels(file_path, backup_path):
    """Restaura os carrosséis do backup com correções de WebP"""
    try:
        # Ler arquivo atual
        with open(file_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Ler backup
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()

        original_content = current_content
        changes_made = []

        # IDs dos carrosséis que precisam ser restaurados
        carousel_ids = ['7c702e79', '54cf0fe6']

        for carousel_id in carousel_ids:
            print(f"Processando carousel {carousel_id}...")

            # Extrair carousel do backup
            backup_carousel = extract_element_block(backup_content, carousel_id)

            if not backup_carousel:
                print(f"  [AVISO] Não foi possível extrair o carousel {carousel_id} do backup")
                continue

            # Corrigir WebP no carousel extraído
            fixed_carousel = fix_webp_in_carousel(backup_carousel)

            # Extrair carousel atual (quebrado)
            current_carousel = extract_element_block(current_content, carousel_id)

            if not current_carousel:
                print(f"  [AVISO] Não foi possível encontrar o carousel {carousel_id} no arquivo atual")
                continue

            # Substituir carousel quebrado pelo corrigido
            current_content = current_content.replace(current_carousel, fixed_carousel)
            changes_made.append(f"Carousel {carousel_id} restaurado")
            print(f"  [OK] Carousel {carousel_id} restaurado")

        # Corrigir logo srcset
        print("Corrigindo logo srcset...")
        current_content = fix_logo_srcset(current_content)
        changes_made.append("Logo srcset corrigido")
        print("  [OK] Logo srcset corrigido")

        if current_content != original_content:
            # Fazer backup
            backup_file = file_path + '.before-carousel-fix'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(original_content)

            # Salvar arquivo corrigido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(current_content)

            return True, changes_made
        else:
            return False, ["Nenhuma alteração necessária"]

    except Exception as e:
        return False, [f"Erro: {str(e)}"]

def main():
    """Função principal"""
    file_path = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html"
    backup_path = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html.webp-bak"

    print("=" * 70)
    print("CORREÇÃO DE LOGO E RESTAURAÇÃO DE CARROSSÉIS")
    print("=" * 70)
    print()

    if not os.path.exists(backup_path):
        print(f"[ERRO] Arquivo de backup não encontrado: {backup_path}")
        return

    success, changes = restore_carousels(file_path, backup_path)

    print()
    print("=" * 70)
    if success:
        print("[SUCESSO] Correções aplicadas:")
        for change in changes:
            print(f"  - {change}")
        print()
        print(f"Backup criado: {file_path}.before-carousel-fix")
    else:
        print("[INFO] Status:")
        for msg in changes:
            print(f"  - {msg}")
    print("=" * 70)

if __name__ == "__main__":
    main()
