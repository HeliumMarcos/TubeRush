# 🚀 TubeRush — TCL C7K 4K60 HDR & Low-Latency Edition

<p align="center">
    <img width="860px" src=".github/assets/TubeRush%20Banner.png">
    <br>
</p>

Cliente YouTube TV sobre **Google Cobalt `27.lts.10` `qa`** (Starboard 18), otimizado para TVs Android/Google TV com SoC **MediaTek MT5896 / Pentonic 700** (como a **TCL C7K**) entregarem **4K (`2160p60 HDR10`)**, seleção multi-codec com marcação em tempo real e **baixa latência estável em lives** — com interface 100% em Português Brasileiro.

---

## ✨ Melhorias implementadas no TubeRush (`v2.1.4`)

### 1. 📦 Identidade própria, Tradução PT-BR Completa e Updater Integrado
- **App unificado:** **TubeRush** (`io.gh.heliummarcos.tizentube.cobalt`) com ícone, banner e splash oficiais do YouTube TV.
- **100% em Português Brasileiro:** todos os menus do TubeRush, configurações do reprodutor, interface e gerenciador de atualizações traduzidos quando a TV/app está em `pt-BR`.
- **TubeRush Updater:** busca e instala atualizações diretamente de `HeliumMarcos/TubeRush` (`releases/latest`), com `versionName` e `versionCode` sincronizados.

### 2. 🎛️ Menu de Qualidade Multi-Codec & Seleção Visual Inteligente (`effectiveBitrate`)
- **Codecs simultâneos:** exibe na mesma lista faixas reais descobertas de **AV1**, **VP9** e **AVC/H.264** para cada resolução (`2160p`, `1440p`, `1080p`, etc.) em layout limpo de duas linhas (resolução/HDR/FPS + codec/Mbps/status).
- **Marcação imediata (`✓`):** acompanha e atualiza instantaneamente a faixa/codec em reprodução ao alternar qualidade durante o vídeo ou live.
- **Hierarquia automática por qualidade visual real:**
  1. Maior resolução (`height`)
  2. Maior taxa de quadros (`fps`)
  3. Faixa dinâmica (`HDR` quando suportado e preferido vs `SDR`, sem misturar HDR e SDR na comparação de bitrate)
  4. Desempate final por **`effectiveBitrate = bps × multiplicador`** (usando `averageBitrate` com fallback para `bitrate` em lives):
     - **VOD:** `AV1 × 1.70`, `VP9/HEVC × 1.35`, `AVC × 1.00`
     - **Live:** `AV1 × 1.50`, `VP9/HEVC × 1.25`, `AVC × 1.00`

### 3. 🔴 Controle Inteligente de Latência ao Vivo & Estabilidade
- **Modo Ao Vivo (Latência) no menu do Reprodutor:**
  - **Equilibrado (Mais estável) — *Pré-selecionado por padrão*:** mantém o buffer enxuto (~3,8–5,0 s em `Normal Latency` e ~2,2 s em `Low Latency`) com aceleração adaptativa suave (`1.06x–1.15x` com preservação de tom) e salto em RAM apenas em atrasos grandes, garantindo baixa latência sem micro-travamentos.
  - **Baixa Latência:** perfil mais agressivo para menor atraso possível com a borda ao vivo.
  - **Padrão do YouTube (Desligado):** desativa o controlador e mantém o buffer nativo do YouTube.
- **Proteção contra perda de quadros (Lives):** monitora `droppedVideoFrames` após a estabilização inicial e desce automaticamente 1 nível de qualidade se detectar sobrecarga sustentada de decodificação (`>= 15%`).
- **Retorno automático ao vivo (PiP/Pause):** reposiciona a transmissão próximo ao ponto ao vivo ao despausar (após `>= 8 s`) ou sair do Mini Player / PiP.
- **Flags Proxima/SABR:** ativa `html5_enable_proxima`, `html5_sabr_force_proxima`, `yt-player-proxima-pref`, pré-aquecimento de `yt-player-bandwidth` e `<link rel="preconnect">`.

### 4. 🔓 Desbloqueio 4K60 HDR, SABR e Otimizações Nativas do Cobalt
- **Limites reais de hardware configuráveis no menu:** teto ajustável para **AV1** (padrão: `40 Mbps`) e **VP9/AVC/HEVC** (padrão: `100 Mbps`) + clamp seguro em probes sintéticos de `isTypeSupported` / `decodingInfo` (`35M–250M → 35M`).
- **Fallback VP9 autenticado (`WEB` / `TVHTML5_SIMPLY`):** busca metadados suplementares autenticados com PO token sem interromper a reprodução quando a sessão TV omite faixas VP9 em `2160p`/`1440p`/`1080p`.
- **Otimizações nativas (`JavaSwitches` & `MediaCodecBridge`):**
  - `EnableQUIC` e `DisableLowEndDeviceMode` ativos
  - `ForceGpuMemAvailableMb = 256` MB e `V8MaxOldSpaceSize = 768` MB
  - `CobaltDynamicMojoPipeSizing` ampliado (`media_size = 2 MB`, `subresource_size = 512 KB`) + `CobaltBypassResourceLoadScheduler`
  - `MediaFormat.KEY_LOW_LATENCY = 1` em `MediaCodecBridge.configureVideo` quando suportado pelos decoders MediaTek (`c2.mtk.av1.decoder`, `c2.mtk.vp9.decoder`, `c2.mtk.avc.decoder`)

---

## 🛠️ Recursos Adicionais Integrados

- 🛑 **Ad Blocker**
- ❗ **SponsorBlock**
- ⏭️ **Controle de velocidade**
- 🔺 **[DeArrow](https://dearrow.ajay.app/)**

---

## ⬇️ Download (Releases Oficiais)

- 👉 **[TubeRush `v2.1.4-c7k-l1` — Releases](https://github.com/HeliumMarcos/TubeRush/releases/latest)**

> 💡 **Arquitetura:** `armeabi-v7a` (`qa`), validado na **TCL C7K (Android 14 / MT5896)** em `2160p60 HDR10` e transmissões ao vivo com baixa latência e estabilidade.

## ❓ Como instalar

1. Baixe `TizenTube-L1-arm.apk` na página de [Releases](https://github.com/HeliumMarcos/TubeRush/releases).
2. Instale na TV via gerenciador de arquivos ou ADB (`adb install -r TizenTube-L1-arm.apk`).
3. Abra o app **TubeRush**.

---

## 🙏 Créditos e Estrutura do Repositório

- **Branch `main`:** código principal unificado do **TubeRush** (`u.js`, `cobalt/`, `starboard/`, `scripts/`, `docs/`, `.github/` e `README.md`), com CI automatizado (`52/52` testes unitários + purge jsDelivr).
- **Branch `cobalt-full`:** árvore original completa do monorepo Chromium/Cobalt para compilações C++ nativas.
- Desenvolvido e mantido por **Helium Marcos (L1)** — baseado no motor [Google Cobalt (`27.lts.10`)](https://cobalt.dev).
