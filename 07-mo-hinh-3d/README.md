# Linh vật 3D · Boss, Em Ngả, Em Ngơ

Ba linh vật trong cẩm nang 2D, dựng lại thành mô hình 3D kiểu nhân vật game: có khung xương, hoạt ảnh đặt tên, vật liệu vải, lông nhung và da vảy, kèm ảnh dựng và trang xem 3D.

Xem online: https://qa-io-vn.github.io/xoem-brand/3d/

## Trong thư mục này

| Thư mục | Nội dung |
|---|---|
| `glb/` | Mô hình dùng ngay cho game, web, Zalo Mini App. Mỗi em một tệp `.glb` (bản đầy đủ) và một tệp `-lite.glb` (khoảng một nửa số tam giác, hợp điện thoại). |
| `blend/` | Tệp nguồn Blender 5.2, mở ra sửa trực tiếp. |
| `anh/` | Ảnh dựng PNG: ảnh chính (`-hero`), nền trong suốt (`-trong-suot`), bảng xoay bốn góc (`-model-sheet`), ảnh cả nhà. `anh/web/` là bản JPG nhẹ cho trang xem. |
| `texture/` | Ba bản đồ pháp tuyến lặp liền: vải dệt, lông nhung, da vảy. |
| `xem-3d.html` | Trang xem 3D: xoay, phóng to, bấm từng động tác, bật tắt viền nét và kiểu tô hoạt hình. Bản đăng trên GitHub Pages nằm ở `docs/3d/`. |

## Từng em

| Em | Tệp | Tam giác (đầy đủ / lite) | Động tác |
|---|---|---|---|
| Boss | `Boss.glb` | 120.476 / 55.176 | `Idle` thở đều, chớp mắt, hơi cà phê bay · `Pat` vỗ tay vịn mời ngồi |
| Em Ngả | `Em-Nga.glb` | 79.828 / 39.496 | `Sleep` thở, bong bóng mũi phồng xẹp, chữ z bay · `Stir` cựa mình, vươn vai, vỡ bong bóng |
| Em Ngơ | `Em-Ngo.glb` | 114.560 / 42.384 | `Idle` nhún, chớp mắt, vẫy đuôi · `Walk` đi bộ lặp · `Forget` nghiêng đầu, nhún vai, dấu hỏi to ra |
| Sofa | `Sofa-Em-Nga.glb` | 72.884 / 33.096 | Đạo cụ, không có hoạt ảnh. Mặt đệm cao 0,556 m, đặt Em Ngả lên đó ở tỉ lệ 0,9. |

Đơn vị mét, trục Y hướng lên, nhân vật quay mặt về +Z theo chuẩn glTF. Tên trái phải (`_L`, `_R`) tính theo hướng của nhân vật.

## Chi tiết đã thêm so với bản 2D

- **Boss:** vải dệt có ánh nhung, viền chỉ đậu quanh đệm và lưng ghế, nút bọc kiểu trám sau lưng, 35 đinh đồng quanh thân, cuộn tay vịn có nút, chân gỗ tiện, đĩa lót sứ hai viền đất nung, lông mày viền chỉ, mắt có tròng nâu cà phê và đốm sáng.
- **Em Ngả:** lông nhung, 46 mũi khâu quanh viền bụng, năm gai nệm vàng đậm, nhãn gối thêu hạt cà phê, bong bóng mũi trong suốt, lông mi, má hồng, đệm chân hồng, chỏm lông xoăn, chóp đuôi cát mịn, chữ z bằng phông Patrick Hand.
- **Em Ngơ:** da vảy rêu, lá rêu dọc sống lưng, vây tai có gân, đốm rêu nhạt, móng chân, ngón tay, đường khâu chữ thập trên bụng, răng và lưỡi có rãnh, ly giấy có quai và băng đất nung, mặt cà phê có latte hình trái tim, đuôi mũi tên đất nung, dấu hỏi nổi.

## Đưa vào dự án

- **Unity:** cài gói glTFast rồi kéo `.glb` vào Assets.
- **Godot 4:** kéo `.glb` vào dự án, AnimationPlayer có đủ tên động tác.
- **Web / Zalo Mini App:** three.js `GLTFLoader`. Viền nét Nâu Cà Phê không nằm trong tệp. Mỗi bộ phận có thuộc tính `outline` (bề dày viền, mét) trong `extras`, trang `xem-3d.html` dùng nó để vẽ viền bằng kỹ thuật vỏ lật mặt.
- **Xem nhanh trên máy:** chạy `python3 -m http.server` trong thư mục này rồi mở `http://localhost:8000/xem-3d.html`.

## Dựng lại

Mã nguồn nằm ở `04-ma-nguon-thiet-ke/3d/`. Cần Blender 5.2 trở lên.

```
BLENDER=/Applications/Blender.app/Contents/MacOS/Blender
for c in boss nga ngo sofa; do
  $BLENDER -b --factory-startup --python 04-ma-nguon-thiet-ke/3d/xoem3d_build.py -- 07-mo-hinh-3d $c duong/toi/PatrickHand-Regular.ttf
done
for m in hero cutout sheet group; do
  $BLENDER -b --factory-startup --python 04-ma-nguon-thiet-ke/3d/xoem3d_render.py -- 07-mo-hinh-3d $m all 07-mo-hinh-3d/anh
done
```

| Muốn đổi | Sửa ở đâu |
|---|---|
| Màu, vật liệu, độ nhung | `PALETTE` và `define_standard_materials()` trong `xoem3d_core.py` |
| Hình dáng, chi tiết từng em | `xoem3d_boss.py`, `xoem3d_nga.py`, `xoem3d_ngo.py`, `xoem3d_sofa.py` |
| Động tác | hàm `animate()` cuối mỗi tệp nhân vật |
| Ánh sáng, góc máy, viền nét khi dựng ảnh | `xoem3d_render.py` |

Phông Patrick Hand (giấy phép OFL) chỉ dùng lúc dựng để tạo chữ z và dấu hỏi thành khối 3D, tệp `.glb` không cần cài phông.
