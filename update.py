import requests
from bs4 import BeautifulSoup
from datetime import datetime

def coletar_destaques():
    hoje = datetime.now().strftime('%d/%m/%Y')
    headers = {'User-Agent': 'Mozilla/5.0'}
    fontes = {
        "Investing": "https://br.investing.com/news/economy",
        "InfoMoney": "https://www.infomoney.com.br/ultimas-noticias/"
    }
    destaques = {}

    for nome, url in fontes.items():
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')

            if nome == "Investing":
                noticias = soup.select("a.title")[:5]
            else:
                noticias = soup.select("a.hl-title")[:5]

            destaques[nome] = []
            for n in noticias:
                titulo = n.get_text(strip=True)
                link = n.get('href')
                if link and not link.startswith("http"):
                    if nome == "Investing":
                        link = "https://br.investing.com" + link
                    else:
                        link = "https://www.infomoney.com.br" + link
                destaques[nome].append({"titulo": titulo, "link": link})
        except Exception as e:
            destaques[nome] = [{"titulo": f"Erro ao coletar notícias ({e})", "link": "#"}]

    return hoje, destaques

def gerar_html(data, destaques):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang='pt-BR'>
<head><meta charset='UTF-8'><title>Panorama do Dia XTRADER</title></head>
<body style='font-family:sans-serif;background:#101820;color:#f2f2f2;padding:20px;'>
<div style='text-align:center;'>
  <img src='logo-xtrader.png' alt='Logo XTRADER' height='60'><h1 style='color:#00aaff'>Panorama do Dia - XTRADER</h1><p>{data}</p>
</div>
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