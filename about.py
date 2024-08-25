import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class AboutScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.about_text = [
            "**Sobre o Jogo:**",
            "O jogo é inspirado em Angry Birds, onde o jogador controla um pássaro",
            "lançado por um estilingue para atingir alvos. Os vetores envolvidos no jogo",
            "são essenciais para a física da movimentação. A força gravitacional é aplicada",
            "ao pássaro tanto pela gravidade padrão quanto pela presença de luas no cenário,",
            "utilizando a fórmula da gravitação universal. O vetor de velocidade reflete a",
            "direção e a rapidez do movimento, enquanto o vetor elástico simula a força do",
            "estilingue ao lançar o pássaro. Esses vetores são visualizados em tempo real,",
            "oferecendo uma visão clara das forças atuantes durante o jogo.",
            "",
            "**Como Jogar:**",
            "1. **Iniciar o Jogo:** Ao abrir o jogo, você será levado à tela inicial.",
            "   Clique em 'Start' para começar.",
            "2. **Controle do Pássaro:** Use o mouse para clicar e segurar o pássaro",
            "   no estilingue. Arraste o pássaro para ajustar a força e a direção do lançamento.",
            "3. **Lançar:** Solte o mouse para lançar o pássaro em direção aos inimigos.",
            "   Tente acertar o máximo de alvos possível para aumentar sua pontuação.",
            "4. **Forças e Obstáculos:** Durante o voo, o pássaro será afetado pela gravidade",
            "   e pela força gravitacional das luas, o que pode alterar sua trajetória.",
            "   Evite obstáculos e aproveite o ambiente para atingir os inimigos.",
            "5. **Reiniciar Jogo:** Se precisar recomeçar, clique no botão de recarregar",
            "   no canto superior esquerdo da tela."
        ]

    def draw(self):
        self.screen.fill((200, 200, 200))
        y_offset = 10
        for line in self.about_text:
            rendered_line = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(rendered_line, (SCREEN_WIDTH // 2 - rendered_line.get_width() // 2, y_offset))
            y_offset += rendered_line.get_height() + 5  
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return False
        return True  