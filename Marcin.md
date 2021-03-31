# Podprojekt  - sieć neuronowa"
**Twórca: Marcin Kwapisz** 

**Klawisz F7 uruchamia program**

Program otrzymuje zdjęcie aktualnego pola i za 
pomocą sieci neuronowej określa jakie to jest pole
i wybiera tryb w jakim ma pracować traktor

Sieć neuronowa została nauczona przy użyciu modułu darknet. Sieć została użyta po
20000 iteracjach treningowych

**Main**
```
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
```
Wywołuje wszystkie pozostałe funkcje programu

**Get_output_layers**
```
   def get_output_layers(self,net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers
```
Zwraca nazwy kolejnych warstw, warstwa wyjściowa nie jest połączona z żadną następną warstwą

**Recognition**
```
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
```
Odpowiada za odebranie zdjęcia od funkcji głównej i 
używa sieci neuronowej do rozpoznania zdjęcia

**Mode**
```
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
```
Na podstawie klasy otrzymanej przez funkcję **recognition** wybiera tryb
w jakim ma pracować traktor