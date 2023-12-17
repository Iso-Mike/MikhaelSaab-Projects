#include <stdio.h>
#include <string.h>

#define MAX_BUF  256
#define IV 0b11001011

unsigned char initKey();
unsigned char processKey(unsigned char);

void encode(unsigned char*, unsigned char*, unsigned char, int);
void decode(unsigned char*, unsigned char*, unsigned char, int);

unsigned char encryptByte(unsigned char, unsigned char, unsigned char);
unsigned char decryptByte(unsigned char, unsigned char, unsigned char);
unsigned char cShiftRight(unsigned char);
unsigned char cShiftLeft(unsigned char);

int readBytes(unsigned char*, int);
unsigned char getBit(unsigned char, int);
unsigned char setBit(unsigned char, int);
unsigned char clearBit(unsigned char, int);


int main() {
  char str[8];
  int  choice;

  unsigned char key;
  unsigned char pt[MAX_BUF] = {0};
  unsigned char ct[MAX_BUF] = {0};
  unsigned char userText;

  printf("\nYou may:\n");
  printf("  (1) Encrypt a message \n");
  printf("  (2) Decrypt a message \n");
  printf("  (0) Exit\n");
  printf("\n  what is your selection: ");
  fgets(str, sizeof(str), stdin);
  sscanf(str, "%d", &choice);


  switch (choice) {

    case 1:
      key = initKey();

      printf("\nEnter plaintext: ");
      getchar();
      userText = readBytes(pt, MAX_BUF);

      printf("\nCiphertext:");

      encode(pt, ct, key, userText);
      for(int i=0; i<userText; i++) {
        printf("%03d ", ct[i]);
      }
      
      break;

    case 2:
      key = initKey();

      printf("\nEnter ciphertext: ");
      
      int index = 0;
      int value;
      while(1) {
        scanf("%d", &value);
        if (value == -1) {
          break;
        }
        ct[index] = (unsigned char)value;
        index++;
      }

      decode(ct, pt, key, index);
      printf("%s", pt);

      break;

    default:

      break;
  }

  return(0);
}

/*
  Function:  initKey
   Purpose:  Prompts the user to enter a partial key, then initializes the full key
    return:  Returns the initialized key 
*/
unsigned char initKey() {
  int tempKey = 0;
  unsigned char key;

  while(1) {
    printf("Enter the partial key value (between 1 and 15): ");

    if (scanf("%d", &tempKey) != 1) {
      printf("Invalid input value must be an integer\n");
      while(getchar() != '\n');
      continue;
    } 
    
    if(tempKey < 1 || tempKey > 15) {
      printf("Invalid input value must be between 1 and 15\n");
      while(getchar() != '\n');
      continue;
    } 

    break;
  }

  key = (unsigned char)tempKey;

  key <<= 4;
  for(int i=7; i>=4; i--) {
    int secondaryPos = (i-1)%4;

    if(getBit(key, i) == 1) {
      key = clearBit(key, secondaryPos);
    } else {
      key = setBit(key, secondaryPos);
    }
  }
  return key;
}

/*
  Function:  processKey
   Purpose:  Updates the key from its current value
       out:  Key to be proccessed
    return:  The proccessed key
*/
unsigned char processKey(unsigned char currKey) {
  if(currKey%3 == 0){
    for(int i = 0; i < 3; i++) {
      currKey = cShiftLeft(currKey);
    }
  } else {
    for(int i = 0; i < 2; i++) {
      currKey = cShiftLeft(currKey);
    }
  }
  return currKey;
}

/*
  Function:  encryptByte
   Purpose:  Encrypts the given plaintext byte
        in:  Plain text to be encrypted
        in:  Key to help encrypt the code
        in:  Previous byte of ciphertext
    return:  The encrypted byte
*/
unsigned char encryptByte(unsigned char pt, unsigned char key, unsigned char prev) {
  unsigned char tempByte = 0;

  for(int i = 0; i < 8; i++) {
    if(getBit(key, i)) {
      prev = cShiftRight(prev);
    }

    if(getBit(pt, i) ^ getBit(prev, 7-i)) {
      tempByte = setBit(tempByte, i);
    } else {
      tempByte = clearBit(tempByte, i);
    }
  }
  return tempByte;
}

