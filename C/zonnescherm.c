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

uint8_t debug;
uint16_t rotation;
uint16_t temperature;
uint16_t light;


/*
	Print the system output like a JSON formatted array so that Python can easily use it.
	The JSON_settings array contains the settings which the Python client can have control over.
	TODO: Implement variables such as rotation_max, light_threshold, temperature_threshold
*/
unsigned char get_JSON_settings(void)
{
	printf("{'type': 'settings', 'debug': %d, 'rotation': %d}\r\n", debug, rotation);
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

//Updaters
void update_temperature( void )
{
	temperature = adc_read(TEMP_PIN);
}

void update_light( void )
{
	light = adc_read(LIGHT_PIN);
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
	
}

/************************************************************************/
/* This is the new input handler which can accept POST requests			*/
/* Viewer discretion is advised.										*/
/************************************************************************/
char input_string[30];
uint8_t input_string_index = 0;
void input_handler()
{
	
	//Return if there is nothing incoming on RX
	if(!message_incomming()){
		return 0;
	}
	
	//Wait for input by the client
	char input = receive();
	char compare_get[30];
	char compare_post[4];
	
	if(input ==	0x0D){
		
		//GET data
		strcpy(compare_get, "d");
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
		
		//POST debugger toggle
		strcpy(compare_post, "debg");
		if(!strncmp(input_string, compare_post,4)){post_debugger();}
		
		//POST manual/automatic toggle
		strcpy(compare_post, "manu");
		if(!strncmp(input_string, compare_post,4)){post_manual();}
		
		//Reset the char array
		input_string_index=0;		
		memset(input_string, NULL, 30);
		return 0;
	}
	
	input_string[input_string_index] = input;
	input_string_index++;
	
}

void post_temperature( char str[30], uint8_t level ){
	printf("Just imagine something happened to the temperature..\r\n");
}

void post_extension( char str[30], uint8_t level ){
	printf("Just imagine something happened to the extensions..\r\n");
}

void post_debugger(){
	debug=!debug;
	printf("debugger:%d\r\n",debug);
}

void post_manual(){
	printf("Just imagine it switched\r\n");
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
	
	while(1){
		SCH_Dispatch_Tasks();
	}		
	
	return 0;
		
}