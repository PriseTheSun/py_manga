import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading

def baixar_manga_por_varredura(url_da_pagina, pasta_destino, callback_progresso=None, callback_fim=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://mangalivre.to/"
    }

    try:
        response = requests.get(url_da_pagina, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        imagens = soup.select('.page-break img')
        
        if not imagens:
            if callback_fim:
                callback_fim("Nenhuma imagem encontrada. Verifique a URL.")
            return

        nome_capitulo = extrair_nome_capitulo(url_da_pagina)
        pasta_capitulo = os.path.join(pasta_destino, nome_capitulo)
        
        if not os.path.exists(pasta_capitulo):
            os.makedirs(pasta_capitulo)

        total = len(imagens)
        if callback_progresso:
            callback_progresso(0, total)

        for index, img in enumerate(imagens):
            url_img = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            
            if not url_img:
                continue

            url_img = str(url_img).strip()
            if url_img.startswith('//'):
                url_img = 'https:' + url_img
            
            extensao = url_img.split('.')[-1].split('?')[0]
            nome_arquivo = f"{index + 1:03d}.{extensao}"
            caminho_completo = os.path.join(pasta_capitulo, nome_arquivo)

            try:
                img_data = requests.get(url_img, headers=headers).content
                with open(caminho_completo, 'wb') as f:
                    f.write(img_data)
                if callback_progresso:
                    callback_progresso(index + 1, total)
            except Exception as e:
                print(f" Erro ao baixar: {nome_arquivo}: {e}")

        if callback_fim:
            callback_fim(None)

    except Exception as e:
        if callback_fim:
            callback_fim(f"Erro: {e}")

def extrair_nome_capitulo(url):
    parsed = urlparse(url)
    caminho = parsed.path.rstrip('/')
    partes = caminho.split('/')
    if len(partes) >= 2:
        return partes[-2] + "_" + partes[-1]
    return "capitulo"

class MangaDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manga Downloader")
        self.root.geometry("500x250")
        self.root.resizable(False, False)
        
        self.diretorio_download = os.path.expanduser("~/Downloads")
        
        self.criar_interface()
    
    def criar_interface(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="URL do Capítulo:").pack(anchor=tk.W, pady=(0, 5))
        
        self.entry_url = ttk.Entry(frame, width=50)
        self.entry_url.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text="Diretório de Download:").pack(anchor=tk.W, pady=(0, 5))
        
        frame_dir = ttk.Frame(frame)
        frame_dir.pack(fill=tk.X, pady=(0, 15))
        
        self.label_dir = ttk.Label(frame_dir, text=self.diretorio_download, background="#f0f0f0", relief=tk.SUNKEN, anchor=tk.W)
        self.label_dir.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_pasta = ttk.Button(frame_dir, text="📁", width=5, command=self.selecionar_diretorio)
        btn_pasta.pack(side=tk.RIGHT)
        
        self.btn_baixar = ttk.Button(frame, text="⬇️ Baixar Capítulo", command=self.iniciar_download)
        self.btn_baixar.pack(pady=(0, 10))
        
        self.progress = ttk.Progressbar(frame, mode='determinate')
        self.progress.pack(fill=tk.X)
        
        self.label_status = ttk.Label(frame, text="", foreground="blue")
        self.label_status.pack(pady=(10, 0))
    
    def selecionar_diretorio(self):
        diretorio = filedialog.askdirectory(initialdir=self.diretorio_download)
        if diretorio:
            self.diretorio_download = diretorio
            self.label_dir.config(text=diretorio)
    
    def iniciar_download(self):
        url = self.entry_url.get().strip()
        
        if not url:
            messagebox.showerror("Erro", "Por favor, insira a URL do capítulo")
            return
        
        if not os.path.exists(self.diretorio_download):
            messagebox.showerror("Erro", "Diretório de download inválido")
            return
        
        self.btn_baixar.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.label_status.config(text="Baixando...")
        
        thread = threading.Thread(target=self.executar_download, args=(url,))
        thread.daemon = True
        thread.start()
    
    def executar_download(self, url):
        def progresso(atual, total):
            self.root.after(0, lambda: self.atualizar_progresso(atual, total))
        
        def fim(erro):
            self.root.after(0, lambda: self.finalizar_download(erro))
        
        baixar_manga_por_varredura(url, self.diretorio_download, progresso, fim)
    
    def atualizar_progresso(self, atual, total):
        percentual = (atual / total) * 100
        self.progress['value'] = percentual
        self.label_status.config(text=f"Baixando {atual}/{total} imagens...")
    
    def finalizar_download(self, erro):
        self.btn_baixar.config(state=tk.NORMAL)
        if erro:
            self.label_status.config(text=erro, foreground="red")
            messagebox.showerror("Erro", erro)
        else:
            self.label_status.config(text="Download concluído!", foreground="green")
            messagebox.showinfo("Sucesso", "Capítulo baixado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MangaDownloaderApp(root)
    root.mainloop()
