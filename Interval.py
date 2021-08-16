class Interval:
   'Common base class for all employees'
   #elements=[]
   def __init__(self):
       self.elements=[]
   def getlen(self):
       return len(self.elements)

   def get(self, index):
       return self.elements[index]
   def append(self, value):
       self.elements.append(value)









