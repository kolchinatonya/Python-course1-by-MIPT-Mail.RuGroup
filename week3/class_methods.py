import os


class CarBase:
    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

    def __init__(self, brand, photo_file_name, carrying, car_type=None):
        if brand == "":
            raise TypeError
        self.brand = brand
        self.photo_file_name = photo_file_name
        if self.get_photo_file_ext() not in {'.jpg', '.jpeg', '.png', '.gif'}:
            raise TypeError
        self.carrying = float(carrying)
        self.car_type = car_type

    def __str__(self):
        return self.car_type

    def __repr__(self):
        return f"solution.{self.car_type.title()}"


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying, 'car')
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    @staticmethod
    def parse_truck_params(body_whl):
        try:
            w_h_l = [float(i) for i in body_whl.split('x')]
            if len(w_h_l) != 3 or any(t < 0 for t in w_h_l):
                return [0.0, 0.0, 0.0]
            return w_h_l
        except ValueError:
            return [0.0, 0.0, 0.0]
        return w_h_l

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying, 'truck')
        self.body_length, self.body_width, self.body_height = self.parse_truck_params(body_whl)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying, 'spec_machine')
        if extra == "":
            raise TypeError
        self.extra = extra


def read_csv(csv_filename):
    import csv
    try:
        res = []
        with open(csv_filename, 'r') as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                res.append(row)
    except FileNotFoundError:
        return []
    return res


def get_car_list(csv_filename):
    csv_list = read_csv(csv_filename)
    car_list = []
    for item in csv_list:
        if len(item) != 7:
            continue
        try:
            if item[0] == 'car':
                car_list.append(Car(item[1], item[3], item[5], item[2]))
            if item[0] == 'truck':
                car_list.append(Truck(item[1], item[3], item[5], item[4]))
            if item[0] == 'spec_machine':
                car_list.append(SpecMachine(item[1], item[3], item[5], item[6]))
        except (TypeError, ValueError):
            pass
    return car_list