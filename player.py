###############################Player Class BEGIN########################################
# for player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filename = 'Sprites/knight.png'
        self.player_ss = SpriteSheet(self.filename)
        self.player_image = self.player_ss.image_at(pygame.Rect(0,0,85,100))
        self.surf = pygame.Surface((85,100))
        self.surf.fill((111,45,43))
        self.rect = self.surf.get_rect()
        self.pos = v((10,150))
        self.vel = v((0,0))
        self.acc = v((0,0))
        self.jumping = False

    def get_image(self):
        return self.player_image

    def move(self):
        self.acc =v((0,0.5))

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                #if self.pos.y < hits[0].rect.bottom:
                   # self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

                self.jumping = False

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
###############################Player Class END##########################################