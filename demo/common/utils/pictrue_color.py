# coding=utf-8
import os

from PIL import Image, ImageDraw

'''
将rgb转为hsl模式，先以h作为分割基本颜色，余下其余颜色按s，l关系区分。
color_level决定颜色级别高级，数字越小，级别越高，不同级别出现时，只保留级别高的。
'''

# def __HSL_to_RGB(h, s, l):
#     def Hue_2_RGB( v1, v2, vH ):
#         while vH<0.0: vH += 1.0
#         while vH>1.0: vH -= 1.0
#         if 6*vH < 1.0 : return v1 + (v2-v1)*6.0*vH
#         if 2*vH < 1.0 : return v2
#         if 3*vH < 2.0 : return v1 + (v2-v1)*((2.0/3.0)-vH)*6.0
#         return v1

#     if not (0 <= s <=1): raise ValueError,"s (saturation) parameter must be between 0 and 1."
#     if not (0 <= l <=1): raise ValueError,"l (lightness) parameter must be between 0 and 1."

#     r,b,g = (l*255,)*3
#     if s!=0.0:
#         if l<0.5 : var_2 = l * ( 1.0 + s )
#         else     : var_2 = ( l + s ) - ( s * l )
#         var_1 = 2.0 * l - var_2
#         r = 255 * Hue_2_RGB( var_1, var_2, h + ( 1.0 / 3.0 ) )
#         g = 255 * Hue_2_RGB( var_1, var_2, h )
#         b = 255 * Hue_2_RGB( var_1, var_2, h - ( 1.0 / 3.0 ) )

#     # return (int(round(r)),int(round(g)),int(round(b)))

def __RGB_to_HSL(r, g, b):
    if not (0 <= r <= 255): raise ValueError, "r (red) parameter must be between 0 and 255."
    if not (0 <= g <= 255): raise ValueError, "g (green) parameter must be between 0 and 255."
    if not (0 <= b <= 255): raise ValueError, "b (blue) parameter must be between 0 and 255."

    var_R = r / 255.0
    var_G = g / 255.0
    var_B = b / 255.0

    var_Min = min(var_R, var_G, var_B)  # Min. value of RGB
    var_Max = max(var_R, var_G, var_B)  # Max. value of RGB
    del_Max = var_Max - var_Min  # Delta RGB value

    l = (var_Max + var_Min) / 2.0
    h = 0.0
    s = 0.0
    if del_Max != 0.0:
        if l < 0.5:
            s = del_Max / (var_Max + var_Min)
        else:
            s = del_Max / (2.0 - var_Max - var_Min)
        del_R = (((var_Max - var_R) / 6.0) + (del_Max / 2.0)) / del_Max
        del_G = (((var_Max - var_G) / 6.0) + (del_Max / 2.0)) / del_Max
        del_B = (((var_Max - var_B) / 6.0) + (del_Max / 2.0)) / del_Max
        if var_R == var_Max:
            h = del_B - del_G
        elif var_G == var_Max:
            h = (1.0 / 3.0) + del_R - del_B
        elif var_B == var_Max:
            h = (2.0 / 3.0) + del_G - del_R
        while h < 0.0: h += 1.0
        while h > 1.0: h -= 1.0

    return (h, s, l)


# font = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', 17)
# path = u'C:\\Users\\Administrator\\Desktop\\tt%s.jpg'
# huan_num = 310
# huan_lst = [360/huan_num*i for i in range(huan_num)]
# sep = 50
# size = huan_num*sep
# im = Image.new('RGB', (size,size))
# draw = ImageDraw.Draw(im)
# for h in [i/100.0 for i in range(101, step=5)]:
# h=210/360.0
# for s in [i/100.0 for i in range(101)]:
#     for l in [i/100.0 for i in range(101)]:
#         c=HSL_to_RGB(h,s,l)
#         draw.rectangle(((s*sep*100, l*sep*100),(s*sep*100+sep-1, l*sep*100+sep-1)), c)
#         draw.text((s*sep*100, l*sep*100), str(s)+'-'+str(l), font=font, fill=(0,0,0))
# im.save(path % h)

# huan_lst = [round(i/300.0,3) for i in range(301)]
# for i,h in enumerate(huan_lst):
#   c=HSL_to_RGB(h,1,0.5)
#   draw.rectangle(((i*sep, 300),(i*sep+sep-1, 800)), c)
#   draw.text((i*sep, 600), str(h), font=font, fill=(0,0,0))
# im.save(path % h)

# a = [0,32,64,96,128,160,192,224]
# for ii,r in enumerate(a):
#     i = 0
#     for g in a:
#         for b in a:
#             draw.rectangle(((55*i, 55*ii),(55*i+50-1, 55*ii+50-1)), (r,g,b))
#             i+=1
# im.save(path)




blackline = ((0.09, 0.19), (0.19, 0.15))
s0, l0 = blackline[0]
s1, l1 = blackline[1]
black_a = (l0 - l1) * 1.0 / (s0 - s1)
black_b = l1 - black_a * s1
# print 'black_a', black_a, black_b

whiteline = ((1.0, 0.94), (0, 0.83))
s0, l0 = whiteline[0]
s1, l1 = whiteline[1]
white_a = (l0 - l1) * 1.0 / (s0 - s1)
white_b = l1 - white_a * s1
# print 'white_a', white_a,white_b

pinkline = ((1.0, 0.65), (0.2, 0.5))
s0, l0 = pinkline[0]
s1, l1 = pinkline[1]
pink_a = (l0 - l1) * 1.0 / (s0 - s1)
pink_b = l1 - pink_a * s1
# print 'pink_a', pink_a,pink_b

