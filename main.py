from requests import get
from parsel   import Selector
from smtplib  import SMTP, SMTPException
from CONFIG   import HEADER, MAIL_ADDR, MAIL_PASS, RECIEVER
from schedule import every, run_pending, repeat

URL   = None
if not URL:
        URL = input('Urun linkini giriniz : ')

FISRTPRICE = None

def check_first_price()->None:
    
    global URL, FISRTPRICE

    product_page = get(URL, headers=HEADER)
    select       = Selector(product_page.text)

    title = select.xpath("normalize-space(//*[contains(@id, 'product-name')])").get()
    print(f"\n{title}")

    FISRTPRICE = float(select.xpath("//*[contains(@id, 'offering-price')]/@content").get())
    print(FISRTPRICE)

@repeat(every(1).hours)
def check_price() -> None:
    global URL, DEGER
    product_page = get(URL, headers=HEADER)
    select       = Selector(product_page.text)
    price = float(select.xpath("//*[contains(@id, 'offering-price')]/@content").get())
    print(price)

    if (price < FISRTPRICE):
        send_mail(title, price)

def send_mail(product:str, price:float) -> None:

    try:
        mail_server = SMTP('smtp.gmail.com', 587, timeout=60)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login(MAIL_ADDR, MAIL_PASS)

        subject = f"{product} Urun Fiyat Dustu. Yeni Fiyat : {price}"
        body    = f"Urune bu linkten gidebilirsin => {URL}"
        content = f"To:{RECIEVER}\nFrom:{MAIL_ADDR}\nSubject:{subject}\n\n{body}"

        mail_server.sendmail(MAIL_ADDR, RECIEVER, content)

        print('Mail Gonderildi!')
    except SMTPException as e:
        print(e)
    finally:
        mail_server.quit()

if not FISRTPRICE:
    check_first_price()

while True:
    run_pending()