from windows_toasts import InteractableWindowsToaster, Toast, ToastImage, ToastDisplayImage, ToastImagePosition
from windows_toasts import ToastProgressBar, ToastDuration, ToastSystemButtonAction, ToastSystemButton
from windows_toasts import ToastButton, ToastSelection, ToastInputSelectionBox,ToastScenario
import aladhan
import customtkinter as ctk
from datetime import datetime, timedelta
import time

def updateWindow(root):

    title_label = ctk.CTkLabel(root, text="Prayer App", font=ctk.CTkFont(size=30, weight="bold"))
    title_label.pack(padx = 10, pady = (40,20))

    scrollableInterface = ctk.CTkScrollableFrame(root, width=500, height=400)
    scrollableInterface.pack(padx = 10, pady = 10)

    root.mainloop()


def calcalateEverything(addy):

    nextPrayerToCurrentPrayer = {
        "Fajr": "Isha",
        "Dhuhr": "Fajr",
        "Asr": "Dhuhr",
        "Maghrib": "Asr",
        "Isha": "Maghrib"
    }

    today = datetime.today()
    yesterday = today - timedelta(1)

    year = aladhan.CalendarDateArg(2023)

    a = aladhan.Client()
    timings: aladhan.Timings = a.get_calendar_by_address(addy, year)
    
    todaytt = False

    for p in timings[str(yesterday.month)][yesterday.day].prayers_only.values():
        if p.time >= today:
            todaytt = True
            nextPrayerName = p.name
            nextPrayerTime = p.time
            
            currentPrayerName = nextPrayerToCurrentPrayer[p.name]
            
            if p.name == "Dhuhr":
                currentPrayerName = "Sunrise"
                sunriseTime = timings[str(yesterday.month)][yesterday.day].sunrise.time # sunrise time
                if sunriseTime > today:
                    currentPrayerName = "Fajr"

            break

    if todaytt == False:
        currentPrayerName = "Isha"
        nextPrayerName = "Fajr"
        nextPrayerTime = timings[str(today.month)][today.day].fajr.time
    
    # print("calculations = ", currentPrayerName, nextPrayerName, nextPrayerTime)

    return currentPrayerName, nextPrayerName, nextPrayerTime


def timeDiffCalc(Nexttime):
    today = datetime.today()
    remain = Nexttime - today
    h, m = remain.seconds//3600, (remain.seconds//60)%60 + 1
    # print("Time left : ", h, m)
    return h, m


def SendNotif3(currentPrayerName, nextPrayerName, nextPrayerTime, h,m):
    # print("Sending Notif 3:", h, m)
    nextPrayerTime = nextPrayerTime.strftime("%#I:%M %p")

    toaster = InteractableWindowsToaster('Prayer Reminder', "PrayerNotifications")
    newToast = Toast()
    strTimeLeft = ""
    if h == 1:
        strTimeLeft += "1 Hour"
    elif h > 1:
        strTimeLeft += f"{int(h)} Hours"
    if h >= 1 and m >= 1:
        strTimeLeft += " and "
    if m >= 1:
        strTimeLeft += f"{int(m)} Minutes"
    newToast.text_fields = ["Current Prayer: " + currentPrayerName, "Next Prayer is " + nextPrayerName + " in " + strTimeLeft + " at " + nextPrayerTime]

    logo = ToastImage("C:/Users/Administrator/Documents/PrayerNotif/LOGO.png")
    image = ToastDisplayImage(logo, position=ToastImagePosition.AppLogo )
    newToast.AddImage(image)

    toaster.show_toast(newToast)


def SendNotif2(currentPrayer, nextPrayerName, nextPrayerTime, h, m):
    nextPrayerTime = nextPrayerTime.strftime("%#I:%M %p")

    toaster = InteractableWindowsToaster('Prayer Reminder', "PrayerNotifications")
    newToast = Toast()
    strTimeLeft = ""
    if h == 1:
        strTimeLeft += "1 Hour"
    elif h > 1:
        strTimeLeft += f"{int(h)} Hours"
    if h >= 1 and m >= 1:
        strTimeLeft += " and "
    if m >= 1:
        strTimeLeft += f"{int(m)} Minutes"

    logo = ToastImage("C:/Users/Administrator/Documents/PrayerNotif/LOGO.png")
    image = ToastDisplayImage(logo, position=ToastImagePosition.AppLogo )
    newToast.AddImage(image)
    
    newToast.text_fields = [currentPrayer + " " + strTimeLeft + " Left", strTimeLeft + " till " + nextPrayerName + " (" + nextPrayerTime + ")"]
    toaster.show_toast(newToast)   


