#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <malloc.h>
#include "inspection_socket.h"

struct sockaddr_in server_addr;
int client_socket;
char buff[BUFF_SIZE];
bool is_connected = false;

//========================================================================================================================
//  서버와 연결
//========================================================================================================================
int inspection_client_open(){
    client_socket  = socket( PF_INET, SOCK_STREAM, 0);

    if( -1 == client_socket)
   {
      printf( "socket 생성 실패\n");
      exit( 1);
   }

   memset( &server_addr, 0, sizeof( server_addr));
   server_addr.sin_family     = AF_INET;
   server_addr.sin_port       = htons( INSPECTION_PORT);
   server_addr.sin_addr.s_addr= inet_addr("127.0.0.1");
   if( -1 == connect( client_socket, (struct sockaddr*)&server_addr, sizeof( server_addr) ) )
   {
      printf( "접속 실패\n");
      return -1;
   }
   is_connected = true;
   return 0;
}

//========================================================================================================================
//  서버로 부터 메세지 수신
//========================================================================================================================
int inspection_client_read(){
    memset(buff,'\0', BUFF_SIZE);
    read ( client_socket, buff, BUFF_SIZE);
    return 0;
}

//========================================================================================================================
//  서버로 메세지 전송
//========================================================================================================================
int inspection_client_write(char* sending){
    write( client_socket, sending, strlen(sending));      // +1: NULL까지 포함해서 전송
    return 0;
}

//========================================================================================================================
//  서버와 연결 해제
//========================================================================================================================
int inspection_client_close(){
    close( client_socket);
    is_connected = false;
    return 0;
}

//========================================================================================================================
//  Json 형식의 String을 구조체로 파싱할 때, 용량을 먼저 계산하기 위한 함수
//========================================================================================================================
int json_parse_count() {
    int return_count = 0,index = 0;

    while(buff[index] != '\0'){
        if(buff[index] == '"')
            return_count++;
        index++;
    }

    return (return_count/6);
}

//========================================================================================================================
//  Json 형식의 String을 InspectOutputList에 할당하는 함수
//========================================================================================================================
void json_parse(OUT InspectOutput * outputList) {
    int index = 0, index2 = 0, index3 = 0, index4 = 0;
    char temp_buf[BUFF_SIZE];
    bool flag = false;

    while(buff[index] != '\0'){
        if(buff[index] == '"'){
            flag = !flag;
            if(flag) {
                memset(temp_buf,'\0',BUFF_SIZE);
                index2 = 0;
            } else {
                if(index3 == 0)
                    memcpy((outputList + index4)->cmd,temp_buf,strlen(temp_buf)+1);
                else if (index3 == 1)
                    (outputList + index4)->result = (strcmp(temp_buf,"True") == 0)?true:false;
                else if (index3 == 2)
                    (outputList + index4)->time = atof(temp_buf);
                index4 = (index3 == 2) ? index4 + 1 : index4;
                index3 = (index3 == 2) ? 0 : index3 + 1;
            }
        } else {
            if(flag) {
                temp_buf[index2] = buff[index];
                index2++;
            }
        }
        index ++;
    }
}


//========================================================================================================================
//  단일 검사 함수 (Inspection Output List 구조체 리턴)
//========================================================================================================================
void inspection_cmd(const char full_path[], const char board_name[], const char parts_name[],
                    int box_x1, int box_x2, int box_y1, int box_y2,
                    int insp_type, OUT InspectOutputList * result) {
    if(!is_connected){
        printf("Please proceed with the \"inspection_client_open()\" first.\n\n");
        exit(-1);
    }

    char sending_buf[BUFF_SIZE];
    char temp_buf[BUFF_SIZE];

    memset(sending_buf,'\0',BUFF_SIZE);

    strcat(sending_buf,"Inspect ");             // Inspection OPCODE

    sprintf(temp_buf, "%d", box_x1);            // box_x1을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", box_y1);            // box_y1을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", box_x2);            // box_x2을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", box_y2);            // box_y2을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    strcat(sending_buf,board_name);             // 검사할 보드 이름
    strcat(sending_buf," ");

    strcat(sending_buf,parts_name);             // 검사할 파츠 이름
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", insp_type);         // insp_type을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    strcat(sending_buf,full_path);             // 검사할 사진의 Path

    inspection_client_write(sending_buf);
    inspection_client_read();
    int result_count = json_parse_count();

    // memcpy(result,buff,strlen(buff)+1);
    result->output_list = (InspectOutput *)malloc(sizeof(InspectOutput)*result_count);
    result->element_num = result_count;

    json_parse(result->output_list);

}


