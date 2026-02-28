import sys

import pygame

from gui.gui import GUI
from rope import Rope

# Pygame başlatma
pygame.init()

# Pencere boyutları (Yükseklik 900 olarak ayarlandı)
WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rope Simulation")

# Renkler
BACKGROUND_COLOR = (20, 20, 30)
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
ROPE_COLOR = (200, 200, 200)
BUTTON_COLOR = (50, 70, 90)
BUTTON_HOVER = (70, 90, 110)
BUTTON_BORDER = (100, 120, 140)

# FPS kontrolü
CLOCK = pygame.time.Clock()
FPS = 60


class Camera:
    """Kamera sınıfı - zoom ve pan işlemleri için."""

    def __init__(self, x=0, y=0, zoom=1.0, min_zoom=0.2, max_zoom=3.0):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def world_to_screen(self, wx, wy):
        """Dünya koordinatlarını ekran koordinatlarına çevirir."""
        return (
            (wx - self.x) * self.zoom + WIDTH / 2,
            (wy - self.y) * self.zoom + HEIGHT / 2,
        )

    def screen_to_world(self, sx, sy):
        """Ekran koordinatlarını dünya koordinatlarına çevirir."""
        return (
            (sx - WIDTH / 2) / self.zoom + self.x,
            (sy - HEIGHT / 2) / self.zoom + self.y,
        )

    def zoom_in(self):
        """Yakınlaş."""
        self.zoom = min(self.zoom * 1.2, self.max_zoom)

    def zoom_out(self):
        """Uzaklaş."""
        self.zoom = max(self.zoom / 1.2, self.min_zoom)

    def reset(self):
        """Kamerayı sıfırla."""
        self.x = 0
        self.y = 0
        self.zoom = 1.0


