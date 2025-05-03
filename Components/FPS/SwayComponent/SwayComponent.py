import cave, cave.math

class SwayComponent(cave.Component):
	active: bool = True
	invert_transform: bool = True
	min: cave.Vector2 = cave.Vector2(-20.0, -20.0)
	max: cave.Vector2 = cave.Vector2(20.0, 20.0)
	position_speed: float = 0.07
	rotation_speed: float = 0.1
	position_amount: float = 0.1
	rotation_amount: float = 30.0
 
	def setActive(self, active: bool):
		self.active = active

	def getActive(self) -> bool:
		return self.active
    
	def start(self, scene: cave.Scene):
		self.setActive(self.active)
  
		if self.invert_transform:
			self.entity.getTransform().setEuler(cave.Vector3(180, 180, 180))
   
		self.position: cave.Vector3 = self.entity.getTransform().getPositionCopy()
		self.rotation: cave.Vector3 = self.entity.getTransform().getEuler()
  
	def _sway(self):
		dt = cave.getDeltaTime()
		events = cave.getEvents()
		mouseMovement: cave.Vector2 = events.getMouseMotion()

		mouseMovement.x = cave.math.clamp(mouseMovement.x, self.min.x, self.max.x)
		mouseMovement.y = cave.math.clamp(mouseMovement.y, self.min.y, self.max.y)
		
		pos = self.entity.getTransform().getPosition()
		pos.x = cave.math.lerp(
					pos.x,
					self.position.x - (mouseMovement.x * self.position_amount) * dt,
					self.position_speed
				)
		pos.y = cave.math.lerp(
					pos.y,
					self.position.y + (mouseMovement.y * self.position_amount) * dt,
					self.position_speed
				)

		rot = self.entity.getTransform().getEuler()
		rot.x = cave.math.lerp(
					rot.x,
					self.rotation.x - (mouseMovement.y * self.rotation_amount) * dt,
					self.rotation_speed
				)
		rot.y = cave.math.lerp(
					rot.y,
					self.rotation.y + (mouseMovement.x * self.rotation_amount) * dt,
					self.rotation_speed
				)
		self.entity.getTransform().setEuler(rot)
  
	def update(self):
		if self.getActive():
			self._sway()
		else: pass
		
	def end(self, scene: cave.Scene):
		pass