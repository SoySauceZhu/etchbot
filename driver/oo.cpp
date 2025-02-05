class LED
{
private:
    unsigned int pin;


public:
    LED()
    {
    };

    ~LED()
    {
    };

    void attach(unsigned int p)
    {
        pin = p;
        pinMode(pin, OUTPUT);
    };

    void on()
    {
        digitalWrite(pin, HIGH):
    };

    void off()
    {
        digitalWrite(pin, LOW);
    };

}
