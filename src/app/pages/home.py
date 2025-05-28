import customtkinter as ctk
from .api_client import APIClient

api = APIClient(base_url='http://localhost:8000/api/v1')

class HomePage(ctk.CTkFrame):
    """Главная страница"""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1a1a1a")  # Тот же фон, что и у других страниц
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        # Заголовок с красивым оформлением
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(40, 30), fill="x", padx=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Панель управления",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color="#ffffff"
        ).pack(side="bottom")

        # Основная область с кнопками
        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        buttons_frame.pack(expand=True, fill="both", padx=50, pady=20)

        # Стили для кнопок
        btn_style = {
            "width": 280,
            "height": 50,
            "font": ctk.CTkFont(size=18, weight="bold"),
            "corner_radius": 10,
            "border_width": 1,
            "border_color": "#444444"
        }

        # Кнопка "Работа с рецептами"
        self.btn_prescriptions = ctk.CTkButton(
            buttons_frame,
            text="📋 Работа с рецептами",
            fg_color="#252525",
            hover_color="#333333",
            text_color="#4d8af0",
            command=lambda: self.controller.show_page("PrescriptionsPage"),
            **btn_style
        )
        self.btn_prescriptions.pack(pady=(0, 20), fill="x")

        # Кнопка "Работа с сотрудниками"
        self.btn_employees = ctk.CTkButton(
            buttons_frame,
            text="👥 Работа с сотрудниками",
            fg_color="#252525",
            hover_color="#333333",
            text_color="#4d8af0",
            command=lambda: self.controller.show_page("EmployeesPage"),
            **btn_style
        )
        self.btn_employees.pack(pady=(0, 20), fill="x")

        # Кнопка "Статистика прибыли сети"
        self.btn_statistics = ctk.CTkButton(
            buttons_frame,
            text="📊 Статистика прибыли сети",
            fg_color="#252525",
            hover_color="#333333",
            text_color="#4d8af0",
            command=lambda: self.controller.show_page("StatisticsPage"),
            **btn_style
        )
        self.btn_statistics.pack(pady=(0, 20), fill="x")

        # Декоративный элемент внизу
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=20)
        footer_frame.pack(side="bottom", fill="x", pady=(0, 10))
        ctk.CTkLabel(
            footer_frame,
            text="Сеть аптек © 2025",
            font=ctk.CTkFont(size=12),
            text_color="#7a7a7a"
        ).pack(side="right", padx=20)