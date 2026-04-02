@echo off
:: ============================================================
::  Senior iAssist — PASSO 2: Publicar / Atualizar no GitHub
::  Use este arquivo para o primeiro push E para commits futuros.
:: ============================================================

:: ── Configuracoes ────────────────────────────────────────────
set PROJETO_DIR=C:\GIT-personal\Senior-iAssist
set GITHUB_USER=mpoffo
set REPO_NAME=Senior-Agent-Debug
set REPO_URL=https://github.com/%GITHUB_USER%/%REPO_NAME%.git

echo.
echo ============================================================
echo   Senior iAssist - Publicar no GitHub
echo   Repositorio: %REPO_URL%
echo ============================================================
echo.

:: ── 1. Entrar na pasta do projeto ───────────────────────────
cd /d "%PROJETO_DIR%"
if errorlevel 1 (
    echo [ERRO] Pasta nao encontrada: %PROJETO_DIR%
    echo Verifique se o caminho esta correto.
    pause
    exit /b 1
)
echo [OK] Pasta do projeto: %PROJETO_DIR%

:: ── 2. Criar .gitignore se nao existir ──────────────────────
if not exist ".gitignore" (
    echo Criando .gitignore...
    (
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *.pyo
        echo .env
        echo venv/
        echo .venv/
        echo.
        echo # Sistema
        echo .DS_Store
        echo Thumbs.db
        echo desktop.ini
        echo.
        echo # Chaves e segredos
        echo *.key
        echo secrets.txt
    ) > .gitignore
    echo [OK] .gitignore criado.
)

:: ── 3. Inicializar Git se ainda nao for um repositorio ──────
if not exist ".git" (
    echo Inicializando repositorio Git...
    git init
    git remote add origin %REPO_URL%
    echo [OK] Repositorio inicializado e remote configurado.
) else (
    echo [OK] Repositorio Git ja existe.
    :: Garantir que o remote esta correto
    git remote set-url origin %REPO_URL% >nul 2>&1
    if errorlevel 1 (
        git remote add origin %REPO_URL% >nul 2>&1
    )
)

:: ── 4. Verificar status antes de commitar ───────────────────
echo.
echo Arquivos que serao enviados:
echo ─────────────────────────────
git status --short
echo ─────────────────────────────

:: ── 5. Mensagem do commit ────────────────────────────────────
echo.
set /p COMMIT_MSG="Mensagem do commit (ENTER para usar mensagem padrao): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=chore: atualizacao do projeto

:: ── 6. Adicionar, commitar e enviar ─────────────────────────
echo.
echo Adicionando arquivos...
git add .

echo Criando commit: %COMMIT_MSG%
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [AVISO] Nenhuma alteracao para commitar, ou erro no commit.
    echo Verifique se ha arquivos novos ou modificados.
    pause
    exit /b 0
)

echo.
echo Enviando para o GitHub...
echo (Se pedir usuario/senha: usuario = %GITHUB_USER% / senha = seu Personal Access Token)
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo [ERRO] Falha no push. Possiveis causas:
    echo   1. O repositorio ainda nao foi criado no GitHub
    echo      Crie em: https://github.com/new
    echo      Nome: %REPO_NAME%  /  NAO inicialize com README
    echo   2. Token sem permissao de "repo"
    echo   3. Token expirado - gere um novo em: https://github.com/settings/tokens
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   SUCESSO! Projeto publicado em:
echo   https://github.com/%GITHUB_USER%/%REPO_NAME%
echo ============================================================
echo.
pause
