#include "cmd_proxy.hpp"
#include "servo.hpp"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define FREQUENCY 160

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

Servo left_eye_x_servo = Servo(pwm, 4, 1500, 990, FREQUENCY, true, false, true);
Servo left_eye_y_servo = Servo(pwm, 5, 1500, 990, FREQUENCY, true, false);
Servo right_eye_x_servo = Servo(pwm, 6, 1500, 990, FREQUENCY, true, false, true);
Servo right_eye_y_servo = Servo(pwm, 7, 1500, 990, FREQUENCY, true, false, true);
Servo eye_lids_servo = Servo(pwm, 8, 1400, 800, FREQUENCY, false, true);
Servo head_rotation_servo = Servo(pwm, 9, 1500, 500, FREQUENCY, true, true);
Servo head_right_servo = Servo(pwm, 10, 1500, 1000, FREQUENCY, true, true);
Servo head_left_servo = Servo(pwm, 11, 1500, 1000, FREQUENCY, true, true, true);

Servo *servos[] = {
  &left_eye_x_servo,
  &left_eye_y_servo,
  &right_eye_x_servo,
  &right_eye_y_servo,
  &eye_lids_servo,
  &head_rotation_servo,
  &head_right_servo,
  &head_left_servo,
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

    // pinMode(17, OUTPUT);
    // digitalWrite(17, LOW);
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


void process_servos()
{
    CmdProxy::process_errors();

    left_eye_x_servo.set(CmdProxy::get_left_eye_x_position());
    left_eye_y_servo.set(CmdProxy::get_left_eye_y_position());
    right_eye_x_servo.set(CmdProxy::get_right_eye_x_position());
    right_eye_y_servo.set(CmdProxy::get_right_eye_y_position());
    eye_lids_servo.set(CmdProxy::get_eye_lids_position());
    head_rotation_servo.set(CmdProxy::get_head_rotation_position());
    head_left_servo.set(CmdProxy::get_head_left_position());
    head_right_servo.set(CmdProxy::get_head_right_position());
    
    pulse();
}

void setup()
{
    Serial.begin(9600);
    servo_setup();
    proxy.start();
}

void loop()
{
    process_servos();
}
