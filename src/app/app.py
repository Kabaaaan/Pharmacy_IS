import customtkinter as ctk

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Сеть аптек — Панель управления")
        self.geometry("1000x800")
        self.resizable(True, True)
        self.minsize(width=800, height=800)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        self.pages = {}

        self.show_page("HomePage")

    def show_page(self, page_name):
        """
        Скрывает текущие страницы и показывает нужную. 
        Создаёт страницу «на лету», если ещё не создана.
        """
        for page in self.pages.values():
            page.pack_forget()

        if page_name not in self.pages:
            if page_name == "HomePage":
                from pages.home import HomePage
                page = HomePage(self.container, self)
            elif page_name == "EmployeesPage":
                from pages.employees import EmployeesPage
                page = EmployeesPage(self.container, self)
            elif page_name == "PrescriptionsPage":
                from pages.prescriptions import PrescriptionsPage
                page = PrescriptionsPage(self.container, self)
            elif page_name == "StatisticsPage":
                from pages.statistics import StatisticsPage
                page = StatisticsPage(self.container, self)
            else:
                from pages.home import HomePage
                page = HomePage(self.container, self)

            self.pages[page_name] = page

        self.pages[page_name].pack(fill="both", expand=True)
