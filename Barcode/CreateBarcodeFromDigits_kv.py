
# pip install python-barcode[images]
from barcode.ean import EAN13
from barcode.writer import ImageWriter

# python -m pip install --upgrade pip setuptools virtualenv
# python -m virtualenv kivy_venv
# kivy_venv\Scripts\activate
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import kivy.properties  
from kivy.properties import NumericProperty




class BarcodeHandler(GridLayout):
    input_barcode_number = ""

    def __init__(self, **kwargs):
        super(BarcodeHandler, self).__init__(**kwargs)
        self.cols = 2
        self.input_lable = Label(text =  "Input number of your barcode")
        self.add_widget(self.input_lable)
        self.texted_barcode = TextInput(text="Please write 12 digits. For example: 783456789012", multiline=False)
        self.texted_barcode.bind(on_text_validate=self.get_barcode)
        self.add_widget(self.texted_barcode)
        self.add_widget(Label(text =  "Get your jpeg barcode!"))
        self.imaged_barcode = Image()
        self.add_widget(self.imaged_barcode)


    def get_barcode(self, instance):
        if (instance.text.isdigit() == False):
            self.input_lable.text = "Please write DIGITS"
        elif (len(instance.text) != 12):
            self.input_lable.text = "Please write 12 digits"
        else:
            my_code = EAN13(instance.text, writer=ImageWriter("JPEG"))
            my_code.save("barcode")
            self.imaged_barcode.source="barcode.jpeg"
            self.imaged_barcode.reload()
class BarcodeApp(App):

    def build(self):
        return BarcodeHandler()

if __name__ == '__main__':
    BarcodeApp().run()

