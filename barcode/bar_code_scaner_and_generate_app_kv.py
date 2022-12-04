"""
Приложение запускается, как камера
Как только камера обнаруживает штрихкод, заменяет себя на соответствующий штрих-код
Картинка хранится под именем "barcode.jpeg"
Есть возможность изменения формата сохранения штрих-кода
"""
# if you on Windows you need to install vcredist_x64.exe from https://aka.ms/highdpimfc2013x64enu
# pip install zbarcam
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_garden.zbarcam import ZBarCam
from pyzbar.pyzbar import ZBarSymbol
from kivy.uix.image import Image
from kivy.clock import Clock

# pip install python-barcode[images]
from barcode.ean import EAN13
from barcode.writer import ImageWriter

class BarcodeScaner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.labl = Label(text="Наведите камеру на штрих-код карты пожалуйста")
        self.add_widget(self.labl)
        self.zbarcam= ZBarCam(code_types=[ZBarSymbol.EAN13])
        self.add_widget(self.zbarcam)

        self.clock = Clock.schedule_interval(self.read_qr_text, 1)

    def read_qr_text(self, *args):
        """Check if zbarcam.symbols is filled and stop scanning in such case"""
        if(len(self.zbarcam.symbols) > 0): # when something is detected
            self.qr_text = self.zbarcam.symbols[0].data.decode('UTF-8') # text from QR
            Clock.unschedule(self.clock)
            self.zbarcam.stop() # stop zbarcam
            self.zbarcam.ids['xcamera']._camera._device.release() # release camera
            my_code = EAN13(self.qr_text, writer=ImageWriter("JPEG"))
            my_code.save("barcode")
            self.imaged_barcode = Image(source="barcode.jpeg")       
            self.remove_widget(self.zbarcam)
            self.remove_widget(self.labl)
            self.add_widget(self.imaged_barcode)


class BarcodeScanerApp(App):

    def build(self):
        return BarcodeScaner()


if __name__ == '__main__':
    BarcodeScanerApp().run()
