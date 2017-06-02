#coding:utf8
'''
Created on 2015年4月16日

@author: 孟晓鑫

'''
import qrcode
import Image

#生成二维码
def create_qrcode(url,qrcode_url,image_w,image_h):
    '''
    url 生成二维码的超链接必须加上    eg： http://www.fuwo.com
    qrcode_url 生成二维码 图片的存储目录    eg :/data/media/fuwo/upload/125/007d044741e505cd91c4a8c873e23bfc/origin.jpg
    
    image_w   二维码的尺寸 宽度   数据类型为 int
    image_h    二维码的尺寸 高度  数据类型为 int
    
    The version parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a 21x21 matrix). Set to None and use the fit parameter when making the code to determine this automatically.

    The error_correction parameter controls the error correction used for the QR Code. The following four constants are made available on the qrcode package:
    
    ERROR_CORRECT_L
    About 7% or less errors can be corrected.
    ERROR_CORRECT_M (default)
    About 15% or less errors can be corrected.
    ERROR_CORRECT_Q
    About 25% or less errors can be corrected.
    ERROR_CORRECT_H.
    About 30% or less errors can be corrected.
    The box_size parameter controls how many pixels each “box” of the QR code is.
    
    The border parameter controls how many boxes thick the border should be (the default is 4, which is the minimum according to the specs).

    ''' 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image()
    img = img.resize((image_w, image_h), Image.ANTIALIAS) 
    img.save(qrcode_url)
    
    pass

#创建带有logo的二维码
def create_qrcode_logo(url,qrcode_url,logo_url,image_w,image_h):
    '''
     url 生成二维码的超链接必须加上    eg： http://www.fuwo.com 数据类型为   字符串
     qrcode_url 生成二维码 图片的存储目录    eg :/data/media/fuwo/upload/125/007d044741e505cd91c4a8c873e23bfc/origin.png 数据类型为   字符串
     logo_url   logo的绝对路径                        eg：/data/media/fuwo/upload/125/007d044741e505cd91c4a8c873e23bfc/logo.png  数据类型为  字符串
     image_w   二维码的尺寸 宽度   数据类型为 int
     image_h    二维码的尺寸 高度  数据类型为 int
     
          参数含义：
     version：值为1~40的整数，控制二维码的大小（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
    
     error_correction： 控制二维码的错误纠正功能。可取值下列4个常量。
     ERROR_CORRECT_L：  大约7%或更少的错误能被纠正。
     ERROR_CORRECT_M （默认）：大约15%或更少的错误能被纠正。
     ERROR_CORRECT_Q：  大约25%或更少的错误能被纠正。
     ERROR_CORRECT_H:  大约30%或更少的错误能被纠正。
    
     box_size：控制二维码中每个小格子包含的像素数。
    
     sborder：控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）

    ''' 
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(url)
    qr.make(fit=True)
     
    img = qr.make_image()
    img = img.convert("RGBA")
     
    logo = Image.open(logo_url,"r")
     
    img_w, img_h = img.size
    icon_w, icon_h = logo.size
   
    #icon = logo.resize((icon_w, icon_h), Image.ANTIALIAS) 
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    logo.load()
    img.paste(logo, (w, h), logo.split()[3])    
    img = img.resize((image_w, image_h), Image.ANTIALIAS) 
    img.save(qrcode_url)

    pass
 
