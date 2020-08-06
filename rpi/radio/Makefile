CC            = g++

.PHONY = all clean

all: rf69_server

rf69_server: rf69_server.o
				g++ -o rf69_server rf69_server.o

rf69_server.o: rf69_server.cpp
				g++ -c rf69_server.cpp

clean:
				rm -rvf *.o rf69_server