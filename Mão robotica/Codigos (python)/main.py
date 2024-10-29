import cv2
import mediapipe as mp
import servo_braco3d as mao

cap = cv2.VideoCapture(0, cv2.CAP_ANY)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

cap.set(3, 640)
cap.set(4, 480)

hands = mp.solutions.hands
Hands = hands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    if not success:
        print("Falha ao capturar imagem.")
        break
    
    img = cv2.flip(img, 1)  # Inverte horizontalmente a imagem

    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hands.process(frameRGB)
    handPoints = results.multi_hand_landmarks
    h, w, _ = img.shape
    pontos = []

    if handPoints:
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                cv2.circle(img, (cx, cy), 4, (255, 0, 0), -1)
                pontos.append((cx, cy))

            if pontos:
                distPolegar = abs(pontos[17][0] - pontos[4][0])
                distIndicador = pontos[5][1] - pontos[8][1]
                distMedio = pontos[9][1] - pontos[12][1]
                distAnelar = pontos[13][1] - pontos[16][1]
                distMinimo = pontos[17][1] - pontos[20][1]

                if distPolegar < 80:
                    mao.abrir_fechar(10, 0)
                else:
                    mao.abrir_fechar(10, 1)

                if distIndicador >= 1:
                    mao.abrir_fechar(9, 1)
                else:
                    mao.abrir_fechar(9, 0)

                if distMedio >= 1:
                    mao.abrir_fechar(8, 1)
                else:
                    mao.abrir_fechar(8, 0)

                if distAnelar >= 1:
                    mao.abrir_fechar(7, 1)
                else:
                    mao.abrir_fechar(7, 0)

                if distMinimo >= 1:
                    mao.abrir_fechar(6, 1)
                else:
                    mao.abrir_fechar(6, 0)

    cv2.imshow('Imagem', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressione 'q' para sair
        break

cap.release()
cv2.destroyAllWindows()
