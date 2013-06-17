#simple converter (taken from Screen EventView) with show better 1.ShortDescription or 2.(Short)ExtendedDescription
#by mogli123

from Components.Converter.Converter import Converter
from Components.Element import cached

class EventDescription(Converter, object):
	EVENT_DESCRIPTION = 0
	
	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "Description":
			self.type = self.EVENT_DESCRIPTION

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return ""
			
		if self.type == self.EVENT_DESCRIPTION:
		        name = event.getEventName()
                        short = event.getShortDescription()
  	                extended = event.getExtendedDescription()
                        empty = ""                 # <-- (empty=" ") string: you can now edit this string like -> (empty = "No Description") and it will show that string when "EventName" and "ShortDescription" has both the same info       
                        if short and short != name:         
                                 empty += ""     
                                 return short
                        elif extended:
                                 if len(extended) > 57:
                                         shortextended = extended[ 0 : 55 ]
                                         shortextended += "..."             
                                         return shortextended
                                 elif len(extended) < 57:
                                         shortextended = extended
                                         return shortextended
                        else:
     	                         return empty 
                                      		
	text = property(getText)
