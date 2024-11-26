import schedule

def run():
    schedule.every().minute.do(print, 'staging test sidecar')
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    run()
