# cowin-fastapi

This app is meant for sending notification on a webhook and it pools cowin public api every 10 seconds.
I am using telegram bot to send myself notification, you can be as creative as you want with this.


# What is Cowin
Cowin is the goverment vaccination tracking and booking system.

# Features
`Tracks available slots`

`Has a ASYNC call running in the background every 10 secs which check for updates in the response and sends it to user if there's any change (Uses in-memory cache for comparison)`

# API Live and Available on 
http://raulmiascowin.herokuapp.com/

# Swagger Docs inbuilt Using FastAPI
http://raulmiascowin.herokuapp.com/docs

# Telegram Webhook View Example
<img src="https://user-images.githubusercontent.com/58909377/123650172-f59e4500-d847-11eb-89d2-36825621e648.jpg" width="400">
<!-- ![Screenshot_2021-06-23-18-44-00-89](https://user-images.githubusercontent.com/58909377/123650172-f59e4500-d847-11eb-89d2-36825621e648.jpg ) -->
