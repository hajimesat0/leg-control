#include <Servo.h>

Servo myServo1;  // create a servo object
Servo myServo2;  // create a servo object

int const recv_size_max = 16;
char cli_string[recv_size_max] = {};
int cli_string_index = 0;

//int const potPin = A0; // analog pin used to connect the potentiometer
int const waitTime = 125;
//int potVal;  // variable to read the value from the analog pin
int angle;   // variable to hold the angle for the servo motor

enum MODE {
  STOP,
  MOVE
};
MODE mode = STOP;

void setup() {
  myServo1.attach(9); // attaches the servo on pin 9 to the servo object
  myServo2.attach(10); // attaches the servo on pin 9 to the servo object
  Serial.begin(9600); // open a serial connection to your computer
  Serial.println("start");
}

void loop() {
  int serial_readable_count = 0;
  bool is_command_received = false;
  serial_readable_count = Serial.available();
  if( serial_readable_count > 0 ) {
    for( int i=0;i<serial_readable_count; i++ ) {
      if( cli_string_index<recv_size_max ) {
        cli_string[cli_string_index] = Serial.read();
        if( cli_string[cli_string_index]=='\n' ) {
          cli_string[cli_string_index] = '\0';
          cli_string_index = 0;
          is_command_received = true;
          break;
        }
        cli_string_index ++;
        if( recv_size_max<=cli_string_index ) {
          Serial.println("recv error");
          cli_string_index = 0;
          break;
        }
      }
    }
  }

  if( is_command_received==true ) {
    String recv_string = String(cli_string);

    if( recv_string.startsWith("test",0)==true ) {
      Serial.println("test reveiced");
    } else if ( recv_string.startsWith("stop",0)==true ) {
      mode = STOP;
    } else if ( recv_string.startsWith("move",0)==true ) {
      mode = MOVE;
    }

  }

  if( mode==MOVE ) {
    myServo1.write(179);

    delay(waitTime);

    myServo1.write(0);

    delay(waitTime);

    myServo2.write(0);

    delay(waitTime);

    myServo2.write(179);

    delay(waitTime);
  }

}
