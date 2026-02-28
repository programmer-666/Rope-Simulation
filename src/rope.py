import pygame

from physics.constraint import Constraint
from physics.particle import Particle


class Rope:
    """Verlet entegrasyonu ile çalışan ip sınıfı."""

    def __init__(
        self,
        start_x,
        start_y,
        num_segments=10,
        segment_length=50,
        start_fixed=True,
        particle_color=(255, 255, 255),
        rope_color=(200, 200, 200),
    ):
        """
        Args:
            start_x: İpin başlangıç X koordinatı
            start_y: İpin başlangıç Y koordinatı
            num_segments: İpin kaç parçadan oluşacağı
            segment_length: Her segmentin uzunluğu
            start_fixed: İpin başlangıç noktası sabit mi?
            particle_color: Partiküllerin rengi
            rope_color: İpin çizgi rengi
        """
        self.particles = []
        self.constraints = []
        self.segment_length = segment_length
        self.rope_color = rope_color

        # Partikülleri oluştur
        for i in range(num_segments + 1):
            x = start_x + i * segment_length
            y = start_y

            particle = Particle(x, y, color=particle_color)

            # İlk partikül sabitse işaretle
            if i == 0 and start_fixed:
                particle.is_fixed = True

            self.particles.append(particle)

        # Constraint'leri oluştur (komşu partikülleri birbirine bağla)
        for i in range(len(self.particles) - 1):
            constraint = Constraint(
                self.particles[i], self.particles[i + 1], stiffness=1.0
            )
            self.constraints.append(constraint)

    def update(self, gravity=0.5, damping=0.99, dt=1.0, constraint_iterations=3):
        """
        İpin fizik güncelleme döngüsü.

        Args:
            gravity: Yerçekimi kuvveti
            damping: Sönümleme katsayısı (enerji kaybı)
            dt: Zaman adımı
            constraint_iterations: Constraint çözme iterasyon sayısı (daha fazla = daha katı)
        """
        # 1. Tüm partikülleri güncelle
        for particle in self.particles:
            particle.update(gravity=gravity, damping=damping, dt=dt)

        # 2. Constraint'leri çöz ( 여러 iterasyon ile daha stabil)
        for _ in range(constraint_iterations):
            for constraint in self.constraints:
                constraint.resolve()

        # 3. Ekran sınırlarına çarpma kontrolü
        width, height = pygame.display.get_surface().get_size()
        for particle in self.particles:
            particle.constrain(width, height)

    def drag_particle(self, mouse_pos, dragged_index=None):
        """
        Fare ile bir partikülü sürüklemek için.

        Args:
            mouse_pos: (x, y) fare pozisyonu
            dragged_index: Sürüklenecek partikülün indeksi (None ise en yakını bul)

        Returns:
            Sürüklenecek partikülün indeksi
        """
        mouse_x, mouse_y = mouse_pos

        if dragged_index is not None and 0 <= dragged_index < len(self.particles):
            # Belirli partikül sürükleniyor
            self.particles[dragged_index].set_position(mouse_x, mouse_y)
            return dragged_index

        # En yakın partikülü bul
        min_dist = float("inf")
        closest_idx = -1

        for i, particle in enumerate(self.particles):
            if particle.is_fixed:
                continue

            dx = particle.x - mouse_x
            dy = particle.y - mouse_y
            dist = (dx * dx + dy * dy) ** 0.5

            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        # Eğer yakında bir partikül varsa sürükle
        if closest_idx != -1 and min_dist < 50:
            self.particles[closest_idx].set_position(mouse_x, mouse_y)
            return closest_idx

        return None

    def is_mouse_over_particle(self, mouse_pos, radius=20):
        """
        Fare bir partikülün üzerinde mi kontrol et.

        Args:
            mouse_pos: (x, y) fare pozisyonu
            radius: Tıklama hassasiyeti

        Returns:
            Partikül indeksi veya None
        """
        mouse_x, mouse_y = mouse_pos

        for i, particle in enumerate(self.particles):
            if particle.is_fixed:
                continue

            dx = particle.x - mouse_x
            dy = particle.y - mouse_y
            dist = (dx * dx + dy * dy) ** 0.5

            if dist < radius:
                return i

        return None

    def draw(self, screen, camera=None):
        """
        İpi ekrana çizer.

        Args:
            screen: Pygame ekran objesi
            camera: Kamera objesi (varsa world-to-screen transform uygular)
        """
        # Constraint'leri çiz (ip segmentleri)
        for constraint in self.constraints:
            constraint.draw(screen, color=self.rope_color, width=3, camera=camera)

        # Partikülleri çiz
        for particle in self.particles:
            particle.draw(screen, camera=camera)
            # Eğer sürüklendiğinde bir gösterga
            if particle.is_being_dragged:
                if camera:
                    screen_x, screen_y = camera.world_to_screen(particle.x, particle.y)
                else:
                    screen_x, screen_y = particle.x, particle.y
                pygame.draw.circle(
                    screen, (255, 255, 0), (int(screen_x), int(screen_y)), 8, 2
                )

    def release_all(self):
        """Tüm partiküllerin sürükleme durumunu serbest bırak."""
        for particle in self.particles:
            particle.is_being_dragged = False
