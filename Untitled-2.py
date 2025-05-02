from pygame import *
from random import randint

# Inisialisasi mixer dan suara
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Gambar yang digunakan
gambar_latar = "galaxy.jpg"
gambar_pemain = "rocket.png"
gambar_peluru = "rocket.png"  # sementara pakai rocket.png juga, bisa diganti nanti
gambar_musuh = "rocket.png"   # sementara pakai rocket.png juga, bisa diganti nanti

# Ukuran jendela game
lebar_jendela = 700
tinggi_jendela = 500

# Kelas dasar untuk semua sprite
class GameSprite(sprite.Sprite):
    def __init__(self, gambar, x, y, lebar, tinggi, kecepatan):
        super().__init__()
        self.image = transform.scale(image.load(gambar), (lebar, tinggi))
        self.speed = kecepatan
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def tampil(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Kelas untuk pemain
class Pemain(GameSprite):
    def update(self):
        tombol = key.get_pressed()
        if tombol[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if tombol[K_RIGHT] and self.rect.x < lebar_jendela - 80:
            self.rect.x += self.speed

    def tembak(self):
        peluru = Peluru(gambar_peluru, self.rect.centerx - 5, self.rect.top, 15, 20, -15)
        peluru_group.add(peluru)
        fire_sound.play()

# Kelas peluru
class Peluru(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Kelas musuh
class Musuh(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > tinggi_jendela:
            self.rect.y = 0
            self.rect.x = randint(80, lebar_jendela - 80)

# Setup jendela dan latar belakang
display.set_caption("Game Tembak-Tembakan")
window = display.set_mode((lebar_jendela, tinggi_jendela))
latar = transform.scale(image.load(gambar_latar), (lebar_jendela, tinggi_jendela))

# Buat objek pemain
pemain = Pemain(gambar_pemain, 5, tinggi_jendela - 100, 80, 100, 10)

# Grup peluru dan musuh
peluru_group = sprite.Group()
musuh_group = sprite.Group()

# Buat beberapa musuh
for i in range(5):
    musuh = Musuh(gambar_musuh, randint(80, lebar_jendela - 80), -40, 80, 50, randint(1, 3))
    musuh_group.add(musuh)

# Variabel game utama
jalan = True
selesai = False
jam = time.Clock()

# Loop utama game
while jalan:
    for e in event.get():
        if e.type == QUIT:
            jalan = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                pemain.tembak()

    if not selesai:
        window.blit(latar, (0, 0))
        pemain.update()
        pemain.tampil()

        peluru_group.update()
        peluru_group.draw(window)

        musuh_group.update()
        musuh_group.draw(window)

        # Deteksi tabrakan peluru dan musuh
        tabrakan = sprite.groupcollide(musuh_group, peluru_group, True, True)
        for musuh_mati in tabrakan:
            musuh_baru = Musuh(gambar_musuh, randint(80, lebar_jendela - 80), -40, 80, 50, randint(1, 3))
            musuh_group.add(musuh_baru)

        display.update()
    jam.tick(60)
