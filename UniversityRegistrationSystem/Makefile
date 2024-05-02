OPT = -Wall

A03: main.o Control.o View.o Course.o CourseArray.o StuArray.o Registration.o RegList.o Student.o School.o
	g++ $(OPT) -o A03 main.o Control.o View.o Course.o CourseArray.o StuArray.o Registration.o RegList.o Student.o School.o

main.o: main.cc defs.h Control.h View.h Course.h CourseArray.h StuArray.h Registration.h RegList.h Student.h School.h 
	g++ $(OPT) -c main.cc

Course.o: Course.cc Course.h defs.h
	g++ $(OPT) -c Course.cc

StuArray.o: StuArray.cc StuArray.h defs.h
	g++ $(OPT) -c StuArray.cc

Registration.o: Registration.cc Registration.h defs.h
	g++ $(OPT) -c Registration.cc

RegList.o: RegList.cc RegList.h defs.h
	g++ $(OPT) -c RegList.cc

Student.o: Student.cc Student.h defs.h
	g++ $(OPT) -c Student.cc

School.o: School.cc School.h defs.h
	g++ $(OPT) -c School.cc

CourseArray.o: CourseArray.cc CourseArray.h defs.h
	g++ $(OPT) -c CourseArray.cc

Control.o: Control.cc Control.h defs.h
	g++ $(OPT) -c Control.cc

View.o: View.cc View.h defs.h
	g++ $(OPT) -c View.cc

clean:
	rm -f *.o A03