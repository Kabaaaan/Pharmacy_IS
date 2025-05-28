import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ctk.CTkLabel(self, text="Главная страница", font=("Arial", 24))
        label.pack(pady=40)
        
        # Создаем 3 кнопки для перехода на разные страницы
        btn1 = ctk.CTkButton(self, text="Страница 1", command=lambda: controller.show_page("Page1"))
        btn1.pack(pady=10)
        
        btn2 = ctk.CTkButton(self, text="Страница 2", command=lambda: controller.show_page("Page2"))
        btn2.pack(pady=10)
        
        btn3 = ctk.CTkButton(self, text="Страница 3", command=lambda: controller.show_page("Page3"))
        btn3.pack(pady=10)