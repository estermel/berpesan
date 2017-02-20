from bs4 import BeautifulSoup
import urllib2
import pandas as pd

with open("DataSMS.csv", "wb") as sms:

    # page scraped: 131-383
    i = 131
    n = 385
    while i < n:
        soup = BeautifulSoup(urllib2.urlopen("http://laporsms.com/laporan-masyarakat/index.php?r=site/index&Sms_page="+str(i)).read(), "lxml")
        table = soup.find('table')
        i += 1
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
        smsData.index += 1
        smsData.append(smsData, ignore_index=True)
        smsData.to_csv(sms, header=False)
        # print smsData
