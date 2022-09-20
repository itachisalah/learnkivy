from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
Window.softinput_mode = 'pan'
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import ParserException
import kivy

class PlaygroundScreen(Screen):
    content_pane = ObjectProperty(None)
    editor_pane = ObjectProperty(None)
    kivy_tree = "test"

    def __init__(self, **kwargs):
        super(PlaygroundScreen, self).__init__(**kwargs)
        self.creation = Builder.load_string(self.editor_pane.text)
        self.content_pane.add_widget(self.creation)

    def on_text(self, val):
        self.kivy_tree = val
        try:
            creation = Builder.load_string(val)
        except SyntaxError as se:
            print("not valid syntax,....")
            return
        except Exception as e:
            print(type(e))
            print(e)
            return
        try:
            self.content_pane.clear_widgets()
            self.content_pane.add_widget(creation)
        except Exception as e:
            print(e)

    def save(self):
        ss= PlaygroundFileSelector(name= 'savescreen')
        app.sm.add_widget(ss)
        app.sm.current = 'savescreen'

    def open(self):
        ops= PlaygroundFileSelectorOpener(name='openscreen')
        app.sm.add_widget(ops)
        app.sm.current='openscreen'

class PlaygroundFileSelector(Screen):
    fileChooser = ObjectProperty(None)
    pathBar = StringProperty("")
    path = StringProperty('test')

    def selected(self, args):
        try:
            self.path = str(args[1][0])
        except:
            print(args)

    def save(self):
        try:
            print("saving time! saving to : {0}". format(self.ptah))
            print(app.pgs.editor_pane.text)
            f= open(self.path, 'w')
            f.write(app.pgs.editor_pane.text)
            f.close()
        except:
            pass
        app.sm.current='pgs'

    def cancel(self):
        self.path = val

class PlaygroundFileSelectorOpener(Screen):
    fileChooser = ObjectProperty(None)
    pathBar = StringProperty("")
    path = StringProperty('test')

    def selected(self, args):
        try:
            self.path = str(args[1][0])
        except:
            print(args)

    def cancel(self):
        app.sm.current= 'pgs'

    def on_text(self,val):
        self.path = val

    def open(self):
        print("opening :{0)".format(self.path))

        content = open(self.path).red()
        app.pgs.editor_pane.text = content

        app.sm.current='pgs'

class PGScreenManager(ScreenManager):
    pass

class PlaygroundApp(App):
    def build(self):
        self.sm = PGScreenManager()
        self.pgs= PlaygroundScreen(name ='pgs')
        self.sm.add_widget(self.pgs)
        self.sm.current='pgs'
        return self.sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


app = None
if __name__=='__main__':
    app = PlaygroundApp()
    app.run()