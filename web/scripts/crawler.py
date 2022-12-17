from bs4 import BeautifulSoup
import requests
import telegram
from hotdeal.models import Deal
from datetime import datetime,timedelta

response = requests.get(
    "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
)
soup = BeautifulSoup(response.text, "html.parser")
BOT_TOKEN = "5972201615:AAFAb4nrg5r2OISfv0SJhlAYWoDD9SnSwV0"

bot = telegram.Bot(token=BOT_TOKEN)

def run():

    # delete deals older than 3days
    row, _ = Deal.objects.filter(created_at__lte=datetime.now() -
                                     timedelta(minutes=60)).delete()
    print(row, "deals deleted")

    for item in soup.find_all("tr", {'class':["list1","list0"]}):
        try:
            image = item.find("img", class_="thumb_border").get("src")[2:]
            image = "http://" + image
            title = item.find("font", class_="list_title").text
            title = title.strip()
            link = item.find("font", class_="list_title").parent.get("href")
            link = "https://www.ppomppu.co.kr" + link
            reply_count = item.find("span", class_="list_comment2").text
            reply_count = int(reply_count)
            up_count = item.find_all("td")[-2].text
            up_count = up_count.split("-")[0]
            up_count = int(up_count)
            if up_count >= 3:
                if (Deal.objects.filter(link__iexact=link).count() == 0):
                    Deal(image_url = image, title=title, link=link, 
                    reply_count=reply_count, up_count=up_count).save()
                    bot.sendMessage(-1001691296488, '{} {}'.format(title, link))
                # print(image, title, link, reply_count, up_count)
        except Exception as e:
            # print(e);
            continue
