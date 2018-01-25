# SOAForPython

---

## project structure
----
#### server side

+ core engine, service engine, watcher engine
+ each service have one service process start by service engine, one watcher thread start by watcher engine
+ service pre work build by core engine
+ each service have param template, define it's detail, template must can be pickled

#### develop side

+ can rewrite 3 callback about watcher:
  + file_change_callback : it's be called every interval and return a service instance & work path's file list
  + before_watch_callback : it's be called before watcher thread be started.
  + after_watch_callback : it's be called when watcher thread will be stopped. 
+ 2 can rewrite 2 method about service
  + build : it's be call in core, it's do pre work before start service
  + prepare_input_file : it's be called after build, and it's prepare file that service need

#### user side

+ can make a param template extends ServiceParamTemplate
+ can add new attributes in ServiceParamTemplate (develop side can use them)

----

+ server side and user side is process isolation, core always running, developer make handler / service, core reload that two packages, and new version be built  

---

## UserGuide:

+ extend WatcherHandler / ServiceProgramTemplate
  + src.hander, src.service are two examples
+ start core
  + src.start_core.py
+ send ServiceParamTemplate class by redis
  + core.test.src 
+ service will start and running like you define in your child classes
  + core.test.plugin have a service example, it's develop by other, we can not see / control / change / hook

+ this framework can develop service's (develop by other) handler / callback quickly, call them simply.

## About Data Stream

+ data stream include two types, out of work path or in work path
+ for example
    + get a file in ftp or other (out of work path), you can write code in service.prepare_input_file
    + upload result file (out of work path), you can write code in after_watcher_callback
+ notice that all callback & service's build and prepare_input_file in same work path, so make file name in param template, them will see each other
+ if here have a complicated example:
```buildoutcfg
serviceA -> data -> ServiceB -> data -> condition no pass-> serviceA -> data -> .... -> serviceB -> data -> pass
```
+ in this case, service need data from other, and have condition & loop, how do we solve that?
  + advice 1: if all services in same work path, just make this logical as a .py file, and this .py file as service be called
  + advice 2: if all services in different work path, think about this:
    1. services send one by one, from client to server
    2. every service called have a result
    + so you know, service's sequence control in client is better than server, like client receive a service result notification, and decide start next or return prev.

+ this frame don't support any data interface now, you need make them by your self, and call them in callback or service.prepare_build_file
+ all service's state you can changed in file_change_callback, it's in redis, you can get it any where, and do what you want.

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


## If you don't make sure you need this repo or not, you can see this:

+ our system have a lots of service, and it's hard to manage.
+ service is other's program, we only can run it.
+ before service start, we need make dir, copy exe, get input files
+ services between them is same, they just run use input, and have some output files.
+ our system concern how to know service's progress and data recycle
+ service maybe delay on each other, it's make a very complicated data stream

this system is a small, pure and clear core, to make developer add new service simply, 
finally, developer only code some callback, fill template, and all services running on themselves way


