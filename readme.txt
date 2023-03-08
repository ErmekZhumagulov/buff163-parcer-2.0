Before using parcer do this:
	Downloads needed:
		py -m pip install selenium
		py -m pip install CurrencyConverter
		py -m pip install PyQt6
	Troubleshooting:
		run code in VS Code to see the errors (to see what version of chromedrive do you need)
		download that version of chromedrive that chrome version do you use
	auto py to exe:
		download it from github
		additional files -> add folder (C:\Users\epicm\AppData\Local\Programs\Python\Python310\Lib\site-packages\currency_converter)

Need to do to run parcer:
	1) open cmd and write:
		cd C:\Program Files\Google\Chrome\Application
		(it is path to installed google chrome in your pc)
	2) then:
		chrome.exe --remote-debugging-port=8989 --user-data-dir="E:\working-folder\buff163-parcer-2\AutomationProfile"
		(change path to yours, where is your downloaded folder,
		for ex.: "D:\work\buff163-parcer-2\" and + name of folder which will be created(name you choose yourself))
	3) in opened browser login buff163
	4) now you can run parcer.py (parcer.exe)
