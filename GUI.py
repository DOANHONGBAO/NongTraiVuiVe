import pygame

class ImageButton:
    def __init__(self, x, y, width, height, text, font, text_color, 
                 image_normal, image_hover=None, hover_text_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hover_text_color = hover_text_color or text_color
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height)) if image_hover else self.image_normal
        self.hovered = False

        # Tạo khung viền sáng khi hover (optional)
        self.border_color = (255, 255, 255)  # Trắng
        self.border_thickness = 3

    def update(self, mouse_pos):
        """Cập nhật trạng thái hover"""
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface, mouse_pos):
        """Vẽ nút lên màn hình"""
        self.update(mouse_pos)  # cập nhật hover

        # Vẽ hình nền nút
        image = self.image_hover if self.hovered else self.image_normal
        surface.blit(image, self.rect.topleft)

        # Vẽ viền sáng nếu hover
        # if self.hovered:
        #     pygame.draw.rect(surface, self.border_color, self.rect, self.border_thickness)

        # Vẽ văn bản
        if self.text:
            color = self.hover_text_color if self.hovered else self.text_color
            text_surf = self.font.render(self.text, True, color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Trả về True nếu nút được nhấn chuột trái"""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered
