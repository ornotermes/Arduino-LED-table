#include <Adafruit_NeoPixel.h>

#define PIN 13

#define WIDTH 16
#define HEIGHT 16

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(HEIGHT * WIDTH, PIN, NEO_GRB + NEO_KHZ800);

int PosX = 0;
int PosY = 0;

int Pixel = 0;

void setup()
{
 Serial.begin( 115200 );
 strip.begin();
 strip.show();
 GoTo(0,0);
}

void loop()
{
  int r,g,b,y,x;
  if (Serial.available() > 0)
  {
    char command = Serial.read();
    switch (command)
    {
      case '?': //What is this device?
        Serial.print("LED_TABLE,W16,H16,R8,G8,B8\n");
        Serial.print("COMMANDS,\"G(oTo)X,Y\",\"S(et)RGB\",\"D(isplay)\",\"C(lear)\"\n");
        break;
      case 'G': //GoTo
      case 'g':
        while(!Serial.available());
        x = Serial.read();
        while(!Serial.available());
        y = Serial.read();
        GoTo(x, y);
        break;
      case 'S': //Set
      case 's':
        while(!Serial.available());
        r = Serial.read();
        while(!Serial.available());
        g = Serial.read();
        while(!Serial.available());
        b = Serial.read();
        strip.setPixelColor(Pixel, r, g ,b);
        Next();
        break;
      case 'D': //Display
      case 'd':
        strip.show();
        Serial.print("K");
        break;
      case 'C': //Clear
      case 'c':
        for(int i = 0; i < HEIGHT * WIDTH; i++)
        {
          strip.setPixelColor(i, 0, 0, 0);
        }
        GoTo(0,0);
        Serial.print("K");
        break;
    }
  }
}

void GoTo(int x, int y)
{
  PosX = x = constrain(x, 0, WIDTH-1);
  PosY = y = constrain(y, 0, HEIGHT-1);
  if(!(y & 1)) x = WIDTH-1 - x;
  
  Pixel = WIDTH*y + x;
}
void Next()
{
  int x = PosX, y = PosY;
  if (x < WIDTH-1) x++;
  else
  {
    x = 0;
    if (y < HEIGHT-1) y++;
    else y = 0;
  }
  GoTo(x, y);
}

