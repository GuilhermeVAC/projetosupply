#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Guilherme";  // Substitua com o nome da sua rede Wi-Fi
const char* password = "1a2b3c4d";  // Substitua com a sua senha Wi-Fi
const char* url = "http://192.168.2.132:5000/api/sensor";  // Substitua com o endereço do seu servidor

const int pirPin = D4;  // Pino do sensor PIR (no seu caso, D4)

WiFiClient client;
HTTPClient http;

bool lastSensorState = LOW;  // Armazena o último estado do sensor
bool motionSent = false;  // Controla se o movimento já foi enviado

void setup() {
  Serial.begin(115200);  // Inicializa a comunicação serial
  pinMode(pirPin, INPUT);  // Define o pino do sensor como entrada

  // Conecta ao Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println();
  Serial.print("Conectando-se ao WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Conexão estabelecida!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void enviarDados(int estado) {
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(client, url);  // Inicia a requisição HTTP
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"posicao_movimentada\":\"A1\", \"estado_sensor\":" + String(estado) + "}";
    int httpResponseCode = http.POST(jsonData);  // Envia os dados para o servidor

    if (httpResponseCode > 0) {
      Serial.println("Dados enviados com sucesso!");
    } else {
      Serial.println("Erro ao enviar dados. Código de resposta: " + String(httpResponseCode));
    }

    http.end();  // Finaliza a requisição HTTP
  } else {
    Serial.println("Erro na conexão WiFi");
  }
}

void loop() {
  // Monitoramento contínuo da conexão
  static unsigned long lastCheck = 0;
  if (millis() - lastCheck >= 5000) {
    Serial.println("\n=== Status do Sistema ===");
    Serial.println("Uptime: " + String(millis() / 1000) + " segundos");

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("WiFi conectado");
      Serial.println("IP: " + WiFi.localIP().toString());
      Serial.println("Força do sinal: " + String(WiFi.RSSI()) + " dBm");
    } else {
      Serial.println("WiFi desconectado - Status: " + String(WiFi.status()));
    }

    // Leitura do sensor
    int sensorValue = digitalRead(pirPin);
    Serial.println("Estado do sensor PIR: " + String(sensorValue));

    // Se o sensor detectar movimento (estado 1) e o movimento não foi enviado ainda
    if (sensorValue == HIGH && lastSensorState == LOW) {
      Serial.println("Movimento detectado!");
      enviarDados(1);  // Envia a informação para o servidor
      motionSent = true;  // Marca que o movimento foi enviado
    } 
    
    // Se o sensor voltar ao estado LOW (sem movimento), não envia nada para o servidor
    else if (sensorValue == LOW) {
      Serial.println("Sem movimento");
      motionSent = false;  // Permite que o próximo movimento seja enviado
    }

    // Atualiza o último estado do sensor
    lastSensorState = sensorValue;

    lastCheck = millis();
  }

  delay(100);
}
