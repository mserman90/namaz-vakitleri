@echo off
:: Chrome tarayıcısını Namaz Vakitleri eklentisi yüklü olarak başlatır
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --load-extension="%~dp0chrome-extension" "chrome://extensions"