miline = ((1.0, 0.72), (0.1, 0.5))
s0, l0 = miline[0]
s1, l1 = miline[1]
mi_a = (l0 - l1) * 1.0 / (s0 - s1)
mi_b = l1 - mi_a * s1
# print 'mi_a', mi_a,mi_b

coffeeline = ((1.0, 0.28), (0.1, 0.5))
s0, l0 = coffeeline[0]
s1, l1 = coffeeline[1]
coffee_a = (l0 - l1) * 1.0 / (s0 - s1)
coffee_b = l1 - coffee_a * s1
# print 'coffee_a', coffee_a,coffee_b

greyaline = ((0.02, 0.5), (0.15, 0.18))
s0, l0 = greyaline[0]
s1, l1 = greyaline[1]
greya_a = (l0 - l1) * 1.0 / (s0 - s1)
greya_b = l1 - greya_a * s1
# print 'greya_a', greya_a,greya_b

greybline = ((0.05, 0.5), (0.14, 0.80))
s0, l0 = greybline[0]
s1, l1 = greybline[1]
greyb_a = (l0 - l1) * 1.0 / (s0 - s1)
greyb_b = l1 - greyb_a * s1
# print 'greyb_a', greyb_a,greyb_b

# path = 'C:\\Users\\Administrator\\Desktop\\image\\source\\d\\'


# path = 'E:\\TEMP\\source\\'
def __colorstrr(color, isprint=0):
    r, g, b = color
    h, s, l = __RGB_to_HSL(r, g, b)
    # if isprint:
    #     print r, g, b
    #     print h, s, l
    # u'白',u'米',u'黄',u'橙',u'绿',u'红',u'蓝',u'紫',u'黑',u'灰',u'粉', u'咖啡'
    if black_a * s + black_b >= l:
        return u'黑色'
    elif white_a * s + white_b <= l:
        return u'白色'
    elif greya_a * s + greya_b > l or greyb_a * s + greyb_b < l:
        return u'灰色'
    else:
        if 0.95 <= h or h < 0.042:
            if pink_a * s + pink_b <= l:  # s>0.2
                return u'粉色'
            else:
                return u'红色'
        elif 0.042 <= h < 0.10:
            if mi_a * s + mi_b <= l:
                return u'米色'
            elif coffee_a * s + coffee_b >= l:
                return u'咖啡色'
            else:
                return u'橙色'
        elif 0.10 <= h <= 0.162:
            if mi_a * s + mi_b <= l:
                return u'米色'
            else:
                return u'黄色'
        elif 0.162 < h < 0.45:
            return u'绿色'
        elif 0.45 <= h <= 0.70:
            return u'蓝色'
        elif 0.70 < h < 0.95:
            return u'紫色'


color_level = {
    1: (u'黄色', u'橙色', u'绿色', u'红色', u'蓝色', u'紫色', u'粉色'),
    2: (u'黑色', u'白色',),
    3: (u'咖啡色',),
    4: (u'米色',),
    5: (u'灰色',),
}


def __final_tags(res, xy):
    def tag_deal(c1, c2, distance):
        if tags and c1 in tags and c2 in tags:
            if (dict(res_tmp)[c1] * 100.0 / xy - dict(res_tmp)[c2] * 100.0 / xy) >= distance:
                tags.remove(c2)
            else:
                tags.remove(c1)
        return tags

    res_tmp = res
    # res_tmp_tag_lst = [i[0] for i in res_tmp]
    tags = []
    for index, i in enumerate(res_tmp):
        rate = i[1] * 100.0 / xy
        if rate > 60 or (index == 0 and rate - res_tmp[index + 1][1] * 100.0 / xy >= 25):
            return [(i[0], rate)]
        if rate >= 15:
            tags.append(i[0])
    tags = list(set(tags))
    flag = 5
    tagst = []
    for i in sorted(color_level.keys()):
        for tag in tags:
            if tag in color_level[i]:
                flag = i
                tagst.append(tag)
        if flag == i:
            break
    tags = tagst
    tags = tag_deal(u'红色', u'粉色', 0)
    tags = tag_deal(u'蓝色', u'紫色', 0)
    tags = sorted([(tag, dict(res_tmp)[tag] * 100.0 / xy) for tag in tags], key=lambda x: x[1], reverse=True)
    return tags
    # return u''.join([u''.join((t[0], str(t[1]))) for t in tags])


def dealpic_color(path):
    if os.path.isfile(path):
        im = Image.open(path)
        # x0,y0=im.size
        im.thumbnail((200, 200))
        x, y = im.size
        colors = im.getcolors(x * y)
        res = {u'白色': 0, u'米色': 0, u'黄色': 0, u'橙色': 0, u'绿色': 0, u'红色': 0, u'蓝色': 0, u'紫色': 0, u'黑色': 0,
               u'灰色': 0, u'粉色': 0, u'咖啡色': 0}
        for count, c in colors:
            colorstr = __colorstrr(c)
            res[colorstr] += count
        res = sorted(res.items(), key=lambda x: x[1], reverse=True)
        # im = Image.open(path)
        # draw = ImageDraw.Draw(im)
        xy = x * y * 1.0
        # for i in range(len(res)):
        #     text = u'%s-%s-%s%%' % (res[i][0], res[i][1], round(res[i][1] / xy * 100, 2))
        #     draw.text((0, i * 30 + 10), text, font=font)
        return __final_tags(res, xy)
        # draw.text((x0/2, 20), text, font=font,fill=(9,9,9))
        # new_img = Image.new('RGB', (x0*2, y0), 255)
        # new_img.paste(im, (x0, 0))
        # imold = Image.open(path)
        # new_img.paste(imold, (0, 0))
        # new_img.save('C:\\Users\\Administrator\\Desktop\\image\\result\\' + filename)
    else:
        return None
