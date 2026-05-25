import cv2
import time
import random
import imutils
from ultralytics import YOLO
from google.colab.patches import cv2_imshow



def process_video(video_path, model_path, save_path, image_size, half_precision):

  print("[INFO]: Video is processing..")

  processed_video = []
  font = cv2.FONT_HERSHEY_SIMPLEX

  model = YOLO(model_path)

  # Class Name and Colors
  class_list = model.names
  color_list = [[random.randint(0, 255) for _ in range(3)] for _ in class_list]

  cap = cv2.VideoCapture(video_path)

  # FPS Detection
  frame_count = 0
  total_fps = 0
  avg_fps = 0

  # FPS Video
  total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  frame_width = int(cap.get(3))
  frame_height = int(cap.get(4))

  while True:

    ret, frame = cap.read()
    if ret == False:
      break

    start = time.time()

    results = model.predict(frame, half=half_precision, imgsz=image_size, verbose=False)
    result = results[0].cpu()
    # print(result)

    xyxy = result.boxes.xyxy.numpy()
    confidence = result.boxes.conf.numpy()
    class_ids = result.boxes.cls.numpy().astype(int)

    results = list(zip(class_ids, confidence, xyxy))

    for result in results :

      class_id, score, box = result
      
      color = color_list[int(class_id)]
      class_name = class_list[int(class_id)]
      cv2.rectangle(frame, (int(box[0]),int(box[1])),  (int(box[2]),int(box[3])), color, 2)

      score = score * 100
      text = f"{class_name}: %{score:.2f}"

      cv2.putText(frame, text ,(int(box[0]), int(box[1] - 10 )), cv2.FONT_HERSHEY_SIMPLEX , 0.5, color, 2)

    end = time.time()
    # cv2_imshow(frame)

    # FPS
    frame_count += 1
    fps = 1 / (end - start)
    total_fps = total_fps + fps
    avg_fps = total_fps / frame_count

    avg_fps_str = float("{:.2f}".format(avg_fps))

    cv2.putText(frame, "FPS: "+str(avg_fps_str), (15, 40), font, 1, (0,0,0), thickness=2)

    processed_video.append(frame)

  out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'XVID'), int(avg_fps), (frame_width, frame_height))
  for frame in processed_video:
      out.write(frame)

  out.release()
  print("[INFO]: Processing task is completed successfully!..")
  print("Result video is saved in: " + save_path)