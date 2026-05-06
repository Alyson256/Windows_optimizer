<div align="center">

# 🪟 win-optimizer

**Scripts de otimização pós-instalação para Windows 11 — seguros, documentados e reversíveis.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Windows 11](https://img.shields.io/badge/Windows-11-0078D4?logo=windows)](https://www.microsoft.com/windows/windows-11)
[![Batch + PowerShell](https://img.shields.io/badge/Batch_%2B_PowerShell-hybrid-5391FE?logo=powershell)](../scripts/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](../CONTRIBUTING.md)

**🌐 Language / Idioma:** &nbsp; [🇺🇸 English](../README.md) &nbsp;|&nbsp; [🇧🇷 Português](pt-BR.md)

</div>

---

## ✨ O que é isso?

Uma coleção de scripts `.bat` (com PowerShell inline para operações de sistema) para deixar uma instalação limpa do Windows 11 mais rápida, silenciosa e privativa — **sem tocar em nada que quebre o sistema**.

Cada script é:
- ✅ **Seguro** — altera apenas serviços não-essenciais e chaves de registro (policies)
- ✅ **Reversível** — o `10_undo_all.bat` restaura tudo para os padrões do Windows
- ✅ **Transparente** — cada alteração é registrada em log com timestamp
- ✅ **Documentado** — confira [RISKS_pt-BR.md](RISKS_pt-BR.md) para detalhes técnicos de cada script

---

## 🚀 Início Rápido

> **Requisitos:** Windows 11, privilégios de Administrador.

```batch
git clone https://github.com/SEU_USUARIO/win-optimizer.git
cd win-optimizer\scripts

:: Clique com o botão direito > Executar como Administrador
00_run_all.bat
```

Cada script também pode ser executado individualmente.

---

## 📂 Estrutura do Projeto

```
win-optimizer/
├── scripts/
│   ├── 00_run_all.bat          ← Launcher mestre (auto-elevação UAC)
│   ├── 01_restore_point.bat    ← Cria ponto de restauração ANTES de tudo
│   ├── 02_services_manual.bat  ← Serviços não-essenciais → Manual
│   ├── 03_disable_recall.bat   ← Desativa Windows Recall (capturas por IA)
│   ├── 04_disable_telemetry.bat← Desativa telemetria e DiagTrack
│   ├── 05_power_plan.bat       ← Plano de Energia de Alto Desempenho
│   ├── 06_visual_tweaks.bat    ← Desativa animações/transparência
│   ├── 07_network_tweaks.bat   ← Nagle off, ajustes TCP, cache de DNS
│   ├── 08_privacy_tweaks.bat   ← ID de anúncios, localização, histórico
│   ├── 09_startup_cleanup.bat  ← Auditoria de inicialização (somente leitura)
│   ├── 10_undo_all.bat         ← Reverte TUDO para o padrão do Windows
│   ├── 11_remove_bloatware.bat ← Remove aplicativos UWP não-essenciais
│   ├── 12_system_cleanup.bat   ← Limpa cache DNS, arquivos Temp e Lixeira
│   └── _lib/                   ← Compartilhado: cores, logger, verificação admin
├── tools/
│   └── check_status.bat        ← Auditoria do estado atual (somente leitura)
└── docs/
    ├── TIPS_pt-BR.md           ← Dicas de instalação limpa & boas práticas
    ├── RISKS_pt-BR.md          ← Descrição de riscos por script
    └── pt-BR.md                ← Documentação em Português
```

---

## 📋 Tabela de Scripts

| Script | Categoria | Risco | Reversível |
|--------|----------|------|-----------|
| `01_restore_point` | Segurança | Nenhum | — |
| `02_services_manual` | Performance | 🟢 Baixo | ✓ |
| `03_disable_recall` | Privacidade | 🟢 Baixo | ✓ |
| `04_disable_telemetry` | Privacidade | 🟢 Baixo | ✓ |
| `05_power_plan` | Performance | 🟢 Baixo | ✓ |
| `06_visual_tweaks` | Performance | 🟢 Baixo | ✓ |
| `07_network_tweaks` | Performance | 🟡 Médio | ✓ |
| `08_privacy_tweaks` | Privacidade | 🟢 Baixo | ✓ |
| `09_startup_cleanup` | Auditoria | Nenhum (apenas leitura) | — |
| `10_undo_all` | Reversão | Nenhum | — |
| `11_remove_bloatware` | Limpeza | 🟢 Baixo | ✓ Store |
| `12_system_cleanup` | Limpeza | Nenhum | — |
| `check_status` | Auditoria | Nenhum (apenas leitura) | — |

> Descrição completa dos riscos de cada script: [RISKS_pt-BR.md](RISKS_pt-BR.md)  
> Dicas para uma instalação limpa do Windows: [TIPS_pt-BR.md](TIPS_pt-BR.md)

---

## 🔄 Revertendo Modificações

Execute `10_undo_all.bat` como Administrador para restaurar todas as configurações para o padrão de fábrica do Windows.
Alternativamente, você pode usar a Restauração do Sistema criada na etapa 01.

---

## 📦 O que NÃO é modificado

Para evitar qualquer chance de quebrar o seu sistema operacional, estes itens são intencionalmente ignorados:

- ❌ Arquivo `hosts` (ver [RISKS_pt-BR.md](RISKS_pt-BR.md) para alternativas)
- ❌ Windows Defender / Central de Segurança
- ❌ Políticas de Windows Update
- ❌ Drivers de hardware e dispositivos
- ❌ Overclock de CPU/GPU

---

## 🤝 Contribuindo

Issues e PRs são muito bem-vindos! Por favor, leia [RISKS_pt-BR.md](RISKS_pt-BR.md) antes de enviar novas modificações.
Novos scripts devem seguir o padrão da pasta `_lib/` (validação de admin, logger, cores) e devem ter um passo de desfazer correspondente no `10_undo_all.bat`.

---

## 📄 Licença

MIT — veja o arquivo [LICENSE](../LICENSE).
