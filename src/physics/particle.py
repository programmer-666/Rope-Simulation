import pygame


class Particle:
    """Bir kütle/nokta temsil eder - Verlet entegrasyonu kullanır."""

    def __init__(self, x, y, radius=5, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.old_x = x  # Önceki pozisyon (Verlet için gerekli)
        self.old_y = y
        self.radius = radius
        self.color = color
        self.mass = 1.0
        self.is_fixed = False  # Sabit nokta mı?
        self.is_being_dragged = False  # Kullanıcı sürükleniyor mu?

    def update(self, dt=1.0, gravity=0.5, damping=0.99):
        """Verlet entegrasyonu ile pozisyonu günceller."""
        if self.is_fixed or self.is_being_dragged:
            return

        # Hız hesapla (position - old_position)
        vx = (self.x - self.old_x) * damping
        vy = (self.y - self.old_y) * damping

        # Önceki pozisyonu güncelle
        self.old_x = self.x
        self.old_y = self.y

        # Yeni pozisyonu hesapla
        self.x += vx
        self.y += vy

        # Yerçekimi ekle
        self.y += gravity * dt * dt

    def constrain(self, width, height):
        """Ekran sınırlarına çarpma kontrolü."""
        if self.is_fixed:
            return

        # Sağ/Sol sınırlar
        if self.x > width - self.radius:
            self.x = width - self.radius
            self.old_x = self.x + (self.x - self.old_x) * 0.5  # Çarpma dampingu
        elif self.x < self.radius:
            self.x = self.radius
            self.old_x = self.x + (self.x - self.old_x) * 0.5

        # Alt/Üst sınırlar
        if self.y > height - self.radius:
            self.y = height - self.radius
            self.old_y = self.y + (self.y - self.old_y) * 0.5
        elif self.y < self.radius:
            self.y = self.radius
            self.old_y = self.y + (self.y - self.old_y) * 0.5

    def apply_force(self, fx, fy):
        """Kütle üzerinde kuvvet uygula."""
        if self.is_fixed or self.is_being_dragged:
            return

        # F = ma => a = F/m, Verlet'de pozisyon doğrudan güncellenir
        self.x += fx / self.mass
        self.y += fy / self.mass

    def set_position(self, x, y):
        """Kütleyi doğrudan konumlandırmak için (sürükleme için)."""
        self.x = x
        self.y = y

    def draw(self, screen, camera=None):
        """Küreyi ekrana çizer. Kamera varsa world-to-screen transform uygular."""
        if camera:
            screen_x, screen_y = camera.world_to_screen(self.x, self.y)
            draw_radius = max(1, int(self.radius * camera.zoom))
            fixed_radius = max(2, int((self.radius + 2) * camera.zoom))
        else:
            screen_x, screen_y = self.x, self.y
            draw_radius = self.radius
            fixed_radius = self.radius + 2

        pygame.draw.circle(
            screen, self.color, (int(screen_x), int(screen_y)), draw_radius
        )

        # Sabit nokta için bir gösterga
        if self.is_fixed:
            pygame.draw.circle(
                screen, (255, 0, 0), (int(screen_x), int(screen_y)), fixed_radius, 2
            )
