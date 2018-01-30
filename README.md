# SOAForPython

---

## What's it is ?

#### This is SOA Frame, Python version. It's a framework to standardize service's development, and make it's development templated. this project delay redis.

Tips: think about this, you have many services but you can't debug them. 
all your work is make these services run on multi computer, 
and 1 project, 1 group services, many projects waiting you to develop ..., if you make code for every projects, it's will very slow,
this frame is help the project like this can develop quickly and make 'services questions about other developer' go away.

finally, make you add new service simply, just only code some callback, fill template, and all services running on themselves way

---
## use this frame you can get : 

+ service / handler support hot reload
+ process isolation modules
+ more speed of product

---


---

## 'service' mean what ?

+ The service, means a program/function/script, with input/output, and all of them make a big system.

+ The system like this, or other complicated state
```
ServiceA -> ServiceB ->
                           ->  ServiceE
ServiceC -> ServiceD ->
```

---
## DevelopGuide:

+ make new handler / service like develop_side's handler & service packages's classes
  + if your service named 'jack', you need:
      + jack_handler.py and JACKHandler class in it
      + jacktest.py and JACKSERVICE class in it
+ if you need some custom operation, add it to common package, and call them in your handler / service
+ make other's service to service_core.servicepool, like 'jack.py'
now boot this frame by these steps:
    1. run src.start.py
    2. run service_core.start.py
    3. run user_side.src.service_example.py 
        + don't forget make s_service_name as 'jack'!
        + don't forget make service_path as 'servicepool/jack.py'!
and you can see some info print to command

---

## project structure
----
#### server side

+ core engine, service engine
+ each service have one service process start by service engine, one watcher thread start by watcher engine
+ each service need param template, the template define it's detail, template must can be pickled

#### develop side

+ can rewrite 3 callback about watcher:
  + file_change_callback : it's be called every interval and return a service instance & work path's file list
  + before_watch_callback : it's be called before watcher thread be started.
  + after_watch_callback : it's be called when watcher thread will be stopped. 
+ can rewrite 1 method about service
  + prepare_input_file : it's be called after build, and it's prepare file that service need


#### user side

+ can make a param template extends ServiceParamTemplate
+ can add new attributes in ServiceParamTemplate (so develop side can use them)

----

+ server side and user side is process isolation, core always running, developer make handler / service, core reload that two packages, and new version be built  

---


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