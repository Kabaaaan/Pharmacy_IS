import customtkinter as ctk
from pages.home import HomePage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Многостраничное приложение")
        self.geometry("600x400")
        
        # Контейнер для всех страниц
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Словарь для хранения страниц
        self.pages = {}
        
        # Инициализация стартовой страницы
        self.show_page("HomePage")
    
    def show_page(self, page_name):
        # Скрыть текущую страницу
        for page in self.pages.values():
            page.pack_forget()
        
        # Если страница еще не создана, создать ее
        if page_name not in self.pages:
            if page_name == "HomePage":
                from pages.home import HomePage
                self.pages[page_name] = HomePage(self.container, self)
            elif page_name == "Page1":
                from pages.page1 import Page1
                self.pages[page_name] = Page1(self.container, self)
            elif page_name == "Page2":
                from pages.page2 import Page2
                self.pages[page_name] = Page2(self.container, self)
            elif page_name == "Page3":
                from pages.page3 import Page3
                self.pages[page_name] = Page3(self.container, self)
        
        # Показать запрошенную страницу
        self.pages[page_name].pack(fill="both", expand=True)