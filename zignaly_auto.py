from zignaly import checkAndBuy
from apscheduler.schedulers.blocking import BlockingScheduler

times = 0
selling = False
def fn():
    global times
    global selling
    res = checkAndBuy(times, selling)
    times = res[0] + 2
    selling = res[1]


scheduler = BlockingScheduler()
# scheduler.add_job(fn, 'interval', seconds=4)
scheduler.add_job(fn, 'interval', seconds=61)
scheduler.start()
fn()