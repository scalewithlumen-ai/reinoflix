#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir URLs absolutas remanescentes que afetam mobile
Foca em JSON-LD schemas e JavaScript config objects
"""

import os
import re

def fix_absolute_urls(content):
    """Remove todas as URLs absolutas do reinoflix.com"""
    original_content = content

    # 1. Corrigir URLs absolutas simples para relativas
    # https://reinoflix.com/ -> /
    content = re.sub(
        r'https://reinoflix\.com/',
        '/',
        content
    )

    # 2. Corrigir URLs absolutas sem barra final
    # https://reinoflix.com -> (vazio ou /, dependendo do contexto)
    # Mas preservar em JSON-LD @id que precisa da URL completa para schema.org
    # Vamos substituir somente em contextos específicos

    # 3. Corrigir JSON escaped (como \"https:\/\/reinoflix.com\/)
    content = re.sub(
        r'https:\\/\\/reinoflix\\.com\\/',
        '\\/',
        content
    )

    # 4. Corrigir URLs em page_permalink e similares
    content = re.sub(
        r'"page_permalink":"https://reinoflix\.com/"',
        '"page_permalink":"/"',
        content
    )

    return content, content != original_content

def process_file(file_path):
    """Processa um arquivo HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fixed_content, changed = fix_absolute_urls(content)

        if changed:
            # Fazer backup
            backup_path = file_path + '.before-mobile-fix'
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
    print("CORREÇÃO DE URLs ABSOLUTAS PARA MOBILE")
    print("=" * 70)
    print()

    file_path = r"C:\Meus Sites\reinoflix\reinoflix.com\index.html"

    if not os.path.exists(file_path):
        print(f"[ERRO] Arquivo não encontrado: {file_path}")
        return

    # Contar URLs absolutas antes
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    before_count = len(re.findall(r'https://reinoflix\.com', content))
    print(f"URLs absolutas encontradas: {before_count}")
    print()

    success, status = process_file(file_path)

    # Contar URLs absolutas depois
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    after_count = len(re.findall(r'https://reinoflix\.com', content))

    print("=" * 70)
    if success:
        print("[SUCESSO] Arquivo corrigido")
        print(f"URLs absolutas antes: {before_count}")
        print(f"URLs absolutas depois: {after_count}")
        print(f"URLs removidas: {before_count - after_count}")
        print()
        print(f"Backup criado: {file_path}.before-mobile-fix")
    else:
        print(f"[INFO] {status}")
    print("=" * 70)

if __name__ == "__main__":
    main()
