import subprocess

i =1

class Queue:

  def __init__(self):
      self.queue = list()

  def addtoq(self,dataval):
# Insert method to add element
      if dataval not in self.queue:
          self.queue.insert(0,dataval)
          return True
      return False

  def size(self):
      return len(self.queue)
  def removefromq(self):
    if len(self.queue)>0:
      return self.queue.pop()
    return ("No elements in Queue!")

# TheQueue = Queue()
# TheQueue.addtoq("(A,,250)")
# TheQueue.addtoq("(B,,200)")
# TheQueue.addtoq("(C,,150)")

# TheQueue.addtoq("(D,,100)")

# TheQueue.addtoq("(E,,50)")

# print(TheQueue.size())


# while i ==1:
#   if TheQueue.size() > 0:
#     x = TheQueue.removefromq()
#     w = tuple(x)
#     print(w)
    # subprocess.call(["java","-cp","jfugue.jar:.","test",x[1],x[3]])

note1 = ("A",30,250)

note = note1[0]
volume = str((note1[1]/255)*16383)
if note1[2]==50:
  duration = "t"
elif note1[2]==100:
  duration ="s"
elif note1[2]==150:
  duration ="i"
elif note1[2]==200:
  duration ="q"
elif note1[2]==250:
  duration ="h"

subprocess.call(["java","-cp","jfugue.jar:.","test",note,duration,volume])
