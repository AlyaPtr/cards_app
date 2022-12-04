"""
Приложение запускается, как камера
Как только камера обнаруживает штрихкод, заменяет себя на соответствующий штрих-код
Картинка хранится под именем "barcode.png"
Есть возможность изменения формата сохранения штрих-кода

Сейчас работает только для QRCODE, EAN13, CODE128, I25
"""

# if you on Windows you need to install vcredist_x64.exe from https://aka.ms/highdpimfc2013x64enu
# pip install zbarcam
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window

from kivy_garden.zbarcam import ZBarCam
from pyzbar.pyzbar import ZBarSymbol
from kivy.uix.image import Image
from kivy.clock import Clock

# pip install python-barcode[images]
import barcode
from barcode.ean import EAN13
from barcode.codex import Code128
from barcode.itf import ITF #I25

# pip install qrcode
import qrcode

class CardScaner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.label_with_instruction = Label(text="Наведите камеру на штрих-код карты пожалуйста")
        self.add_widget(self.label_with_instruction)
        self.zbarcam= ZBarCam()
        #code_types=[ZBarSymbol.EAN13]
        #self.add_widget(self.zbarcam)  
        #self.zbarcam.size = (Window.size[0], Window.size[1])  

        self.add_widget(self.zbarcam)

        self.clock = Clock.schedule_interval(self.read_qr_text, 1)

    def read_qr_text(self, *args):
        """Check if zbarcam.symbols is filled and stop scanning in such case"""
        if(len(self.zbarcam.symbols) > 0): # when something is detected
            #print(', '.join([str(symbol) for symbol in self.zbarcam.symbols]))
            standart_of_code = self.zbarcam.symbols[0].type # type of standart of code (one of card_information or qr-code)
            texted_code = self.zbarcam.symbols[0].data.decode('UTF-8') # information from card
            if standart_of_code == 'QRCODE':
                img = qrcode.make(texted_code)
                img.save("card_information.png")
            elif standart_of_code == 'EAN13':
                img = EAN13(texted_code, writer=ImageWriter("PNG"))
                img.save("card_information")
            elif standart_of_code == 'CODE128':
                img = Code128(texted_code, writer=ImageWriter("PNG"))
                img.save("card_information")
            elif standart_of_code == 'I25':
                img = ITF(texted_code, writer=ImageWriter("PNG"))
                img.save("card_information")
            else:
                return
            # image with generated code saved as card_information.png

            Clock.unschedule(self.clock) # stop repeating
            self.zbarcam.stop() # stop zbarcam
            self.zbarcam.ids['xcamera']._camera._device.release() # release camera

            self.imaged_barcode = Image(source="card_information.png")   
                
            self.remove_widget(self.zbarcam)
            self.remove_widget(self.label_with_instruction)
            self.add_widget(self.imaged_barcode)


class CardScanerApp(App):

    def build(self):
        return CardScaner()

if __name__ == '__main__':
    CardScanerApp().run()
