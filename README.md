# Senior Agent Debug

Ferramenta interna para visualizar agentes, traces e diagnóstico via IA da plataforma Senior (ambiente Homologx).

## Arquivos

| Arquivo | Versão | Descrição |
|---|---|---|
| `senior-agent-debug.html` | v0.15.3 | Frontend single-page (servido pelo proxy) |
| `proxy.py` | v1.3.0 | Proxy local Flask — serve o HTML, repassa chamadas ao MLflow e Gemini |
| `skill-login.md` | — | Documentação do fluxo de autenticação Senior |
| `senior-design-system-SKILL.md` | v1.0.0 | Skill reutilizável com tokens do Design System Senior |

## Como executar

```bash
pip install flask requests
set GEMINI_API_KEY=AIza...
set GEMINI_MODEL=gemini-2.5-flash   # opcional, este é o default
python proxy.py
```

Abrir: http://127.0.0.1:5000

## Configuração

| Variável de ambiente | Default | Descrição |
|---|---|---|
| `GEMINI_API_KEY` | *(obrigatório)* | Chave da API Gemini (Google AI Studio) |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Modelo Gemini usado no diagnóstico |

> O frontend **não** hardcoda o modelo — ele é sempre lido do `GEMINI_MODEL` no proxy.

## Arquitetura

```
Browser
  └── http://127.0.0.1:5000
        ├── GET  /              → serve senior-agent-debug.html
        ├── GET/POST /mlflow/*  → proxy → MLflow ALB (homolog)
        └── POST /gemini        → proxy → Gemini API v1 (Google)

Senior Platform (Homologx)
  └── /t/senior-x/platform/iassist/api/v1/agents  → lista de agentes
```

---

## Changelog

### senior-agent-debug.html v0.15.3 — 2026-04-02
- **Fix:** Removido `system_instruction` do payload Gemini — campo não existe no endpoint `v1`
- System prompt agora injetado como primeiro par `user`/`model` no array `contents`, compatível com todos os modelos na API v1

### senior-agent-debug.html v0.15.2 — 2026-04-02
- **Rename:** Arquivo renomeado de `senior-iassist.html` para `senior-agent-debug.html`
- **Rename:** Nome do app alterado de "iAssist" / "Senior iAssist" para "Agent Debug" / "Senior Agent Debug" em toda a interface
- Chaves de storage atualizadas: `senior_iassist_token` → `senior_agent_debug_token`, `senior_iassist_wiki` → `senior_agent_debug_wiki`
- Prefixo de log `[iAssist]` → `[AgentDebug]`

### proxy.py v1.3.0 — 2026-04-02
- **Rename:** Referências a `senior-iassist.html` atualizadas para `senior-agent-debug.html`
- Nome do app no console e docstring atualizados para "Senior Agent Debug"

### senior-agent-debug.html v0.15.1 — 2026-04-02
- **Feat:** Suporte a autenticação via postMessage (plataforma Senior embarcada em iframe)
- Detecta automaticamente execução em iframe (`window.parent !== window`)
- Envia `{ type: 'TALENT_MINING_READY' }` ao parent ao inicializar
- Recebe payload `{ token, servicesUrl }` da plataforma e aplica o token na sessão
- Token via postMessage salvo em `sessionStorage` (nunca `localStorage`)
- Validação de origem: aceita apenas domínios `*.senior.com.br` e mesma origin
- Fallback após 2s: tenta `sessionStorage` → `localStorage` → tela de login
- `loadStored()` prioriza `sessionStorage` sobre `localStorage`
- `doLogout()` limpa ambos `sessionStorage` e `localStorage`

### senior-agent-debug.html v0.15.0 — 2026-04-02
- **Feat:** Design System Senior aplicado em toda a interface
- Cor primária migrada de verde (#1D9E75) para azul Senior (#5B9BD5)
- Fontes: Inter (headings) + Open Sans (body) via Google Fonts
- Background da página: #F3F4F6 (gray-10 Senior)
- Border-radius migrado para escala Senior: 4px inputs, 6px cards, 10px containers
- Sombras com sistema de elevação Senior
- Botões: font-weight 400 Open Sans, filter brightness() no hover
- Tabs ativas: azul primário #5B9BD5
- Status badges: tokens --color-green/red/orange com bordas semitransparentes
- Inputs: borda 1px solid #B8BFC7, focus com box-shadow rgba(91,155,213,0.15)
- Tabelas: headers uppercase bold, fundo #F9FAFB
- Cards com box-shadow de elevação e transição hover

### proxy.py v1.2.0 — 2026-04-02
- Versão atualizada no comentário de cabeçalho e no print do console

### proxy.py v1.1.0 — 2026-04-02
- **Fix:** Default do modelo atualizado para gemini-2.5-flash
- **Fix:** API alterada de v1beta para v1

### senior-agent-debug.html v0.14.13 — 2026-04-02
- **Fix:** Adicionado comentário de versão na primeira linha do HTML

### senior-agent-debug.html v0.14.12 — 2026-04-02
- **Fix:** Handler de focus protege todas as telas autenticadas

### senior-agent-debug.html v0.14.11 — 2026-04-02
- **Fix:** Removido _model hardcoded do frontend

### senior-agent-debug.html v0.14.10 — 2026-04-02
- **Fix:** Substituído gemini-2.0-flash-lite por modelo atualizado

### senior-agent-debug.html v0.14.9 — versão base
- Versão inicial registrada no projeto

### senior-design-system-SKILL.md v1.0.0 — 2026-04-02
- **Novo:** Skill criada com todos os tokens do Design System Senior
- Inclui: CSS variables, tipografia, paleta completa, espaçamentos, border-radius, sombras e specs de componentes
- Checklist de migração para aplicar o design em arquivos HTML existentes
