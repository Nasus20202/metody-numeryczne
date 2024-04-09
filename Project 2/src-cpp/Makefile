OBJS	= main.o matrix.o helpers.o solvers.o
SOURCE	= main.cpp matrix.cpp helpers.cpp solvers.cpp
HEADER	= matrix.h helpers.h solvers.h
OUT	= main.out
EXE = main.exe
CC	 = g++
FLAGS	 = -g -c -Wall -O3
LFLAGS	 = 

all: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)
all-win: $(OBJS)
	$(CC) -g $(OBJS) -o $(EXE) $(LFLAGS)

main.o: main.cpp
	$(CC) $(FLAGS) main.cpp 

matrix.o: matrix.cpp
	$(CC) $(FLAGS) matrix.cpp 

helpers.o: helpers.cpp
	$(CC) $(FLAGS) helpers.cpp 

solvers.o: solvers.cpp
	$(CC) $(FLAGS) solvers.cpp

clean:
	rm -f $(OBJS) $(OUT)

clean-win:
	del $(OBJS) $(EXE) *.gch

run: $(OUT)
	./$(OUT)

build: all
build-win: all-win

build-run: build run
build-run-win: build-win run

build-run-clean: build-run clean
build-run-clean-win: build-run-win clean-win