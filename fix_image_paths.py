#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir caminhos de imagens sem barra inicial
Corrige: src="wp-content -> src="/wp-content
"""

import os
import re

def fix_image_paths(content):
    """Adiciona barra inicial em todos os caminhos de imagens"""
    original_content = content

    # 1. Corrigir src="wp-content para src="/wp-content
    content = re.sub(
        r'src="wp-content/',
        r'src="/wp-content/',
        content
    )

    # 2. Corrigir href="wp-content para href="/wp-content
    content = re.sub(
        r'href="wp-content/',
        r'href="/wp-content/',
        content
    )

    # 3. Corrigir data-src="wp-content para data-src="/wp-content
    content = re.sub(
        r'data-src="wp-content/',
        r'data-src="/wp-content/',
        content
    )

    # 4. Corrigir data-lazyloaded="wp-content para data-lazyloaded="/wp-content
    content = re.sub(
        r'data-lazyloaded="wp-content/',
        r'data-lazyloaded="/wp-content/',
        content
    )

    # 5. Corrigir srcset com wp-content sem barra
    # Exemplo: srcset="wp-content/... -> srcset="/wp-content/...
    content = re.sub(
        r'srcset="wp-content/',
        r'srcset="/wp-content/',
        content
    )

    # 6. Corrigir dentro de srcset quando há vírgula
    # Exemplo: , wp-content/... -> , /wp-content/...
    content = re.sub(
        r',\s*wp-content/',
        r', /wp-content/',
        content
    )

    return content, content != original_content

def process_file(file_path):
    """Processa um arquivo HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content, changed = fix_image_paths(content)

        if changed:
            # Fazer backup
            backup_path = file_path + '.before-path-fix'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Salvar arquivo corrigido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)

            return True, "Corrigido"
        else:
            return False, "Sem alterações"

    except Exception as e:
        return False, f"Erro: {str(e)}"

def main():
    """Função principal"""
    print("=" * 70)
    print("CORREÇÃO DE CAMINHOS DE IMAGENS")
    print("=" * 70)
    print()

    file_path = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html"

    if not os.path.exists(file_path):
        print(f"[ERRO] Arquivo não encontrado: {file_path}")
        return

    # Contar problemas antes
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    before_count = len(re.findall(r'(?:src|href|data-src|data-lazyloaded|srcset)="wp-content/', content))
    print(f"Caminhos sem barra inicial encontrados: {before_count}")
    print()

    success, status = process_file(file_path)

    # Contar problemas depois
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    after_count = len(re.findall(r'(?:src|href|data-src|data-lazyloaded|srcset)="wp-content/', content))

    print("=" * 70)
    if success:
        print("[SUCESSO] Arquivo corrigido")
        print(f"Caminhos problemáticos antes: {before_count}")
        print(f"Caminhos problemáticos depois: {after_count}")
        print(f"Caminhos corrigidos: {before_count - after_count}")
        print()
        print(f"Backup criado: {file_path}.before-path-fix")
    else:
        print(f"[INFO] {status}")
    print("=" * 70)

if __name__ == "__main__":
    main()
