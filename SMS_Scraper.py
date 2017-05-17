
from bs4 import BeautifulSoup
import urllib2
import pandas as pd

TrainingOutput = "DataSMS.csv"
TestingOutput = "DataTestSMS.csv"

with open(TestingOutput, "wb") as sms:

    # page scraped: 131-383 (Jun-Nov 2016) AS INITIAL DATA TO BE TRAINED
    # page scraped: 1-50 AS AS TESTING DATA, scraped at: May 17, 2017
    i = 1
    n = 51
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
