import requests
from bs4 import BeautifulSoup
import telegram
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

bot = telegram.Bot(token = '1184811565:AAH0_DQbaiQuEeU-48UFn0-OMzNRTc42A-U')

URL = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date="

def today_IMAX_open():
    now = datetime.datetime.now()
    YMD = now.strftime('%Y%m%d')

    todayURL = "{}{}".format(URL, YMD)

    URLrequest = requests.get(todayURL)

    #해당 URL의 HTML 소스를 str형태로 모두 가져옴
    #str형태이므로 .strip() 사용가능

    soup = BeautifulSoup(URLrequest.text, 'html.parser')
    #str형태로 된 URLrequest변수의 내용을 html로서 재해석함.
    #태그, 클래스와 같은 html요소들을 구분해주므로
    #.select(), .find() 등의 메소드를 통해 태그와 클래스 검색 가능

    #imax가 포함된 태그 찾기
    imax = soup.select('div span.imax')

    #태그가 있다면 이름 출력
    if(imax):
        for i in imax:
            imax_title = i.find_parent('div', class_='col-times')
            imax_title = imax_title.select_one('div.info-movie > a > strong')
            message = '{}{}{}'.format('<', imax_title.text.strip(), '> 의 imax 예매가 열렸습니다.')
            bot.sendMessage(chat_id=1215333727, text=message)
            scheduler.pause()

    #사용자id확인방법
    #for i in bot.getUpdates():
    #    print(i.message)


scheduler = BlockingScheduler()
scheduler.add_job(today_IMAX_open, 'interval', seconds=30)
scheduler.start()