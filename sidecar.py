import schedule
from print import print_service_binding_files

def run():
    schedule.every().minute.do(print_service_binding_files)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    run()
