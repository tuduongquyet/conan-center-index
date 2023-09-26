#include <iostream>
#include <woff2/decode.h>

int main()
{
    uint8_t dummy;
    woff2::ComputeWOFF2FinalSize(&dummy, 1);
    return 0;
}

