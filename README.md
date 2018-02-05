# tobus

---

## What's it is ?

this project include two parts, the one of them is 'tobus' module, 
this module make you define a module with redis message bus quickly,
it support 1 to 1, 1 to N message.

other is a service develop frame made by tobus, 
to standardize service's development, and make it's development templated. this project delay redis.


## 'tobus' Usege

### define a module attach to bus

```buildoutcfg
from toBus import ModuleBase

class CoreEngineModule(ModuleBase):

    def __init__(self, redis_ip, redis_port, redis_db, module_name):
        super(CoreEngineModule, self).__init__(redis_ip, redis_port, redis_db, module_name)

    def start(self):
        msg_from_bus = self.recv_queue.get()
        # ...
        self.send_queue.put(msg_to_bus)
```

### define a msg flow in bus

```buildoutcfg
from toBus import BaseMessage
import redis

msg = BaseMessage()
your_class = YourClass()
msg.content = your_class
msg.direction = ['module_name_1', 'module_name_2']
msg.msg_id = '1'
```

### send msg to bus

```buildoutcfg
redis = redis.StrictRedis('localhost', '6379', 0)
redis.lpush('bus', pickle.dumps(msg))
```

### define a bus

```buildoutcfg
from toBus import MsgBus


class CustomMsgBus(MsgBus):

    access_modules = set()

    def __init__(self, redis_ip, redis_port, redis_db):
        super(CustomMsgBus, self).__init__(redis_ip, redis_port, redis_db)

    def start_bus(self):
        self.start()

    def msg_recv_callback(self, msg):
        print msg

    def msg_send_callback(self, msg):
        print msg
```
---

## service develop frame made by tobus


Tips: think about this :
+ you have many services but you can't debug them. 
+ all your work is make these services run on multi computer, 
this frame is help the project like this can develop quickly and make 'services questions about other developer' go away.

finally, make you add new service simply, 
just only code some callback, fill template, 
and all services running on themselves way


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

+ put a exist service to service_module.service_core.service_pool
+ new two py files to service_module.service_core.develop_side's handler and service folder, as a_handler.py and a.py
+ run service_module.service_core.start.py
+ run startall.py in toBusUsege folder
+ run send_msg.py in client folder to test it
    + don not forget change send_msg's ServiceParamTemplate's s_service_name to 'a', and service_path to 'service_pool/a.py'

----


+ this frame don't support any data interface now, you need make them by your self, and call them in callback or service.prepare_build_file
+ all service's state you can changed in file_change_callback, it's in redis, you can get it any where, and do what you want.