/*
  Function:  encode
   Purpose:  Encrypts each plaintext character in the array
        in:  Array of plaintext characters to be encrypted
       out:  Array of cipher characters to store the encrypted text
        in:  Key to be proccesed
        in:  Number of bytes 
*/
void encode(unsigned char *pt, unsigned char *ct, unsigned char key, int numBytes) {
  for(int i = 0; i< numBytes; i++) {
    key = processKey(key);
    if(i == 0) {
      ct[i] = encryptByte(pt[i], key, IV);
    } else {
      ct[i] = encryptByte(pt[i], key, ct[i-1]);
    }
  }
}

/*
  Function:  decryptByte
   Purpose:  Decrypts the given ciphertext byte
        in:  Cipher text to be decrypted 
        in:  Key to help decrypt the code
        in:  Previous byte of ciphertext
    return:  The decrypted byte
*/
unsigned char decryptByte(unsigned char ct, unsigned char key, unsigned char prev) {
  unsigned char tempByte = 0;

  for(int i = 0; i < 8; i++) {
    if(getBit(key, i)) {
      prev = cShiftRight(prev);
    }

    if(getBit(ct, i) ^ getBit(prev, 7-i)) {
      tempByte = setBit(tempByte, i);
    } else {
      tempByte = clearBit(tempByte, i);
    }
  }
  return tempByte;
}

/*
  Function:  decode
   Purpose:  Decrypts each ciphertext byte in the array
        in:  Array of ciphertext characters to be encrypted
       out:  Array of plain characters to store the decrypted text
        in:  Key to be proccesed
        in:  Number of bytes 
*/
void decode(unsigned char *ct, unsigned char *pt, unsigned char key, int numBytes) {
  for(int i = 0; i< numBytes; i++) {
    key = processKey(key);
    if(i == 0) {
      pt[i] = decryptByte(ct[i], key, IV);
    } else {
      pt[i] = decryptByte(ct[i], key, ct[i-1]);
    }
  }
}

/*
  Function:  readBytes
   Purpose:  reads characters from the standard input
       out:  the buffer containing the bytes read
        in:  the capacity of the buffer (maximum size)
    return:  the number of bytes actually read from the user
*/
int readBytes(unsigned char* buffer, int max) {
  int num = 0;

  fgets((char*)buffer, max, stdin);
  num = strlen((char*)buffer) - 1;
  buffer[num] = '\0';

  return num;
}

/*
  Function:  getBit
   Purpose:  retrieve value of bit at specified position
        in:  character from which a bit will be returned
        in:  position of bit to be returned
    return:  value of bit n in character c (0 or 1)
*/
unsigned char getBit(unsigned char c, int n) {
  return ((c & (1 << n)) >> n );
}

/*
  Function:  setBit
   Purpose:  set specified bit to 1
        in:  character in which a bit will be set to 1
        in:  position of bit to be set to 1
    return:  new value of character c with bit n set to 1
*/
unsigned char setBit(unsigned char c, int n) {
  return c | (1 << n);
}

/*
  Function:  clearBit
   Purpose:  set specified bit to 0
        in:  Byte to be shifted
        in:  position of bit to be set to 0
    return:  new value of character c with bit n set to 0
*/
unsigned char clearBit(unsigned char c, int n) {
  return c & (~(1 << n));
}

/*
  Function:  cShiftLeft
   Purpose:  Perform a circular left shift by one bit
       out:  Byte to be shifted
    return:  Byte after the shift
*/
unsigned char cShiftLeft(unsigned char byte) {
  char firstBit = getBit(byte, 7);
  byte <<= 1;
  if(firstBit == 0) {
    byte = clearBit(byte, 0);
  } else {
    byte = setBit(byte, 0);
  }
  return byte;
}

/*
  Function:  cShiftRight
   Purpose:  Perform a circular right shift by one bit
       out:  Byte to be shifted
    return:  Byte after the shift
*/
unsigned char cShiftRight(unsigned char byte) {
  char firstBit = getBit(byte, 0);
  byte >>= 1;
  if(firstBit == 0) {
    byte = clearBit(byte, 7);
  } else {
    byte = setBit(byte, 7);
  }
  return byte;
}