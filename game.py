import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Definição das dimensões da janela do jogo
largura = 900
altura = 550
tela = pygame.display.set_mode((largura, altura))

image_backgroud = pygame.image.load('background.png').convert()
image_backgroud = pygame.transform.scale(image_backgroud, (largura, altura))

largura_carro = 100
altura_carro = 100
image_carro = pygame.image.load('carro.png').convert_alpha()
image_carro = pygame.transform.scale(image_carro, (largura_carro, altura_carro))

largura_manga = 60
altura_manga = 60
image_manga = pygame.image.load('manga.png').convert_alpha()
image_manga = pygame.transform.scale(image_manga, (largura_manga, altura_manga))

largura_moeda = 50
altura_moeda = 50
image_moeda = pygame.image.load('moeda.png').convert_alpha()
image_moeda = pygame.transform.scale(image_moeda, (largura_moeda, altura_moeda))

# Classe para representar o carro
class Jogador(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = largura // 2
        self.rect.bottom = altura - 90
        self.velocidade = 6

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        # Impede que o carro saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe para representar as mangas
class Maca(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(largura // 4, largura * 3 // 4 - largura_manga)
        self.rect.y = random.randint(-altura_manga, -10)
        self.velocidade = 10
        self.renasce()

    def renasce(self):
        self.rect.x = random.randint(largura // 4, largura * 3 // 4 - largura_manga)
        self.rect.y = random.randint(-altura_manga, -10)
        self.velocidade = random.randint(2, 4)

    def update(self):
        self.rect.y += self.velocidade

        # Verifica se a manga saiu da tela
        if self.rect.top > altura:
            self.renasce()

# Classe para representar as moedas
class Moeda(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(largura // 4, largura * 3 // 4 - largura_moeda)
        self.rect.y = random.randint(-altura_moeda, -10)
        self.velocidade = 10
        self.renasce()

    def renasce(self):
        self.rect.x = random.randint(largura // 4, largura * 3 // 4 - largura_moeda)
        self.rect.y = random.randint(-altura_moeda, -10)
        self.velocidade = random.randint(2, 4)

    def update(self):
        self.rect.y += self.velocidade

        # Verifica se a moeda saiu da tela
        if self.rect.top > altura:
            self.renasce()

# Instanciando o carro
jog = Jogador(image_carro)

# Criando um grupo de sprites
sprites = pygame.sprite.Group()
sprites.add(jog)

# Criando um grupo para as mangas
macas = pygame.sprite.Group()

# Criando um grupo para as moedas
moedas = pygame.sprite.Group()

# Inicialização do placar
placar = 0

# Inicialização das vidas
vidas = 3

# Inicialização do clock
clock = pygame.time.Clock()

# Loop principal do jogo
while True:
    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Adiciona mangas aleatoriamente
    if len(macas) < 2:
        maca = Maca(image_manga)
        macas.add(maca)
        sprites.add(maca)

    # Adiciona moedas aleatoriamente
    if len(moedas) < 1:
        moeda = Moeda(image_moeda)
        moedas.add(moeda)
        sprites.add(moeda)

    # Verifica colisões com as mangas
    if len(pygame.sprite.spritecollide(jog, macas, True)) != 0:
        vidas -= 1

    # Verifica colisões com as moedas
    if len(pygame.sprite.spritecollide(jog, moedas, True)) != 0:
        placar += 1

    # Atualiza os sprites
    sprites.update()

    # Desenha o fundo
    tela.blit(image_backgroud, (0, 0))

    # Desenha os sprites
    sprites.draw(tela)

    # Desenha o placar
    fonte = pygame.font.SysFont(None, 36)
    texto_placar = fonte.render("Placar: " + str(placar), True, (255, 255, 255))
    tela.blit(texto_placar, (10, 10))

    # Desenha as vidas
    texto_vidas = fonte.render("Vidas: " + str(vidas), True, (255, 255, 255))
    tela.blit(texto_vidas, (10, 50))

    # Verifica se o número de vidas é igual a 0
    if vidas == 0:
        pygame.quit()
        sys.exit()

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de atualização do jogo
    clock.tick(30)

