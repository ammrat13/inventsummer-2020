/*
    This file defines the pins and structures needed for IO.
*/


// Include guard
#ifndef IO_H
#define IO_H


// Required for Arduino stuff
#include <Arduino.h>
// Required for screen IO
#include <U8g2lib.h>


// Note that pins 16 and 17 are swapped due to a bug
const uint32_t WN_LED_PIN = 1;
const uint32_t LS_LED_PIN = 2;
const uint32_t BUZZER_PIN = 7;
const uint32_t UP_BUT_PIN = 16;
const uint32_t DN_BUT_PIN = 17;

// For U8g2 Screen
extern U8G2_SSD1327_MIDAS_128X128_F_HW_I2C SCREEN;


// Include guard
#endif
