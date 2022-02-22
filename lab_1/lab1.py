from PIL import Image
import numpy as np

'''
# task 1
im = Image.new('RGB', (800, 600))

arr = np.array(im)

for i in range(600):
    for j in range(800):
        #for k in range(3):
            #arr[i, j, k] = 0 # 1.1 task
            #arr[i, j, k] = 255 # 1.2 task
        #arr[i, j] = (255, 128, 0) # 1.3 task
        elem = (i + j)%256 #1.4 task
        arr[i, j] = (elem, elem, elem) #1.4 task
im = Image.fromarray(arr)
im.save('image 1_4.png', srgb=3)
'''


class MyImage:

    def __init__(self):
        self.img_arr = []
        self.width = 0
        self.heigh = 0
        self.delta_t = 0.01

    def arr_init(self, width, height, color=(0, 0, 0)):
        self.img_arr = np.zeros((width, height, 3), dtype=np.uint8)
        self.width = width
        self.height = height
        if color != (0, 0, 0):
            for i in range(width):
                for j in range(height):
                    self.img_arr[i, j] = color

    def save(self, file, **params):
        im = Image.fromarray(self.img_arr, 'RGB')
        im.save(file, **params)

    def show(self):
        im = Image.fromarray(self.img_arr, 'RGB')
        im.show()

    def draw_line_1(self, start_point, end_point, color=(255, 255, 255)):
        x0 = start_point[0]
        x1 = end_point[0]
        y0 = start_point[1]
        y1 = end_point[1]
        for t in np.arange(0, 1, self.delta_t):
            x = int(x1 * t + x0 - x0 * t)
            y = int(y1 * t + y0 - y0 * t)
            self.img_arr[y, x] = color

    def draw_line_2(self, start_point, end_point, color=(255, 255, 255)):
        x0 = int(start_point[0])
        x1 = int(end_point[0])
        y0 = start_point[1]
        y1 = end_point[1]
        for x in range(x0, x1 + 1):
            t = (x - x0) / (x1 - x0)
            y = int(y0 - y0 * t + y1 * t)
            self.img_arr[y, x] = color

    def draw_line_2_fixed(self, start_point, end_point, color=(255, 255, 255)):
        x0 = int(start_point[0])
        x1 = int(end_point[0])
        y0 = int(start_point[1])
        y1 = int(end_point[1])
        steep = False
        if (abs(x0 - x1) < abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in range(x0, x1 + 1):
            t = (x - x0) / (x1 - x0)
            y = int(y0 - y0 * t + y1 * t)
            if steep:
                self.img_arr[x, y] = color
            else:
                self.img_arr[y, x] = color

    def draw_line_brezenhem(self, start_point, end_point, color=(255, 255, 255)):
        x0 = start_point[0]
        x1 = end_point[0]
        y0 = start_point[1]
        y1 = end_point[1]
        steep = False
        if (abs(x0 - x1) < abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        derr = abs(dy / dx)
        error = 0
        y = int(y0)
        for x in range(int(x0), int(x1 + 1)):
            if steep:
                self.img_arr[x, y] = color
            else:
                self.img_arr[y, x] = color
            error += derr
            if error > 0.5:
                if y1 > y0:
                    y += 1
                else:
                    y -= 1
                error -= 1


'''                
img = MyImage()
img.arr_init(200, 200)
for i in range(0, 13):
    alpha = 2*np.pi*i/13
    img.draw_line_brezenhem((100, 100), (100 + 95*np.cos(alpha), 100 + 95*np.sin(alpha)))
img.save('image 2_4.png', srgb=3)
img.show()
'''


class ObjParsed:

    def __init__(self):
        self.dots_arr = []
        self.polygons = []

    def from_obj_file(self, filepath):
        '''
        v - dots
        vt - texture
        vn - normals_index
        f v1\vt1\vn1 v2\vt2\vn2 v3\vt3\vn3 ... - polygon
        '''
        obj = open(filepath)
        string_obj = obj.read()
        dot_lines = [x for x in string_obj.split('\n') if 'v ' in x]
        f_lines = [f for f in string_obj.split('\n') if 'f ' in f]
        for line in dot_lines: # saving dots
            splitted = line.split()
            dot = [float(splitted[1]), float(splitted[2]), float(splitted[3])]
            self.dots_arr.append(dot)
        for line in f_lines: # saving lines
            splitted = line.split()
            poly = []
            for i in (1, len(splitted) -1 ):
                poly.append(int(splitted[i].split('/')[0]))
            self.polygons.append(poly)


    def task5(self):
        img_array = np.zeros((1000, 1000, 3), dtype=np.uint8)
        for dot in self.dots_arr:
            x = dot[0]
            y = dot[1]
            i = int(50 * x + 500)
            j = int(50 * y + 500)
            img_array[-j, i] = (255, 255, 255)
        im = Image.fromarray(img_array)
        im.show()
        im.save('helmet1.png', srgb=3)

    def task7(self):
        image = MyImage()
        image.arr_init(1000,1000)
        for poly in self.polygons:
            for i in range(1, len(poly)):
                start_dot_with_z = self.dots_arr[poly[i-1] - 1]
                end_dot_with_z = self.dots_arr[poly[i] - 1]
                start_dot = (start_dot_with_z[0] * 50 + 500, -(start_dot_with_z[1] * 50 + 500))
                end_dot = (end_dot_with_z[0] * 50 + 500, -(end_dot_with_z[1] * 50 + 500))
                if start_dot == end_dot:
                    continue
                image.draw_line_brezenhem(start_dot, end_dot, (255,255,255))
        image.show()
        image.save('helmet2.png', srgb = 3)




obj = ObjParsed()

obj.from_obj_file("StormTrooper.obj")
obj.task7()