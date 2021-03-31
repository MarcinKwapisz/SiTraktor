import numpy as np
import cv2
import pygame


class main():
    def __init__(self,traktor,field,ui,path):
        self.traktor = traktor
        self.field = field
        self.ui = ui
        self.path = path
        self.mode_value = 0

    def get_output_layers(self,net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    def recognition(self,photo):
        image = photo

        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        with open("si.names", 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

        net = cv2.dnn.readNet("si_20000.weights", "si.cfg")

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(self.get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    class_ids.append(class_id)
        return class_ids[0]

    def main(self):
        self.pole = self.ui.field_images[self.field.get_value(self.traktor.get_poz())]
        self.img = pygame.surfarray.array3d(self.pole)
        self.img = self.img.transpose([1,0,2])
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        self.reco = self.mode(self.recognition(self.img))
        if self.reco == 10:
            print("Nic nie trzeba robić")
        else:
            self.traktor.set_mode(self.reco)

    def mode(self,mode):
        self.mode_value = mode
        if self.mode_value in [0, 1, 2, 3]:
            return 0
        elif self.mode_value in [1, 3, 5, 7]:
            return 1
        elif self.mode_value in [0, 1, 4, 5]:
            return 2
        elif self.mode_value in [8]:
            return 3
        elif self.mode_value in [6]:
            return 10

    def main_collective(self,poz = None):
        if poz is None:
            poz = self.traktor.get_poz()
        self.pole = self.ui.field_images[self.field.get_value(poz)]
        self.img = pygame.surfarray.array3d(self.pole)
        self.img = self.img.transpose([1, 0, 2])
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        self.reco = self.recognition(self.img)
        return self.reco