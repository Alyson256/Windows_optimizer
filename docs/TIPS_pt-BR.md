# 💡 Dicas de Instalação e Configuração

Melhores práticas para uma instalação limpa do Windows 11 — antes de executar quaisquer scripts de otimização.

---

## 🔌 Instale o Windows Sem Internet (Dica Mais Importante)

Quando a instalação do Windows 11 pedir para você conectar ao Wi-Fi ou Ethernet — **não conecte**.

**Por que isso importa:**
- Conectar durante a configuração força você a entrar com uma **conta da Microsoft** (não há opção de conta local na edição Home)
- O Windows baixa e instala **bloatwares adicionais** atrelados à sua conta da Microsoft
- Habilita a **sincronização de atividades**, ID de anúncios e Cortana desde o primeiro uso

**Como burlar isso no Windows 11:**

**Método 1 — Sem cabo:** Simplesmente não conecte o cabo de rede / não conecte no Wi-Fi durante a configuração.

**Método 2 — Se Wi-Fi/Ethernet for detectado automaticamente:**
```
Na tela "Vamos conectar você a uma rede":
  Pressione Shift + F10  →  abre um prompt de comando
  Digite: OOBE\BYPASSNRO
  Pressione Enter  →  o PC reinicia e oferece "Não tenho internet"
```

**Método 3 — Em versões mais recentes (24H2+):**
```
Na tela de rede:
  Pressione Shift + F10
  Digite: start ms-cxh:localonly
  Pressione Enter
```

> Após a instalação ser concluída, você pode conectar à internet normalmente e rodar estes scripts.

---

## 🏠 Crie uma Conta Local

Durante a configuração offline, o Windows permitirá que você crie uma conta local.
Mantenha seu nome de usuário **curto, sem espaços, sem acentos** — ele se tornará sua pasta `C:\Users\nomedeusuario`.

---

## 🔄 Adiar Atualizações do Windows (Primeiro Uso)

Antes de conectar à internet pela primeira vez:

1. Vá para **Configurações → Windows Update → Opções Avançadas**
2. Clique em **"Pausar atualizações"** por 1 a 5 semanas
3. Então conecte à internet e deixe **apenas os drivers** instalarem primeiro
4. Execute estes scripts de otimização
5. Depois despause as atualizações

Isso evita que o Windows instale aplicativos "recomendados" indesejados durante o primeiro ciclo de atualização.

---

## 🧹 Pule / Negue Tudo Durante o OOBE

Nas telas pós-instalação "Vamos personalizar sua experiência", escolha sempre:

| Tela | Escolha recomendada |
|------|---------------------|
| Dados de diagnóstico | **Apenas os obrigatórios** (mínimo) |
| Escrita a tinta e digitação | **Não** |
| Experiências personalizadas | **Não** |
| Localizar meu dispositivo | **Não** (a menos que necessário) |
| Localização | **Não** |
| ID de Anúncio | **Não** |

---

## 🖥️ Ordem de Instalação de Drivers

Após a primeira inicialização, instale os drivers nesta ordem para evitar conflitos:

1. **Chipset** (AMD ou Intel — do site da fabricante da placa-mãe, não do Windows Update)
2. **Placa de Vídeo (GPU)** (NVIDIA/AMD/Intel — do site oficial deles, não o GeForce Experience completo)
3. **Áudio** (Realtek, etc.)
4. **Rede** (se necessário)
5. Todo o resto

> **Evite instalação completa ("full install") do GeForce Experience / AMD Software** — eles adicionam processos significativos em segundo plano.
> Instale **apenas o driver puro da GPU** usando a opção "Personalizada → Instalação Limpa".

---

## 🛡️ Recomendações do Windows Defender

- Mantenha o Windows Defender **ativado** — ele é leve e eficaz em uma instalação limpa
- Desative **"Enviar amostras automaticamente"** nas configurações do Defender
- Os scripts de telemetria deste repositório NÃO mexem no Defender

---

## 📦 Primeiros Aplicativos Recomendados (Pós-Instalação)

| Categoria | Recomendação | Por quê |
|-----------|--------------|---------|
| Navegador | [Firefox](https://firefox.com) / [Brave](https://brave.com) | Menos telemetria que o Edge |
| Gerenciador de Pacotes | [winget](https://learn.microsoft.com/pt-br/windows/package-manager/) | Integrado, não precisa instalar |
| Drivers GPU | Direto de [nvidia.com](https://nvidia.com) / [amd.com](https://amd.com) | Fuja dos launchers pesados |
| 7-Zip | `winget install 7zip.7zip` | Gratuito, sem anúncios |
| VLC | `winget install VideoLAN.VLC` | Substitui Filmes & TV |

---

## ⚡ Instalação Rápida via winget (após rodar os scripts deste repositório)

```powershell
# Execute no PowerShell como Administrador
winget install 7zip.7zip VideoLAN.VLC Mozilla.Firefox --accept-source-agreements --accept-package-agreements
```
