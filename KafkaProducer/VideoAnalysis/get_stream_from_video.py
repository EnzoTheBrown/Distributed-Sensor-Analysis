import cv2


class CatchStream:
    def __init__(self, link):
        self.link = link

    def chunk_stream(self, chunk_size):
        while True:
            pass
            # get the stream func
            # open a thread 10 size in sec
            # when the timer down cut the stream send it to handle stream
            # and restart the func


class HandleStream:
    def __init__(self, file_name):
        if type(file_name) is list:
            self.is_list = True
            self.caps = []
            for file_namee in file_name:
                caps.append(cv2.VideoCapture(file_namee))
        else:
            self.is_list = False
            self.cap = cv2.VideoCapture(file_name)

    def divide_stream(self):
        _, frame = self.cap.read()
        if frame is not None:
            height, width, channels = frame.shape
            # upper left corner
            frame_upper_left_corner = frame[0:int(height/2) + 50, 0:int(width/2) + 50]
            # down left corner
            frame_down_left_corner = frame[int(height/2) - 50: height, 0:int(width/2)]
            # upper right corner
            frame_upper_right_corner = frame[0:int(height/2) + 50, int(width/2) - 50:width]
            # down right corner
            frame_down_right_corner = frame[int(height/2) - 50:height, int(width/2) - 50:width]
            # on peut récuperer ce flux en l'encodant en bytes et en l'envoyant sous format JSon à l'application voulue
            return [frame_upper_left_corner, frame_down_left_corner, frame_upper_right_corner, frame_down_right_corner]

    def divide_streams(self):
        return [cc.read() for cc in self.caps]

    def get_flow(self):
        if self.is_list:
            return divide_streams()
        return divide_stream()


    @staticmethod
    def get_image(list_images):
        i = 0
        for img in list_images:
            cv2.imshow("img"+str(i), img)
            i += 1

    def display(self):
        while True:
            self.get_image(self.divide_stream())
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        self.cap.release()
        cv2.destroyAllWindows()


# stream = HandleStream('people-walking.mp4')
# stream.display()
