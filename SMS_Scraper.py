from bs4 import BeautifulSoup
import urllib2
import pandas as pd

with open("smsData.csv", "wb") as sms:

    # page scraped: 122-376
    n = 122
    while n < 376:
        soup = BeautifulSoup(urllib2.urlopen("http://laporsms.com/laporan-masyarakat/index.php?r=site/index&Sms_page=" + str(n)).read(), "lxml")
        n += 1
        table = soup.find('table')

        # generate lists
        type_ = []
        content_ = []
        submitted_ = []
        received_ = []
        sender_ = []

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            if len(cells) == 5:
                type_.append(cells[0].find(text=True))
                content_.append(cells[1].find(text=True))
                submitted_.append(cells[2].find(text=True))
                received_.append(cells[3].find(text=True))
                sender_.append(cells[4].find(text=True))

        smsData = pd.DataFrame(type_, columns=['type'])
        smsData['content'] = content_
        smsData['submitted'] = submitted_
        smsData['received'] = received_
        smsData['sender'] = sender_
        # start the index from 1 not 0
        smsData.index += 1
        # write to csv file
        smsData.append(smsData, ignore_index=True).to_csv(sms, header=False)
        # print smsData
