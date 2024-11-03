
#ifndef servo_hpp
#define servo_hpp
#include <Adafruit_PWMServoDriver.h>

class Servo
{ 
public:
    Servo(
        Adafruit_PWMServoDriver &rServoDriver,
        uint8_t servoIdx,
        uint16_t midPulseWidth_us,
        uint16_t pulseWidthRange_us,
        uint16_t frequency_hz,
        boolean smoothed=true,
        boolean linear=true,
        boolean reversed = false);

void centre();

void set(uint16_t position);
void set(uint16_t position, uint16_t min, uint16_t max);

boolean pulse();

private: 
    Adafruit_PWMServoDriver &mServoDriver;
    uint8_t mServoIdx;
    uint16_t mMinSteps;
    uint16_t mMaxSteps;
    boolean mReversed;
    boolean mSmoothed;
    boolean mLinearMovement;
    uint16_t mDesiredSteps;
    uint16_t mCurrentSteps;

    uint16_t getNewSteps();
    uint16_t getLinearNewSteps();
    uint16_t getProportionalNewSteps();

    static uint16_t getStepsForPulseWidth(uint16_t pulseWidth, uint16_t frequency_hz);
}; 

#endif
