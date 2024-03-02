#include "cmd_proxy.hpp"
#include "servo.hpp"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define FREQUENCY 160

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

Servo left_eye_x_servo = Servo(pwm, 0, 1440, 450, FREQUENCY);
Servo left_eye_y_servo = Servo(pwm, 1, 1600, 400, FREQUENCY);
Servo right_eye_x_servo = Servo(pwm, 2, 1450, 450, FREQUENCY);
Servo right_eye_y_servo = Servo(pwm, 3, 1550, 400, FREQUENCY, true);
Servo eye_lids_servo = Servo(pwm, 4, 1400, 800, FREQUENCY);
Servo head_rotation_servo = Servo(pwm, 5, 1500, 500, FREQUENCY);
Servo head_right_servo = Servo(pwm, 6, 1500, 1650, FREQUENCY, true);
Servo head_left_servo = Servo(pwm, 7, 1500, 1650, FREQUENCY);

Servo *servos[] = {
  &left_eye_x_servo,
  &left_eye_y_servo,
  &right_eye_x_servo,
  &right_eye_y_servo,
  &eye_lids_servo,
  &head_rotation_servo,
};

CmdProxy proxy = CmdProxy();

void servo_setup()
{
    Serial.println("Servo setup");

    pwm.begin();
    pwm.setPWMFreq(FREQUENCY);

    for (Servo *pServo : servos)
    {
        pServo->centre();
    }
}

boolean pulse()
{
    boolean done = true;
    for (Servo *pServo : servos)
    {
        done &= pServo->pulse();
    }
    return done;
}

void setup()
{
    Serial.begin(9600);
    servo_setup();
    proxy.start();
}

void loop()
{
    left_eye_x_servo.set(CmdProxy::get_left_eye_x_position());
    left_eye_y_servo.set(CmdProxy::get_left_eye_y_position());
    right_eye_x_servo.set(CmdProxy::get_right_eye_x_position());
    right_eye_y_servo.set(CmdProxy::get_right_eye_y_position());
    head_rotation_servo.set(CmdProxy::get_head_rotation_position());
    head_left_servo.set(CmdProxy::get_head_left_position());
    head_right_servo.set(CmdProxy::get_head_right_position());
    
    pulse();
    delay(10);
}
