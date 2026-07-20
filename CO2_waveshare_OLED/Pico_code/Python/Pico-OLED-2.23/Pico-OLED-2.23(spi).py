from machine import Pin,SPI
import framebuf
import time

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class OLED_2inch23(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 32
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()
        
        self.white =   0xffff
        self.balck =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        
        self.write_cmd(0xAE)#turn off OLED display*/
    
        self.write_cmd(0x04)#turn off OLED display*/

        self.write_cmd(0x10)#turn off OLED display*/ 
    
        self.write_cmd(0x40)#set display start linen(40h~7Fh) 
        self.write_cmd(0x81)#Set SEG Output Current Brightness 
        self.write_cmd(0x80)#set contrast control register   
        self.write_cmd(0xA1)#Set Segment Re-map 
        self.write_cmd(0xA6)#Set Normal/Inverse Display(A7 Inverse)
        self.write_cmd(0xA8)#Set Multiplex Ratio
        self.write_cmd(0x1F)#Set Higher Column Start Address for Page Addressing Mode (10h~1Fh) 
        self.write_cmd(0xC8)#Set COM Output Scan Direction (C0h/C8h) 
        self.write_cmd(0xD3)#Set Display Offset 
        self.write_cmd(0x00)#Set Lower Column Start Address for Page Addressing Mode (00h~0Fh) 
        self.write_cmd(0xD5)#Set Display Clock Divide Ratio/ Oscillator Frequency 
        self.write_cmd(0xF0) #-not offset
        self.write_cmd(0xD8)#Set Area Color Mode ON/OFF & Low Power Display Mode 
        self.write_cmd(0x05)
        self.write_cmd(0xD9)#--set pre-charge period
        self.write_cmd(0xC2)
        self.write_cmd(0xDA) #--set com pins hardware configuration 
        self.write_cmd(0x12)   
        self.write_cmd(0xDB)#Set VCOMH Deselect Level
        self.write_cmd(0x08) 
        self.write_cmd(0xAF) #Set Display ON/OFF (ACh/AEh/AFh) 

    def show(self):
        for page in range(0,4):
            self.write_cmd(0xb0 + page)
            self.write_cmd(0x04)
            self.write_cmd(0x10)
            self.dc(1)
            for num in range(0,128):
                self.write_data(self.buffer[page*128+num])
        
          
if __name__=='__main__':

    OLED = OLED_2inch23()
    OLED.fill(0x0000) 
    OLED.show()
    OLED.rect(0,0,128,32,OLED.white)
    OLED.rect(10,6,20,20,OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.fill_rect(40,6,20,20,OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.rect(70,6,20,20,OLED.white)
    time.sleep(0.5)
    OLED.show()
    OLED.fill_rect(100,6,20,20,OLED.white)
    time.sleep(0.5)
    OLED.show()
    time.sleep(1)
    
    OLED.fill(0x0000)
    OLED.line(0,0,5,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,20,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,35,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,65,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,95,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,125,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,125,21,OLED.white)
    OLED.show()
    time.sleep(0.1)
    OLED.line(0,0,125,11,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(0,0,125,3,OLED.white)
    OLED.show()
    time.sleep(0.01)
    
    OLED.line(127,1,125,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,110,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,95,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,65,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,35,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,1,31,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,1,21,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,1,11,OLED.white)
    OLED.show()
    time.sleep(0.01)
    OLED.line(127,1,1,1,OLED.white)
    OLED.show()
    time.sleep(1)
    
    OLED.fill(0x0000) 
    OLED.text("128 x 32 Pixels",1,2,OLED.white)
    OLED.text("Pico-OLED-2.23",1,12,OLED.white)
    OLED.text("SSD1503",1,22,OLED.white)  
    OLED.show()
    
    time.sleep(1)
    OLED.fill(0xFFFF)