def SendNotif1(currentPrayerName, nextPrayerName, nextPrayerTime, timeDiffHours, timeDiffMins):
    nextPrayerTime = nextPrayerTime.strftime("%#I:%M %p")

    toaster = InteractableWindowsToaster('Prayer Reminder', "PrayerNotifications")
    newToast = Toast()

    logo = ToastImage("C:/Users/Administrator/Documents/PrayerNotif/LOGO.png")
    image = ToastDisplayImage(logo, position=ToastImagePosition.AppLogo )
    newToast.AddImage(image)

    # newToast.launch_action = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    newToast.scenario = ToastScenario.Reminder

    selections = (ToastSelection('10', '10 minute'), ToastSelection('5', '5 minutes'), ToastSelection('1', '1 minute'))
    selectionBox = ToastInputSelectionBox(
        'snoozeBox', caption='Snooze duration', selections=selections, default_selection=selections[0]
    )
    newToast.AddInput(selectionBox)

    snoozeButton = ToastSystemButton(ToastSystemButtonAction.Snooze, 'Remind Me Later', relatedInput=selectionBox)
    dismissBox = ToastSystemButton(ToastSystemButtonAction.Dismiss)
    newToast.AddAction(snoozeButton)
    newToast.AddAction(dismissBox)

    # newToast.AddAction(ToastSystemButton(ToastSystemButtonAction.Dismiss, "dismiss"))

    # newToast.AddAction(ToastButton("InshAllah"))
    
    newToast.progress_bar = ToastProgressBar(status="Time Left", progress=.6, progress_override=f"{int(timeDiffMins)} minutes")
    
    newToast.text_fields = ["Current Prayer: " + currentPrayerName, "Next Prayer is " + nextPrayerName + " in " + f"{int(timeDiffHours)} hours and {int(timeDiffMins)} minutes" + " at " + nextPrayerTime]
    toaster.show_toast(newToast)


def main():
    addy = "atlanta, ga, usa"
    currentPrayerName, nextPrayerName, nextPrayerTime = calcalateEverything(addy)

    h, m = timeDiffCalc(nextPrayerTime)

    SendNotif1(currentPrayerName, nextPrayerName, nextPrayerTime, h, m)

    root = ctk.CTk()

    root.geometry("750x500")
    root.title("Prayer App")
    root.iconbitmap("logo.ico")

    # updateWindow(root)

    
    while True:
        time.sleep(60)

        currentPrayerName, nextPrayerName, nextPrayerTime = calcalateEverything(addy)
        
        h, m = timeDiffCalc(nextPrayerTime)

        if h == 1 and m == 0:
            SendNotif2(currentPrayerName, nextPrayerName, nextPrayerTime, h, m)

        if h == 0 and m == 30:
            SendNotif2(currentPrayerName, nextPrayerName, nextPrayerTime, h, m)

        if h == 0 and m == 10:
            SendNotif2(currentPrayerName, nextPrayerName, nextPrayerTime, h, m)

        if h == 0 and m == 5:
            SendNotif2(currentPrayerName, nextPrayerName, nextPrayerTime, h, m)

        if h == 0 and m == 1:
            """
            print("Sending Notif 3 m = 1")
            currentPrayerName, nextPrayerName, nextPrayerTime = calcalateEverything(addy)
            SendNotif3(currentPrayerName, nextPrayerName, nextPrayerTime, h,m)
            """
            time.sleep(60)
            currentPrayerName, nextPrayerName, nextPrayerTime = calcalateEverything(addy)
            h, m = timeDiffCalc(nextPrayerTime)

            SendNotif3(currentPrayerName, nextPrayerName, nextPrayerTime, h,m)  
        """
        if h == 0 and m == 0:
            print("Sending Notif 3 m = 0")
            currentPrayerName, nextPrayerName, nextPrayerTime = calcalateEverything(addy)
            SendNotif3(currentPrayerName, nextPrayerName, nextPrayerTime, h,m)
            time.sleep(60)
            currentPrayerName, nextPrayerName, nextPrayerTime = calcalateEverything(addy)
            h, m = timeDiffCalc(nextPrayerTime)
            SendNotif3(currentPrayerName, nextPrayerName, nextPrayerTime, h,m)
        """
    

if __name__ == "__main__":
    main()