//========================================================================================================================
//  복수 검사 함수 (Inspection Output Multi List 구조체 리턴)
//========================================================================================================================
void inspection_cmds (const char full_path[], const char board_name[], const char parts_name[][BUFF_SIZE],
                      int boxes_x1[], int boxes_x2[], int boxes_y1[], int boxes_y2[],
                      int insp_types[], int box_count, OUT InspectOutputMultiList * results) {
    if(!is_connected){
        printf("Please proceed with the \"inspection_client_open()\" first.\n\n");
        exit(-1);
    }

    results->multi_list = (InspectOutputList *)malloc(sizeof(InspectOutputList)*box_count);
    results->list_num = box_count;

    for(int i = 0; i < box_count; i ++){

        inspection_cmd(full_path,board_name,parts_name[i],
                       boxes_x1[i],boxes_x2[i], boxes_y1[i], boxes_y2[i],
                       insp_types[i], (results->multi_list + i));

    }
}


//========================================================================================================================
//  단일 학습 함수 (학습 결과 리턴)
//========================================================================================================================
void learn_cmd_debug (const char full_path[], const char board_name[], const char parts_name[],
                int box_x1, int box_x2, int box_y1, int box_y2,
                int learn_type, OUT int* learn_result){
    if(!is_connected){
        printf("Please proceed with the \"inspection_client_open()\" first.\n\n");
        exit(-1);
    }

    char sending_buf[BUFF_SIZE];
    char temp_buf[BUFF_SIZE];

    memset(sending_buf,'\0',BUFF_SIZE);

    strcat(sending_buf,"LearnData ");             // Inspection OPCODE

    sprintf(temp_buf, "%d", box_x1);            // box_x1을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", box_y1);            // box_y1을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", box_x2);            // box_x2을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", box_y2);            // box_y2을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    strcat(sending_buf,board_name);             // 학습할 보드 이름
    strcat(sending_buf," ");

    strcat(sending_buf,parts_name);             // 학습할 파츠 이름
    strcat(sending_buf," ");

    sprintf(temp_buf, "%d", learn_type);         // learn_type을 스트링으로 변환
    strcat(sending_buf,temp_buf);
    strcat(sending_buf," ");

    strcat(sending_buf,full_path);             // 학습할 사진의 Path

    inspection_client_write(sending_buf);
    inspection_client_read();

    int result = 0;
    result = atoi(buff);

    *learn_result = result;
}


//========================================================================================================================
//  단일 학습 함수
//========================================================================================================================
void learn_cmd (const char full_path[], const char board_name[], const char parts_name[],
                int box_x1, int box_x2, int box_y1, int box_y2,
                int learn_type) {
    int temp = 0;
    learn_cmd_debug(full_path,board_name,parts_name,box_x1,box_x2,box_y1,box_y2,learn_type,&temp);
}


//========================================================================================================================
//  복수 학습 함수 (학습 결과 리턴)
//========================================================================================================================
void learn_cmds_debug (const char full_path[], const char board_name[], const char parts_name[][BUFF_SIZE],
                 int boxes_x1[], int boxes_x2[], int boxes_y1[], int boxes_y2[], int learn_types[],
                 int box_count, OUT int learn_results[]) {
    if(!is_connected){
        printf("Please proceed with the \"inspection_client_open()\" first.\n\n");
        exit(-1);
    }

    for(int i = 0; i < box_count; i ++){

        learn_cmd_debug(full_path,board_name,parts_name[i],
                       boxes_x1[i],boxes_x2[i], boxes_y1[i], boxes_y2[i],
                       learn_types[i], (learn_results+i));

    }
}

