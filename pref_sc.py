from prefect import flow, task
from scrap_smlab import scrap_smlab
from prefect.schedules import Interval
from datetime import timedelta, datetime

@task(retries=3, name="Scraping SM Lab IMOEX")
def smscr():
    scrap_smlab()

@flow
def go_run():
    smscr()

if __name__ == "__main__":
    go_run.serve(schedule=Interval(timedelta(minutes=5)))