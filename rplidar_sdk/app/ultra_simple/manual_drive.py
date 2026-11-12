import RPi.GPIO as GPIO
import sys, termios, tty

# Configuración de pines Motor A
IN1, IN2, ENA = 17, 27, 12
# Configuración de pines Motor B
IN3, IN4, ENB = 22, 23, 13

pwmA = None
pwmB = None

def init_gpio():
    global pwmA, pwmB
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
    GPIO.setup([ENA, ENB], GPIO.OUT)
    pwmA = GPIO.PWM(ENA, 1000)
    pwmB = GPIO.PWM(ENB, 1000)
    pwmA.start(0)
    pwmB.start(0)

def cleanup():
    if pwmA: pwmA.stop()
    if pwmB: pwmB.stop()
    GPIO.cleanup()

# --- Funciones de movimiento ---
def adelante(vel=50):
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(vel); pwmB.ChangeDutyCycle(vel)
    print("UGV adelante, velocidad:", vel)

def atras(vel=50):
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(vel); pwmB.ChangeDutyCycle(vel)
    print("UGV atrás, velocidad:", vel)

def izquierda(vel=50):
    GPIO.output(IN1, GPIO.HIGH); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(vel); pwmB.ChangeDutyCycle(vel)
    print("UGV girando izquierda")

def derecha(vel=50):
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH); GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(vel); pwmB.ChangeDutyCycle(vel)
    print("UGV girando derecha")

def stop():
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(0); pwmB.ChangeDutyCycle(0)
    print("UGV detenido")

# --- Modo consola WASD ---
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    try:
        init_gpio()
        print("Control WASD: W=adelante, S=atrás, A=izquierda, D=derecha, X=stop, Q=salir")
        while True:
            tecla = getch().lower()
            if tecla == 'w': adelante()
            elif tecla == 's': atras()
            elif tecla == 'a': izquierda()
            elif tecla == 'd': derecha()
            elif tecla == 'x': stop()
            elif tecla == 'q': break
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
        print("GPIO liberado, programa terminado")