from zignaly import checkAndBuy
from apscheduler.schedulers.blocking import BlockingScheduler

times = 0
selling = False
boughtAt = 1000000000
def z_fn():
    global times
    global selling
    global boughtAt
    res = checkAndBuy(times, selling, boughtAt)
    times = res[0] + 2
    selling = res[1]
    boughtAt = res[2]


scheduler = BlockingScheduler()
# scheduler.add_job(fn, 'interval', seconds=4)
scheduler.add_job(fn, 'interval', seconds=61)
scheduler.start()
fn()
