# Define required macros here
SHELL = /bin/sh

CFLAG = -Wall -g
CC = gcc


txt2html: txt2html.o

clean:
	-rm -f *.o core *.core

