import cv2
import numpy as np
import threading
# import pythonToArduino as pa

# 設定
color = 1 # 検出する色を指定（1=青,2=緑,3=赤,0=黒）
# カメラ番号を指定
cam_id = 1
# IP WebcamのURLを指定
webcam = False
url='http://192.168.43.146:8080/shot.jpg'
# 画像表示用の変数
g_frame = None
g_dst = None
g_mask = None
g_hsv = None

# 迷路を検出して台形補正する
def keystone_correction(img):
    # 大きさの計算
    size = img.shape[0] * img.shape[1]
    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 入力座標の選定
    best_white = 0
    best_approx = []
    # スレッシュホールドを変えて対象が見つかるまでループする
    for white in range(50, 150, 20):
        # 二値化
        ret, th1 = cv2.threshold(gray, white, 255, cv2.THRESH_BINARY)
        # 輪郭抽出
        image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 角の数が4つ、面積が10%〜70%を満たすものを選定
        max_area = 0
        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            tmp = cv2.approxPolyDP(cnt, epsilon, True)
            if 4 == len(tmp):
                area = cv2.contourArea(tmp)
                if max_area < area and size * 0.1 <= area and area <= size * 0.7:
                    best_approx = tmp
                    max_area = area
        if 0 != max_area:
            best_rate = max_area / size * 100
            best_white = white
            break
    # 台形が見つかったか判定
    if 0 == best_white:
        # print("The analysis failed.")
        return None
    # 4つの頂点を並び替える
    points = sorted(best_approx[:,0,:], key=lambda x:x[1]) # yが小さいもの順に並び替え。
    top = sorted(points[:2], key=lambda x:x[0]) # 前半二つは四角形の上。xで並び替えると左右も分かる。
    bottom = sorted(points[2:], key=lambda x:x[0], reverse=True) # 後半二つは四角形の下。同じくxで並び替え。
    points = top + bottom # 分離した二つを再結合。
    # 台形補正を実行
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[364,0],[364,257],[0,257]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(364,257))
    # 結果出力
    # print("Best parameter: white={} (rate={})".format(best_white, best_rate))
    # 検出した矩形を表示
    cv2.drawContours(img, [best_approx], -1, (0, 255, 0), 3)
    return dst

# 各色の位置を検出する
def color_pick(img, color):
    global g_hsv





    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    g_hsv = cv2.hconcat(cv2.split(hsv))
    # 最大の領域を選定
    max_area = 0
    best_cnt = None
    for cnt in contours:
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        tmp = cv2.approxPolyDP(cnt, epsilon, True)
        area = cv2.contourArea(tmp)
        if max_area < area:
            best_cnt = cnt
            max_area = area
    # 対象が見つかったか判定
    if best_cnt is None:
        # print("color pick failed.")
        return None, None, None
    # 領域の重心を計算
    try:
        M = cv2.moments(best_cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    except ZeroDivisionError:
        # たまにゼロ割になってしまうケースが有るので対処
        print("ZeroDivisionError!!")
        return None, None, None
    # 検出した領域を表示
    cv2.drawContours(img, [best_cnt], -1, (0, 255, 0), 3)
    return mask, cx, cy


def color_select(hue: object, image: object) -> object:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue += 180
    hue %= 180
    range = 20
    hue_max = hue + range
    hue_min = hue - 20
    hsv_min = np.array([hue_min, 60, 60])
    hsv_max = np.array([hue_max, 255, 255])
    if hue_min < hue_max:
        mask: None = cv2.inRange(hsv, hsv_min, hsv_max)
    else:
        mask = cv2.inRange(hsv, 0, hsv_max)
        mask += cv2.inRange(hsv, hsv_min, 180)
    return mask


def detect_center_of_gravity(cnt):
    try:
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M["m00"])
        cy = int(M['m01'] / M["m00"])
        return cx, cy
    except ZeroDivisionError:
        # たまにゼロ割になってしまうケースが有るので対処
        print("ZeroDivisionError!!")


def nothing():
    pass


# 画像処理スレッド
def capture_thread():
    global g_frame
    global g_dst
    global g_mask

    # FPS計算用の変数を初期化
    base_t = prev_t = time.perf_counter()
    current_t = 0
    cnt = 0
    while 1:
        if webcam:
            # Use urllib to get the image from the IP camera
            imgResp = urllib.request.urlopen(url)
            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            # Finally decode the array to OpenCV usable format ;)
            frame = cv2.imdecode(imgNp, -1)
        else:
            # 動画を1フレーム読み込む
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 360))
        if frame is None:
            cv2.waitKey(1)
            continue
        # 迷路を検出して台形補正する
        dst = keystone_correction(frame)
        g_frame = frame
        if dst is not None:
            # 迷路の中から指定色の物体を検出する
            mask, cx, cy = color_pick(dst, color)
            g_dst = dst
            g_mask = mask
            if cx is not None and cy is not None:
                # mqttで座標を送信
                client.publish('enemy', '%d:%d' % (cx, cy))
        # FPSを計算する
        current_t = time.perf_counter()
        cnt += 1
        dt = current_t - base_t
        if dt > 1.0:
            base_t = current_t
            fps = cnt / dt
            cnt = 0
            print('fps = %.2f' % fps)
        # FPS調整用のSleep時間を計算
        # current_t = time.perf_counter()
        # dt = 0.095 - (current_t - prev_t)
        # if dt > 0:
        #     time.sleep(dt)
        # prev_t = time.perf_counter()


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 500, 300)
# Create trackbars for color change
cv2.createTrackbar('Hue', 'image', 0, 180, nothing)

cap = cv2.VideoCapture(0)

# 画像処理スレッドを立ち上げる
th = threading.Thread(target=capture_thread)
th.start()

if cap.isOpened() != 1:
    print('カメラが接続されていない')
kernel = np.ones((5, 5), np.uint8)
while cap.isOpened():
    timeave = 0
    for i in range(10):
        k = cv2.waitKey(1 & 0xFF)
        if k == 27:
            break
        hue = cv2.getTrackbarPos('Hue', 'image')
        # Capture frame-by-
        # e1 = cv2.getTickCount()

        # 通しで100msec
        ret, frame = cap.read()  # 15msec
        mask = color_select(hue, frame)  # 10msec
        # cv2.imshow('mask', mask)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 1msec
        cv2.imshow('opening', opening)
        image, contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 1msec
        contours.sort(key=cv2.contourArea, reverse=True)  # 0msec
        cv2.putText(frame, 'count =' + str(len(contours)), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1,
                    cv2.LINE_AA)  # 0msec
        if len(contours) > 0:  # 1msec
            cv2.drawContours(frame, [contours[0]], 0, (0, 255, 0), 3)
            cx, cy = detect_center_of_gravity(contours[0])
            cv2.putText(frame, " (" + str(cx) + "," + str(cy) + ")", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 0), 1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 0), -1)
            x = cx
        cv2.imshow('image', frame)  # 65msec
        # e2 = cv2.getTickCount()
        # pa.sendtoArd(x)
        # print(x)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time = (e2 - e1) / cv2.getTickFrequency()
        # timeave = (timeave * i + time) / (i + 1)
    # print(timeave)

cap.release()
cv2.destroyAllWindows()
