/*
 * zonnescherm.c
 *
 * Created: 26-10-2018 12:38:35
 *  Author: Arnold
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <avr/sfr_defs.h>

#define F_CPU 16E6
#include <util/delay.h>

#include "serial.h"
#include "connection.h"
#include "adc.h"

// Data holders
uint8_t debug;
uint16_t light;
uint16_t rotation;
uint16_t temperature;

uint16_t tmph;
uint16_t tmpl;
uint16_t exth;
uint16_t extl;
uint16_t luxh;
uint16_t luxl;
uint8_t manual;

//Arrays
#define max_index 12
uint16_t temps[max_index];
uint16_t lights[max_index];
uint8_t temp_index;
uint8_t light_index;


/*
	Print the system output like a JSON formatted array so that Python can easily use it.
	The JSON_settings array contains the settings which the Python client can have control over.
	TODO: Implement variables such as rotation_max, light_threshold, temperature_threshold
*/
unsigned char get_JSON_settings(void)
{
	//printf("{'type': 'settings', 'manual': %d, 'debug': %d, 'rotation': %d, 'temperature_max_threshold': %d, 'temperature_min_threshold': %d, 'light_max_threshold': %d, 'light_min_threshold': %d, 'extension_max': %d, 'extension_min': %d}\r\n", manual, debug, rotation, tmph, tmpl, luxh, luxl, exth, extl);
	printf("{'type': 'settings', 'manual': %d, 'debug': %d, 'rotation': %d, 'temperature':{'max': %d, 'min': %d}, 'light':{'max': %d, 'min': %d}, 'extension':{'max': %d, 'min': %d}}\r\n", manual, debug, rotation, tmph, tmpl, luxh, luxl, exth, extl);
	return 0;
}

/*
	Print the system output like a JSON formatted array so that Python can easily use it.
	The JSON_data array contains the data obtained by the sensors.
	TODO: Also send older data and average numbers of the variables
*/
unsigned char get_JSON_data(void)
{
	
	//Debugger
	if(debug){
		update_temperature();
		update_light();	
	}
	
	printf("{'type': 'current_data', 'rotation': %d, 'temperature': %d, 'light_intensity': %d}\r\n", rotation, temperature, light);
	return 0;
}

//average
//calculate the average from the array temps
float average_temp()
{
	int i;
	float avg, som = 0.0;
	for (i = 0; i < max_index; i++)
	{
		som += temps[i];
	}
	avg = som / (max_index - 1);
	return avg;
}

//calculate the average from the array lights
float average_light()
{
	int i;
	float avg, som = 0.0;
	for (i = 0; i < max_index; i++)
	{
		som += lights[i];
	}
	avg = som / (max_index - 1);
	return avg;
}

//Adds to array
//Adds the value temperature to the array temps
float temp_add_array(temperature)
{
	temps[temp_index] = temperature;
	temp_index ++;	
	
	if (temps[(max_index - 1)] > 0)
	{
		temperature = average_temp(temps);
	}
}

//Adds the value light to the array lights
float light_add_array(light)
{
	lights[light_index] = light;
	light_index ++;
	
	if (lights[(max_index - 1)] > 0)
	{
		light = average_light(lights);
	}
}



//Updaters
void update_temperature( void )
{
	temperature = adc_read(TEMP_PIN);
	temperature = temp_add_array();
}

void update_light( void )
{
	light = adc_read(LIGHT_PIN);
	light = light_add_array();
}


//Setup things
void setup( void )
{
	
	DDRB = 0xFF;			//Set DDRB as output
	
	adc_init();				//Init Analog to Digital Converter
	uart_init();			//Init Serial
	SCH_Init_T1();			//Init Scheduler
	stdout = &mystdout;		//Init printf()
	
	update_light();
	update_temperature();
	
	tmph = 50;
	tmpl = 0;
	exth = 50;
	extl = 0;
	luxh = 50;
	luxl = 0;
	manual = 1;
	
}

