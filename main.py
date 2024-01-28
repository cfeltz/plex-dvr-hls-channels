from common.grabber import Grabber

def main():

    grabber = Grabber()
    grabber.load_config('configs/config.json')

    grabber.load_web_config()

    grabber.do_work()

    print("fortnite")


if __name__ == '__main__':
    main()
