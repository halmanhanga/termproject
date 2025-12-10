import sys
import struct

def get_png_size(path):
    with open(path, "rb") as f:
        data = f.read(24)
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("PNG 아님")
        width, height = struct.unpack(">II", data[16:24])
        return width, height

def get_jpg_size(path):
    with open(path, "rb") as f:
        data = f.read()

    if data[0:2] != b"\xff\xd8":
        raise ValueError("JPG 아님")

    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i+1]
        i += 2

        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            length = struct.unpack(">H", data[i:i+2])[0]
            height, width = struct.unpack(">HH", data[i+3:i+7])
            return width, height

        length = struct.unpack(">H", data[i:i+2])[0]
        i += length

    raise ValueError("JPEG 크기 정보 못 찾음")

def get_image_size(path):
    with open(path, "rb") as f:
        sig = f.read(10)

    if sig.startswith(b"\x89PNG"):
        return get_png_size(path)
    if sig[0:2] == b"\xff\xd8":
        return get_jpg_size(path)

    raise ValueError("지원하지 않는 형식")

def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py 이미지파일")
        return

    path = sys.argv[1]
    try:
        w, h = get_image_size(path)
        print(f"{path}: {w} x {h} px")
    except Exception as e:
        print("오류:", e)

if __name__ == "__main__":
    main()
