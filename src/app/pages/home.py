import customtkinter as ctk
from .api_client import APIClient

api = APIClient(base_url='http://localhost:8000/api/v1')

class HomePage(ctk.CTkFrame):
    """
    Главная страница. Тёмная тема, нейтральные кнопки навигации.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#2B2B2B")
        self.controller = controller

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self,
            text="Панель управления сетью аптек",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.label_title.pack(pady=(50, 20))

        # Кнопки-навигации
        btn_width = 250
        btn_height = 45
        btn_font = ctk.CTkFont(size=16)

        self.btn_prescriptions = ctk.CTkButton(
            self,
            text="Работа с рецептами",
            width=btn_width, height=btn_height,
            font=btn_font,
            fg_color="#444444",
            hover_color="#555555",
            text_color="white",
            command=lambda: controller.show_page("PrescriptionsPage")
        )
        self.btn_prescriptions.pack(pady=(0, 15))

        self.btn_employees = ctk.CTkButton(
            self,
            text="Работа с сотрудниками",
            width=btn_width, height=btn_height,
            font=btn_font,
            fg_color="#444444",
            hover_color="#555555",
            text_color="white",
            command=lambda: controller.show_page("EmployeesPage")
        )
        self.btn_employees.pack(pady=(0, 15))

        self.btn_statistics = ctk.CTkButton(
            self,
            text="Статистика прибыли сети",
            width=btn_width, height=btn_height,
            font=btn_font,
            fg_color="#444444",
            hover_color="#555555",
            text_color="white",
            command=lambda: controller.show_page("StatisticsPage")
        )
        self.btn_statistics.pack(pady=(0, 15))
