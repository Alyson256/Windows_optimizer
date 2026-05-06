# Riscos e Detalhes

Explicação transparente sobre o que cada script faz, quais chaves de registro são alteradas e quais os riscos envolvidos.

---

## 02 — Serviços → Manual

**Risco: 🟢 Baixo**

Altera para `start=demand` (Manual), e NÃO `start=disabled` (Desativado).
O serviço continuará iniciando caso o Windows ou outro aplicativo solicite.

| Serviço | Padrão | Alterado para | Impacto se interrompido |
|---------|--------|---------------|-------------------------|
| SysMain | Automático | Manual | Sem pré-carregamento de disco. Impacto imperceptível em SSDs. |
| WSearch | Automático | Manual | Indexação de pesquisa pausada. A busca de arquivos ainda funciona. |
| DiagTrack | Automático | Manual | Telemetria para de enviar dados. |
| XblAuthManager | Automático | Manual | Login do Xbox Live pode pedir senha no primeiro uso. |
| RemoteRegistry | Automático | Manual | Edição remota de registro desativada. |

---

## 03 — Desativar Windows Recall

**Risco: 🟢 Baixo**

Escreve `DisableAIDataAnalysis = 1` nas chaves de Diretiva de Grupo (Group Policy):
- `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsAI`
- `HKCU\Software\Policies\Microsoft\Windows\WindowsAI`

Essas são **chaves de política** — elas sobrescrevem as configurações do usuário, mas podem ser removidas de forma limpa.
Afeta apenas builds do Windows 11 24H2 ou superiores (≥ 26100).

---

## 04 — Desativar Telemetria

**Risco: 🟢 Baixo**

- Define `AllowTelemetry = 0` em dois caminhos de política.
- No Windows 11 **Home**, a Microsoft pode forçar um mínimo de nível 1 (Básico) apesar da chave estar definida como 0. Isso é padrão do Windows. A chave ainda é escrita.
- NÃO modifica o arquivo `hosts` (sem risco de bloquear os servidores de atualização do Windows).

### Opcional: Bloqueio no arquivo Hosts
Se você deseja bloquear pontos finais de telemetria em nível de rede, pode adicionar entradas manualmente em `C:\Windows\System32\drivers\etc\hosts`. Isso não é feito automaticamente porque pode, ocasionalmente, bloquear serviços legítimos da Microsoft (ex: CDNs de atualização que compartilham IPs).

---

## 05 — Plano de Energia

**Risco: 🟢 Baixo**

- O plano de Alto Desempenho consome mais energia — relevante apenas para notebooks na bateria.
- Desativar a hibernação remove o arquivo `hiberfil.sys` (~tamanho da sua RAM). Isso é irreversível a partir deste script; execute `10_undo_all.bat` ou rode `powercfg /h on` manualmente.
- Desativar o "Fast Startup" (Inicialização Rápida) significa um desligamento ligeiramente mais lento. Isso é intencional — a Inicialização Rápida é uma hibernação híbrida que pode causar problemas de estado em drivers ao ligar o PC.

---

## 06 — Ajustes Visuais

**Risco: 🟢 Baixo / 🟢 Nenhum**

Todas as alterações são feitas em `HKCU` (apenas para o usuário atual). A suavização de fontes ClearType é explicitamente preservada para manter a boa legibilidade.
O Explorer (Windows) é reiniciado automaticamente — a barra de tarefas piscará brevemente.

---

## 07 — Ajustes de Rede

**Risco: 🟡 Médio**

- **Algoritmo Nagle desativado**: Pode aumentar ligeiramente o uso de largura de banda de upload (mais pacotes pequenos). Benéfico para jogos, videochamadas e SSH. Sem desvantagens para a maioria das conexões de banda larga.
- **ECN desativado**: Alguns roteadores raros não suportam ECN e podem derrubar conexões. Desativar isso evita esse caso isolado.
- **NetworkThrottlingIndex**: Definir como `0xFFFFFFFF` remove o estrangulamento em segundo plano do Windows em streams de multimídia. Benéfico para jogos e softwares de áudio (DAWs).

---

## 08 — Ajustes de Privacidade

**Risco: 🟢 Nenhum**

Todas as chaves são de nível de usuário (`HKCU`) ou chaves de política que o Windows lê, mas das quais não depende para estabilidade.
O acesso à câmera/microfone **não** é alterado — eles continuam controláveis pelo usuário em Configurações > Privacidade.

---

## 09 — Auditoria de Inicialização

**Risco: Nenhum (somente leitura)**

Exibe uma lista de entradas de registro de inicialização e tarefas agendadas. Nenhuma alteração é feita.

---

## 10 — Desfazer Tudo

**Risco: 🟢 Nenhum**

Restaura os padrões **excluindo chaves de política** (a abordagem mais limpa — evita escrever valores incorretos).
Os serviços são revertidos para o estado padrão de fábrica correto (`Automático` ou `Manual`). Os efeitos visuais voltam para "Deixar o Windows escolher".

---

## 11 — Remover Bloatware

**Risco: 🟢 Baixo**

Remove aplicativos UWP pré-instalados via PowerShell. Não afeta componentes cruciais do sistema operacional. O script pausa para perguntar se a Xbox Game Bar (que possui funcionalidade nativa de gravação de tela) deve ser removida. Todos os aplicativos podem ser reinstalados livremente através da Microsoft Store.

---

## 12 — Limpeza de Sistema e Rede

**Risco: Nenhum**

Esvazia pastas temporárias oficiais do Windows (`%TEMP%`, `C:\Windows\Temp`), limpa o cache de resolução de DNS do adaptador de rede, exclui o cache de download de atualizações limpas do Windows e esvazia a lixeira globalmente. Essencialmente equivale ao uso de um limpador padrão do Windows, sem risco aos dados do usuário ou arquivos de sistema.
