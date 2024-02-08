import math

import pygame

from crafting import combine


pygame.init()


class Fonts:
    f32 = pygame.font.SysFont(None, 32)


class Colors:
    bg = (210, 208, 186)
    alt_bg = (182, 190, 156)
    text = (30, 27, 24)
    sidebar = (94, 116, 127)
    other = (138, 113, 106)


class Item:
    def __init__(self, text: str, x: float, y: float):
        self.text = text
        self.x = x
        self.y = y

        self.xv = 0
        self.yv = 0
        self.radius = 50
        self.text_img = Fonts.f32.render(
            self.text,
            antialias=True,
            color=Colors.text,
        )

    def update(self, dt: float):
        self.x += self.xv * dt
        self.y += self.yv * dt

        # Push away from others
        for item in workspace_items:
            if item is self:
                continue

            dx = self.x - item.x
            dy = self.y - item.y
            dist = (dx**2 + dy**2) ** 0.5
            if dist < 150:
                self.xv += dx / dist * math.exp(-dist / 50) * 1000 * dt
                self.yv += dy / dist * math.exp(-dist / 50) * 1000 * dt
        
        # Also from sides
        w, h = pygame.display.get_window_size()
        self.xv += max(100 - self.x, 0)
        self.xv -= max(self.x + 100 - w, 0)
        self.yv += max(100 - self.y, 0)
        self.yv -= max(self.y + 100 - h, 0)

        # Framerate independent velocity decay
        self.xv *= math.exp(math.log(0.005) * dt)
        self.yv *= math.exp(math.log(0.005) * dt)

    def draw(self, screen: pygame.Surface):
        mx, my = pygame.mouse.get_pos()
        radius = self.radius
        if ((self.x - mx) ** 2 + (self.y - my) ** 2) ** 0.5 < self.radius:
            radius = 55

        pygame.draw.circle(
            screen,
            color=Colors.alt_bg,
            center=(self.x, self.y),
            radius=radius,
        )
        w, h = self.text_img.get_size()
        screen.blit(self.text_img, (self.x - w / 2, self.y - h / 2))


workspace_items = [
    Item("Water", 200, 200),
    Item("Fire", 400, 200),
    Item("Wind", 200, 400),
    Item("Earth", 400, 400),
]


def run():
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    held_item = None

    pygame.display.set_caption("Finite Craft")
    icon = Fonts.f32.render("FC", antialias=True, color=100)
    pygame.display.set_icon(icon)

    last_mx, last_my = pygame.mouse.get_pos()

    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for item in workspace_items:
                    if ((item.x - mx) ** 2 + (item.y - my) ** 2) ** 0.5 < 50:
                        held_item = item

                if held_item is not None:
                    v = workspace_items
                    v.append(v.pop(v.index(held_item)))

            elif event.type == pygame.MOUSEBUTTONUP:
                if held_item is not None:
                    for item in workspace_items:
                        if item is held_item:
                            continue

                        if (
                            (item.x - mx) ** 2 + (item.y - my) ** 2
                        ) ** 0.5 < item.radius:
                            # v.pop(v.index(held_item))
                            # v.pop(v.index(item))
                            new_text = combine(held_item.text, item.text)
                            new_x = (held_item.x + item.x) / 2
                            new_y = (held_item.y + item.y) / 2
                            v.append(Item(new_text, new_x, new_y))
                            break

                    held_item.xv = (mx - last_mx) / dt
                    held_item.yv = (my - last_my) / dt

                held_item = None

        if held_item:
            held_item.x, held_item.y = pygame.mouse.get_pos()

        screen.fill(Colors.bg)

        for item in workspace_items:
            item.update(dt)
            item.draw(screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        last_mx, last_my = mx, my

    pygame.quit()
