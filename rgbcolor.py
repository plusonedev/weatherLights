import datetime
from colour import Color


class RGBColor:
	def __init__(self, locationObject):
		self.location = locationObject
	
	
	def color(self):
		
		if self.location.currentTime > self.location.sunRise and self.location.currentTime <= self.location.midDay:
			quadrant = "Beta"
			color1 = Color("red")
			color2 = Color("yellow")
			quadrantDelta = self.location.midDay - self.location.sunRise
			quadrantEnd = self.location.midDay

		elif self.location.currentTime > self.location.midDay and self.location.currentTime <= self.location.sunSet:
			quadrant = "Gamma"
			color1 = Color("yellow")
			color2 = Color("red")
			quadrantDelta = self.location.sunSet - self.location.midDay	
			quadrantEnd = self.location.sunSet
			
		elif self.location.currentTime > self.location.sunSet and self.location.currentTime <= self.location.endDay:
			quadrant = "Delta"
			color1 = Color("red")
			color2 = Color("blue")
			quadrantDelta = self.location.endDay - self.location.sunSet
			quadrantEnd = self.location.endDay
			
		else:
			quadrant = "Alpha"
			color1 = Color("blue")
			color2 = Color("red")
			quadrantDelta = self.location.sunRise - self.location.endDay
			quadrantEnd = self.location.sunRise
		
		print(quadrant, quadrantDelta, quadrantEnd)
		
		#convert the timeDelta object into minutes
		minutes = quadrantDelta.seconds / 60
		
		#Color shade will change once per 10 minutes
		lightDivisions = round(minutes / 10)
		

		lightShades = list(color1.range_to(color2, lightDivisions))
		
		quadrantDelta = quadrantEnd - self.location.currentTime
		
		quadrantOffset = quadrantDelta.seconds / 60
		quadrantOffset = round(quadrantOffset / 10 - 1)
		
		if quadrantOffset < 0:
			quadrantOffset = 0
		
		redChannel = round(lightShades[quadrantOffset].rgb[0] * 255)
		greenChannel = round(lightShades[quadrantOffset].rgb[1] * 255)
		blueChannel = round(lightShades[quadrantOffset].rgb[2] * 255)
		
		rgb = [redChannel, greenChannel, blueChannel]
		
		return rgb

