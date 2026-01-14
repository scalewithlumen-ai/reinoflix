#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover códigos maliciosos de cloaking dos arquivos HTML
"""

import os
import re
import glob

def remover_cloaking(conteudo):
    """Remove todos os códigos maliciosos identificados"""

    # 1. Remover script litespeed_docref do início
    conteudo = re.sub(
        r'<script data-no-optimize="1">var litespeed_docref=sessionStorage\.getItem\("litespeed_docref"\);.*?sessionStorage\.removeItem\("litespeed_docref"\)\);</script>\s*',
        '',
        conteudo,
        flags=re.DOTALL
    )

    # 2. Remover script de redirecionamento malicioso (handleClick)
    conteudo = re.sub(
        r'<script type="litespeed/javascript">function getUrlParameters\(\)\{.*?adicionarEventoRedirect\(\)</script>\s*',
        '',
        conteudo,
        flags=re.DOTALL
    )

    # Versão sem type="litespeed/javascript"
    conteudo = re.sub(
        r'<script\s*(?:src="data:text/javascript;base64,[^"]+"|defer)?>\s*function getUrlParameters\(\)\{.*?adicionarEventoRedirect\(\)\s*</script>\s*',
        '',
        conteudo,
        flags=re.DOTALL
    )

    # 3. Remover script de auto-reload do LiteSpeed
    conteudo = re.sub(
        r'<script data-no-optimize="1">var litespeed_vary=document\.cookie\.replace.*?window\.location\.reload\(!0\)\)\}\)\);</script>\s*',
        '',
        conteudo,
        flags=re.DOTALL
    )

    # 4. Remover scripts base64 maliciosos
    conteudo = re.sub(
        r'<script\s+src="data:text/javascript;base64,[^"]*(?:Z2V0VXJsUGFyYW1ldGVycw|dmFyIGxpdGVzcGVlZF92YXJ5)[^"]*"\s+defer></script>\s*',
        '',
        conteudo,
        flags=re.DOTALL
    )

    return conteudo

def processar_arquivo(caminho_arquivo):
    """Processa um arquivo HTML removendo cloaking"""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        conteudo_original = conteudo
        conteudo_limpo = remover_cloaking(conteudo)

        if conteudo_limpo != conteudo_original:
            # Fazer backup
            backup_path = caminho_arquivo + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(conteudo_original)

            # Salvar arquivo limpo
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo_limpo)

            return True, "Limpo"
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
        alterado, status = processar_arquivo(arquivo)
        arquivo_relativo = os.path.relpath(arquivo, diretorio)

        if alterado:
            print(f"[OK] {arquivo_relativo} - {status}")
            modificados += 1
        else:
            print(f"     {arquivo_relativo} - {status}")

    print("-" * 60)
    print(f"\nTotal: {modificados} arquivos modificados de {len(arquivos_html)}")
    print("\nBackups criados com extensão .backup")

if __name__ == "__main__":
    main()
