# Xo em · Bộ thiết kế thương hiệu

Quán cà phê pha chậm ở 93 Marina, Ecopark (Văn Giang, Hưng Yên). Tên cũ: Xofa.

> **Ghé vào. Ngồi xuống. Có em lo.**
> Slow coffee · Comfy seats

## Trong kho này có gì

| Thư mục | Nội dung | Dùng khi |
|---|---|---|
| `01-cam-nang/` | Cẩm nang thương hiệu 22 trang (PDF) và ảnh PNG từng trang | Xem tổng thể, gửi người mới, gửi xưởng tham khảo |
| `02-bo-file-thuong-hieu/` | Logo SVG/PNG (4 kiểu × 4 màu), logo 4 ô X-O-E-M, linh vật Boss · Em Ngả · Em Ngơ, 3 mẫu họa tiết, bảng màu, phông chữ | Gửi xưởng in, làm biển, đăng mạng xã hội |
| `03-website-zalo-app/` | Thiết kế website (3 trang), ứng dụng Zalo cho khách (8 màn hình), ứng dụng cho nhân viên và quản lý (8 màn hình), bản PDF | Giao cho người lập trình |
| `docs/` | Bản thiết kế bấm thử (HTML), mở `docs/index.html` hoặc bật GitHub Pages để xem online | Xem luồng gọi món như thật |
| `04-ma-nguon-thiet-ke/` | Tệp nguồn của canvas thiết kế và các script Python đã dùng để dựng | Chỉnh sửa, dựng lại khi đổi màu, đổi chữ |
| `05-luu-tru/` | Bộ Xô Ngơ, bản so sánh logo Xofa · Xô Ngơ · Xo em, bộ cốc giấy Chử Đồng Tử | Tham khảo, không dùng chính thức |

## Màu

| Tên | Mã | Vai trò |
|---|---|---|
| Đất Nung | `#C8553D` | Màu chính |
| Kem Sữa | `#F6EEDF` | Màu nền |
| Nâu Cà Phê | `#2B1D16` | Chữ, đường viền |
| Vàng Bơ | `#F2C14E` | Điểm nhấn |
| Rêu Sồi | `#5E7A4A` | Dòng trà, cây |
| Cát Mịn | `#E8D5B5` | Màu phụ |

Mã CMYK trong cẩm nang là quy đổi tham khảo. In thử trước khi in số lượng lớn.

## Phông chữ

Miễn phí trên Google Fonts, giấy phép mở OFL: **Baloo 2** (tiêu đề), **Be Vietnam Pro** (nội dung), **Patrick Hand** (chữ viết tay).

## Xem bản bấm thử trên mạng (GitHub Pages)

1. Vào **Settings → Pages** của kho này.
2. Mục *Source* chọn nhánh `main`, thư mục `/docs`, bấm **Save**.
3. Sau khoảng 1–2 phút, trang hiện ở địa chỉ GitHub hiển thị ngay trên mục Pages.

Nếu kho để chế độ riêng tư, GitHub Pages có thể cần gói trả phí. Khi đó cứ tải kho về rồi mở `docs/index.html` bằng trình duyệt.

## Việc cần điền trước khi dùng thật

- Giá món, tên món thật, số điện thoại, Wi‑Fi, thông tin chỗ đỗ xe.
- Tên tài khoản `@xoem.ecopark` và tên miền `xoem.vn` là gợi ý, cần kiểm tra còn trống.
- Ứng dụng Zalo mới là thiết kế giao diện, chưa phải ứng dụng chạy thật.
- Tra cứu nhãn hiệu “Xo em” trên cơ sở dữ liệu của Cục Sở hữu trí tuệ trước khi in số lượng lớn.

## Ghi chú về script

Các script trong `04-ma-nguon-thiet-ke/scripts/` là bản nháp đã dùng để dựng thiết kế, đang trỏ tới đường dẫn của máy dựng (`/home/claude/...`). Muốn chạy lại cần sửa đường dẫn và tải phông chữ về thư mục `fonts/`.

## Cập nhật 25/11/2026
- Website thêm 5 trang: Quà lưu niệm, Câu chuyện, Sự kiện & workshop, Tuyển dụng, Góc đọc.
- Ứng dụng Zalo thêm 14 màn hình trạng thái (xin quyền, giỏ trống, lỗi thanh toán, mất mạng, bảng lương theo công, báo cáo tuần, đổi cửa hàng...).
- Tài liệu: Đặc tả kỹ thuật và Kế hoạch đổi tên Xofa → Xo em (Claude Docs).

## Phát triển tiếp

| Muốn làm | Sửa ở đâu | Chạy lệnh |
|---|---|---|
| Đổi màu, logo, linh vật dùng chung | `04-ma-nguon-thiet-ke/scripts/brand_em.py` | `python3 brand_em.py` rồi `python3 render_brand_em.py` |
| Thêm/sửa màn hình ứng dụng Zalo | `scripts/app_screens.py` (màn chính), `scripts/app_more.py` (trạng thái) | `python3 app_build2.py` |
| Thêm/sửa trang web | `scripts/app_web.py`, `scripts/app_more.py` | `python3 app_build2.py` |
| Cập nhật bản bấm thử trên GitHub Pages | thư mục `docs/` sinh tự động | `python3 sync_repo.py` |

Cài đặt (máy có Python 3.11+):

```
pip install -r 04-ma-nguon-thiet-ke/requirements.txt
playwright install chromium
```

Phông chữ cần có: Baloo 2, Be Vietnam Pro, Patrick Hand (Google Fonts, giấy phép OFL), Archivo Black và Fredoka cho logo 4 ô. Các script đang trỏ tới thư mục phông `/home/claude/fonts`; sửa biến `F` trong `app_build2.py` cho đúng máy của bạn.

Bản bấm thử: bật **Settings → Pages → Branch `main` / thư mục `/docs`** trên GitHub, sau đó mở `https://<tên-tài-khoản>.github.io/xoem-brand/`.

Quy ước chỗ trống: `[GIÁ]`, `[SỐ]`, `[NGÀY]`, `[NHÂN VIÊN 1]`, `[SỐ ĐIỆN THOẠI]`… là dữ liệu thật cần điền trước khi in hoặc đưa lên mạng.
