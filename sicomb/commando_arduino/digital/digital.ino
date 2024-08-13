#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

// Criar uma instância de SoftwareSerial nos pinos 2 (RX) e 3 (TX)
SoftwareSerial mySerial(2, 3);

// Usar a instância de SoftwareSerial para o sensor de impressao digital
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

int num = 3;
int parm = -1;

void setup() {
  Serial.begin(115200);
  mySerial.begin(57600);  // Configurar a velocidade de comunicacao com o sensor

  while (!Serial);  // Para Yun/Leo/Micro/Zero/...
  delay(100);
  finger.begin(57600);
  delay(5);

  if (finger.verifyPassword()) {
    Serial.println("Sensor de impressao digital encontrado.");
  } else {
    Serial.println("Erro ao encontrar o sensor de impressao digital.");
    while (1) { delay(1); }
  }

  finger.getParameters();
  finger.getTemplateCount();

  Serial.println("Started");
}

void loop() {
  parm = -1;

  String inputString = "";
  String commandString = "";
  String firstParam = "";

  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n'); // Le até encontrar uma quebra de linha
    processCommand(inputString);
  }

  if (num == 1) {
    int findId = 1;
    Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo");

    while (findId != 0) {
      findId = getFingerprintID();
      delay(50);
    }

    num = 0;
  } else if (num == 2) {
    if (parm >= 0)
      while (!getFingerprintEnroll(parm));
    num = 0;
  } else if (num == 3) {
    while (1) {
      if (Serial.available()) {
        inputString = Serial.readStringUntil('\n'); // Le até encontrar uma quebra de linha
        processCommand(inputString);
      }

      if (num == 4) {
        break;
      }

      Serial.println("FINGERPRINT::SUCCESS::Started");
      num = 0;
    }
  }
}

// FUNcaO PARA LER A DIGITAL E RETORNAR O ID COM NÍVEL DE CONFIANcA
uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
  }

  // OK success!
  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("FINGERPRINT::ERROR::Nao foi encontrado nenhuma digital que pareie!");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("FINGERPRINT::ERROR::Erro de comunicacao com o sensor!");
      return p;
    case FINGERPRINT_FEATUREFAIL:
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.print("FINGERPRINT::");
    Serial.print(finger.fingerID);
    Serial.print("::");
    Serial.println(finger.confidence);
    return p;
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("FINGERPRINT::ERROR::Erro de comunicacao com o sensor!");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("FINGERPRINT::ERROR::Nao foi encontrado nenhuma digital que pareie!");
    return 0;
  } else {
    Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
    return p;
  }
}

// FUNcaO PARA CADASTRAR UMA NOVA DIGITAL
uint8_t getFingerprintEnroll(int value) {
  int p = -1;
  Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        break;
      case FINGERPRINT_NOFINGER:
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("Imaging error");
        break;
      default:
        Serial.println("Unknown error");
        break;
    }
  }

  // OK success!
  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }
  Serial.println("FINGERPRINT::USERMESSAGE::Remova o dedo!");
  delay(2000);
  p = 0;
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }

  Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo novamente");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        break;
      case FINGERPRINT_NOFINGER:
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("Imaging error");
        break;
      default:
        Serial.println("Unknown error");
        break;
    }
  }

  // OK success!
  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.createModel();
  if (p == FINGERPRINT_OK) {
    Serial.println("Prints matched!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    Serial.println("FINGERPRINT::ERROR::Dedo incorreto! Voce deve colocar o mesmo dedo!");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  Serial.print("ID ");
  Serial.println(value);
  p = finger.storeModel(value);
  if (p == FINGERPRINT_OK) {
    Serial.println("FINGERPRINT::SUCCESS");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("FINGERPRINT::ERROR::Erro de comunicacao com o sensor!");
    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {
    Serial.println("Could not store in that location");
    return p;
  } else if (p == FINGERPRINT_FLASHERR) {
    Serial.println("Error writing to flash");
    return p;
  } else {
    Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
    return p;
  }
  return true;
}

void processCommand(const String& input) {
  num = 0;
  parm = -1;

  int spaceIndex = input.indexOf(' ');

  if (spaceIndex != -1) {
    num = input.substring(0, spaceIndex).toInt();
    parm = input.substring(spaceIndex + 1).toInt();
  } else {
    num = input.toInt();
  }
}