🌟 Nông Trại Vui Vẻ 🌾
Nông Trại Vui Vẻ là một trò chơi mô phỏng dạng thẻ bài, được phát triển bằng thư viện Pygame của Python. Người chơi quản lý một nông trại thông qua các hoạt động như trồng trọt, chăn nuôi, giao dịch với thương gia và tích lũy điểm số. Trò chơi mang phong cách đồ họa cổ điển medieval, với giao diện thân thiện và cơ chế kéo thả trực quan. 🎮
📑 Mục Lục

Tính Năng 🌱
Yêu Cầu Hệ Thống 💻
Cài Đặt 🔧
Hướng Dẫn Chơi 🕹️
Điều Khiển 🖱️
Cấu Trúc Dự Án 📂
Đóng Góp 🤝
Tài Liệu Tham Khảo 📚
Liên Hệ 📧

🌱 Tính Năng

🌿 Quản lý nông trại: Trồng cây, chăn nuôi động vật, thu hoạch và giao dịch vật phẩm.
🃏 Cơ chế thẻ bài: Kéo thả thẻ để thực hiện các hành động trong game.
🎨 Giao diện thân thiện: Menu điều hướng, hiệu ứng âm thanh và đồ họa phong cách medieval.
💰 Tương tác với thương gia: Mua bán vật phẩm để tối ưu hóa điểm số.
🏆 Hệ thống điểm: Tính điểm dựa trên hiệu quả quản lý nông trại.
💾 Lưu trữ tiến độ: Hỗ trợ lưu dữ liệu người chơi qua file JSON.

💻 Yêu Cầu Hệ Thống

🖥️ Hệ điều hành: Windows, macOS, hoặc Linux.
🐍 Python: Phiên bản 3.8 trở lên.
📦 Thư viện yêu cầu:
Pygame (pip install pygame)
Các thư viện Python chuẩn (không cần cài thêm): json, random, threading.


⚙️ Phần cứng: RAM 4GB, CPU 1.5GHz trở lên, màn hình độ phân giải tối thiểu 800x600.

🔧 Cài Đặt

Tải mã nguồn 📥:
git clone https://github.com/DOANHONGBAO/NongTraiVuiVe.git
cd NongTraiVuiVe


Cài đặt Python 🐍:

Tải và cài Python từ python.org.
Đảm bảo thêm Python vào PATH trong quá trình cài đặt.


Cài đặt thư viện Pygame 🎮:
pip install pygame


Chạy game 🚀:
python main.py



🕹️ Hướng Dẫn Chơi

Khởi động 🚪: Chạy main.py để vào màn hình menu chính.
Đăng nhập 🔑: Nhập tên người chơi để bắt đầu.
Chế độ chơi 🎲:
Gameplay chính: Kéo thả thẻ bài để quản lý động vật, giao dịch với thương gia, và tích lũy điểm. 🐄
Chế độ nông trại: Trồng cây, thu hoạch, và quản lý kho vật phẩm. 🌽


Kết thúc 🏁: Điểm số được hiển thị khi hoàn thành game, với tùy chọn quay lại menu.

🖱️ Điều Khiển

🖱️ Chuột trái: Nhấn để chọn, kéo thả thẻ bài hoặc tương tác với giao diện.
🔙 Phím Esc: Thoát hoặc quay về menu chính.
✅ Phím Enter: Xác nhận trong màn hình đăng nhập hoặc menu.
🖲️ Chuột di chuyển: Di chuyển con trỏ để tương tác với các nút và vật phẩm.

📂 Cấu Trúc Dự Án
NongTraiVuiVe/
│
├── main.py              # Điểm vào chính của game 🎯
├── audio.py            # Quản lý âm thanh nền 🎵
├── animal.py           # Quản lý động vật và hiệu ứng 🐖
├── plant.py            # Quản lý cây trồng và cánh đồng 🌾
├── items.py            # Hệ thống vật phẩm và kho 🎒
├── player.py           # Thông tin và hành động của người chơi 👨‍🌾
├── gameplay.py         # Logic màn hình chính 🎲
├── farming_screen.py   # Logic màn hình nông trại 🌱
├── GUI.py              # Giao diện người dùng (nút, menu) 🖼️
├── settings_manager.py # Quản lý cài đặt game ⚙️
├── merchant.py         # Logic thương gia 💸
├── transitions.py      # Hiệu ứng chuyển cảnh ✨
├── login.py            # Màn hình đăng nhập 🔐
├── menu.py             # Màn hình menu chính 📜
├── assets/             # Tài nguyên (hình ảnh, âm thanh) 🖼️🎶
└── README.md           # Tài liệu hướng dẫn 📝

🤝 Đóng Góp
Chúng tôi hoan nghênh mọi đóng góp để cải thiện game! Để đóng góp:

Fork repository từ GitHub. 🍴
Tạo branch mới:git checkout -b feature/ten-chuc-nang


Commit thay đổi:git commit -m "Mô tả thay đổi"


Push và tạo Pull Request:git push origin feature/ten-chuc-nang


Mô tả chi tiết thay đổi trong Pull Request. 📝

Vui lòng tuân thủ chuẩn mã nguồn Python (PEP 8) và thêm docstring cho các hàm mới. ✅
📚 Tài Liệu Tham Khảo

📖 Pygame Documentation
📘 Python Documentation
🎨 Nguồn tài nguyên hình ảnh: Pixabay, OpenGameArt
💡 Hỗ trợ kỹ thuật: Stack Overflow, GeeksforGeeks

📧 Liên Hệ

Tác giả: Đoàn Hồng Bảo 👨‍💻
Email: Liên hệ qua GitHub Issues
GitHub: DOANHONGBAO 🌐


🌈 Cảm ơn bạn đã trải nghiệm Nông Trại Vui Vẻ! Hãy tận hưởng niềm vui quản lý nông trại và chia sẻ ý kiến để game ngày càng hoàn thiện! 🚜
