/*
 * distance.c
 *
 * Measure distance
 *
 * Created: 05-11-2018 13:45:23
 * Author: Rein Gankema
 * HC-SR04
 */
 
#include <avr/io.h>
#include <stdlib.h>
#include <stdio.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#define F_CPU 16E6
#include "distance.h"
#include "serial.h"

int echoPIN = 3;

static volatile int gv_echo = 0; // a 16 bit flag
static volatile int gv_count = 0;
uint8_t distance = 0;


/*
int read(uint8_t pin)
{
	if (PIND & _BV(pin)) { // if pin set in port
	return HIGH;
} else {
	return LOW;
}
}
*/

void write(uint8_t pin, uint8_t val)
{
	if (val == LOW) {
		PORTD &= ~(_BV(pin)); // clear bit
	} else {
		PORTD |= _BV(pin); // set bit
	}
}

void init_ports(void)
{
	DDRD = 0b00000010;			//Set TRIG pin on output (PIN 1);
	_delay_ms(50);

}

void Initialize_external_interrupt(void)
{
	EIMSK |= (1 << INT1);	// enable INT1
	EICRA |= (1 << ISC11);	// set INT1 to trigger while rising edge = HIGH
}

void init_timer()
// prescaling : max time = 2^16/16E6 = 4.1 ms, 4.1 >> 2.3, so no prescaling required
// normal mode, no prescale, stop timer
{
	cli();				//Clear interrupts
	TCCR1B = 0;			//Set timer to 0
}

uint16_t Pulse()
{
		//Restart HC-SR04 by setting TRIG pin back to LOW
		_delay_ms(2000);
		write(PIND1, LOW);
		_delay_us(1);
		//Send a pulse
		write(PIND1, HIGH); //Set PIN 0 HIGH
		_delay_us(10);
		write(PIND1, LOW); //Set PIN 0 LOW
		
}	

uint16_t calc_cm()
{
	/*Convert the distance in us to cm			
	
	Formula:	Distance = Time * Speed
	Speed from HC SR04 = 343 m/s (speed of sound)
	340 m/s = 0.034 us/cm
	Time = gv_echo
	Distance = (gv_echo * 0.0343) / 2
	
	U divide by 2 because the pulse travels forwards and back
	
	*/			
	
	distance = ((gv_echo * 0.0343) / 2);										
}


int main(void)
{
	init_ports();						//Init ports
	init_timer();						//Init timer
	Initialize_external_interrupt();	//Init interrupts
	uart_init();						//Init UART
	stdout = &mystdout;
	sei();
									//enable interrupts

	while (1)
	{
		Pulse();
		calc_cm();
		printf("distance %d \r\n: ", distance);
	}
}

ISR (INT1_vect)
{	
	if (gv_count==1)				//when logic from HIGH to LOW
		{
			TCCR1B = 0;					//disabling counter
			gv_echo = TCNT1;			//count memory is updated to integer
			TCNT1= 0;					//resetting the counter memory
			gv_count = 0;				//Set count to 0
		}

	if (gv_count==0)				//when logic change from LOW to HIGH
		{
			TCCR1B |= _BV(CS10);		//enabling counter (TCNT1) without any prescaling
			gv_count=1;					//Set count to 1
		}
	}

