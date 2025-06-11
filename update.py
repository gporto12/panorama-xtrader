import requests
from bs4 import BeautifulSoup
from datetime import datetime

def coletar_destaques():
    hoje = datetime.now().strftime('%d/%m/%Y')
    headers = {'User-Agent': 'Mozilla/5.0'}
    fontes = {
        "Investing": "https://br.investing.com/news/",
        "InfoMoney": "https://www.infomoney.com.br/ultimas-noticias/"
    }
    destaques = {}
    for nome, url in fontes.items():
        try:
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            if nome == "Investing":
                noticias = soup.select("a.title")[:5]
            else:
                noticias = soup.select("a.article__title")[:5]
            destaques[nome] = [
                {"titulo": n.text.strip(), "link": n['href']} for n in noticias if n.get('href')
            ]
        except Exception:
            destaques[nome] = [{"titulo": "Erro ao carregar notícias.", "link": "#"}]
    return hoje, destaques

def gerar_html(data, destaques):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang='pt-BR'>
<head><meta charset='UTF-8'><title>Panorama do Dia XTRADER</title></head>
<body style='font-family:sans-serif;background:#101820;color:#f2f2f2;padding:20px;'>
<h1 style='text-align:center;color:#00aaff;'>Panorama do Dia - XTRADER</h1>
<p style='text-align:center;'>{data}</p>
""")
        for fonte, lista in destaques.items():
            f.write(f"<h2 style='color:#00aaff'>{fonte}</h2><ul>")
            for item in lista:
                f.write(f"<li><a href='{item['link']}' style='color:#00aaff;'>{item['titulo']}</a></li>")
            f.write("</ul>")
        f.write("<p style='text-align:center;font-size:0.8em;color:#888'>© XTRADER - Conteúdo automatizado</p></body></html>")

if __name__ == "__main__":
    data, noticias = coletar_destaques()
    gerar_html(data, noticias)