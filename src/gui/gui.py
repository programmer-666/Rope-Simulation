import pygame


class GUI:
    """Menü, bilgi yazısı ve UI elementleri için sınıf."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_tiny = pygame.font.SysFont(None, 18)

        self.simulation_running = False
        self.show_help = True

    def toggle_simulation(self):
        """Simülasyonu başlat/durdur."""
        self.simulation_running = not self.simulation_running

    def draw_title(self, screen):
        """Ana başlığı çizer."""
        title_text = self.font_large.render("Rope Simulation", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))
        screen.blit(title_text, title_rect)

    def draw_status(self, screen):
        """Simülasyon durumunu çizer."""
        if self.simulation_running:
            status_text = self.font_medium.render(
                "Simulation Running", True, (100, 255, 100)
            )
        else:
            status_text = self.font_medium.render("Paused", True, (255, 255, 100))

        status_rect = status_text.get_rect(
            center=(self.width // 2, self.height // 4 + 60)
        )
        screen.blit(status_text, status_rect)

    def draw_help(self, screen):
        """Yardım menüsünü çizer."""
        if not self.show_help:
            return

        help_lines = [
            "Controls:",
            "  SPACE  - Start/Stop Simulation",
            "  R      - Reset Rope",
            "  Click  - Grab and drag rope segments",
            "  ESC    - Exit",
        ]

        y_offset = self.height - 150
        for line in help_lines:
            text = self.font_small.render(line, True, (150, 150, 150))
            screen.blit(text, (20, y_offset))
            y_offset += 25

    def draw_params(self, screen, params):
        """Simülasyon parametrelerini çizer."""
        x, y = self.width - 200, 20

        for key, value in params.items():
            text = self.font_tiny.render(f"{key}: {value}", True, (200, 200, 200))
            screen.blit(text, (x, y))
            y += 20

    def draw(self, screen):
        """Tüm UI elementlerini çizer."""
        self.draw_title(screen)
        self.draw_status(screen)
        self.draw_help(screen)
