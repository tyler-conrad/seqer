from kivy.lang import Builder

from seqer.uix.aligned_label import AlignedLabel

Builder.load_string('''
<ScaledLabel>:
    font_size: 72
''')


class ScaledLabel(AlignedLabel):
    def update(self, dt=None):
        if not self.texture:
            return

        padding = self.widget_padding
        padded_width = self.width - (padding[0] + padding[2])
        padded_height = self.width - (padding[1] + padding[3])
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

        x = {
            'left': padding[0] + self.x,
            'center': self.center_x - rect_width * 0.5,
            'right': self.right - (rect_width + padding[2])
        }[self.horz_align]

        y = {
            'bottom': padding[3] + self.y,
            'center': self.center_y - rect_height * 0.5,
            'top': self.top - (rect_height + padding[1]),
        }[self.vert_align]

        self.rect.pos = x, y
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
                    vert_align: 'bottom'
                    horz_align: 'center'
            BoxLayout:
                orientation: 'vertical'
                ScaledLabel:
                    horz_align: 'left'
                ScaledLabel:
                    horz_align: 'right'
                ScaledLabel:
                    vert_align: 'bottom'
                    horz_align: 'center'

    ''')))
    runTouchApp()
