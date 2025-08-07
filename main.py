from bs4 import BeautifulSoup
import lxml, requests
from dotenv import load_dotenv
import smtplib, os

port = 587

headers = {

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",

}

url ="https://www.amazon.com/Apple-Generation-Cancelling-Transparency-Personalized/dp/B0BDHWDR12/?_encoding=UTF8&pd_rd_w=DVhtg&content-id=amzn1.sym.d7921927-1bbc-4dfe-a747-3f025a69edd0&pf_rd_p=d7921927-1bbc-4dfe-a747-3f025a69edd0&pf_rd_r=AQC999XB1KM45W5N2D16&pd_rd_wg=RiIFH&pd_rd_r=9f0727c4-c566-40d8-8b64-290dc06e4546&ref_=pd_hp_d_btf_fabric-cecml-prisma"
response = requests.get(url=url, headers=headers)
load_dotenv()
# print(response.text)

soup = BeautifulSoup(response.text, "lxml")

whole = soup.find("span", class_="a-price-whole").get_text()
fraction =soup.find("span", class_="a-price-fraction").get_text()
current_amount = float(whole) + float(fraction)/100
threshold_amount = 200.0
# print(current_amount)

if current_amount<threshold_amount:

    server = smtplib.SMTP(os.getenv("SMTP_ADDRESS"), port)
    server.starttls()
    server.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))

    from_address = os.getenv("EMAIL_ADDRESS")
    to_address = os.getenv("EMAIL_ADDRESS")
    subject = "Amazon Price Tracker Alert"
    body = (f"Hello, the price  of Airpods Pro is now ${current_amount}.\n"
            f"The link to buy: {url}")
    email = f"Subject: {subject}\n\n{body}"

    server.sendmail(from_address, to_address, email)
    server.quit()