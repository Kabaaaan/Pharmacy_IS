import customtkinter as ctk

class Page3(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ctk.CTkLabel(self, text="Это Страница 1", font=("Arial", 24))
        label.pack(pady=40)
        
        # Кнопка назад с иконкой стрелки
        back_btn = ctk.CTkButton(
            self, 
            text="← Назад", 
            command=lambda: controller.show_page("HomePage"),
            width=100,
            height=40,
            fg_color="transparent",
            hover_color="#333333",
            text_color=("gray10", "gray90")
        )
        back_btn.place(x=20, y=20)
        
        # Дополнительный контент страницы
        content = ctk.CTkLabel(self, text="Здесь может быть ваш контент для страницы 3")
        content.pack(pady=20)