import pygame


class Constraint:
    """İki partikül arasındaki mesafe kısıtlaması (ip segmenti)."""

    def __init__(self, p1, p2, stiffness=1.0):
        """
        Args:
            p1: İlk partikül
            p2: İkinci partikül
            stiffness: İpin esnekliği (1.0 = katı, <1.0 = esnek)
        """
        self.p1 = p1
        self.p2 = p2
        self.stiffness = stiffness

        # İlk mesafeyi hesapla (ipin doğal uzunluğu)
        dx = p1.x - p2.x
        dy = p1.y - p2.y
        self.rest_length = (dx * dx + dy * dy) ** 0.5

    def resolve(self):
        """İki partikül arasındaki mesafeyi sabit uzunluğa ayarla."""
        # Partiküller arasında vektor
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y

        # Mevcut mesafe
        distance = (dx * dx + dy * dy) ** 0.5

        if distance == 0:
            return  # Mesafe 0 ise çözüm yok

        # Mesafe farkı (ne kadar uzaklaştığımız)
        difference = (self.rest_length - distance) / distance

        # İstenen farklılığı uygula
        # stiffness < 1 ise yumuşak kısıtlama
        adjust_x = dx * difference * 0.5 * self.stiffness
        adjust_y = dy * difference * 0.5 * self.stiffness

        # Her iki partikülü de orta noktaya doğru taşı
        if not self.p1.is_fixed and not self.p1.is_being_dragged:
            self.p1.x += adjust_x
            self.p1.y += adjust_y

        if not self.p2.is_fixed and not self.p2.is_being_dragged:
            self.p2.x -= adjust_x
            self.p2.y -= adjust_y

    def draw(self, screen, color=(200, 200, 200), width=2, camera=None):
        """Constraint çizimi (ip segmenti). Kamera varsa world-to-screen transform uygular."""
        if camera and hasattr(camera, "world_to_screen"):
            p1_x, p1_y = camera.world_to_screen(self.p1.x, self.p1.y)
            p2_x, p2_y = camera.world_to_screen(self.p2.x, self.p2.y)
            line_width = max(1, int(width * camera.zoom))
            pygame.draw.line(
                screen,
                color,
                (int(p1_x), int(p1_y)),
                (int(p2_x), int(p2_y)),
                line_width,
            )
        else:
            pygame.draw.line(
                screen,
                color,
                (int(self.p1.x), int(self.p1.y)),
                (int(self.p2.x), int(self.p2.y)),
                width,
            )
