#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover referências ao WebP Express e usar imagens originais
"""

import os
import re

def fix_webp_references(file_path):
    """Remove tags <picture> com WebP e mantém apenas as imagens originais"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Remover tags <picture> completas com source webp
        # Padrão: <picture><source srcset="...webp" ...><img ...></picture>
        # Substituir pela tag <img> interna apenas

        # Primeiro, extrair e substituir tags picture completas
        picture_pattern = r'<picture>(<source[^>]*webp[^>]*>)+(<img[^>]*>)</picture>'

        def replace_picture(match):
            # Pega apenas a tag img
            return match.group(2)

        content = re.sub(picture_pattern, replace_picture, content, flags=re.DOTALL)

        # 2. Remover referências a webp-express em srcset e src
        content = re.sub(
            r'https://reinoflix\.com/wp-content/webp-express/webp-images/uploads/',
            '/wp-content/uploads/',
            content
        )

        # 3. Remover extensões .webp duplicadas de caminhos de imagens
        # Ex: /uploads/2024/05/image.png.webp -> /uploads/2024/05/image.png
        content = re.sub(
            r'(/wp-content/uploads/[^"\s]+\.(png|jpg|jpeg))\.webp',
            r'\1',
            content,
            flags=re.IGNORECASE
        )

        # 4. Remover data-src com webp
        content = re.sub(
            r'data-src="[^"]*webp-express[^"]*"',
            '',
            content
        )

        # 5. Limpar atributos vazios que podem ter sobrado
        content = re.sub(r'\s+data-src=""', '', content)
        content = re.sub(r'\s+srcset=""', '', content)

        # 6. Remover classe webpexpress-processed
        content = re.sub(r'\s*webpexpress-processed', '', content)

        if content != original_content:
            # Fazer backup
            backup_path = file_path + '.webp-bak'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

            # Salvar arquivo corrigido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, "Corrigido"
        else:
            return False, "Sem alterações"

    except Exception as e:
        return False, f"Erro: {str(e)}"

def main():
    """Função principal"""
    diretorio = r"C:\Meus Sites\reinoflix\reinoflix.com"

    # Encontrar todos arquivos HTML
    arquivos_html = []
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if file.endswith('.html'):
                arquivos_html.append(os.path.join(root, file))

    print(f"Encontrados {len(arquivos_html)} arquivos HTML")
    print("-" * 60)

    modificados = 0
    for arquivo in arquivos_html:
        alterado, status = fix_webp_references(arquivo)
        arquivo_relativo = os.path.relpath(arquivo, diretorio)

        if alterado:
            print(f"[OK] {arquivo_relativo} - {status}")
            modificados += 1
        else:
            print(f"     {arquivo_relativo} - {status}")

    print("-" * 60)
    print(f"\nTotal: {modificados} arquivos modificados de {len(arquivos_html)}")
    print("\nCorreções aplicadas:")
    print("- Removidas tags <picture> com WebP")
    print("- Corrigidos caminhos webp-express para uploads normais")
    print("- Removidas extensões .webp duplicadas")
    print("\nBackups criados com extensão .webp-bak")

if __name__ == "__main__":
    main()
