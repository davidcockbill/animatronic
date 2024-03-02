#include "servo.hpp"


Servo::Servo(
    Adafruit_PWMServoDriver &servoDriver,
    uint8_t servoIdx,
    uint16_t midPulseWidth_us,
    uint16_t pulseWidthRange_us,
    uint16_t frequency_hz,
    boolean reversed):
        mServoDriver(servoDriver),
        mServoIdx(servoIdx),
        mMinSteps(getStepsForPulseWidth(midPulseWidth_us - (pulseWidthRange_us/2), frequency_hz)),
        mMaxSteps(getStepsForPulseWidth(midPulseWidth_us + (pulseWidthRange_us/2), frequency_hz)),
        mReversed(reversed),
        mSmoothed(true),
        mLinearMovement(true),
        mDesiredSteps(getStepsForPulseWidth(midPulseWidth_us, frequency_hz)),
        mCurrentSteps(getStepsForPulseWidth(midPulseWidth_us, frequency_hz))
{
}

void Servo::centre()
{
    set(0);
}

void Servo::set(uint16_t position, uint16_t min_position=0, uint16_t max_position=2000)
{
    uint16_t steps = mReversed ?
        map(position, min_position, max_position, mMaxSteps, mMinSteps) :
        map(position, min_position, max_position, mMinSteps, mMaxSteps);
    if (mSmoothed)
    {
        mDesiredSteps = steps;
    }
    else
    {
        mServoDriver.setPWM(mServoIdx, 0, steps);
    }
}

boolean Servo::pulse()
{
    boolean done = true;
    if (mSmoothed)
    {
        if (mDesiredSteps != mCurrentSteps)
        {
            uint16_t newSteps = getNewSteps();
            mServoDriver.setPWM(mServoIdx, 0, newSteps);
            mCurrentSteps = newSteps;
            done = false;
        }
    }
    return done;
}

uint16_t Servo::getNewSteps()
{
    return mLinearMovement ? getLinearNewSteps() : getProportionalNewSteps();
}

uint16_t Servo::getLinearNewSteps()
{
    uint16_t stepSize = 1;
    if (abs(mDesiredSteps - mCurrentSteps) > stepSize)
    {
        if (mCurrentSteps < mDesiredSteps)
        {
            return mCurrentSteps + stepSize;
        }
        else if (mCurrentSteps > mDesiredSteps)
        {
            return mCurrentSteps - stepSize;
        }
    }
    return mDesiredSteps;
}

uint16_t Servo::getProportionalNewSteps()
{
    if (abs(mDesiredSteps - mCurrentSteps) < 10)
    {
        return mDesiredSteps;
    }
    return (mDesiredSteps * 0.1) + (mCurrentSteps * 0.9);
}

uint16_t Servo::getStepsForPulseWidth(uint16_t pulseWidth_us, uint16_t frequency_hz)
{
    double cycleTime_us = 1000000 / frequency_hz;
    double singleStepTime_us = cycleTime_us / 4096;
    uint16_t stepsForPulse = pulseWidth_us / singleStepTime_us;
    return stepsForPulse;
}
