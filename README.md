# 🐮🌾 Nông Trại Vui Vẻ - Game Quản Lý Thẻ Bài và Trang Trại

**Nông Trại Vui Vẻ** là một game kết hợp giữa quản lý trang trại và thẻ bài được phát triển bằng Python và Pygame. Người chơi sẽ xây dựng nông trại, thu thập động vật, tích trữ thức ăn và sử dụng các lá bài sự kiện để kiếm vàng và phát triển trang trại.

---

## 🚀 Tính năng nổi bật

- 🎴 **Thẻ bài sự kiện:** Rút và chọn 3 lá bài mỗi ngày để nhận điểm hoặc hiệu ứng đặc biệt.
- 🐷 **Động vật & Thức ăn:** Mua sắm và quản lý động vật, thức ăn từ thương gia.
- 🛍️ **Thương gia:** Ghé thăm mỗi 2 ngày với các mặt hàng ngẫu nhiên.
- 📅 **Quản lý thời gian:** Mỗi ngày là một lượt chơi với giới hạn rút bài và chơi bài.
- 💰 **Tính điểm:** Tính tổng điểm mỗi ngày dựa trên các lá bài được chơi và tài sản sở hữu.
- 🗺️ **Bản đồ tile map:** Hệ thống bản đồ nông trại sử dụng PyTMX với tile 32x32.
- 🖼️ **Giao diện tùy chỉnh:** Khung lá bài có thể bật tắt, hiệu ứng chọn bài nổi bật, bố cục vòng cung đẹp mắt.

---

## 🧱 Cấu trúc thư mục

NongTraiVuiVe/ ├── assets/ │ ├── tiles/ │ │ └── summer farm tilemap.png │ └── images/ │ └── Fences.png ├── cards/ │ ├── Card.py │ ├── card_data.py ├── gameplay.py ├── player.py ├── merchant.py ├── tile_loader.py ├── calculateScore.py ├── main.py └── README.md

---

## 🛠️ Cài đặt & Chạy game

### 1. Cài đặt thư viện cần thiết:

pip install pygame pytmx

###2. Chạy game:

python main.py
