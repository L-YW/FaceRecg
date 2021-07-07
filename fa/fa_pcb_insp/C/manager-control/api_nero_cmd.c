/*
 * Author: Kim Hyun-ki <khkraining@falinux.com>
 *
 * Create On : 2020. 09. 10
 *
 */ 

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#include <api_udp_client.h>

char send_data[1024];

int nero_cmd_open(void)
{
	udp_client_open();

	return 0;
}

int nero_cmd_close(void)
{
	udp_client_close();

	return 0;
}

int nero_cmd_send_to_server(void)
{
	udp_client_send(send_data, strlen(send_data));
	memset(send_data, 0, 1024);

	return 0;
}

int nero_test(void)
{
	//sprintf(send_data, "{\"cmd\":\"neuro_capture\",\"path\":\"/image/test51.jpg\"}");
	sprintf(send_data, "{\"cmd\":\"fpga_image_check\"}");
	//sprintf(send_data, "{\"cmd\":\"{\"result\":1}\"}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_check_error(void)
{
	sprintf(send_data, "{\"cmd\":\"neuro_teaching\",\"teaching\":\"./capture2.png-1-(3840x2160)-(2328,890,2598,963)-(2325,1493,2585,1574)\"}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_check_normal(void)
{
	sprintf(send_data, "{\"cmd\":\"neuro_teaching\",\"teaching\":\"./capture.png-0-(3840x2160)-(2328,890,2598,963)-(2325,1493,2585,1574)\"}");

	nero_cmd_send_to_server();

	return 0;
}

int nero_teaching_good(void)
{
	//sprintf(send_data, "{\"cmd\":\"neuro_teaching\",\"teaching\":\"./capture.png-0-(3840x2160)-(2328,890,2598,963)-(2325,1493,2585,1574)\"}");
	sprintf(send_data, "{\"cmd\":\"neuro_teaching\",\"teaching\":\"./capture.png-0-(3840x2160)-(2328,890,2598,963)\"}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_teaching_bad(void)
{
	sprintf(send_data, "{\"cmd\":\"neuro_teaching\",\"teaching\":\"./bad.png-1-(3840x2160)-(2328,890,2598,963)-(2325,1493,2585,1574)\"}");

	nero_cmd_send_to_server();

	return 0;
}

int nero_learn_normal(void)
{
	sprintf(send_data, "{\"cmd\":\"fpga_learn_normal\"}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_learn_error(void)
{
	sprintf(send_data, "{\"cmd\":\"fpga_learn_error\"}");

	nero_cmd_send_to_server();

	return 0;
}

int nero_time(void)
{
	sprintf(send_data, "{\"cmd\":\"fpga_proc_time\"}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_cap(void)
{
	sprintf(send_data, "{\"cmd\":\"control_capture\"}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_result_good(void)
{
	sprintf(send_data, "{\"cmd\":\"image_check_result\",\"result\":0}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_result_bad(void)
{

	sprintf(send_data, "{\"cmd\":\"image_check_result\",\"result\":1}");

	nero_cmd_send_to_server();

	return 0;
}
int nero_update(void)
{
	sprintf(send_data, "{\"cmd\":\"update\"}");

	nero_cmd_send_to_server();

	return 0;
}


