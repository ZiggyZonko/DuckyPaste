from win10toast import *

def show_notification(toaster, title, message):
    toaster.show_toast(
        title,
        message,
        duration=2,
        threaded=True
    )