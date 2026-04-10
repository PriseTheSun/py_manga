# 📚 Manga Downloader

Aplicação desktop com interface gráfica para baixar capítulos de mangá a partir de URLs do site **MangaLivre** (`mangalivre.to`).

---

## ✨ Funcionalidades

- Interface gráfica simples e intuitiva (Tkinter)
- Seleção de diretório de download via explorador de arquivos
- Barra de progresso em tempo real durante o download
- Download em thread separada (não trava a interface)
- Organização automática das imagens por capítulo em subpastas
- Suporte a imagens com atributos `src`, `data-src` e `data-lazy-src`

---

## 🛠️ Tecnologias

Este projeto utiliza as seguintes tecnologias e bibliotecas:

- **[Python 3](https://www.python.org/):** Linguagem de programação base.
- **[Tkinter](https://docs.python.org/3/library/tkinter.html):** Toolkit padrão do Python para criação de interfaces gráficas (GUI).
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/):** Biblioteca para extração de dados (scraping) de arquivos HTML.
- **[Requests](https://requests.readthedocs.io/):** Biblioteca HTTP para enviar requisições e baixar conteúdos da web.
- **[Threading](https://docs.python.org/3/library/threading.html):** Módulo para execução de tarefas em segundo plano, mantendo a interface responsiva.
- **[LXML](https://lxml.de/):** Parser de alto desempenho para processamento de HTML e XML.

---

## 🖥️ Pré-requisitos

- **Sistema operacional:** Linux (testado no Ubuntu 24.04)
- **Python:** 3.12+

---

## 🚀 Instalação e Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd py_manga
```

### 2. Instale as dependências do sistema

> Necessário apenas uma vez. Requer senha de administrador (sudo).

```bash
sudo apt-get install -y python3-tk python3-venv python3-pip
```

| Pacote | Motivo |
|---|---|
| `python3-tk` | Interface gráfica (Tkinter) |
| `python3-venv` | Criação do ambiente virtual |
| `python3-pip` | Gerenciador de pacotes Python |

### 3. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as dependências Python

```bash
pip install requests beautifulsoup4 lxml
```

| Pacote | Versão testada | Motivo |
|---|---|---|
| `requests` | 2.33.1 | Requisições HTTP para baixar as páginas e imagens |
| `beautifulsoup4` | 4.14.3 | Scraping do HTML para encontrar as imagens |
| `lxml` | 6.0.3 | Parser HTML rápido usado pelo BeautifulSoup |

---

## ▶️ Como Rodar

### Opção 1 — Com o ambiente virtual ativado

```bash
source venv/bin/activate
python3 manga.py
```

### Opção 2 — Apontando diretamente para o Python do venv

```bash
./venv/bin/python3 manga.py
```

---

## 🧭 Como Usar

1. Abra o aplicativo com um dos comandos acima.
2. Cole a **URL do capítulo** no campo "URL do Capítulo".
   - Exemplo: `https://mangalivre.to/manga/nome-do-manga/capitulo-1`
3. Clique em **📁** para escolher a pasta onde as imagens serão salvas (padrão: `~/Downloads`).
4. Clique em **⬇️ Baixar Capítulo** e aguarde o download terminar.
5. As imagens serão salvas em uma subpasta dentro do diretório escolhido, nomeada automaticamente a partir da URL.

---

## 📁 Estrutura do Projeto

```
py_manga/
├── manga.py        # Script principal com a lógica e a interface
├── venv/           # Ambiente virtual Python (gerado localmente, não versionado)
└── README.md       # Este arquivo
```

---

## 🛠️ Configurando o Interpretador no VS Code

Para que o VS Code reconheça os pacotes instalados no `venv` e elimine os avisos de importação:

1. Pressione `Ctrl+Shift+P`
2. Busque por **"Python: Select Interpreter"**
3. Selecione a opção que aponta para `./venv/bin/python3`

---

## ⚠️ Observações

- O script foi desenvolvido para o site **MangaLivre** (`mangalivre.to`) e depende da estrutura de CSS `.page-break img` para localizar as imagens. Outros sites podem não ser compatíveis sem adaptação.
- Certifique-se de ter uma conexão estável com a internet durante o download.
- O arquivo `venv/` não deve ser commitado no Git. Adicione ao `.gitignore`:

```
venv/
```

---

## ❌ Solução de Problemas

### Erro: `ModuleNotFoundError: No module named 'bs4'`

Se você vir este erro ao tentar rodar `python3 manga.py`, significa que o seu terminal está tentando usar o Python global do sistema em vez do ambiente virtual onde as bibliotecas foram instaladas.

**Solução:**
Certifique-se de ativar o ambiente virtual antes de rodar, ou aponte diretamente para ele:

```bash
# Opção A: Ativar antes
source venv/bin/activate
python3 manga.py

# Opção B: Rodar direto pelo venv
./venv/bin/python3 manga.py
```

---

## 📄 Licença

Projeto para uso pessoal e educacional.
