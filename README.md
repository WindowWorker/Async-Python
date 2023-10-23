# Async Python Reverse Proxy

This project is part of a personal effort to get a better understanding of certain programming languages.
I have found one of the best ways to get a good feel for an unfamiliar lqnguage is to build a reverse proxy ysing only the standard library. 
It had been a while since I really used Python so I did this as a sort of refresher.
This reverse proxy is pounted at the Python official site. 
You can see the end result here:

[https://python.patrickring.net](https://python.patrickring.net)

Some additional requirements that I gave myself are to try and emulate promises as used in JavaScript using asyncio and to wrap every method that interacted with io to be wrapped in sync.
