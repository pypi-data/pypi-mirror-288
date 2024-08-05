import wx
from ctypes import windll

# 폰트 로드
def load_font(font_path, font_name, size):
    '''
    폰트 리소스를 로드해서 wxpython Font로 반환
    '''
    windll.gdi32.AddFontResourceW(font_path)
    font = wx.Font(size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, font_name)
    return font


