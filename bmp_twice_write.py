from random import randint
from re import findall


#  ************** BMP 生成部分START **************

# 获取颜色
def get_color( color: tuple = (0, 0, 0) ):
    return "".join(chr(x) for x in color)[ ::-1 ]


# 获取长度
def get_hex( i: int = "", byte: int = 1 ):
    return "".join(
        chr(int(x, 16)) for x in findall("\w{2}", hex(i)[ 2: ].zfill(byte * 2))[ ::-1 ]
    )


# 生成bmp图像字节流
def BMP( width: int = 256, height: int = 256, color: tuple = (-1, -1, -1), hideString: str = "<?php phpinfo(); ?>" ):
    # 初始化一些24位BMP的固有信息
    BMP_image = {
        "head": "\x42\x4D",
        "OffBits": get_hex(i = 54, byte = 4),
        "bSize": get_hex(i = 40, byte = 4),
        "width": get_hex(i = width, byte = 4),
        "height": get_hex(i = height, byte = 4),
        "Planes": get_hex(i = 1, byte = 2),
        "BigCount": get_hex(i = 24, byte = 2),
        "Compression": get_hex(i = 0, byte = 4),
        "XpelsPerMete": get_hex(i = 0, byte = 4),
        "YpelsPerMete": get_hex(i = 0, byte = 4),
        "ClrUsed": get_hex(i = 0, byte = 4),
        "ClrImportant": get_hex(i = 0, byte = 4),
    }

    # 各个像素的rbg，从左往右，从下往上
    Color_part = ""
    String_part = [hideString[i*3:(i+1)*3] for i in range(len(hideString)//3 + 1)]
    Write = False
    if height * width < len(hideString) * 2.5:
        print("Error -> string too long.")
        exit()


    for row in range(height):
        if not Write and row >= height //2:
            Write = True

        for col in range(width):
            if Write:
                if len(String_part) != 0:
                    stringPart = String_part.pop(0)
                    if len(stringPart) < 3:
                        stringPart += "\x00" * (3 - len(stringPart))
                    Color_part += stringPart
                    continue
                else:
                    Write = False
            Color_part += get_color(
            color = (
                    randint(0, 255) if color[ 0 ] == -1 else color[ 0 ],
                    randint(0, 255) if color[ 1 ] == -1 else color[ 1 ],
                    randint(0, 255) if color[ 2 ] == -1 else color[ 2 ],
                )
            )

    BMP_image[ "SizeImage" ] = get_hex(i = len(Color_part), byte = 4)
    BMP_image[ "Size" ] = get_hex(i = len(Color_part) + 54, byte = 4)

    # 组装各个部分
    image = (
            BMP_image[ "head" ]
            + BMP_image[ "Size" ]
            + get_hex(i = 0, byte = 2 + 2)
            + BMP_image[ "OffBits" ]
            + BMP_image[ "bSize" ]
            + BMP_image[ "width" ]
            + BMP_image[ "height" ]
            + BMP_image[ "Planes" ]
            + BMP_image[ "BigCount" ]
            + BMP_image[ "Compression" ]
            + BMP_image[ "SizeImage" ]
            + BMP_image[ "XpelsPerMete" ]
            + BMP_image[ "YpelsPerMete" ]
            + BMP_image[ "ClrUsed" ]
            + BMP_image[ "ClrImportant" ]
            + Color_part
    )

    return image.encode("latin1")


#  ************** BMP 生成部分END **************

if __name__ == '__main__':
    with open("a.bmp","wb") as f:
        f.write(BMP(width=256,height=256,color=(200,0,225),hideString="<?php phpinfo(); ?>"))
