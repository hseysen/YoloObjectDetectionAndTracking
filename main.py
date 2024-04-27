import torch
from PIL import Image
import cv2
import tracking


class ObjectTracker:
    def __init__(self, video_file):
        # Inference
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5x", pretrained=True)
        self.model.eval()

        # Tracking
        self.objects = []

        # Video Input
        self.video_capture = cv2.VideoCapture(video_file)
        self.video_fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_dims = (self.video_width, self.video_height)
        self.video_total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # Video Output
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_output = cv2.VideoWriter("videos/result.mp4", self.fourcc, self.video_fps, self.video_dims)

        # Customization
        self.bbox_color = (0, 153, 255)
        self.bbox_thickness = 2
        self.text_font_scale = 1
        self.text_color = (0, 0, 255)
        self.text_thickness = 2
        self.circle_radius = 5
        self.circle_color = (0, 255, 0)
        self.circle_thickness = -1
        self.line_color = (255, 125, 0)
        self.line_thickness = 2
    
    def __del__(self):
        self.video_capture.release()
        self.video_output.release()

    @staticmethod
    def preprocess_image(image):
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    def draw_inference(self, frame, inference, _id, fell):
        x_min, y_min, x_max, y_max, centroid_x, centroid_y = inference
        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), self.bbox_color, self.bbox_thickness)
        cv2.putText(frame, f"person {_id} (Fell: {'yes' if fell else 'no'})", (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, self.text_font_scale, self.text_color, self.text_thickness)
        cv2.circle(frame, (centroid_x, centroid_y), self.circle_radius, self.circle_color, self.circle_thickness)
        return frame

    def run(self):
        current_frame = 0
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            cv2.line(frame, tracking.line1.start, tracking.line1.end, self.line_color, self.line_thickness)
            cv2.line(frame, tracking.line2.start, tracking.line2.end, self.line_color, self.line_thickness)

            results = self.model(self.preprocess_image(frame))
            boxes = results.xyxy[0][:, :4].cpu().numpy()
            labels = results.xyxy[0][:, 5].cpu().numpy()

            current_frame_objects = []
            for box, label in zip(boxes, labels):
                if int(label) == 0:
                    x_min, y_min, x_max, y_max = box
                    centroid_x = int((x_min + x_max) / 2)
                    centroid_y = int((y_min + y_max) / 2)
                    current_frame_objects.append((x_min, y_min, x_max, y_max, centroid_x, centroid_y))

            new_objects = []
            object_pool = self.objects.copy()
            for i, inference in enumerate(current_frame_objects):
                x_min, y_min, x_max, y_max, centroid_x, centroid_y = inference
                closest_dist = float("inf")
                closest_indx = -1
                for k, object in enumerate(object_pool):
                    dist = object.get_distance(centroid_x, centroid_y)
                    if dist > 200:
                        continue
                    if closest_dist > dist:
                        closest_dist = dist
                        closest_indx = k
                if closest_indx == -1:
                    new_objects.append(i)
                else:
                    this_obj = object_pool.pop(closest_indx)
                    for obj in self.objects:
                        if obj == this_obj:
                            obj.update(centroid_x, centroid_y)
                    frame = self.draw_inference(frame, inference, this_obj.id, this_obj.fell)
            
            for i, object in reversed(list(enumerate(self.objects))):
                if object in object_pool:
                    if object.can_remove():
                        self.objects.pop(i)
            for i in new_objects:
                x_min, y_min, x_max, y_max, centroid_x, centroid_y = current_frame_objects[i]
                new_obj = tracking.Object(centroid_x, centroid_y)
                self.objects.append(new_obj)
                frame = self.draw_inference(frame, inference, new_obj.id, new_obj.fell)
            
            self.video_output.write(frame)
            current_frame += 1
            print(f"Progress: {current_frame}/{self.video_total_frames}", end="\r")


def main():
    tracker = ObjectTracker("videos/cs.mp4")
    tracker.run()
    print("\nFinished Running!")


if __name__ == "__main__":
    main()
