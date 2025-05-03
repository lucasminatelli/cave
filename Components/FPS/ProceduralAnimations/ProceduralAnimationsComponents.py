import cave, cave.math

class ProceduralAnimationsComponent(cave.Component):
	active: bool = True
	invert_transform: bool = True
	speed_idle: float = 2.0
	speed_walking: float = 6.0
	speed_running: float = 12.0
	speed_jumping: float = 3.5
	amplitude_idle: cave.Vector2 = cave.Vector2(0.1, 0.05)
	amplitude_walking: cave.Vector2 = cave.Vector2(0.4, 0.8)
	amplitude_running: cave.Vector2 = cave.Vector2(1.2, 0.8)
	limit_x: float = 0.5
	limit_y: float = 0.05
	position_speed: float = 0.05
	position_amount:float = 0.1
 
	def _animates(self):
		dt = cave.getDeltaTime()
		characterComponent: cave.CharacterComponent = self.entity.getRootParent().get("Character")
		if not characterComponent:
			raise Exception("CharacterComponent missing")	
    
		self.elapsedTime += dt
		bob: cave.Vector2 = cave.Vector2(0.0, 0.0)
		bob.x = cave.math.sin(self.elapsedTime * self.speed) * self.amplitude.x
		bob.y = cave.math.cos(self.elapsedTime * self.speed) * self.amplitude.y
		bob.y = cave.math.abs(bob.y) if self.getPlayerMovementStatus() != 'idle' else bob.y
  
		pos: cave.Vector3 = self.entity.getTransform().getPosition()
  
		if characterComponent.onGround():
			pos.x = cave.math.lerp(pos.x, self.initialPosition.x + bob.x, self.position_speed * dt)
			pos.y = cave.math.lerp(pos.y, self.initialPosition.y + bob.y, self.position_speed * dt)
   
		else: # falling / jumping
			characterCurrentFallSpeed = characterComponent.getCurrentFallSpeed() * self.speed_jumping
			pos.y = cave.math.lerp(
					pos.y,
					pos.y + (characterCurrentFallSpeed * self.position_amount * dt),
					self.position_speed
				)
			pos.y = cave.math.clamp(pos.y, self.initialPosition.y - self.limit_y, self.initialPosition.y + self.limit_y)
 
	def setActive(self, active: bool):
		self.active = active

	def getActive(self) -> bool:
		return self.active
  
	def getPlayerMovementStatus(self) -> str:
		playerComponent: cave.PlayerComponent = self.entity.getRootParent().get("Player")
		if not playerComponent:
			raise Exception("PlayerComponent missing")
	
		if playerComponent.isWalking():
			if playerComponent.isRunning() and playerComponent.runSpeed != playerComponent.walkSpeed:
				return 'running'
			return 'walking'
		if not playerComponent.isWalking() and not playerComponent.isRunning():
			return 'idle'
		else: return ''
   
	def start(self, scene: cave.Scene):
		self.setActive(self.active)
  
		if self.invert_transform:
			self.entity.getTransform().setEuler(cave.Vector3(180, 180, 180))
     
		self.speeds = {
			"idle": self.speed_idle,
			"walking": self.speed_walking,
			"running": self.speed_running,
		}
		self.amplitudes = {
			"idle": self.amplitude_idle,
			"walking": self.amplitude_walking,
			"running": self.amplitude_running,
		}
  
		self.speed = 0.0
		self.amplitude = 0.0
		self.elapsedTime = 0.0
		self.initialPosition: cave.Vector3 = self.entity.getTransform().getPositionCopy()
		self.initialRotation: cave.Vector3 = self.entity.getTransform().getEuler()
		self.mouseMovement: cave.Vector2 = cave.Vector2(0.0, 0.0)

	def update(self):
		if self.getActive():
			events = cave.getEvents()
			self.mouseMovement = -events.getMouseMotion()
	
			playerMovementStatus = self.getPlayerMovementStatus()
	
			if playerMovementStatus:		
				self.amplitude	= self.amplitudes[playerMovementStatus]
				self.speed = self.speeds[playerMovementStatus]
	
				self._animates()
		else: pass
		
	def end(self, scene: cave.Scene):
		pass
	