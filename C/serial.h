#define UBBRVAL 51

static int put_char(char c, FILE *stream);
static FILE mystdout = FDEV_SETUP_STREAM(put_char, NULL, _FDEV_SETUP_WRITE);

void uart_init()
{
	//Set baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	
	//Disable U2X mode
	UCSR0A = 0;
	
	//Enable transmitter and receiver
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	
	//Set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

/*
	Function for the printf function
	Almost identical to the transmit function
*/
static int put_char(char c, FILE *stream)
{
	loop_until_bit_is_set(UCSR0A, UDRE0); // wait for UDR to be clear
	UDR0 = c;    //send the character
	return 0;
}

/*
	Transmit data to the client
	Reference: ATMEGA328p Datasheet 20.6.1
*/
void transmit(unsigned char data){
	/* Wait for empty transmit buffer */
	while( !(UCSR0A & (1<<UDRE0)) );
	
	/* Put data into buffer, sends the data */
	UDR0 = data;
}

/*
	Receive input from the client
	Reference: ATMEGA328p Datasheet 20.7.1
*/
unsigned char receive( void )
{
	/* Wait for data to be received */
	while ( !(UCSR0A & (1<<RXC0)) );
	/* Get and return received data from buffer */
	return UDR0;
}

/************************************************************************/
/* Check if there is any data incomming. If so; return 1				*/
/************************************************************************/
int message_incomming( void )
{
	if((UCSR0A & (1<<RXC0))){
		return 1;
	} else {
		return 0;
	}
}