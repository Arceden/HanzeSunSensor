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
#define HIGH 0x1
#define LOW 0x0
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

static volatile int gv_count;
static volatile int gv_echo = 0;

//Arrays
#define max_index 12
uint16_t temp_list[max_index];
uint16_t light_list[max_index];
uint8_t temp_index=0;
uint8_t light_index=0;


void write(uint8_t pin, uint8_t val)
{
	if (val == LOW) {
		PORTD &= ~(_BV(pin)); // clear bit
	} else {
		PORTD |= _BV(pin); // set bit
	}
}

uint16_t get_average(uint16_t l[max_index])
{
	
	int sum = 0;
	uint8_t i;
	
	for(i=0;i<max_index;i++){
		sum+=l[i];
		if(l[i]==0){break;}
	}
	
	return sum/i;
	
}

/*
	Print the system output like a JSON formatted array so that Python can easily use it.
	The JSON_settings array contains the settings which the Python client can have control over.
*/
unsigned char get_JSON_settings(void)
{
	printf("{'type': 'settings', 'manual': %d, 'debug': %d, 'rotation': %d, 'temperature':{'max': %d, 'min': %d}, 'light':{'max': %d, 'min': %d}, 'extension':{'max': %d, 'min': %d}}\r\n", manual, debug, rotation, tmph, tmpl, luxh, luxl, exth, extl);
	return 0;
}

/*
	Print the system output like a JSON formatted array so that Python can easily use it.
	The JSON_data array contains the data obtained by the sensors.
*/
unsigned char get_JSON_data(void)
{
	
	//Debugger
	if(debug){
		update_temperature();
		update_light();	
		update_rotation();
	}
	
	uint16_t temperature_avg = get_average(temp_list);
	uint16_t light_avg = get_average(light_list);
	
	printf("{'type': 'current_data', 'temperature': %d, 'light_intensity': %d}\r\n", temperature_avg, light_avg);
	return 0;
}


//Updaters
void update_temperature( void )
{
	temperature = adc_read(TEMP_PIN);
	temp_list[temp_index]=temperature;
	temp_index++;
	if(temp_index==max_index)temp_index=0;
}

void update_light( void )
{
	light = adc_read(LIGHT_PIN);
	light_list[light_index]=light;
	light_index++;
	if(light_index==max_index)light_index=0;
}

void update_rotation( void )
{

	//Restart HC-SR04 by setting TRIG pin back to LOW
	_delay_ms(10);
	write(PIND2, LOW);
	_delay_us(1);
	//Send a pulse
	_delay_ms(10);
	write(PIND2, HIGH); //Set PIN 0 HIGH
	_delay_us(10);
	write(PIND2, LOW); //Set PIN 0 LOW
	
	rotation = ((gv_count / 16) / 58.2);
	
	if (rotation < 1)
	{
		rotation = 0;
	}
}


//Setup things
void setup( void )
{
	
	DDRB = 0xFF;			//Set DDRB as output
	
	//Setup for ultrasonic sensor
	DDRD = 0b00000100;		//Set triggerpin for the ultrasonic sensor as output
	
	EIMSK |= (1 << INT1);	// enable INT1
	EICRA |= (1 << ISC10);	// set INT1 to trigger while rising edge = HIGH
	//
	
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
		//SCH_Add_Task(update_temperature, 0, 4000);
		//SCH_Add_Task(update_light, 0, 3000);
		SCH_Add_Task(update_temperature, 0, 500);
		SCH_Add_Task(update_light, 0, 500);
		//SCH_Add_Task(update_rotation, 0, 100);
		SCH_Add_Task(get_JSON_data, 0, 6000);
	}	
	
	SCH_Start();
	
	while(1)
	{
		
		SCH_Dispatch_Tasks();
	}		
	
	return 0;
		
}

//Interrupt for the ultrasonic sensor to get the pulse time in microseconds
/*
ISR (INT1_vect)
{
	if (gv_echo==1)					//when logic from HIGH to LOW
	{
		TCCR1B = 0;					//disabling counter
		gv_count = TCNT1;			//count memory is updated to integer
		TCNT1= 0;					//resetting the counter memory
		gv_echo = 0;				//Set count to 0
		TCCR1B = (1 << CS12) | (1 << WGM12);
	}

	if (gv_echo==0)					//when logic change from LOW to HIGH
	{
		TCCR1B = 0;
		TCCR1B |= _BV(CS10);		//enabling counter (TCNT1) without any prescaling
		gv_echo=1;					//Set count to 1
	}
}
*/