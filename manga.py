import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def baixar_manga_por_varredura(url_da_pagina, pasta_destino):
    # 1. Configuração de Headers para evitar bloqueios
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://mangalivre.to/"
    }

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    try:
        # 2. Pega o conteúdo HTML da página do capítulo
        print(f"Acedendo a: {url_da_pagina}")
        response = requests.get(url_da_pagina, headers=headers)
        response.raise_for_status() # Verifica se a página carregou com sucesso
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Procura por imagens dentro da classe 'page-break'
        # O seletor '.page-break img' procura todas as tags <img> dentro de elementos com classe 'page-break'
        imagens = soup.select('.page-break img')
        
        if not imagens:
            print("Nenhuma imagem encontrada com a classe 'page-break'. Verifique se a estrutura do site mudou.")
            return

        print(f"Encontradas {len(imagens)} imagens. A iniciar download...")

        for index, img in enumerate(imagens):
            # Tenta pegar o link da imagem (pode estar no 'src' ou as vezes em 'data-src')
            url_img = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            
            if not url_img:
                continue

            # Limpa espaços em branco e garante que a URL está completa
            url_img = url_img.strip()
            if url_img.startswith('//'):
                url_img = 'https:' + url_img
            
            # Define o nome do arquivo local (001.webp, 002.webp...)
            extensao = url_img.split('.')[-1].split('?')[0] # Pega a extensão (webp, jpg, etc)
            nome_arquivo = f"{index + 1:03d}.{extensao}"
            caminho_completo = os.path.join(pasta_destino, nome_arquivo)

            # 4. Faz o download da imagem real
            try:
                img_data = requests.get(url_img, headers=headers).content
                with open(caminho_completo, 'wb') as f:
                    f.write(img_data)
                print(f" Baixado: {nome_arquivo}")
            except Exception as e:
                print(f" Erro ao baixar a imagem {index+1}: {e}")

        print("\nDownload concluído!")

    except Exception as e:
        print(f"Erro ao aceder à página: {e}")

# --- EXECUÇÃO ---
# Substitua pela URL da PÁGINA onde você lê o mangá, não o link direto da imagem.
url_capitulo_site = "https://mangalivre.to/manga/chainsaw-man-pt-br/capitulo-14" 
baixar_manga_por_varredura(url_capitulo_site, "manga_baixado")