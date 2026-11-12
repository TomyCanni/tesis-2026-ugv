from flask import Flask, render_template, Response, request
import socket, struct, cv2, threading, time
from collections import deque

# Importar el módulo de control
import manual_drive as control

app = Flask(__name__)

# Inicializar GPIO al arrancar el servidor
control.init_gpio()

# --- Cámara: abrir una sola vez ---
cap = cv2.VideoCapture(0)

def gen_camera():
    while True:
        if not cap.isOpened():
            cap.open(0)
        ret, frame = cap.read()
        if not ret:
            continue
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# --- LIDAR: socket y buffer circular ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 9000))
s.listen(1)
print("Servidor LIDAR escuchando en puerto 9000...")

print("Esperando conexión del LIDAR...")
conn, _ = s.accept()
print("Conexión LIDAR establecida.")

lidar_buffer = deque(maxlen=3)

def lidar_reader():
    global lidar_buffer
    while True:
        try:
            size_data = conn.recv(4)
            if not size_data:
                continue
            size = struct.unpack("I", size_data)[0]
            data = b''
            while len(data) < size:
                packet = conn.recv(size - len(data))
                if not packet:
                    break
                data += packet
            if data:
                lidar_buffer.append(data)
        except Exception as e:
            print("Error en LIDAR:", e)
            break

threading.Thread(target=lidar_reader, daemon=True).start()

def gen_lidar():
    global lidar_buffer
    while True:
        if lidar_buffer:
            frame = lidar_buffer[-1]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/camera')
def camera():
    return Response(gen_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/lidar')
def lidar():
    return Response(gen_lidar(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Endpoint de control para el dashboard ---
@app.route('/control', methods=['POST'])
def control_endpoint():
    cmd = request.json.get('command')
    if cmd == 'w': control.adelante()
    elif cmd == 's': control.atras()
    elif cmd == 'a': control.izquierda()
    elif cmd == 'd': control.derecha()
    elif cmd == 'x': control.stop()
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)