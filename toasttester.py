from win10toast import ToastNotifier

toaster = ToastNotifier()
toaster.show_toast("Updated Filter!","Dont forget to refresh the filter on the options menu.", duration=3, icon_path="chaos.ico")