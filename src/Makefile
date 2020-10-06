app.out : haar.o
	g++ -o app.out haar.o -lwiringPi `pkg-config --libs opencv`

haar.o : haar.cpp
	g++ -c -o haar.o haar.cpp

clean :
	rm -f *.o
	rm -f app.out
