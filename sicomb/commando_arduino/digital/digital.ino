#include <Adafruit_Fingerprint.h>

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&Serial2);

int num = 3;
int parm = -1;

void setup()
{
  Serial.begin(115200);
  Serial1.begin(115200);

  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
  } else {
    while (1) { delay(1); }
  }

  finger.getParameters();
  finger.getTemplateCount();

	Serial.println("Started");
}

void loop()
{
  parm = -1;

  String inputString = "";
  String commandString = "";
  String firstParam = "";

  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n'); // Lê até encontrar uma quebra de linha

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
    while(1) {
      if (Serial.available()) {
        inputString = Serial.readStringUntil('\n'); // Lê até encontrar uma quebra de linha
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

// FUNCAO PARA LER A DIGITAL E RETORNAR O ID COM NIVEL CONFIANCA //
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
      // Serial.println("Image too messy");
      Serial.println("FINGERPRINT::ERROR::Não foi encontrado nenhuma digital que pareie!");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("FINGERPRINT::ERROR::Erro de comunicação com o sensor!");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      // Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      // Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
    default:
      Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
      return p;
  }
  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    // Serial.println("Found a print match!");
    Serial.print("FINGERPRINT::"); 
    Serial.print(finger.fingerID);
    Serial.print("::"); 
    // Serial.print("NIVEL DE CONFIANCA: "); 
    Serial.println(finger.confidence);
    return p;
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("FINGERPRINT::ERROR::Erro de comunicação com o sensor!");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    Serial.println("FINGERPRINT::ERROR::Não foi encontrado nenhuma digital que pareie!");
    return 0;
  } else {
    Serial.println("FINGERPRINT::ERROR::Erro desconhecido!");
    return p;
  }
}


// FUNCAO PARA CADASTRAR UMA NOVA DIGITAL //
uint8_t getFingerprintEnroll(int value)
{
  int p = -1;
  Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo");
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      // Serial.println("Image taken");
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
  switch (p)
  {
  case FINGERPRINT_OK:
    // Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
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
  while (p != FINGERPRINT_NOFINGER)
  {
    p = finger.getImage();
  }
  // Serial.print("ID ");
  // Serial.println(value);
  p = -1;
  Serial.println("FINGERPRINT::USERMESSAGE::Coloque o dedo novamente");
  while (p != FINGERPRINT_OK)
  {
    p = finger.getImage();
    switch (p)
    {
    case FINGERPRINT_OK:
      // Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      // Serial.print(".");
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
  switch (p)
  {
  case FINGERPRINT_OK:
    // Serial.println("Image converted");
    break;
  case FINGERPRINT_IMAGEMESS:
    Serial.println("Image too messy");
    return p;
  case FINGERPRINT_PACKETRECIEVEERR:
    Serial.println("Communication error");
    return p;
  case FINGERPRINT_FEATUREFAIL:
    Serial.println("Could not find fingerprint features");
    return p;
  case FINGERPRINT_INVALIDIMAGE:
    Serial.println("Could not find fingerprint features");
    return p;
  default:
    Serial.println("Unknown error");
    return p;
  }
  // OK converted!
  // Serial.print("Creating model for #");
  // Serial.println(value);
  p = finger.createModel();
  if (p == FINGERPRINT_OK)
  {
    Serial.println("Prints matched!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_ENROLLMISMATCH)
  {
    Serial.println("FINGERPRINT::ERROR::Dedo incorreto! Você deve colocar o mesmo dedo!");
    return p;
  }
  else
  {
    Serial.println("Unknown error");
    return p;
  }

  Serial.print("ID ");
  Serial.println(value);
  p = finger.storeModel(value);
  if (p == FINGERPRINT_OK)
  {
    Serial.println("FINGERPRINT::SUCCESS");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR)
  {
    Serial.println("FINGERPRINT::ERROR::Erro de comunicação com o sensor!");
    return p;
  }
  else if (p == FINGERPRINT_BADLOCATION)
  {
    Serial.println("Could not store in that location");
    // Serial.println("FINGERPRINT::ERROR::Erro!");
    return p;
  }
  else if (p == FINGERPRINT_FLASHERR)
  {
    Serial.println("Error writing to flash");
    // Serial.println("FINGERPRINT::ERROR::Erro!");
    return p;
  }
  else
  {
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