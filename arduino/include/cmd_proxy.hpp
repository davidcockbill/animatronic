#include <Arduino.h>
#ifndef cmd_proxy_hpp
#define cmd_proxy_hpp


class CmdProxy
{ 
public:
    CmdProxy();

    void start();
    void stop();

    static uint16_t get_left_eye_x_position();
    static uint16_t get_left_eye_y_position();
    static uint16_t get_right_eye_x_position();
    static uint16_t get_right_eye_y_position();
    static uint16_t get_eye_lids_position();
    static uint16_t get_head_rotation_position();
    static uint16_t get_head_left_position();
    static uint16_t get_head_right_position();

    static void process_errors();
    static void set_error_msg(const char *msg);
    static void process_command(byte spi_buffer[]);

private:
    volatile static uint16_t left_eye_x_position;
    volatile static uint16_t left_eye_y_position;
    volatile static uint16_t right_eye_x_position;
    volatile static uint16_t right_eye_y_position;
    volatile static uint16_t eye_lids_position;
    volatile static uint16_t head_rotation_position;
    volatile static uint16_t head_left_position;
    volatile static uint16_t head_right_position;

    static char error_msg[];
    volatile static int errors;
};

#endif
