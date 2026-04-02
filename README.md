# Senior iAssist

Ferramenta interna para visualizar agentes, traces e diagnóstico via IA da plataforma Senior iAssist (ambiente Homologx).

## Arquivos

| Arquivo | Descrição |
|---|---|
| `senior-iassist.html` | Frontend single-page (servido pelo proxy) |
| `proxy.py` | Proxy local Flask — serve o HTML, repassa chamadas ao MLflow e Gemini |
| `skill-login.md` | Documentação do fluxo de autenticação Senior |

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
        ├── GET  /                  → serve senior-iassist.html
        ├── GET/POST /mlflow/*      → proxy → MLflow ALB (homolog)
        └── POST /gemini            → proxy → Gemini API (Google)

Senior Platform (Homologx)
  └── /t/senior-x/platform/iassist/api/v1/agents  → lista de agentes
```

---

## Changelog

### v0.14.11 — 2026-04-02
- **Fix:** Removido `_model` hardcoded do frontend — modelo agora lido exclusivamente via `GEMINI_MODEL` no proxy
- **Fix:** `proxy.py` atualizado com default `gemini-2.5-flash` (nome correto atual da API Google)

### v0.14.10 — 2026-04-02
- **Fix:** Substituído `gemini-2.0-flash-lite` (descontinuado) por `gemini-2.5-flash-preview-04-17` no HTML
- Versão intermediária — modelo ainda hardcoded no frontend

### v0.14.9 — versão base recebida
- Versão inicial registrada no projeto
