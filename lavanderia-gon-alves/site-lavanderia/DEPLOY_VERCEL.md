# Deploy na Vercel

Este projeto é um site estático demonstrativo. O build não usa dependências externas e gera a versão final em `dist/`.

## Pelo painel da Vercel

1. Envie esta pasta para um repositório GitHub, GitLab ou Bitbucket.
2. Na Vercel, escolha **Add New > Project** e importe o repositório.
3. O arquivo `vercel.json` preencherá automaticamente:
   - Framework: `Other`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Clique em **Deploy**.

Nenhuma variável de ambiente é necessária.

## Pela CLI

```bash
npm install -g vercel
vercel
```

Para publicar como produção:

```bash
vercel --prod
```

## Antes da versão oficial

- Substitua as imagens e depoimentos demonstrativos pelos materiais aprovados pelo cliente.
- Confirme telefones, horários, cidades e regiões de coleta.
- Remova `noindex, nofollow` de `index.html`.
- Troque o conteúdo de `robots.txt` para permitir indexação.
- Configure domínio próprio e ferramenta de métricas.