//========================================================================================================================
//  복수 학습 함수
//========================================================================================================================
void learn_cmds (const char full_path[], const char board_name[], const char parts_name[][BUFF_SIZE],
                 int boxes_x1[], int boxes_x2[], int boxes_y1[], int boxes_y2[], int learn_types[],
                 int box_count) {
    int * temp = (int *)malloc(sizeof(int) * box_count);
    learn_cmds_debug(full_path,board_name,parts_name,boxes_x1,boxes_x2,boxes_y1,boxes_y2,learn_types,box_count,temp);
}


//========================================================================================================================
//  단일 검사 결과 프린트 함수
//========================================================================================================================
void print_inspection_result(InspectOutputList inspection_result){
    InspectOutput * list = inspection_result.output_list;
    for(int i = 0 ; i < inspection_result.element_num; i++) {
        printf("  \"\033[1;32m%s\033[0m\" : ",list->cmd);
        printf(" [ %s\033[0m, ",(list->result)?"\033[1;32mtrue":"\033[1;31mfalse");
        printf("\033[1;36m%f\033[0m ]",list->time);
        printf("\n");
        list ++;
    }
}


//========================================================================================================================
//  복수 검사 결과 프린트 함수
//========================================================================================================================
void print_inspection_results(InspectOutputMultiList inspection_results){
    printf("===========================================\n");
    for(int i = 0 ; i < inspection_results.list_num; i++) {
        InspectOutputList temp = inspection_results.multi_list[i];
        print_inspection_result(temp);
        if(i != inspection_results.list_num - 1)
            printf("-------------------------------------------\n");
    }
    printf("===========================================\n");
}

void reset_inspection_result(InspectOutputList *inspection_result){
    InspectOutput * list = inspection_result->output_list;
    for(int i=0; i<inspection_result->element_num;i++){
        free(list);
        list++;
    }
    free(list);
    inspection_result->element_num = 0;
}

