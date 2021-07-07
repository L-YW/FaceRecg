#
# falinux 라이블러리를 사용하는 어플용 Makefile
#

#CROSS_PREFIX   = arm-generic-linux-gnueabi
#CROSS_PREFIX	= mipsel-linux
#CROSS_PREFIX	= arm-linux
#CROSS_VERSION  = 3.4.4

#CROSS_PREFIX	= aarch64-linux-gnu


#CP_DIR          = /nfs/woo/zeroboot/wiegand/
CP_DIR          = ./


## 사용자 소스
TARGET		= app-manager-ctrl
SRCS		=  main.c api_udp_client.c api_nero_cmd.c
TOPDIR          = ../

#---------------------------------------------------------------------
## 소스레벨의 라이브러리
SRCS_COMMON     = 
SRCS_FANET		= 
SRCS_GXLIB		= 

SRCS           += $(SRCS_COMMON) $(SRCS_FANET) $(SRCS_GXLIB)

## 인클루드	디렉토리
#DIR_INC			= $(TOPDIR)include/
#INC_COMMON		= $(DIR_INC)common/
#INC_FANET		= $(DIR_INC)fanet/
#INC_GXLIB		= $(DIR_INC)gxlib/
#INC_GXCTRL		= $(DIR_INC)gxctrl/
INCLUDEDIRS		+= -I. -I$(DIR_INC) -I$(INC_COMMON) -I$(INC_FANET) -I$(INC_GXLIB) -I$(INC_GXCTRL)

LIVDIRS			+= 

OBJS			= $(SRCS:.c=.o)
CFLAGS			= $(INCLUDEDIRS) -W -Wall -O2
LDFLAGS			= $(LIVDIRS)
LDFLAGS 	   += -lpthread
LIBS			= -lm 

#---------------------------------------------------------------------
CC				=	$(CROSS_PREFIX)-gcc
CXX			 	=	$(CROSS_PREFIX)-g++
AR				=	$(CROSS_PREFIX)-ar rc
AR2				=	$(CROSS_PREFIX)-ranlib
RANLIB			=	$(CROSS_PREFIX)-ranlib
LD				=	$(CROSS_PREFIX)-ld
NM				=	$(CROSS_PREFIX)-nm
STRIP			=	$(CROSS_PREFIX)-strip
OBJCOPY		 	=	$(CROSS_PREFIX)-objcopy
CP	= cp
MV	= mv
#--------------------------------------------------------------------

all : $(TARGET)
	#cp $^ $(CP_DIR)

$(TARGET) : $(OBJS)
	$(CC) $(LDFLAGS) $(OBJS) -o $@ $(LIBS) 
	$(NM) $(TARGET) > $(TARGET).map

%.o:%.c
	@echo "Compiling $< ..."
	$(CC) -c $(CFLAGS) -o $@ $<

%.o:%.cc
	@echo "C++ compiling $< ..."
	$(CXX) -c $(CFLAGS) $(CXXFLAGS) -o $@ $<

dep :
	$(CC)	-M	$(INCLUDEDIRS)	$(SRCS) > .depend

clean:
	rm -f *.bak
	rm -f *.map
	rm -f *.o
	rm -f $(OBJS)
	rm -f $(TARGET)

distclean: clean
	rm -rf .depend	


ifeq (.depend,$(wildcard .depend))
include .depend
endif


