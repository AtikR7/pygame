"""pygame module for loading and rendering fonts (freetype alternative)"""

__all__ = ['Font', 'init', 'quit', 'get_default_font', 'get_init', 'SysFont']

from pygame._freetype import init, Font as _Font, get_default_resolution
from pygame._freetype import quit, get_default_font, was_init as _was_init
from pygame._freetype import __PYGAMEinit__
from pygame.sysfont import match_font, get_fonts, SysFont as _SysFont
from pygame import encode_file_path
from pygame.compat import bytes_, unicode_, as_unicode, as_bytes
from pygame import Surface as _Surface, Color as _Color, SRCALPHA as _SRCALPHA

class Font(_Font):
    """Font(filename, size) -> Font
       Font(object, size) -> Font
       create a new Font object from a file (freetype alternative)

       This Font type differs from font.Font in that it can render glyphs
       for Unicode code points in the supplementary planes (> 0xFFFF).
       """

    __encode_file_path = staticmethod(encode_file_path)
    __get_default_resolution = staticmethod(get_default_resolution)
    __default_font = encode_file_path(get_default_font())

    __unull = as_unicode(r"\x00")
    __bnull = as_bytes("\x00")

    def __init__(self, file, size=-1):
        if size <= 1:
            size = 1
        if isinstance(file, unicode_):
            try:
                bfile = self.__encode_file_path(file, ValueError)
            except ValueError:
                bfile = ''
        else:
            bfile = file
        if isinstance(bfile, bytes_) and bfile == self.__default_font:
            file = None
        if file is None:
            resolution = int(self.__get_default_resolution() * 0.6875)
            if resolution == 0:
                kwds['resolution'] = 1
        else:
            resolution = 0
        super(Font, self).__init__(file, size=size, resolution=resolution)
        self.strength = 1.0 / 12.0
        self.kerning = False
        self.origin = True
        self.pad = True
        self.ucs4 = True
        self.underline_adjustment = 1.0

    def render(self, text, antialias, color, background=None):
        """render(text, antialias, color, background=None) -> Surface
           draw text on a new Surface"""

        if text is None:
            text = ""
        if (isinstance(text, unicode_) and  # conditional and
            self.__unull in text):
            raise ValueError("A null character was found in the text")
        if (isinstance(text, bytes_) and  # conditional and
            self.__bnull in text):
            raise ValueError("A null character was found in the text")
        save_antialiased = self.antialiased
        self.antialiased = bool(antialias)
        try:
            s, r = super(Font, self).render(text, color, background)
            return s
        finally:
            self.antialiased = save_antialiased

    def set_bold(self, value):
        """set_bold(bool) -> None
           enable fake rendering of bold text"""

        self.wide = bool(value)

    def get_bold(self):
        """get_bold() -> bool
           check if text will be rendered bold"""
 
        return self.wide

    def set_italic(self, value):
        """set_italic(bool) -> None
           enable fake rendering of italic text"""

        self.oblique = bool(value)

    def get_italic(self):
        """get_italic() -> bool
           check if the text will be rendered italic"""

        return self.oblique

    def set_underline(self, value):
        """set_underline(bool) -> None
           control if text is rendered with an underline"""

        self.underline = bool(value)

    def get_underline(self):
        """set_bold(bool) -> None
           enable fake rendering of bold text"""

        return self.underline

    def metrics(self, text):
        """metrics(text) -> list
           Gets the metrics for each character in the pased string."""

        return self.get_metrics(text)

    def get_ascent(self):
        """get_ascent() -> int
           get the ascent of the font"""

        return self.get_sized_ascender()

    def get_descent(self):
        """get_descent() -> int
           get the descent of the font"""

        return self.get_sized_descender()

    def get_height(self):
        """get_height() -> int
           get the height of the font"""

        return self.get_sized_ascender() - self.get_sized_descender() + 1

    def get_linesize(self):
        """get_linesize() -> int
           get the line space of the font text"""

        return self.get_sized_height();

    def size(self, text):
        """size(text) -> (width, height)
           determine the amount of space needed to render text"""

        return self.get_rect(text).size

FontType = Font

def get_init():
   """get_init() -> bool
      true if the font module is initialized"""

   return _was_init()

def SysFont(name, size, bold=0, italic=0, constructor=None):
    """pygame.ftfont.SysFont(name, size, bold=False, italic=False, constructor=None) -> Font
       create a pygame Font from system font resources (freetype alternative)

       This will search the system fonts for the given font
       name. You can also enable bold or italic styles, and
       the appropriate system font will be selected if available.

       This will always return a valid Font object, and will
       fallback on the builtin pygame font if the given font
       is not found.

       Name can also be a comma separated list of names, in
       which case set of names will be searched in order. Pygame
       uses a small set of common font aliases, if the specific
       font you ask for is not available, a reasonable alternative
       may be used.

       if optional contructor is provided, it must be a function with
       signature constructor(fontpath, size, bold, italic) which returns
       a Font instance. If None, a pygame.ftfont.Font object is created.
    """
    if constructor is None:
        def constructor(fontpath, size, bold, italic):
            font = Font(fontpath, size)
            font.set_bold(bold)
            font.set_italic(italic)
            return font

    return _SysFont(name, size, bold, italic, constructor)

del _Font, get_default_resolution, encode_file_path, as_unicode, as_bytes