//========================================================================================================================
//  예제 코드
//========================================================================================================================
void example_code(){

    // 변수 선언 및 초기화 부분
    char pwd[BUFF_SIZE];
    getcwd( pwd, BUFF_SIZE );
    char file_path_normal[BUFF_SIZE];
    char file_path_none[BUFF_SIZE];
    char file_path_marking[BUFF_SIZE];
    char file_path_test[BUFF_SIZE];
    char dot_jpg[] = ".jpg";
    char number_str[10][2] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};
    char expected_result[9][4] = {"?/?", "T/?", "?/T", "T/T", "F/F", "F/T", "T/F", "F/?", "?/F"};
    strcpy(file_path_normal,pwd);
    strcat(file_path_normal,"/good/good-1.jpg");
    strcpy(file_path_none,pwd);
    strcat(file_path_none,"/emptyall/empty_all-1.jpg");
    strcpy(file_path_marking,pwd);
    strcat(file_path_marking,"/bad/bad-1.jpg");
    strcpy(file_path_test,pwd);
    strcat(file_path_test,"/test/test_");
    char parts[2][BUFF_SIZE] = { "partsUp","partsDown"};
    // None & Normal Range
    int pos_1_x1[2] = {2081,2081};
    int pos_1_x2[2] = {2255,2255};
    int pos_1_y1[2] = {901,1493};
    int pos_1_y2[2] = {963,1557};

    // Marking Range
    int pos_2_x1[2] = {2149,2141};
    int pos_2_x2[2] = {2320,2315};
    int pos_2_y1[2] = {892,1491};
    int pos_2_y2[2] = {954,1555};

    // Inpsection Range
    int pos_3_x1[2] = {2080,2070};
    int pos_3_x2[2] = {2254,2244};
    int pos_3_y1[2] = {891,1490};
    int pos_3_y2[2] = {953,1554};

    int inspect_types[2] = {PARTS_NONE | MARKING , PARTS_NONE | MARKING};
    int learn_types_NORMAL[2] = {NORMAL,NORMAL};
    int learn_types_MARKING[2] = {MARKING,MARKING};
    int learn_types_NONE[2] = {PARTS_NONE,PARTS_NONE};
    InspectOutputList inspection_result;
    InspectOutputMultiList inspection_results;
    int learn_resultArr[2] = {0,0};
    int learn_result = 0;

    // 서버 연결
    inspection_client_open();


    /*
    // 단일 학습
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;32m learn_cmd (단일 학습 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    learn_cmd_debug (file_path,"board",parts[2],
                     pos_x1[2],pos_x2[2],pos_y1[2],pos_y2[2],
                     learn_types[2],&learn_result);

    printf("learn result : %d\n",learn_result);
    printf("\n");


    // 복수 학습
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;32m learn_cmds (복수 학습 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    learn_cmds_debug (file_path2,"board",parts,
                      pos_x1,pos_x2,pos_y1,pos_y2,
                      learn_types,2,learn_resultArr);

    for(int i = 0; i < 2 ; i++)
        printf("learn result : %d\n",learn_resultArr[i]);
    printf("\n");


    // 단일 검사
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;33m inspection_cmd (단일 검사 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    inspection_cmd(file_path,"board",parts[0],
                   pos_x1[0],pos_x2[0],pos_y1[0],pos_y2[0],
                   inspect_types[0],&inspection_result);

    print_inspection_result(inspection_result);
    printf("\n");


    // 복수 검사
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;33m inspection_cmds (복수 검사 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    inspection_cmds(file_path,"board",parts,
                    pos_x1,pos_x2,pos_y1,pos_y2,
                    inspect_types,3,&inspection_results);

    print_inspection_results(inspection_results);
    printf("\n\n");
    */

    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;32m learn_cmds (복수 학습 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    learn_cmds_debug (file_path_normal,"board",parts,
                      pos_1_x1,pos_1_x2,pos_1_y1,pos_1_y2,
                      learn_types_NORMAL,2,learn_resultArr);
    for(int i = 0; i < 2 ; i++)
        printf("learn result : %d\n",learn_resultArr[i]);
    printf("\n");

    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;32m learn_cmds (복수 학습 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    learn_cmds_debug (file_path_marking,"board",parts,
                      pos_1_x1,pos_1_x2,pos_1_y1,pos_2_y2,
                      learn_types_MARKING,2,learn_resultArr);
    for(int i = 0; i < 2 ; i++)
        printf("learn result : %d\n",learn_resultArr[i]);
    printf("\n");

    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\033[1;32m learn_cmds (복수 학습 명령) test\033[0m\n");
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    learn_cmds_debug (file_path_none,"board",parts,
                      pos_2_x1,pos_2_x2,pos_2_y1,pos_2_y2,
                      learn_types_NONE,2,learn_resultArr);
    for(int i = 0; i < 2 ; i++)
        printf("learn result : %d\n",learn_resultArr[i]);
    printf("\n");


    for(int i = 0; i < 9; i ++) {
        char file_path_input[BUFF_SIZE];
        strcpy(file_path_input,file_path_test);
        strcat(file_path_input,number_str[i]);
        strcat(file_path_input,dot_jpg);
        printf("%s\n\n",file_path_input);

        printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
        printf("\033[1;33m inspection_cmds (복수 검사 명령) test\033[0m\n");
        printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
        inspection_cmds(file_path_input,"board",parts,
                        pos_3_x1,pos_3_x2,pos_3_y1,pos_3_y2,
                        inspect_types,2,&inspection_results);

        print_inspection_results(inspection_results);
        printf("%s",expected_result[i]);
        printf("\n\n");
    }
    // 서버 연결 해제
    inspection_client_close();
}

int main() {
    example_code();
}
