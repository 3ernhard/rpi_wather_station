#define PIN	0
#define BAUD	9600
#define WAIT	1000


void print_celsius() {
    float k {log(10000.0 * ((1024.0 / analogRead(PIN) - 1)))};
    Serial.println((1 / (0.001129148 + (0.000234125 + (0.0000000876741 * k * k)) * k)) - 273.15);
}


void setup() {
	Serial.begin(BAUD);
}


void loop() {
	print_celsius();
	delay(WAIT);
}
