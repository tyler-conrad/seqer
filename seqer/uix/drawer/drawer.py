from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.animation import Animation

from navigation_drawer import NavigationDrawer

Builder.load_string('''
<SidePanel>:
    y: (self.parent.y + self.parent.height - self.parent.side_panel_width) + \
       (1-self.parent._anim_progress)* \
       self.parent.side_panel_init_offset*self.parent.side_panel_width \
       if self.parent.orientation == 'vertical' \
       else self.parent.y

    x: self.parent.x - \
       (1-self.parent._anim_progress)* \
       self.parent.side_panel_init_offset*self.parent.side_panel_width \
       if self.parent.orientation == 'horizontal' \
       else self.parent.x

    height: self.parent.side_panel_width \
        if self.parent.orientation == 'vertical' \
        else self.parent.height

    width: self.parent.side_panel_width \
        if self.parent.orientation == 'horizontal' \
        else self.parent.width

    opacity: self.parent.side_panel_opacity + \
             (1-self.parent.side_panel_opacity)*self.parent._anim_progress
    canvas:
        Color:
            rgba: (0,0,0,1)
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        Color:
            rgba: (0,0,0,(1-self.parent._anim_progress)*self.parent.side_panel_darkness)
        Rectangle:
            size: self.size
            pos: self.pos

<MainPanel>:
    x: self.parent.x + \
       self.parent._anim_progress * \
       self.parent.side_panel_width * \
       self.parent.main_panel_final_offset \
       if self.parent.orientation == 'horizontal' \
       else self.parent.x

    y: self.parent.y - \
       self.parent._anim_progress * \
       self.parent.side_panel_width * \
       self.parent.main_panel_final_offset \
       if self.parent.orientation == 'vertical' \
       else self.parent.y

    size: self.parent.size
    canvas:
        Color:
            rgba: (0,0,0,1)
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        Color:
            rgba: (0,0,0,self.parent._anim_progress*self.parent.main_panel_darkness)
        Rectangle:
            size: self.size
            pos: self.pos

<-Drawer>:
    size_hint: (1,1)
    _side_panel: sidepanel
    _main_panel: mainpanel
    _join_image: joinimage
    side_panel_width: min(dp(250), 0.5*self.width)
    SidePanel:
        id: sidepanel

    MainPanel:
        id: mainpanel

    Widget:
        id: joinimage
    # Image:
    #     id: joinimage
    #     opacity: min(sidepanel.opacity, 0 if root._anim_progress < 0.00001 \
    #              else min(root._anim_progress*40,1))
    #     source: root._choose_image(root._main_above, root.separator_image)
    #     mipmap: False
    #
    #     width: root.separator_image_width \
    #         if root.orientation == 'horizontal' \
    #         else root.width
    #
    #     height: root._side_panel.height \
    #         if root.orientation == 'horizontal' \
    #         else root.separator_image_width
    #
    #     x: ((mainpanel.x - self.width + 1) if root._main_above \
    #        else (sidepanel.x + sidepanel.width - 1)) \
    #        if root.orientation == 'horizontal' \
    #        else root.x
    #
    #     y: (((mainpanel.y + mainpanel.height) - self.height + 1) if root._main_above \
    #        else ((sidepanel.y + 1))) \
    #        if root.orientation == 'vertical' \
    #        else root.y
    #
    #     allow_stretch: True
    #     keep_ratio: False
''')


class SidePanel(BoxLayout):
    pass


class MainPanel(BoxLayout):
    pass


class Drawer(NavigationDrawer):
    orientation = StringProperty('vertical')

    def on_touch_down(self, touch):
        col_self = self.collide_point(*touch.pos)
        col_side = self._side_panel.collide_point(*touch.pos)
        col_main = self._main_panel.collide_point(*touch.pos)

        if self._anim_progress < 0.001:  # i.e. closed
            def valid_region():
                if self.orientation == 'horizontal':
                    return (self.x
                            <= touch.x
                            <= (self.x + self.touch_accept_width))
                else:
                    top = (self.y + self.height)
                    return (top
                            >= touch.y
                            >= (top - self.touch_accept_width))

            if not valid_region():
                self._main_panel.on_touch_down(touch)
                return False
        else:
            if col_side and not self._main_above:
                self._side_panel.on_touch_down(touch)
                return False

            def valid_region():
                if self.orientation == 'horizontal':
                    return (self._main_panel.x
                        <= touch.x
                        <= (self._main_panel.x + self._main_panel.width))
                else:
                    return ((self._main_panel.y + self._main_panel.height)
                        >= touch.y
                        >= self._main_panel.y)

            if not valid_region():
                if self._main_above:
                    if col_main:
                        self._main_panel.on_touch_down(touch)
                    elif col_side:
                        self._side_panel.on_touch_down(touch)
                else:
                    if col_side:
                        self._side_panel.on_touch_down(touch)
                    elif col_main:
                        self._main_panel.on_touch_down(touch)
                return False

        Animation.cancel_all(self)
        self._anim_init_progress = self._anim_progress
        self._touch = touch
        touch.ud['type'] = self.state
        touch.ud['panels_jiggled'] = False  # If user moved panels back
                                            # and forth, don't default
                                            # to close on touch release
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch is self._touch:
            def progress():
                if self.orientation == 'horizontal':
                    return max(0, min(self._anim_init_progress
                        + ((touch.x - touch.ox) / self.side_panel_width), 1))
                else:
                    return max(0, min(self._anim_init_progress
                        + ((touch.oy - touch.y) / self.side_panel_width), 1))

            self._anim_progress = progress()
            if self._anim_progress < 0.975:
                touch.ud['panels_jiggled'] = True
        else:
            super(NavigationDrawer, self).on_touch_move(touch)
            return

