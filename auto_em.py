import qrcode
from PIL import Image
from BlindWatermark import test_ncc
from BlindWatermark import watermark


watermark_size = (64, 64)

# watermark encode


def wm_enc(ori_img_path, watermark_str, out_path):
    # 4399和2333是两个随机种子,36和20是用于嵌入算法的除数,理论上第一个除数要大于第二个,除数越大鲁棒性越强,但是除数越大,输出图片的失真越大,需要权衡后决定
    #这两个随机种子最好对不同图片有不同的取值, 防止种子暴露而使得所有图片失去保护
    # 第二个除数可以不加,增加对水印鲁棒性没有明显的提升,但是会一定情况想影响输出图片的质量
    bwm1 = Image.open(ori_img_path)
    resize_ = 1
    if bwm1.size[0] < watermark_size[0] * 8:
        resize_ = watermark_size[0] * 10 / bwm1.size[0]
    if bwm1.size[1] * resize_ < watermark_size[1] * 8:
        resize_ = watermark_size[1] * 10 / bwm1.size[1]
    if resize_ > 1:
        bwm1 = bwm1.resize([int(i * resize_)
                            for i in bwm1.size], Image.ANTIALIAS)
        bwm1.save(ori_img_path)
    bwm1 = watermark(4399, 2333, 36, 20)

    # 读取原图
    bwm1.read_ori_img(ori_img_path)

    watermark_path = 'qrcode_temp.png'

    gen_qrcode(watermark_str, watermark_path)

    # 读取水印
    bwm1.read_wm(watermark_path)

    # 在原图中嵌入水印并输出到'out.png'
    # 用NCC数值化判断输出图片与原图的相似度
    bwm1.embed(out_path)


# watermark decode
def wm_dec(enc_img_path, watermark_path):
    bwm1 = Image.open(enc_img_path)
    resize_ = 1
    if bwm1.size[0] < watermark_size[0] * 8:
        resize_ = watermark_size[0] * 10 / bwm1.size[0]
    if bwm1.size[1] * resize_ < watermark_size[1] * 8:
        resize_ = watermark_size[1] * 10 / bwm1.size[1]
    if resize_ > 1:
        bwm1 = bwm1.resize([int(i * resize_)
                            for i in bwm1.size], Image.ANTIALIAS)
        bwm1.save(enc_img_path)
    # 用之前嵌入水印的参数,实例化对象,注意需要设定水印的长宽
    bwm1 = watermark(4399, 2333, 36, 20, wm_shape=watermark_size)
    # 注意需要在输出的水印的同级目录下创建 Y_U_V/ 文件夹, 否则单通道提取出来的水印不会被保存
    bwm1.extract(enc_img_path, watermark_path)


def gen_qrcode(s, qrcode_path):
    img = qrcode.make(s)
    # resize_ = [int(ori_size / 10) for ori_size in ori_sizes]
    img = img.resize(watermark_size)
    img.save(qrcode_path)


# wm_enc('pic/sfz.jpg', '仅用于银行', 'pic/out.png')

wm_dec('pic/broken.png', 'pic/wm_out.png')

# gen_qrcode('用户xxx', 'pic/qrcode.png')
