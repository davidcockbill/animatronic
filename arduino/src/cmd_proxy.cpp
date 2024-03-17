#include "cmd_proxy.hpp"
#include <SPI.h>

#define PROTOCOL_START 0x55
#define PROTOCOL_END 0xAA

#define LEFT_EYE_X_CMD 0
#define LEFT_EYE_Y_CMD 1
#define RIGHT_EYE_X_CMD 2
#define RIGHT_EYE_Y_CMD 3
#define EYE_LIDS_CMD 4
#define HEAD_ROTATION_CMD 5
#define HEAD_RIGHT_CMD 6
#define HEAD_LEFT_CMD 7

volatile uint16_t CmdProxy::left_eye_x_position = 1000;
volatile uint16_t CmdProxy::left_eye_y_position = 1000;
volatile uint16_t CmdProxy::right_eye_x_position= 1000;
volatile uint16_t CmdProxy::right_eye_y_position = 1000;
volatile uint16_t CmdProxy::eye_lids_position = 1000;
volatile uint16_t CmdProxy::head_rotation_position = 1000;
volatile uint16_t CmdProxy::head_left_position = 1000;
volatile uint16_t CmdProxy::head_right_position = 1000;

char CmdProxy::error_msg[50] = "";
volatile int CmdProxy::errors = 0;


CmdProxy::CmdProxy()
{
}

void CmdProxy::start()
{
    pinMode(MISO, OUTPUT);
    pinMode(MOSI, OUTPUT);
    pinMode(SCK, INPUT);
    SPCR |= _BV(SPE);
    SPI.attachInterrupt();

    Serial.println("Started SPI");
}

void CmdProxy::stop()
{
    SPI.detachInterrupt();
    Serial.println("Stopped SPI");
}

uint16_t CmdProxy::get_left_eye_x_position()
{
    return left_eye_x_position;
}

uint16_t CmdProxy::get_left_eye_y_position()
{
    return left_eye_y_position;
}

uint16_t CmdProxy::get_right_eye_x_position()
{   
    return right_eye_x_position;
}

uint16_t CmdProxy::get_right_eye_y_position()
{
    return right_eye_y_position;
}

uint16_t CmdProxy::get_eye_lids_position()
{
    return eye_lids_position;
}

uint16_t CmdProxy::get_head_rotation_position()
{
    return head_rotation_position;
}

uint16_t CmdProxy::get_head_left_position()
{
    return head_left_position;
}

uint16_t CmdProxy::get_head_right_position()
{
    return head_right_position;
}

void CmdProxy::process_errors()
{
    if (strlen(error_msg) != 0)
    {
        errors++;
        Serial.print(error_msg);
        Serial.print( "[");
        Serial.print(errors);
        Serial.println("]");

        strcpy(error_msg, "");
    }
}

void CmdProxy::set_error_msg(const char *msg)
{
    if (strlen(error_msg) == 0)
    {
        strncpy(error_msg, msg, sizeof(error_msg));
    }
}

void CmdProxy::process_command(byte spi_buffer[])
{
    int idx = 0;
    byte start = spi_buffer[idx++];
    byte key = spi_buffer[idx++];
    int value = spi_buffer[idx++] << 8;
    value |=  spi_buffer[idx++];
    byte end = spi_buffer[idx++];

    if (start == PROTOCOL_START && end == PROTOCOL_END)
    {
        switch (key)
        {
            case LEFT_EYE_X_CMD:
                left_eye_x_position = value;
                break;
            case LEFT_EYE_Y_CMD:
                left_eye_y_position = value;
                break;
            case RIGHT_EYE_X_CMD:
                right_eye_x_position = value;
                break;
            case RIGHT_EYE_Y_CMD:
                right_eye_y_position = value;
                break;
            case EYE_LIDS_CMD:
                eye_lids_position = value;
                break;
            case HEAD_ROTATION_CMD:
                head_rotation_position = value;
                break;
            case HEAD_RIGHT_CMD: 
                head_right_position = value;
                break;
            case HEAD_LEFT_CMD:
                head_left_position = value;
                break;
        }
    }
    else
    {
        set_error_msg("Protocol Marker error");
    }
}


ISR (SPI_STC_vect)
{
    static int spi_buffer_idx = 0;
    static byte spi_buffer[5];
    static int max_bytes = sizeof(spi_buffer) / sizeof(byte);

    noInterrupts();
    byte data = SPDR;
    if (spi_buffer_idx == 0 && data != PROTOCOL_START)
    {
        CmdProxy::set_error_msg("Protocol Start Marker error");
    }
    else
    {
        spi_buffer[spi_buffer_idx] = data;
        ++spi_buffer_idx;

        if (spi_buffer_idx == max_bytes)
        {
            CmdProxy::process_command(spi_buffer);
            spi_buffer_idx = 0;
        }
    }
    interrupts();
}