if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.popup import Popup
    from kivy.uix.image import Image
    from kivy.core.window import Window
    from kivy.uix.widget import Widget
    from kivy.metrics import dp

    navigationdrawer = Drawer()

    side_panel = BoxLayout(orientation='vertical')
    side_panel.add_widget(Label(text='Panel label'))
    popup = Popup(title='Sidebar popup',
                  content=Label(
                      text='You clicked the sidebar\npopup button'),
                  size_hint=(0.7, 0.7))
    first_button = Button(text='Popup\nbutton')
    first_button.bind(on_release=popup.open)
    side_panel.add_widget(first_button)
    side_panel.add_widget(Button(text='Another\nbutton'))
    navigationdrawer.add_widget(side_panel)

    label_head = (
        '[b]Example label filling main panel[/b]\n\n[color=ff0000](p'
        'ull from left to right!)[/color]\n\nIn this example, the le'
        'ft panel is a simple boxlayout menu, and this main panel is'
        ' a BoxLayout with a label and example image.\n\nSeveral pre'
        'set layouts are available (see buttons below), but users ma'
        'y edit every parameter for much more customisation.')
    main_panel = BoxLayout(orientation='vertical')
    label_bl = BoxLayout(orientation='horizontal')
    label = Label(text=label_head, font_size='15sp',
                  markup=True, valign='top')
    label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
    label_bl.add_widget(label)
    label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
    main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
    main_panel.add_widget(label_bl)
    main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
    navigationdrawer.add_widget(main_panel)
    label.bind(size=label.setter('text_size'))

    def set_anim_type(name):
        navigationdrawer.anim_type = name

    def set_transition(name):
        navigationdrawer.opening_transition = name
        navigationdrawer.closing_transition = name

    modes_layout = BoxLayout(orientation='horizontal')
    modes_layout.add_widget(Label(text='preset\nanims:'))
    slide_an = Button(text='slide_\nabove_\nanim')
    slide_an.bind(on_press=lambda j: set_anim_type('slide_above_anim'))
    slide_sim = Button(text='slide_\nabove_\nsimple')
    slide_sim.bind(on_press=lambda j: set_anim_type('slide_above_simple'))
    fade_in_button = Button(text='fade_in')
    fade_in_button.bind(on_press=lambda j: set_anim_type('fade_in'))
    reveal_button = Button(text='reveal_\nbelow_\nanim')
    reveal_button.bind(on_press=
                       lambda j: set_anim_type('reveal_below_anim'))
    slide_button = Button(text='reveal_\nbelow_\nsimple')
    slide_button.bind(on_press=
                      lambda j: set_anim_type('reveal_below_simple'))
    modes_layout.add_widget(slide_an)
    modes_layout.add_widget(slide_sim)
    modes_layout.add_widget(fade_in_button)
    modes_layout.add_widget(reveal_button)
    modes_layout.add_widget(slide_button)
    main_panel.add_widget(modes_layout)

    transitions_layout = BoxLayout(orientation='horizontal')
    transitions_layout.add_widget(Label(text='anim\ntransitions'))
    out_cubic = Button(text='out_cubic')
    out_cubic.bind(on_press=
                   lambda j: set_transition('out_cubic'))
    in_quint = Button(text='in_quint')
    in_quint.bind(on_press=
                  lambda j: set_transition('in_quint'))
    linear = Button(text='linear')
    linear.bind(on_press=
                lambda j: set_transition('linear'))
    out_sine = Button(text='out_sine')
    out_sine.bind(on_press=
                  lambda j: set_transition('out_sine'))
    transitions_layout.add_widget(out_cubic)
    transitions_layout.add_widget(in_quint)
    transitions_layout.add_widget(linear)
    transitions_layout.add_widget(out_sine)
    main_panel.add_widget(transitions_layout)

    button = Button(text='toggle NavigationDrawer state (animate)',
                    size_hint_y=0.2)
    button.bind(on_press=lambda j: navigationdrawer.toggle_state())
    button2 = Button(text='toggle NavigationDrawer state (jump)',
                     size_hint_y=0.2)
    button2.bind(on_press=lambda j: navigationdrawer.toggle_state(False))
    button3 = Button(text='toggle _main_above', size_hint_y=0.2)
    button3.bind(on_press=navigationdrawer.toggle_main_above)
    main_panel.add_widget(button)
    main_panel.add_widget(button2)
    main_panel.add_widget(button3)

    Window.add_widget(navigationdrawer)

    runTouchApp()
