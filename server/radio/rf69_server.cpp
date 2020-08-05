#include <bcm2835.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#include <RH_RF69.h>
#include <RH_RF69.h>

#define RF_CS_PIN RPI_V2_GPIO_P1_26
#define RF_RST_PIN RPI_V2_GPIO_P1_22

#define RF_FREQUENCY 433.0

RH_RF69 rf69(RF_CS_PIN);

// Ctrl-C Handler
volatile sig_atomic_t force_exit = false;

void sig_handler(int sig)
{
  printf("\n%s Break received, exiting!\n", __BASEFILE__);
  force_exit=true;
}

int main(int argc, const char *argv[])
{
    signal(SIGINT, sig_handler);
    printf("%s\n", __BASEFILE__);

    if (!bcm2835_init())
    {
        fprintf(stderr, "%s bcm2835_init() Failed\n\n", __BASEFILE__);
        return 1;
    }

    printf("RF69 CS=GPIO%d", RF_CS_PIN);

#ifdef RF_RST_PIN
    printf(", RST=GPIO%d", RF_RST_PIN);
    // Pulse a reset on module
    pinMode(RF_RST_PIN, OUTPUT);
    digitalWrite(RF_RST_PIN, LOW);
    bcm2835_delay(150);
    digitalWrite(RF_RST_PIN, HIGH);
    bcm2835_delay(100);
#endif

    if (!rf69.init())
    {
        fprintf(stderr, "\nRF69 module init failed, Please verify wiring/module\n");
    }
    else
    {
        printf("\nRF69 module seen OK!\r\n");

        rf69.setTxPower(20);

        // Now we change back to Moteino setting to be
        // compatible with RFM69 library from lowpowerlabs
        rf69.setModemConfig(RH_RF69::FSK_MOTEINO);

        rf69.setFrequency(RF_FREQUENCY);

        rf69.setModeRx();

        printf("OK @ %3.2fMHz\n", RF_FREQUENCY);
        printf("Listening packet...\n");

        //Begin the main body of code
        while (!force_exit)
        {
            if (rf69.available())
            {
                uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
                uint8_t len = sizeof(buf);
                uint8_t from = rf69.headerFrom();
                uint8_t to = rf69.headerTo();
                uint8_t id = rf69.headerId();
                uint8_t flags = rf69.headerFlags();
                int8_t rssi = rf69.lastRssi();

                if (rf69.recv(buf, &len))
                {
                    printf("Packet[%02d] #%d => #%d %ddB: ", len, from, to, rssi);
                    printbuffer(buf, len);
                }
                else
                {
                    Serial.print("receive failed");
                }
                printf("\n");
            }
            bcm2835_delay(5);
        }
    }
    printf("\n%s Ending\n", __BASEFILE__);
    bcm2835_close();
    return 0;
}