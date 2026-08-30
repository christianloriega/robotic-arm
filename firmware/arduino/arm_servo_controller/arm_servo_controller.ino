#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN 500
#define SERVOMAX 2500

#define SERVO_COUNT 6

// Maximum angle for each servo
const int MAX_ANGLE[SERVO_COUNT] = {
  270, // Servo 0 - 40kg
  270, // Servo 1 - 40kg
  270, // Servo 2 - 25kg
  180, // Servo 3 - MG90S
  180, // Servo 4 - MG90S
  180, // Servo 5 - MG90S
};

int angleToMicroseconds(int servo, int angle){
  return  map(angle, 0, MAX_ANGLE[servo], SERVOMIN, SERVOMAX);
}

void setup() {
  Serial.begin(115200);

  pwm.begin();
  pwm.setPWMFreq(50);

  delay(500);

  Serial.println("Arm Initilizing");
}

void loop()
{
  if (Serial.available())
  {
    String command = Serial.readStringUntil('\n');
    command.trim();

    int angles[SERVO_COUNT];

    int parsed = sscanf(
      command.c_str(),
      "%d,%d,%d,%d,%d,%d",
      &angles[0],
      &angles[1],
      &angles[2],
      &angles[3],
      &angles[4],
      &angles[5]
    );

    if (parsed == SERVO_COUNT)
    {
      for (int i = 0; i < SERVO_COUNT; i++)
      {
        angles[i] = constrain(
          angles[i],
          0,
          MAX_ANGLE[i]
        );

        int pulse = angleToMicroseconds(i, angles[i]);

        pwm.writeMicroseconds(i, pulse);
      }

      Serial.print("Moved: ");

      for (int i = 0; i < SERVO_COUNT; i++)
      {
        Serial.print(angles[i]);

        if (i < SERVO_COUNT - 1)
        {
          Serial.print(",");
        }
      }

      Serial.println();
    }
    else
    {
      Serial.println("ERROR: expected 6 angles");
    }
  }
}
