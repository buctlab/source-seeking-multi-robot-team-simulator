import pygame


class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, map_size, block_color, pos, block_img, size, data):
        super().__init__()
        self.data = data
        self.block_color = block_color
        self.image = pygame.image.load(block_img)
        self.rect = self.image.get_rect()
        self.size = size
        self.wd_size = int(map_size / size)
        self.pos = pos
        self.rect.left, self.rect.top = -100, -100
        self.update((0, 0))

    # draw obstacle in each frame
    def update(self, *args, **kwargs):
        current_pos = args[0]
        if current_pos[0] <= self.pos[0] < current_pos[0] + self.wd_size and \
                current_pos[1] <= self.pos[1] < current_pos[1] + self.wd_size:
            self.rect.left, self.rect.top = (
                (self.pos[0] - current_pos[0]) * self.size, (self.pos[1] - current_pos[1]) * self.size)
        else:
            self.rect.left, self.rect.top = -100, -100
