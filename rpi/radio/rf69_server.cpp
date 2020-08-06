#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>
#include <termios.h>
#include <time.h>
#include <stdbool.h>
#include <stropts.h>
#include <poll.h>

#include <errno.h>

#define BAUDRATE B115200
#define DEVICE "/dev/ttyACM0"

int set_interface_attribs(int fd, int speed, int parity)
{
    struct termios tty;
    memset(&tty, 0, sizeof tty);
    if (tcgetattr(fd, &tty) != 0)
    {
        printf("error %d from tcgetattr", errno);
        return -1;
    }

    cfsetospeed(&tty, speed);
    cfsetispeed(&tty, speed);

    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8; // 8-bit chars
    // disable IGNBRK for mismatched speed tests; otherwise receive break
    // as \000 chars
    tty.c_iflag &= ~IGNBRK; // disable break processing
    tty.c_lflag = 0;        // no signaling chars, no echo,
                            // no canonical processing
    tty.c_oflag = 0;        // no remapping, no delays
    tty.c_cc[VMIN] = 0;     // read doesn't block
    tty.c_cc[VTIME] = 5;    // 0.5 seconds read timeout

    tty.c_iflag &= ~(IXON | IXOFF | IXANY); // shut off xon/xoff ctrl

    tty.c_cflag |= (CLOCAL | CREAD);   // ignore device controls,
                                       // enable reading
    tty.c_cflag &= ~(PARENB | PARODD); // shut off parity
    tty.c_cflag |= parity;
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CRTSCTS;

    if (tcsetattr(fd, TCSANOW, &tty) != 0)
    {
        return -1;
    }
    return 0;
}

void set_blocking(int fd, int should_block)
{
    struct termios tty;
    memset(&tty, 0, sizeof tty);
    if (tcgetattr(fd, &tty) != 0)
    {
        printf("error %d from tggetattr", errno);
        return;
    }

    tty.c_cc[VMIN] = should_block ? 1 : 0;
    tty.c_cc[VTIME] = 5; // 0.5 seconds read timeout

    if (tcsetattr(fd, TCSANOW, &tty) != 0)
        printf("error %d setting term attributes", errno);
}

int main(void)
{
    int fd;
    char buf[255];
    int variable;
    struct pollfd fds[1];
    int ret, res;

    /* open the device */
    fd = open(DEVICE, O_RDWR | O_NOCTTY | O_NONBLOCK);
    if (fd == 0)
    {
        perror(DEVICE);
        printf("Failed to open DEVICE \"/dev/ttyACM0\"\n");
        exit(-1);
    }

    set_interface_attribs(fd, BAUDRATE, 0);
    set_blocking(fd, 0);

    /* Open STREAMS device. */
    fds[0].fd = fd;
    fds[0].events = POLLRDNORM;

    for (;;) // forever
    {
        ret = poll(fds, 1, 1000); //wait for response

        if (ret > 0)
        {
            /* An event on one of the fds has occurred. */
            if (fds[0].revents & POLLHUP)
            {
                printf("Hangup\n");
            }
            if (fds[0].revents & POLLRDNORM)
            {
                res = read(fd, buf, 255);
                buf[res] = 0; // terminate buffer
                sscanf(buf, "%d\n", &variable);
                printf("Received %d\n", variable);
            }
        }
    }
}