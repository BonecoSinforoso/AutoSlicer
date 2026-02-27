# ✂️ Auto Sprite Slicer

Auto Sprite Slicer é uma ferramenta simples para fatiar automaticamente uma spritesheet em várias sprites individuais.  
Você só abre a imagem, clica em **Slice** e ele salva cada sprite detectada em arquivos separados.

## 🖼️ Como funciona

O Auto Sprite Slicer detecta "ilhas" de conteúdo na imagem (componentes conectados), calcula o *bounding box* de cada uma e exporta cada sprite como PNG.

Compatível com:
- ✅ **PNG com fundo transparente (alpha = 0)** — funciona com arte de qualquer cor, inclusive **branca**
- ✅ **JPEG / PNG sem alpha** — tenta detectar o fundo pela cor do pixel no canto superior esquerdo

## 🚀 Como usar

### Modo GUI (interface)
```bash
python AutoSlicer.py
```

1. Clique em **📂 Abrir Imagem** e selecione a spritesheet
2. Clique em **✂️ Fatiar!**
3. As sprites serão salvas em `sprites_output/`

### Modo CLI (sem GUI)
```bash
python AutoSlicer.py minha_spritesheet.png
```

## 📦 Requisitos

```bash
pip install pillow scipy
```

- Python 3.8+ recomendado
- Tkinter normalmente já vem com a instalação padrão do Python

## ⚙️ Configurações

Edite as constantes no topo do arquivo:

| Parâmetro | O que faz | Padrão |
|---|---|---|
| `ALPHA_THRESHOLD` | Alpha mínimo para considerar como conteúdo | `32` |
| `PADDING` | Margem extra (px) ao redor de cada sprite | `2` |
| `OUTPUT_DIR` | Pasta de saída | `sprites_output` |

## 📁 Saída

Os arquivos são gerados como:
- `sprite_001.png`
- `sprite_002.png`
- ...

Dentro da pasta `sprites_output/`, preservando RGBA quando disponível.

## 🏗️ Gerar executável (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed AutoSlicer.py
```

O executável vai aparecer em `dist/`.

## 📄 Licença

MIT — veja o arquivo [LICENSE](LICENSE).
