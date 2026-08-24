# Tool Tải File Cấu Hình VPN US Miễn Phí (VPN Gate)

Công cụ này tự động kết nối với API công cộng của VPN Gate (dự án nghiên cứu của Đại học Tsukuba, Nhật Bản) để tìm, lọc và tải xuống các cấu hình OpenVPN (.ovpn) có tốc độ tốt nhất tại Mỹ.

## Yêu cầu
- Máy tính đã cài đặt **Python** (sử dụng lệnh `py`).
- Phần mềm **OpenVPN Connect** (hoặc client OpenVPN bất kỳ) để sử dụng các file cấu hình đã tải.

## Cách sử dụng

1. Mở terminal tại thư mục `vpn/`.
2. Chạy lệnh sau để tải các cấu hình VPN mới nhất:
   ```bash
   py get_us_vpns.py
   ```
3. Công cụ sẽ tự động lưu 5 cấu hình VPN tốt nhất vào thư mục `us_vpns/`.
4. Nhập (Import) bất kỳ file `.ovpn` nào trong thư mục `us_vpns/` vào ứng dụng OpenVPN Connect của bạn và nhấn Connect để đổi IP sang Mỹ.

*Lưu ý: Vì đây là các VPN miễn phí từ cộng đồng, danh sách server và trạng thái kết nối có thể thay đổi liên tục. Nếu một server không kết nối được hoặc chậm, bạn có thể chạy lại script để cập nhật danh sách cấu hình mới nhất.*
