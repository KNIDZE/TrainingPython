from pygame import *
from random import *
window = display.set_mode()
clock = time.Clock()


bg = transform.scale(
    image.load('res/galaxy.jpg'),
    (window.get_width(), window.get_height())
)


# pygame -> sprite -> Sprite
class GameSprite(sprite.Sprite):

    def __init__(self, x, y, width, height, image_name, speed):
        super().__init__()
        self.image = transform.scale(
            image.load(image_name),
            (width, height)
        )
        self.speed = speed
        self.rect = self.image.get_rect() # взяти хітбокс з картинки
        self.rect.x, self.rect.y = x, y # встановити початкові кординати картинки
        self.cool_down = 0 # властивість, яка рахує кількість кадрів, що пройшла з пострілу
        self.direction = 'right'

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
# Player - клас спадкоємець класу GameSprite
class Player(GameSprite):

    # flip - віддзеркалити
    def flip(self):
        self.image = transform.flip(self.image, False, True)
    def update(self):
        self.cool_down += 1 # кожен кадр збільшувати cooldown на 1
        pressed_keys = key.get_pressed()  # отримати всі клавіші, які натиснуті
        if pressed_keys[K_a]:

            self.rect.x -= self.speed
        if pressed_keys[K_d]:
            self.rect.x += self.speed
        if pressed_keys[K_SPACE] and self.cool_down > 60: # якщо пройшло більше 60 кадрів і користувач натиснув пробіл
            bullet = Bullet(self.rect.x + 25, self.rect.y, 20, 40, 'res/bullet.png', 5)
            bullets.add(bullet)
            self.cool_down = 0
        if pressed_keys[K_t]:
            self.flip()


class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed

class Enemy(GameSprite):

    def update(self):
        global lose
        self.rect.y += self.speed
        if self.rect.y > 500:# поточна кордината ворога
            lose = True
player = Player(400, window.get_height() - 150, 70, 100, 'res/rocket.png', 5)
game = True
lose = False

enemies = sprite.Group()
bullets = sprite.Group()
# randint - випадкове ціле число
# на сцені завжди має бути 7 ворогів
score = 0
while game:
    while len(enemies) < 7:
        #               рандомний х від 0 до ширини вікна
        enemy = Enemy(randint(0, window.get_width()-80), - 80, 80, 60, 'res/ufo.png', 1)
        # Додаю до групи
        enemies.add(enemy)

    pressed_keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT or pressed_keys[K_ESCAPE]:
            game = False

    # якщо монстри врізаються в гравця - знищити монстрів
    sprite.spritecollide(player, enemies, True)
    # перевіряє, чи торкнулися спрайти однієї групи спрайтів іншої
    # ( група 1, група 2, знищувати спрати 1?, знищвати спайти 2?)
    strikes = sprite.groupcollide(bullets, enemies, True, True)
    for bullet in strikes:
        #  strikes[bullet] - [enemy1 sprite, enemy2] список спрайтів, які зникли
        score += len(strikes[bullet]) # додати кількість вбитих ворогів
    # доробити програму до кінця:
    # зробити поразку (якщо хочете - перемогу)
    # Якщо у вас це є - зробіть систему HP
    # Додайте свої текстурки
    # Завдання з *: Треба зробити бонуси!
    if score == 20:
        # font.SysFont(Назва шрифта, розмір) - створити об'єкт шрифт певного розміру
        # .render(text, True, color) - на основі шрифта створити текст певного кольору
        # вікно.blit(text, (x, y)) - показати у вікні певне зображення в певних кординатах
        # щоб шрифти працювали, треба на початку написати init()
        text = font.SysFont('Algerian', 150).render("You WON", True, (50, 150, 100))
        window.blit(text, (100, 300))
        display.update()
        time.wait(5000)
        game = False
    enemies.update() # звертаємось до всіх спрайтів в групі
    bullets.update()

    window.blit(bg, (0,0))
    enemies.draw(window)
    bullets.draw(window)
    player.update()
    player.draw()


    display.update()
    clock.tick(60)



