# Reinoflix - Streaming Cristão Infantil

Site de streaming cristão infantil com mais de 300 filmes e histórias bíblicas.

## Status do Projeto

✅ Código malicioso removido (cloaking scripts)
✅ Comentários HTTrack removidos
✅ URLs otimizadas para deploy no Netlify
✅ Pronto para produção

## Estrutura do Projeto

```
reinoflix/
├── reinoflix.com/          # Arquivos principais do site
│   ├── index.html          # Página inicial
│   ├── elreino/            # Página El Reino
│   ├── obrigado/           # Página de agradecimento
│   ├── wp-content/         # Conteúdo WordPress
│   │   ├── uploads/        # Imagens e vídeos
│   │   └── plugins/        # Plugins
│   └── wp-includes/        # Bibliotecas WordPress
├── reinoflix-fixed/        # Versão backup
├── reinoflix-tailwind/     # Versão Tailwind
└── limpar_cloaker.py       # Script de limpeza de malware
```

## Deploy no Netlify

### Configuração Recomendada

**Build settings:**
- Base directory: `reinoflix.com`
- Publish directory: `reinoflix.com`
- Build command: (deixe vazio)

### Arquivo de Configuração

Crie um arquivo `netlify.toml` na raiz com:

```toml
[build]
  publish = "reinoflix.com"
  command = ""

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Correções Aplicadas

### 1. Remoção de Cloaking (Commit: 04fa280)

Removidos 3 tipos de scripts maliciosos:
- Script de redirecionamento de cliques (handleClick)
- Script de auto-reload (litespeed_vary)
- Script de manipulação de referrer (litespeed_docref)

**Arquivos afetados:** 13 arquivos HTML

### 2. Otimização para Netlify (Commit: bfd4cb0)

- ✅ Removidos comentários HTTrack
- ✅ URLs absolutas convertidas para relativas
- ✅ Correção de caminhos de recursos

**Arquivos corrigidos:** 17 arquivos HTML

### 3. Correção de Imagens WebP (Commit: 0e0ce2c)

**Problema:** Imagens retornando 404 devido ao WebP Express

O plugin WordPress WebP Express gera imagens WebP dinamicamente, mas essas não existem no deploy estático.

**Solução:**
- ✅ Removidas tags `<picture>` com sources WebP
- ✅ Corrigidos caminhos de `/webp-express/webp-images/` para `/uploads/`
- ✅ Removidas extensões `.webp` duplicadas
- ✅ Usando imagens originais PNG/JPG que existem no servidor

**Arquivos corrigidos:** 13 arquivos HTML
**Erros resolvidos:** FOLHA-GOSPEL.png.webp, FOLHA-GOSPEL-1.png.webp e outros

## Scripts Úteis

### limpar_cloaker.py
Remove códigos maliciosos de cloaking dos arquivos HTML.

```bash
python limpar_cloaker.py
```

### fix_netlify.py
Remove comentários HTTrack e corrige URLs para Netlify.

```bash
python fix_netlify.py
```

### fix_webp.py
Remove referências ao WebP Express e usa imagens originais.

```bash
python fix_webp.py
```

Corrige:
- Remove tags `<picture>` com WebP
- Atualiza caminhos de imagens
- Remove extensões .webp duplicadas

## Problemas Conhecidos e Soluções

### Imagens não carregam
✅ **Solucionado** - URLs absolutas foram convertidas para relativas

### Imagens WebP retornam 404
✅ **Solucionado** - Removidas referências ao WebP Express, usando imagens originais

### Mensagem HTTrack aparece antes do site
✅ **Solucionado** - Comentários HTTrack foram removidos

### Redirecionamentos estranhos
✅ **Solucionado** - Scripts de cloaking foram removidos

## Tecnologias Utilizadas

- HTML5
- WordPress (estrutura base)
- LiteSpeed Cache
- Elementor
- Facebook Pixel
- Typebot

## Licença

All rights reserved - Reinoflix / Reino Flix

## Contato

Site: https://reinoflix.com
