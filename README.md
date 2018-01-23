# SOAForPython

---

## Notice ! This frame is developing, it's unstable, so do not use it.

---

## What's it is ?

#### This is SOA Frame, Python version. It's a framework to standardize service's development, and make it's development templated. this project delay redis.

---

+ The service, means a program/function/script, with input/output, and all of them make a big system.

+ The system like this, or other complicated state
```
ServiceA -> ServiceB ->
                           ->  ServiceE
ServiceC -> ServiceD ->
```

Data stream is a question this frame try to solve too.

## progress :

+ add template about param / service
+ add core / service / wathcer engine
+ add a example about how to make a simple service

## todo

- add watcher callback
- add Data Persistence Interface
- add truly service and run it
- add user guide


## If you don't make sure you need this repo or not, you can see this:

+ our system have a lots of service, and it's hard to manage.
+ service is other's program, we only can run it.
+ before service start, we need make dir, copy exe, get input files
+ services between them is same, they just run use input, and have some output files.
+ our system concern how to know service's progress and data recycle
+ service maybe delay on each other, it's make a very complicated data stream

this system is a small, pure and clear core, to make developer add new service simply, 
finally, developer only code some callback, fill template, and all services running on themselves way



