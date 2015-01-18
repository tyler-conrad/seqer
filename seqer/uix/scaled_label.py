from kivy.lang import Builder

from seqer.uix.aligned_label import AlignedLabel

Builder.load_string('''
<ScaledLabel>:
    font_size: '72dp'
''')


class ScaledLabel(AlignedLabel):
    def calc_rect_size(self):
        padding = self.widget_padding
        padded_width = self.width - (padding[0] + padding[2])
        padded_height = self.height - (padding[1] + padding[3])
        if not padded_height:
            return 0.0, 0.0
        padded_aspect = padded_width / padded_height

        tex_width, tex_height = self.texture.size
        tex_aspect = tex_width / tex_height

        if tex_aspect >= padded_aspect:
            scale_factor = padded_width / tex_width
            rect_width = padded_width
            rect_height = tex_height * scale_factor
        else:
            scale_factor = padded_height / tex_height
            rect_height = padded_height
            rect_width = tex_width * scale_factor

        return rect_width, rect_height

    def update(self, dt=None):
        if not self.texture:
            return

        rect_width, rect_height = self.calc_rect_size()
        self.rect.pos = self.calc_rect_pos(rect_width, rect_height)
        self.rect.size = rect_width, rect_height


class FontScaledLabel(ScaledLabel):
    def update(self, dt=None):
        if not self.texture:
            return

        rect_width, rect_height = self.calc_rect_size()
        tex_width, tex_height = self.texture.size

        if rect_width >= tex_width or rect_height >= tex_height:
            rect_width = tex_width
            rect_height = tex_height

        self.rect.pos = self.calc_rect_pos(rect_width, rect_height)
        self.rect.size = rect_width, rect_height


if __name__ == '__main__':
    from textwrap import dedent

    from kivy.core.window import Window
    from kivy.base import runTouchApp
    from kivy.lang import Builder

    Window.add_widget(Builder.load_string(dedent('''
        <ScaledLabel>:
            color: 1.0, 1.0, 1.0, 1.0
            text: 'aligned label really long'
            font_size: 72

        BoxLayout:
            orientation: 'vertical'

            BoxLayout:
                orientation: 'horizontal'
                ScaledLabel:
                    horz_align: 'left'
                ScaledLabel:
                    horz_align: 'right'
                ScaledLabel:
                    align: 'left', 'bottom'

            BoxLayout:
                orientation: 'vertical'
                ScaledLabel:
                    horz_align: 'left'
                ScaledLabel:
                    horz_align: 'right'
                ScaledLabel:
                    vert_align: 'bottom'
                    horz_align: 'center'

            FloatLayout:
                orientation: 'horizontal'

                Widget:
                    size_hint: None, None
                    pos: 0.0, 0.0
                    size: 100.0, 100.0

                    canvas:
                        Color:
                            rgba: 1.0, 0.0, 0.0, 1.0
                        Rectangle:
                            pos: self.pos
                            size: self.size

                FontScaledLabel:
                    size_hint: None, None
                    pos: 0.0, 0.0
                    size: 100.0, 100.0

                Widget:
                    size_hint: None, None
                    pos: 100.0, 0.0
                    size: 50.0, 50.0

                    canvas:
                        Color:
                            rgba: 1.0, 0.0, 0.0, 1.0
                        Rectangle:
                            pos: self.pos
                            size: self.size

                FontScaledLabel:
                    size_hint: None, None
                    pos: 100.0, 0.0
                    size: 50.0, 50.0
    ''')))
    runTouchApp()
