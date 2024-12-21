import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt

class CostCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Себестоимость продукции растениеводства")
        self.setGeometry(200, 200, 600, 400)

        # Поля ввода
        self.create_input_fields()

        # Кнопки
        self.calc_button = QPushButton("Рассчитать себестоимость")
        self.calc_button.clicked.connect(self.calculate_cost)

        self.graph_button = QPushButton("Показать график")
        self.graph_button.clicked.connect(self.show_graph)

        # Результаты
        self.result_label = QLabel("Результат: ")

        # Макет
        layout = QVBoxLayout()
        layout.addLayout(self.input_layout)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.graph_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def create_input_fields(self):
        # Поля ввода данных
        self.input_layout = QGridLayout()

        # Тип культуры
        self.input_layout.addWidget(QLabel("Тип культуры:"), 0, 0)
        self.crop_type = QComboBox()
        self.crop_type.addItems(["Овощи открытого грунта", "Овощи закрытого грунта", "Картофель"])
        self.input_layout.addWidget(self.crop_type, 0, 1)

        # Площадь посева, в гектарах
        self.input_layout.addWidget(QLabel("Площадь посева (га):"), 1, 0)
        self.area_input = QLineEdit()
        self.input_layout.addWidget(self.area_input, 1, 1)

        # Урожайность ц/га.
        self.input_layout.addWidget(QLabel("Урожайность (ц/га):"), 2, 0)
        self.yield_input = QLineEdit()
        self.input_layout.addWidget(self.yield_input, 2, 1)

        # Производственные затраты тыс. руб.
        self.input_layout.addWidget(QLabel("Производственные затраты (тыс. руб):"), 3, 0)
        self.cost_input = QLineEdit()
        self.input_layout.addWidget(self.cost_input, 3, 1)

    def calculate_cost(self):
        # Получение данных из полей ввода
        crop = self.crop_type.currentText()
        area = float(self.area_input.text())
        yield_per_hectare = float(self.yield_input.text())
        production_costs = float(self.cost_input.text())

        # Процент отходов по типу культуры
        waste_percent = {
            "Овощи открытого грунта": 10.0,
            "Овощи закрытого грунта": 5.0,
            "Картофель": 7.0
        }[crop]

        # Расчет производственной себестоимости
        effective_yield = yield_per_hectare * area * (1 - waste_percent / 100) #выход продукции (с учётом отходов)
        unit_cost = production_costs / effective_yield

        # Вывод результата
        self.result_label.setText(f"Результат: Себестоимость 1 ц = {unit_cost:.2f} тыс. руб.")
        self.unit_cost = unit_cost  # Сохранение для графика

    def show_graph(self):
        # Плановая себестоимость тыс. руб.
        planned_cost = 1200
        actual_cost = getattr(self, "unit_cost", None)

        if actual_cost is None:
            self.result_label.setText("Сначала рассчитайте себестоимость!")
            return

        # Построение графика
        plt.bar(["Фактическая себестоимость", "Плановая себестоимость"], [actual_cost, planned_cost], color=["blue", "orange"])
        plt.ylabel("Себестоимость (тыс. руб.)")
        plt.title("Сравнение фактической и плановой себестоимости")
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CostCalculatorApp()
    window.show()
    sys.exit(app.exec())