def draw_grid(camera):
    """Arka planda şık bir ızgara çizer."""
    line_color = (40, 40, 50)
    grid_size = 50

    # Ekran sınırlarını dünya koordinatlarına çevir
    world_left, world_top = camera.screen_to_world(0, 0)
    world_right, world_bottom = camera.screen_to_world(WIDTH, HEIGHT)

    # Zemin ızgarası
    start_x = int(world_left // grid_size * grid_size)
    end_x = int(world_right // grid_size * grid_size + grid_size)
    start_y = int(world_top // grid_size * grid_size)
    end_y = int(world_bottom // grid_size * grid_size + grid_size)

    for x in range(start_x, end_x + 1, grid_size):
        screen_x, screen_y = camera.world_to_screen(x, start_y)
        screen_x_end, screen_y_end = camera.world_to_screen(x, end_y)
        pygame.draw.line(
            SCREEN, line_color, (screen_x, screen_y), (screen_x_end, screen_y_end), 1
        )

    for y in range(start_y, end_y + 1, grid_size):
        screen_x, screen_y = camera.world_to_screen(start_x, y)
        screen_x_end, screen_y_end = camera.world_to_screen(end_x, y)
        pygame.draw.line(
            SCREEN, line_color, (screen_x, screen_y), (screen_x_end, screen_y_end), 1
        )


def draw_button(screen, rect, text, font, hovered):
    """Buton çizer."""
    color = BUTTON_HOVER if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BUTTON_BORDER, rect, 2)

    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def draw_slider(screen, rect, value, min_val, max_val, label, font):
    """Slider çizer."""
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    pygame.draw.rect(screen, BUTTON_BORDER, rect, 2)

    # Etiket
    label_surf = font.render(f"{label}: {int(value)}", True, WHITE)
    screen.blit(label_surf, (rect.left, rect.top - 25))

    # Slider valisi
    total_width = rect.width - 20
    slider_width = max(
        10, min(total_width, (value - min_val) / (max_val - min_val) * total_width)
    )

    slider_rect = pygame.Rect(
        rect.left + 10, rect.top + 5, slider_width, rect.height - 10
    )
    pygame.draw.rect(screen, BLUE, slider_rect)

    return slider_rect


def clamp(value, min_val, max_val):
    """Değeri min ve max değerler arasında kırp."""
    return max(min_val, min(value, max_val))


def main():
    """Ana oyun döngüsü."""
    # GUI ve Rope nesnelerini oluştur
    gui = GUI(WIDTH, HEIGHT)

    # Kamera nesnesi
    camera = Camera(zoom=1.0, min_zoom=0.2, max_zoom=3.0)

    # Simülasyon parametreleri - %25 genişletilmiş aralıklar
    params = {
        "num_segments": 15,
        "segment_length": 35,
        "gravity": 0.5,
        "damping": 0.99,
        "constraint_iterations": 5,
    }

    # Yeni aralıklar ( %25 genişletilmiş )
    PARAM_RANGES = {
        "gravity": (0.1, 2.5),
        "damping": (0.85, 1.0),
        "segments": (2, 5000),
        "segment_length": (15, 187),
    }

    # İpin başlangıç_parametreleri
    start_x = 0
    start_y = 0
    rope = Rope(
        start_x=start_x,
        start_y=start_y,
        num_segments=params["num_segments"],
        segment_length=params["segment_length"],
        start_fixed=True,
        particle_color=WHITE,
        rope_color=ROPE_COLOR,
    )

    # Fare ile sürükleme değişkenleri
    dragged_particle_index = None
    mouse_down = False
    active_slider = None
    dragging_camera = False
    last_mouse_pos = (0, 0)

    # UI kontrolleri
    button_rect = pygame.Rect(WIDTH - 220, 100, 200, 40)
    gravity_slider_rect = pygame.Rect(WIDTH - 220, 160, 200, 30)
    damping_slider_rect = pygame.Rect(WIDTH - 220, 210, 200, 30)
    segments_slider_rect = pygame.Rect(WIDTH - 220, 260, 200, 30)
    length_slider_rect = pygame.Rect(WIDTH - 220, 310, 200, 30)

    # Zoom butonları
    zoom_in_rect = pygame.Rect(10, 10, 40, 40)
    zoom_out_rect = pygame.Rect(60, 10, 40, 40)
    zoom_reset_rect = pygame.Rect(110, 10, 60, 40)

    hover_states = {
        "reset": False,
        "gravity": False,
        "damping": False,
        "segments": False,
        "length": False,
        "zoom_in": False,
        "zoom_out": False,
        "zoom_reset": False,
    }

    running = True
    paused = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Hover durumlarını güncelle
        hover_states["reset"] = button_rect.collidepoint(mouse_pos)
        hover_states["gravity"] = gravity_slider_rect.collidepoint(mouse_pos)
        hover_states["damping"] = damping_slider_rect.collidepoint(mouse_pos)
        hover_states["segments"] = segments_slider_rect.collidepoint(mouse_pos)
        hover_states["length"] = length_slider_rect.collidepoint(mouse_pos)
        hover_states["zoom_in"] = zoom_in_rect.collidepoint(mouse_pos)
        hover_states["zoom_out"] = zoom_out_rect.collidepoint(mouse_pos)
        hover_states["zoom_reset"] = zoom_reset_rect.collidepoint(mouse_pos)

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    gui.simulation_running = not paused
                elif event.key == pygame.K_r:
                    # Rope'u resetle
                    rope = Rope(
                        start_x=start_x,
                        start_y=start_y,
                        num_segments=params["num_segments"],
                        segment_length=params["segment_length"],
                        start_fixed=True,
                        particle_color=WHITE,
                        rope_color=ROPE_COLOR,
                    )
                    dragged_particle_index = None
                    active_slider = None
                    camera.reset()
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    camera.zoom_in()
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    camera.zoom_out()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Reset butonuna tıklandı
                    if hover_states["reset"]:
                        rope = Rope(
                            start_x=start_x,
                            start_y=start_y,
                            num_segments=params["num_segments"],
                            segment_length=params["segment_length"],
                            start_fixed=True,
                            particle_color=WHITE,
                            rope_color=ROPE_COLOR,
                        )
                        dragged_particle_index = None
                        active_slider = None
                    # Zoom butonları
                    elif hover_states["zoom_in"]:
                        camera.zoom_in()
                    elif hover_states["zoom_out"]:
                        camera.zoom_out()
                    elif hover_states["zoom_reset"]:
                        camera.reset()
                    # Slider'lara tıklandı
                    elif hover_states["gravity"]:
                        active_slider = "gravity"
                        mouse_down = True
                    elif hover_states["damping"]:
                        active_slider = "damping"
                        mouse_down = True
                    elif hover_states["segments"]:
                        active_slider = "segments"
                        mouse_down = True
                    elif hover_states["length"]:
                        active_slider = "length"
                        mouse_down = True
                    # Kamera sürüklemesi
                    elif (
                        hover_states["zoom_in"]
                        or hover_states["zoom_out"]
                        or hover_states["zoom_reset"]
                    ):
                        dragging_camera = True
                        last_mouse_pos = mouse_pos
                    else:
                        # rope üzerine tıklandı
                        world_pos = camera.screen_to_world(mouse_pos[0], mouse_pos[1])
                        particle_index = rope.is_mouse_over_particle(
                            world_pos, radius=25 / camera.zoom
                        )
                        if particle_index is not None:
                            dragged_particle_index = particle_index
                            rope.particles[particle_index].is_being_dragged = True
                            mouse_down = True
                        else:
                            mouse_down = True
                elif event.button == 4:  # Mouse scroll up (zoom in)
                    camera.zoom_in()
                elif event.button == 5:  # Mouse scroll down (zoom out)
                    camera.zoom_out()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # Slider Releases
                    if active_slider is not None:
                        active_slider = None
                        mouse_down = False
                    elif mouse_down is True:
                        mouse_down = False
                        if (
                            dragged_particle_index is not None
                            and dragged_particle_index < len(rope.particles)
                        ):
                            rope.particles[
                                dragged_particle_index
                            ].is_being_dragged = False
                        dragged_particle_index = None
                    dragging_camera = False
            elif event.type == pygame.MOUSEMOTION:
                # Slider hareketi
                if active_slider is not None:
                    if active_slider == "gravity":
                        rel_x = clamp(
                            mouse_pos[0] - gravity_slider_rect.left - 10, 0, 180
                        )
                        min_val, max_val = PARAM_RANGES["gravity"]
                        params["gravity"] = round(
                            min_val + (rel_x / 180) * (max_val - min_val), 2
                        )
                    elif active_slider == "damping":
                        rel_x = clamp(
                            mouse_pos[0] - damping_slider_rect.left - 10, 0, 180
                        )
                        min_val, max_val = PARAM_RANGES["damping"]
                        params["damping"] = round(
                            min_val + (rel_x / 180) * (max_val - min_val), 3
                        )
                    elif active_slider == "segments":
                        rel_x = clamp(
                            mouse_pos[0] - segments_slider_rect.left - 10, 0, 180
                        )
                        min_val, max_val = PARAM_RANGES["segments"]
                        params["num_segments"] = int(
                            min_val + (rel_x / 180) * (max_val - min_val)
                        )
                        # Segment sayısı değişince rope'u yeniden oluştur
                        rope = Rope(
                            start_x=start_x,
                            start_y=start_y,
                            num_segments=params["num_segments"],
                            segment_length=params["segment_length"],
                            start_fixed=True,
                            particle_color=WHITE,
                            rope_color=ROPE_COLOR,
                        )
                        dragged_particle_index = None
                    elif active_slider == "length":
                        rel_x = clamp(
                            mouse_pos[0] - length_slider_rect.left - 10, 0, 180
                        )
                        min_val, max_val = PARAM_RANGES["segment_length"]
                        params["segment_length"] = int(
                            min_val + (rel_x / 180) * (max_val - min_val)
                        )
                        # Segment uzunluğu değişince rope'u yeniden oluştur
                        rope = Rope(
                            start_x=start_x,
                            start_y=start_y,
                            num_segments=params["num_segments"],
                            segment_length=params["segment_length"],
                            start_fixed=True,
                            particle_color=WHITE,
                            rope_color=ROPE_COLOR,
                        )
                        dragged_particle_index = None
                # Kamera sürüklemesi
                elif dragging_camera:
                    dx = mouse_pos[0] - last_mouse_pos[0]
                    dy = mouse_pos[1] - last_mouse_pos[1]
                    camera.x -= dx / camera.zoom
                    camera.y -= dy / camera.zoom
                    last_mouse_pos = mouse_pos
                elif mouse_down is True and dragged_particle_index is not None:
                    world_pos = camera.screen_to_world(mouse_pos[0], mouse_pos[1])
                    rope.drag_particle(world_pos, dragged_particle_index)

        # EKRANI TEMİZLE
        SCREEN.fill(BACKGROUND_COLOR)

        # IZGARAYI ÇİZ
        draw_grid(camera)

        # GUI'yi çiz
        gui.draw(SCREEN)

        # Parametre bilgilerini çiz
        sim_params = {
            "Segments": len(rope.particles) - 1,
            "FPS": int(CLOCK.get_fps()),
            "Paused": "Yes" if paused else "No",
            "Gravity": params["gravity"],
            "Damping": params["damping"],
            "Zoom": f"{camera.zoom:.2f}x",
        }
        gui.draw_params(SCREEN, sim_params)

        # UI Kontrollerini çiz
        font_small = pygame.font.SysFont(None, 20)
        font_tiny = pygame.font.SysFont(None, 16)

        # Zoom butonları
        draw_button(SCREEN, zoom_in_rect, "+", font_small, hover_states["zoom_in"])
        draw_button(SCREEN, zoom_out_rect, "-", font_small, hover_states["zoom_out"])
        draw_button(
            SCREEN, zoom_reset_rect, "RESET", font_small, hover_states["zoom_reset"]
        )

        # Reset button
        draw_button(
            SCREEN, button_rect, "RESET ROPE", font_small, hover_states["reset"]
        )

        # Sliders
        draw_slider(
            SCREEN,
            gravity_slider_rect,
            params["gravity"],
            PARAM_RANGES["gravity"][0],
            PARAM_RANGES["gravity"][1],
            "Gravity",
            font_tiny,
        )
        draw_slider(
            SCREEN,
            damping_slider_rect,
            params["damping"],
            PARAM_RANGES["damping"][0],
            PARAM_RANGES["damping"][1],
            "Damping",
            font_tiny,
        )
        draw_slider(
            SCREEN,
            segments_slider_rect,
            params["num_segments"],
            PARAM_RANGES["segments"][0],
            PARAM_RANGES["segments"][1],
            "Segments",
            font_tiny,
        )
        draw_slider(
            SCREEN,
            length_slider_rect,
            params["segment_length"],
            PARAM_RANGES["segment_length"][0],
            PARAM_RANGES["segment_length"][1],
            "Segment Length",
            font_tiny,
        )

        # Rope'u güncelle ve çiz
        if not paused:
            rope.update(
                gravity=params["gravity"],
                damping=params["damping"],
                dt=1.0,
                constraint_iterations=params["constraint_iterations"],
            )

        # Rope'un çizimi için kamera transform uygula
        rope.draw(SCREEN, camera)

        # EKRANI GÜNCELLE
        pygame.display.flip()

        # FPS KONTROLÜ
        CLOCK.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
