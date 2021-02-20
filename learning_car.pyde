import string
# import neat

class Border:

	def __init__(self):
		self.all = []

	def show(self):
		for item in self.all:
			item.show()

	def checkIntersect(self):
		pass


class LineBorder:

	def __init__(self, x1, y1, x2, y2):
		self.start = [x1, y1]
		self.end = [x2, y2]

	def show(self):
		stroke(0)
		strokeWeight(6)
		line(self.start[0], self.start[1], self.end[0], self.end[1])

	def intersect(self, line):
		pass


class CurveBorder:

	def __init__(self, x1, y1, r, a1, a2):
		self.center = [x1, y1]
		self.angle = [a1, a2]
		self.r = r

	def show(self):
		stroke(0)
		strokeWeight(6)
		noFill()
		arc(self.center[0], self.center[1], self.r*2, self.r*2, self.angle[0], self.angle[1])

	def intersect(self):
		pass


class Car:

	def __init__(self, x, y, a):
		self.engine = 0
		self.speed = 0
		self.max_speed = 12
		self.car_direction = a
		self.drive_direction = a
		self.pos = [x, y]

		self.slide = 0
		self.slide_left = False
		self.slide_right = False

		self.img = loadImage('C:\\Users\\Cliff\\Documents\\Processing\\learning_car\\redcar.png')
		self.img_crashed = loadImage('C:\\Users\\Cliff\\Documents\\Processing\\learning_car\\redcar_crashed.png')
		self.crashed = False


	def checkControls(self):
		if keys['w']:
			self.speed -= 0.4
		if keys['s']:
			self.speed += 0.4

		if abs(self.speed) > self.max_speed:
			if self.speed > self.max_speed:
				self.speed = self.max_speed
			else:
				self.speed = -self.max_speed

		if keys['w'] == keys['s']:
			self.speed = reduce(self.speed, 0.25)

		# ====================================

		if (abs(self.speed / self.max_speed)) < 0.5:
			if keys['a']:
				self.car_direction -= ((PI/16) - (PI/24) * (abs(self.speed) / self.max_speed))
			if keys['d']:
				self.car_direction += ((PI/16) - (PI/24) * (abs(self.speed) / self.max_speed))
			self.drive_direction = self.car_direction
			print('turn 1')
		
		else:
			if not keys[' ']:
				if keys['a']:
					self.car_direction -= ((PI/16) - (PI/24) * (abs(self.speed) / self.max_speed))
				if keys['d']:
					self.car_direction += ((PI/16) - (PI/24) * (abs(self.speed) / self.max_speed))
				self.drive_direction = self.car_direction
				print('turn 2')

			else:
				if keys['a']:
					self.slide -= 1
				if keys['d']:
					self.slide += 1

				if self.slide < -10:
					self.slide = -10
				if self.slide > 10:
					self.slide = 10

				if self.slide == -10:
					self.car_direction -= PI/24
					self.drive_direction -= PI/24
					print('in drift')

				elif self.slide == 10:
					self.car_direction += PI/24
					self.drive_direction += PI/24
					print('in drift')

				else:
					if keys['a'] != keys['d']:
						if keys['a']:
							self.car_direction -= PI/72

						elif keys['d']:
							self.car_direction += PI/72
						print('preparation', self.car_direction, self.slide)



	def update(self):
		if self.car_direction > 2*PI:
			self.car_direction -= 2*PI
		elif self.car_direction < 0:
			self.car_direction += 2*PI
			
		if self.drive_direction > 2*PI:
			self.drive_direction -= 2*PI
		elif self.drive_direction < 0:
			self.drive_direction += 2*PI

		self.pos[0] += (self.speed * sin(self.drive_direction) * -1)
		self.pos[1] += (self.speed * cos(self.drive_direction))


	def show(self):
		imageMode(CENTER)
		translate(self.pos[0], self.pos[1])
		rotate(self.car_direction)

		if self.crashed:
			image(self.img_crashed, 0, 0, 18, 32)
		else:
			image(self.img, 0, 0, 18, 32)

		translate(-self.pos[0], -self.pos[1])
		rotate(-self.car_direction)



	def radar(self):
		pass



def reduce(a, b):
	# reduce the abs value of a by b but does not change sign
	if abs(a) < b:
		return 0
	if a > 0:
		return (a - b)
	return (a + b)


def keyPressed():
	keys[key] = True


def keyReleased():
	keys[key] = False


def updateScreen():
	background(200, 200, 200)
	road.show()


def setup():
	size(1600, 900)
	background(255, 255, 255)
	frameRate(60)


def draw():
	updateScreen()
	player.checkControls()
	player.update()
	player.show()





if __name__ == '__main__':
	keys = {}
	for char in string.printable:
		keys[char] = False

	player = Car(450, 150, PI/2)

	road = Border()
	road.all.append(LineBorder(450, 100, 1150, 100))
	road.all.append(LineBorder(450, 200, 1150, 200))
	road.all.append(LineBorder(450, 700, 1150, 700))
	road.all.append(LineBorder(450, 800, 1150, 800))
	road.all.append(CurveBorder(450, 450, 350, PI/2, 3*PI/2))
	road.all.append(CurveBorder(450, 450, 250, PI/2, 3*PI/2))
	road.all.append(CurveBorder(1150, 450, 350, -PI/2, PI/2))
	road.all.append(CurveBorder(1150, 450, 250, -PI/2, PI/2))

