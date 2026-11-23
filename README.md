# 🚀 TubeRush

<p align="center">
  <img src=".github/assets/TubeRush%20Banner.png" alt="TubeRush — banner oficial do projeto" width="860">
</p>

**YouTube na TV, do seu jeito.**

Cliente alternativo do YouTube TV para **Android TV / Google TV**, baseado no **Google Cobalt** e no projeto [TizenTubeCobalt](https://github.com/reisxd/TizenTubeCobalt), com foco em **4K60, HDR, seleção de codecs, áudio multicanal e baixa latência em transmissões ao vivo**.

[![Última versão](https://img.shields.io/github/v/release/HeliumMarcos/TubeRush?label=Vers%C3%A3o)](https://github.com/HeliumMarcos/TubeRush/releases/latest) [![Downloads](https://img.shields.io/github/downloads/HeliumMarcos/TubeRush/total?label=Downloads)](https://github.com/HeliumMarcos/TubeRush/releases) [![Issues](https://img.shields.io/github/issues/HeliumMarcos/TubeRush)](https://github.com/HeliumMarcos/TubeRush/issues)

**[⬇️ Baixar APK](https://github.com/HeliumMarcos/TubeRush/releases/latest)** · **[📋 Versões](https://github.com/HeliumMarcos/TubeRush/releases)** · **[🛠️ Código-fonte](https://github.com/HeliumMarcos/TubeRush)** · **[🐛 Reportar problema](https://github.com/HeliumMarcos/TubeRush/issues)**

> **Ambiente principal de desenvolvimento e testes:** TCL C7K (Android 14 / MediaTek MT5896). A disponibilidade de formatos e a estabilidade variam conforme o dispositivo, o vídeo, o decodificador e a versão do YouTube TV.

## ✨ Principais recursos

| Área | Recursos |
| --- | --- |
| **Vídeo** | Seleção de representações 2160p, 1440p, 1080p e inferiores, conforme disponibilidade; codecs AV1, VP9 e AVC/H.264; identificação de FPS, HDR e bitrate |
| **Qualidade** | Menu multi-codec e indicação da representação em reprodução; classificação por qualidade e bitrate efetivo |
| **Limites de bitrate** | Valores padrão configurados de **40 Mbps para AV1** e **100 Mbps para VP9/AVC/HEVC**, sujeitos à compatibilidade do hardware |
| **Fallback** | Estratégias de busca e seleção de representações alternativas quando a qualidade preferida não está disponível |
| **Áudio** | Seleção de faixas e suporte a Dolby Digital Plus (E-AC-3) e Dolby Digital (AC-3), quando oferecidos pelo conteúdo e suportados pela saída de áudio |
| **Lives** | Perfis de latência **Equilibrado**, **Baixa Latência** e **Padrão do YouTube**; ajustes adaptativos de buffer e proteção contra perda sustentada de quadros |
| **Interface** | Menus e configurações do TubeRush em português brasileiro |
| **Extras** | Recursos derivados do projeto original, como bloqueio de anúncios, SponsorBlock, DeArrow e controle de velocidade, sujeitos à compatibilidade |
| **Atualizações** | Integração com os Releases do TubeRush para consultar novas versões |

### 🎬 Vídeo e qualidade

A seleção multi-codec procura apresentar as representações efetivamente descobertas para cada vídeo, com resolução, FPS, HDR, codec e bitrate. O algoritmo de qualidade utiliza **effectiveBitrate** para comparar alternativas e considera características do formato e do conteúdo.

Os limites configurados representam critérios de seleção e **não garantem** que todo fluxo dentro do limite será decodificado. Alguns formatos dependem de manifestos, sessão, autenticação e suporte do player. A descoberta de faixas adicionais por **SABR / Proxima** e mecanismos de fallback continua sujeita a testes práticos.

### 🔊 Áudio

O TubeRush busca oferecer controle sobre as faixas disponíveis, incluindo **DD+ (E-AC-3)** e **DD (AC-3)**. A reprodução multicanal depende da faixa disponibilizada pelo YouTube, do dispositivo e da configuração de passthrough/saída de áudio. A troca entre codecs e idiomas deve ser validada em cada ambiente.

### 🔴 Transmissões ao vivo

O perfil **Equilibrado (Mais estável)** é a preferência padrão a partir da versão `v2.1.4` (mantido na `v2.1.5`). Há também opções de menor latência e de comportamento padrão do YouTube. O controlador procura reduzir atrasos sem comprometer a fluidez, mas a latência real depende da transmissão e da rede.

## ⬇️ Instalação

1. Acesse **[Releases — versão mais recente (`v2.1.5-c7k-l1`)](https://github.com/HeliumMarcos/TubeRush/releases/latest)**.
2. Baixe o APK `TubeRush-armv7.apk` (arquitetura ARMv7 / `armeabi-v7a`).
3. Instale o APK pelo gerenciador de arquivos da TV ou via ADB, autorizando a instalação quando necessário.
4. Abra o **TubeRush** e configure suas preferências.

Exemplo de instalação via ADB:

```bash
adb install -r TubeRush-armv7.apk
```

> Confira sempre os **Assets** da versão escolhida. A instalação com `-r` depende da compatibilidade da assinatura e do identificador do pacote já instalado.

## 🧩 Compatibilidade e validação

**Dispositivo de referência:** TCL C7K com Android 14 e chipset MediaTek MT5896; testes de áudio com soundbar LG S95TR.

A presença de **4K60, HDR, AV1, VP9 ou DD+** no menu não constitui garantia de reprodução em qualquer aparelho. Os resultados dependem do vídeo, da sessão do YouTube, do codec, do perfil de mídia, do decoder e da conexão. Funcionalidades como fallback de formatos, alternância de áudio e estabilidade de lives devem continuar sendo verificadas em testes reais.

## 🗂️ Estrutura do repositório

A branch `main` contém as seguintes entradas principais:

```text
.github/     Automação e workflows
cobalt/      Motor Cobalt e integração de reprodução
docs/        Documentação técnica
scripts/     Scripts e ferramentas auxiliares
starboard/   Integração com a plataforma
u.js         Personalizações do cliente
README.md    Apresentação do projeto
```

A documentação técnica herdada do Cobalt está em [`docs/`](docs/). Consulte [GitHub Actions](https://github.com/HeliumMarcos/TubeRush/actions) para o estado das compilações e dos testes; não presuma que um build foi aprovado sem verificar a execução correspondente.

## 🛠️ Desenvolvimento e contribuições

O código-fonte está disponível na branch [`main`](https://github.com/HeliumMarcos/TubeRush/tree/main). Para relatar falhas, inclua versão do APK, modelo da TV, versão do Android, vídeo de referência, codec e passos para reproduzir o problema em [Issues](https://github.com/HeliumMarcos/TubeRush/issues).

## 🙏 Créditos e licenças

**TubeRush** é uma personalização independente mantida por **HeliumMarcos (L1)**, baseada em [TizenTubeCobalt](https://github.com/reisxd/TizenTubeCobalt), [TizenTube](https://github.com/reisxd/TizenTube) e [Google Cobalt](https://cobalt.dev), além de componentes Chromium e outras dependências de código aberto. As licenças e os direitos dos componentes originais permanecem com seus respectivos autores.

**TubeRush não é um aplicativo oficial do YouTube nem do Google.**
