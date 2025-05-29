import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        
        self._drag_data = {"x": 0, "y": 0}
        
        self.show_splash_screen()   
        self.setup_main_window()
        self.show_page("HomePage")
        
        self.after(2500, self.transition_to_main_app)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_splash_screen(self):
        """Создает и показывает заставку с возможностью перемещения"""
        self.splash = ctk.CTkToplevel(self)
        self.splash.overrideredirect(True)
        self.splash.attributes("-topmost", True)
        
        self.splash.bind("<ButtonPress-1>", self.start_move)
        self.splash.bind("<ButtonRelease-1>", self.stop_move)
        self.splash.bind("<B1-Motion>", self.on_move)
        
        splash_width = 500
        splash_height = 250
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        self.splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        
        border_frame = ctk.CTkFrame(self.splash, border_width=2, border_color="#3A7EBF")
        border_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        ctk.CTkLabel(
            border_frame,
            text="💊 Аптечная сеть",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=40)
        
        ctk.CTkLabel(
            border_frame,
            text="Загрузка панели управления...",
            font=ctk.CTkFont(size=14)
        ).pack()
        
        self.progress = ctk.CTkProgressBar(border_frame, mode="indeterminate")
        self.progress.pack(fill="x", padx=50, pady=30)
        self.progress.start()

    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def stop_move(self, event):
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def on_move(self, event):
        x = self.splash.winfo_x() + (event.x - self._drag_data["x"])
        y = self.splash.winfo_y() + (event.y - self._drag_data["y"])
        self.splash.geometry(f"+{x}+{y}")

    def transition_to_main_app(self):
        """Плавный переход к главному окну"""
        for i in range(10, -1, -1):
            alpha = i/10
            self.splash.attributes("-alpha", alpha)
            self.splash.update()
            self.after(20)
        
        self.progress.stop()
        self.splash.destroy()
        self.deiconify()
        
        self.attributes("-alpha", 0)
        for i in range(0, 11):
            alpha = i/10
            self.attributes("-alpha", alpha)
            self.update()
            self.after(20)

    def setup_main_window(self):
        """Настраивает основное окно приложения"""
        self.title("Сеть аптек — Панель управления")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.minsize(width=1000, height=800)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)
        
        self.create_navigation_frame()
        
        self.main_frame = ctk.CTkFrame(self.container, corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True)
        
        self.pages = {}
        self.current_page = None

    def transition_to_main_app(self):
        """Переход от заставки к основному окну"""
        self.progress.stop()
        
        self.splash.destroy()
        
        self.deiconify()

    def on_close(self):
        """Обработчик закрытия основного окна"""
        self.destroy()
        self.quit()  

    def create_navigation_frame(self):
        """Создает панель навигации"""
        self.nav_frame = ctk.CTkFrame(self.container, width=220, corner_radius=0)
        self.nav_frame.pack(side="left", fill="y")
        self.nav_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            self.nav_frame,
            text="Аптечная сеть",
            font=ctk.CTkFont(size=20, weight="bold"),
            pady=20
        ).pack()
        
        nav_buttons = [
            ("🏠 Главная", "HomePage"),
            ("👥 Сотрудники", "EmployeesPage"),
            ("📋 Рецепты", "PrescriptionsPage"),
            ("📊 Статистика", "StatisticsPage")
        ]
        
        for text, page in nav_buttons:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=text,
                command=lambda p=page: self.show_page(p),
                corner_radius=8,
                height=50,
                anchor="w",
                font=ctk.CTkFont(size=16),
                fg_color="transparent",
                hover_color=("gray70", "gray30"),
                text_color=("gray10", "gray90")
            )
            btn.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.nav_frame, text="").pack(fill="x", expand=True)
        
        ctk.CTkLabel(
            self.nav_frame,
            text="Версия 1.0.0\n© 2025",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
            pady=10
        ).pack(side="bottom")

    def show_page(self, page_name):
        """Показывает страницу с анимацией"""
        if self.current_page == page_name:
            return
        
        if page_name not in self.pages:
            if page_name == "HomePage":
                from pages.home import HomePage
                page = HomePage(self.main_frame, self)
            elif page_name == "EmployeesPage":
                from pages.employees import EmployeesPage
                page = EmployeesPage(self.main_frame, self)
            elif page_name == "PrescriptionsPage":
                from pages.prescriptions import PrescriptionsPage
                page = PrescriptionsPage(self.main_frame, self)
            elif page_name == "StatisticsPage":
                from pages.statistics import StatisticsPage
                page = StatisticsPage(self.main_frame, self)
            else:
                from pages.home import HomePage
                page = HomePage(self.main_frame, self)
            
            self.pages[page_name] = page
        
        if self.current_page:
            self.pages[self.current_page].pack_forget()
        
        self.pages[page_name].pack(fill="both", expand=True)
        self.current_page = page_name
        self.update_navigation_buttons(page_name)

    def update_navigation_buttons(self, active_page):
        """Обновляет стиль кнопок навигации"""
        for widget in self.nav_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                if active_page in widget.cget("command").__code__.co_names:
                    widget.configure(fg_color=("#3A7EBF", "#1F538D"))
                else:
                    widget.configure(fg_color="transparent")