/************************************************************************/
/* This is the new input handler which can accept POST requests			*/
/* Viewer discretion is advised.										*/
/************************************************************************/
char input_string[30];
uint8_t input_string_index = 0;
uint8_t incomming_message = 0;
void input_handler()
{
	
	//Return if there is nothing incoming on RX
	if(!message_incomming() && incomming_message==0){
		return 0;
	}
	
	//Wait for input by the client
	char input = receive();
	char compare_get[30];
	char compare_post[4];
	
	if(input ==	0x0D||input == 0x5C||input == 0x24){
		
		//GET data
		strcpy(compare_get, "d");
		if(!strcmp(input_string, compare_get)){get_JSON_data();}
			
		strcpy(compare_get, "data");
		if(!strcmp(input_string, compare_get)){get_JSON_data();}
	
			
		//GET settings
		strcpy(compare_get, "s");
		if(!strcmp(input_string, compare_get)){get_JSON_settings();}

		//POST temp_threshold HIGH
		strcpy(compare_post, "tmph");
		if(!strncmp(input_string, compare_post,4)){post_temperature(input_string, 1);}

		//POST temp_threshold LOW
		strcpy(compare_post, "tmpl");
		if(!strncmp(input_string, compare_post,4)){post_temperature(input_string, 0);}
		
		//POST maximum extension
		strcpy(compare_post, "exth");
		if(!strncmp(input_string, compare_post,4)){post_extension(input_string, 1);}
		
		//POST minimum extension
		strcpy(compare_post, "extl");
		if(!strncmp(input_string, compare_post,4)){post_extension(input_string, 0);}
			
		//POST max lux
		strcpy(compare_post, "luxh");
		if(!strncmp(input_string, compare_post,4)){post_light(input_string, 1);}
			
		//POST min lux
		strcpy(compare_post, "luxl");
		if(!strncmp(input_string, compare_post,4)){post_light(input_string, 0);}
		
		
		//POST debugger toggle
		strcpy(compare_post, "debg");
		if(!strncmp(input_string, compare_post,4)){post_debugger();}
		
		//POST manual/automatic toggle
		strcpy(compare_post, "manu");
		if(!strncmp(input_string, compare_post,4)){post_manual();}
		
		//Reset the char array
		incomming_message=1;
		input_string_index=0;		
		memset(input_string, NULL, 30);
		
		return 0;
	}
	
	input_string[input_string_index] = input;
	input_string_index++;
	
}

int decode_values( char ar[30] )
{
	
	char tmp[25];
	uint8_t x=0;
	int i;
	
	while(ar[x+5]!=NULL){
		tmp[x]=ar[x+5];
		x++;
	}
	sscanf(tmp, "%d", &i);
	return i;
	
}

void post_temperature( char str[30], uint8_t level ){
	
	uint16_t v = decode_values(str);
	if(level){
		tmph=v;
	}else{
		tmpl=v;
	}
	
	printf("{'type':'post_request', 'success': 1}");
	
}

void post_extension( char str[30], uint8_t level ){
	
	uint16_t v = decode_values(str);
	if(level){
		exth=v;
	}else{
		extl=v;
	}
	
	printf("{'type':'post_request', 'success': 1}");
		
}

void post_light( char str[30], uint8_t level ){
	
	uint16_t v = decode_values(str);
	if(level){
		luxh=v;
	}else{
		luxl=v;
	}
	
	printf("{'type':'post_request', 'success': 1}");
		
}

void post_debugger(){
	debug=!debug;
	printf("{'type':'post_request', 'success': 1}");
}

void post_manual(){
	manual=!manual;
	printf("{'type':'post_request', 'success': 1}");
}

void main(void)
{
	
	light = 0;
	rotation = 0;
	temperature = 0;
	debug = 1;	//If debugger is true (1), all the sensors will be updated when JSON formatted data is requested
	
	setup();
	
	SCH_Add_Task(input_handler, 0, 1);
	
	if(!debug){
		SCH_Add_Task(update_temperature, 0, 4000);
		SCH_Add_Task(update_light, 0, 3000);
		SCH_Add_Task(get_JSON_data, 0, 6000);
	}	
	
	SCH_Start();
	
	while(1)
	{
		
		SCH_Dispatch_Tasks();
	}		
	
	return 0;
		
}