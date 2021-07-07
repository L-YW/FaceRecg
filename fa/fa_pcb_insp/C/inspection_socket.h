#ifndef _INSPECTION_SOCKET_SERVER
#define _INSPECTION_SOCKET_SERVER

#include <stdbool.h>
#define INSPECTION_PORT 5843
#define BUFF_SIZE   1025
#define OUT

enum EnumInspType {
    NORMAL              = 0b0000000000,        // No.0 정상
    PARTS_WRONG         = 0b0000000001,        // No.1 오삽
    PARTS_NONE          = 0b0000000010,        // No.2 미삽
    SOLDERING_NONE      = 0b0000000100,        // No.3 미납
    SOLDERING_LITTLE    = 0b0000001000,        // No.4 소납
    SOLDERING_OVER      = 0b0000010000,        // No.5 과납
    MARKING             = 0b0000100000,        // No.6 마킹
    CIRCUIT_SHORT       = 0b0001000000,        // No.7 쇼트
    PARTS_CRACK         = 0b0010000000,        // No.8 부품 crack
    SOLDERING_CRACK     = 0b0100000000,        // No.9 납땜 crack
    PARTS_REVERSE       = 0b1000000000,        // No.10 역삽
};

extern int inspection_client_open();
extern int inspection_client_write(char* sending);
extern int inspection_client_close();

// 자세한 사용 방법은 example_code() 참조

//========================================================================================================================
//  검사 하나의 결과를 저장하는 구조체.
//
//    cmd에는 검사 명령 (ex.PARTS_WRONG), result에는 결과 (true/false), time에는 검사에 걸린 시간을 저장한다.
//========================================================================================================================
typedef struct _InspectOutput {
    char cmd[BUFF_SIZE];
    bool result;
    float time;
} InspectOutput;

//========================================================================================================================
//  단일 검사 결과를 받아 왔을 때, 결과를 저장하는 구조체
//
//    예를들어 18 = 0b 00 0001 0010 의 검사타입을 송신한다면, 
//    output_list에 InpectOutput이 2개 저장되며,
//    element_num 에는 2가 저장된다.
//========================================================================================================================
typedef struct _InspectOutputList {
    InspectOutput * output_list;
    int element_num;
} InspectOutputList;

//========================================================================================================================
//  복수 검사 결과를 받아 왔을 때, 결과를 저장하는 구조체
//
//    예를들어 1 = 0b 00 0000 0001 / 23 = 0b 00 0001 0111 의 검사타입을 한 번에 송신한다면, 
//    multi_list에는 InpectOutputList가 2개 저장되며,
//    list_num 에는 2가 저장된다.
//    
//    또한 multi_list[0]의 output_list에는 InpectOutput이 1개 저장되고
//    multi_list[0]의 element_num에는 1이,
//    multi_list[1]의 output_list에는 InspectOutput이 4개,
//    multi_list[1]의 element_num에는 4가 저장된다.
//========================================================================================================================
typedef struct _InspectOutputMultiList {
    InspectOutputList * multi_list;
    int list_num;
} InspectOutputMultiList;

//========================================================================================================================
//  단일 영역 검사
//      검사할 이미지의 절대 경로, 보드이름, 파츠이름, x1,x2, y1, y2, 검사 타입, 검사 결과를 받을 char[]
//========================================================================================================================
extern void inspection_cmd (const char full_path[], const char board_name[], const char parts_name[],
                            int box_x1, int box_x2, int box_y1, int box_y2,
                            int insp_type, OUT InspectOutputList * result);


//========================================================================================================================
//  복수 영역 검사
//      검사할 이미지의 절대 경로, 보드이름, 파츠이름 배열 , x1 배열,x2 배열, y1 배열, y2 배열,
//      검사 타입 배열, 검사 횟수, 검사 결과를 받을 char[] 배열 (출력)
//========================================================================================================================
extern void inspection_cmds (const char full_path[], const char board_name[], const char parts_name[][BUFF_SIZE],
                             int boxes_x1[], int boxes_x2[], int boxes_y1[], int boxes_y2[],
                             int insp_types[], int box_count, OUT InspectOutputMultiList * results);


//========================================================================================================================
//  단일 영역 학습 
//      학습할 이미지의 절대 경로, 보드이름, 파츠이름, x1,x2, y1, y2, 학습 타입(반드시 2의 제곱수이어야 함)
//========================================================================================================================
extern void learn_cmd (const char full_path[], const char board_name[], const char parts_name[],
                       int box_x1, int box_x2, int box_y1, int box_y2,
                       int learn_type);


//========================================================================================================================
//  단일 영역 학습 (학습 결과 리턴)
//      학습할 이미지의 절대 경로, 보드이름, 파츠이름, x1,x2, y1, y2,
//      학습 타입(반드시 2의 제곱수이어야 함), 검사 결과를 받을 int의 주솟값
//========================================================================================================================
extern void learn_cmd_debug (const char full_path[], const char board_name[], const char parts_name[],
                             int box_x1, int box_x2, int box_y1, int box_y2,
                             int learn_type, OUT int* learn_result);


//========================================================================================================================
//  복수 영역 학습 
//      학습할 이미지의 절대 경로, 보드이름, 파츠이름 배열, x1 배열,x2 배열, y1 배열, y2 배열,
//      학습 타입(반드시 2의 제곱수이어야 함) 배열, 학습 횟수
//========================================================================================================================
extern void learn_cmds (const char full_path[], const char board_name[], const char parts_name[][BUFF_SIZE],
                        int boxes_x1[], int boxes_x2[], int boxes_y1[], int boxes_y2[], int learn_types[],
                        int box_count);


//========================================================================================================================
//  복수 영역 학습 (학습 결과 리턴)
//      학습할 이미지의 절대 경로, 보드이름, 파츠이름 배열, x1 배열,x2 배열, y1 배열, y2 배열,
//      학습 타입(반드시 2의 제곱수이어야 함) 배열, 학습 횟수, 검사 결과를 받을 int 배열
//========================================================================================================================
extern void learn_cmds_debug (const char full_path[], const char board_name[], const char parts_name[][BUFF_SIZE],
                              int boxes_x1[], int boxes_x2[], int boxes_y1[], int boxes_y2[], int learn_types[],
                              int box_count, OUT int learn_results[]);

extern void reset_inspection_result(InspectOutputList *inspection_result);
//========================================================================================================================
//  검사 결과 구조체 프린트 함수 (단일 검사 / 복수 검사)
//========================================================================================================================
extern void print_inspection_result(InspectOutputList inspection_result);
extern void print_inspection_results(InspectOutputMultiList inspection_results);


#endif
