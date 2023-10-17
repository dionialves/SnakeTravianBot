import queue 
import threading 
import time 
  
thread_exit_Flag = 0
  
class sample_Thread (threading.Thread): 
   def __init__(self, threadID, name, q): 
      threading.Thread.__init__(self) 
      self.threadID = threadID 
      self.name = name 
      self.q = q 

   def run(self): 
      print ("initializing " + self.name) 
      process_data(self.name, self.q) 
      print ("Exiting " + self.name) 


def process_data(threadName, q): 
   while not thread_exit_Flag: 
      queueLock.acquire() 
      if not workQueue.empty(): 
         data = q.get() 
         queueLock.release() 
         print ("% s processing % s" % (threadName, data)) 
      else: 
         queueLock.release() 
         time.sleep(1) 
  
thread_list = ["Thread-1", "Thread-2", "Thread-3"] 
name_list = ["A", "B", "C", "D", "E"] 
queueLock = threading.Lock() 
workQueue = queue.Queue(10) 
threads = [] 
threadID = 1

for thread_name in thread_list: 
   thread = sample_Thread(threadID, thread_name, workQueue) 
   thread.start() 
   threads.append(thread) 
   threadID += 1
queueLock.acquire() 
for items in name_list: 
   workQueue.put(items) 
  
queueLock.release() 
while not workQueue.empty(): 
   pass
thread_exit_Flag = 1
for t in threads: 
   t.join() 
print ("Exit Main Thread") 