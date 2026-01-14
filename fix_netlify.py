#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover comentários HTTrack e corrigir URLs para deploy no Netlify
"""

import os
import re
import glob

def fix_html_file(file_path):
    """Remove comentários HTTrack e corrige URLs absolutas"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 1. Remover comentários do HTTrack
        # Remover linhas como: <!-- Mirrored from ... -->
        content = re.sub(
            r'<!--\s*Mirrored from[^>]*-->',
            '',
            content
        )

        # Remover linhas como: <!-- Created by HTTrack ... -->
        content = re.sub(
            r'<!--\s*Created by HTTrack[^>]*-->',
            '',
            content
        )

        # Remover linhas como: <!-- Added by HTTrack --><meta http-equiv="content-type" ... /><!-- /Added by HTTrack -->
        content = re.sub(
            r'<!--\s*Added by HTTrack\s*--><meta http-equiv="content-type"[^>]*/><!--\s*/Added by HTTrack\s*-->',
            '',
            content
        )

        # 2. Corrigir URLs absolutas para relativas (manter domínio interno)
        # Substituir https://reinoflix.com/ por caminhos relativos apenas para recursos locais
        # Manter URLs do Facebook, CDNs externos, etc.

        # Corrigir hrefs internos
        content = re.sub(
            r'href="https://reinoflix\.com/',
            'href="/',
            content
        )

        # Corrigir srcs de imagens/scripts internos
        content = re.sub(
            r'src="https://reinoflix\.com/',
            'src="/',
            content
        )

        # Corrigir srcset de imagens
        content = re.sub(
            r'srcset="https://reinoflix\.com/',
            'srcset="/',
            content
        )

        # Corrigir data-src (lazy loading)
        content = re.sub(
            r'data-src="https://reinoflix\.com/',
            'data-src="/',
            content
        )

        # Corrigir URLs em JSON/JavaScript inline
        content = re.sub(
            r'"https:\\\\/\\\\/reinoflix\\.com\\\\/',
            '"\\\\//',
            content
        )

        # Limpar linhas vazias múltiplas deixadas pelos comentários removidos
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original_content:
            # Fazer backup
            backup_path = file_path + '.bak'
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
        alterado, status = fix_html_file(arquivo)
        arquivo_relativo = os.path.relpath(arquivo, diretorio)

        if alterado:
            print(f"[OK] {arquivo_relativo} - {status}")
            modificados += 1
        else:
            print(f"     {arquivo_relativo} - {status}")

    print("-" * 60)
    print(f"\nTotal: {modificados} arquivos modificados de {len(arquivos_html)}")
    print("\nCorreções aplicadas:")
    print("- Removidos comentários HTTrack")
    print("- Corrigidas URLs absolutas para relativas")
    print("\nBackups criados com extensão .bak")

if __name__ == "__main__":
    main()
