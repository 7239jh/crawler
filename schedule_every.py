import schedule
import time 
from autocrawler import crawler               
schedule.every().day.at('16:20').do(crawler)

while True:
    schedule.run_pending()
    time.sleep(2)          