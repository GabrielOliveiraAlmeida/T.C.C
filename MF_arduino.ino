// Esse codigo recebe um valor para setar o respectivo PWM na saída da ESP-32
// Esse codigo envia um valor de tempo T1, representando o tempo entre dois pulsos consecutivos
// Como eu posso fazer pra uma saida não interferir na leitura?


String texto;
char caractere;

int n= 0;
int ledAzul = 2;
int ledPWM = 14;
int entrada = 4;
unsigned long k = 1000;

int  pulso = 0;
unsigned long delta = 0;
unsigned long tempoant = 0;
float Rpm = 0;
float A = 0;
int PWM_int;
int a;


void IRAM_ATTR funcao_ISR()
 { 
  if(n==0)
  {
    tempoant = millis();
    n = 1;
  }
  else if (n==1)
  { 
  delta = (millis()-tempoant);
  tempoant = millis(); 
  }
}

void setup() {
  Serial.begin(9600);
  attachInterrupt(entrada, funcao_ISR, RISING);
  ledcAttachPin(ledPWM,0);
  ledcSetup(0,490,10);
  ledcWrite(0,1023);
}

 void loop() {

  if(Serial.available() > 0)
    {
    caractere = Serial.read();
    if (caractere == 'r')
    {
      Serial.println(delta);
    }

    else if (caractere == 'x')
    {
      delta = 0;
      n = 0;
      ledcWrite(0,1023);
    }

    else if (caractere == 'w')
    { 
       PWM_int = texto.toInt();
       ledcWrite(0,PWM_int);
       texto = "";
    }
    else texto.concat(caractere);
    }

}





