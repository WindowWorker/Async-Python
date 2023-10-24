# Async Python Reverse Proxy

This project is part of a personal effort to get a better understanding of certain programming languages.
I have found one of the best ways to get a good feel for an unfamiliar lqnguage is to build a reverse proxy ysing only the standard library. 
It had been a while since I really used Python so I did this as a sort of refresher.
This reverse proxy is pounted at the Python official site. 
You can see the end result here:

[https://python.patrickring.net](https://python.patrickring.net)

Some additional requirements that I gave myself are to try and emulate promises as used in JavaScript using asyncio and to wrap every method that interacted with io to be wrapped in async.
The project structure is a little strange because itbis setup to deploy both as a standalone server on replit and as a vercel serverless function.
I mostly use replit for testing and vercel as production.

## Lessons Learned
I found out through trial and error that the standard http libraries are not http2 compatible. 
I had to disable all http2 and http3 networking capabilities on the host or else tcp connections would be left open and just hang the server.
I also learned that if I were designing a system, I would not use python to perform this particular function.
while it is easy to enable multithreading between requests, it is difficult to manage asynchronous execution on an individual request level without blocking the whole thread, something JavaScript does by default.
I did cone up with some decent workarounds to do just that but doing a `thread.sleep(0)` for every promise that I create seems like a heavy handed workaround. 
All in all I learned a lot more about how concurrency in Python works that I previously knew. 