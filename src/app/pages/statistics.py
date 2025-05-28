import customtkinter as ctk
from datetime import datetime, date
from tkinter import messagebox
from .home import api
import threading


class StatisticsPage(ctk.CTkFrame):
    """Страница статистики прибыли сети по заказам."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1a1a1a")
        self.controller = controller
        self._orders_data = []
        self.loading_spinner = None
        self._setup_ui()
        self.load_orders_data()

    def _setup_ui(self):
        self._create_header()
        self._create_filters_panel()
        self._create_summary_panel()
        self._create_orders_list()
        self._create_back_button()

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=20)
        
        
        ctk.CTkLabel(
            header_frame,
            text="Статистика прибыли сети",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color="#ffffff"
        ).pack(side="bottom")
        

    def _create_filters_panel(self):
        top_frame = ctk.CTkFrame(
            self, 
            fg_color="#252525", 
            corner_radius=14,
            border_width=1,
            border_color="#333333",
            height=160  
        )
        top_frame.pack(fill="x", padx=20, pady=(25, 25))

        ctk.CTkLabel(
            top_frame,
            text="Показать заказы с даты:",
            font=ctk.CTkFont(size=15),
            text_color="#d6d6d6"
        ).pack(side="left", padx=(15, 5), pady=(15, 15))

        self.entry_filter_date = ctk.CTkEntry(
            top_frame,
            placeholder_text="дд.мм.ГГГГ",
            width=120,
            fg_color="#333333",
            border_color="#444444",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        self.entry_filter_date.pack(side="left", padx=(0, 5), pady=10)

        buttons_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        buttons_frame.pack(side="left", padx=(10, 0), pady=10)
        
        ctk.CTkButton(
            buttons_frame,
            text="Применить",
            width=110,
            height=32,
            fg_color="#4d8af0",
            hover_color="#3a7ae0",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            command=self.refresh_orders_list
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            buttons_frame,
            text="Сбросить",
            width=100,
            height=32,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            command=self.reset_filter
        ).pack(side="left")

    def _create_summary_panel(self):
        self.summary_frame = ctk.CTkFrame(
            self, 
            fg_color="#252525", 
            corner_radius=14,
            border_width=1,
            border_color="#333333"
        )
        self.summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            self.summary_frame,
            text="ОБЩАЯ СТАТИСТИКА",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#7a7a7a"
        ).place(x=15, y=8)

        stats_frame = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        stats_frame.pack(pady=(15, 10), padx=15, fill="x")
        
        self.lbl_orders = ctk.CTkLabel(
            stats_frame,
            text="📦 0 заказов",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4d8af0",
            anchor="w"
        )
        self.lbl_orders.pack(fill="x", pady=(0, 5))

        self.lbl_revenue = ctk.CTkLabel(
            stats_frame,
            text="💰 0.00 ₽",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4d8af0",
            anchor="w"
        )
        self.lbl_revenue.pack(fill="x")

    def _create_orders_list(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(0, 10), fill="x", padx=20)
        
        ctk.CTkLabel(
            header_frame,
            text="ИСТОРИЯ ЗАКАЗОВ",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#7a7a7a"
        ).pack(side="left")

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, 
            width=800, 
            height=400, 
            corner_radius=14, 
            fg_color="#252525",
            border_width=1,
            border_color="#333333"
        )
        self.scrollable_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def _create_back_button(self):
        ctk.CTkButton(
            self,
            text="← Назад",
            width=100,
            height=36,
            fg_color="#333333",
            hover_color="#444444",
            border_color="#555555",
            border_width=1,
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10,
            command=lambda: self.controller.show_page("HomePage")
        ).place(x=20, y=20)

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            return None

    def reset_filter(self):
        self.entry_filter_date.delete(0, "end")
        self.load_orders_data()

    def load_orders_data(self, start_date: date = None):
        self._show_loading_spinner()

        def fetch_data():
            try:
                params = {"start_date": start_date.isoformat()} if start_date else {}
                response = api.get(endpoint='order', params=params)

                if response and isinstance(response, list):
                    self._orders_data = response
                    self.after(100, lambda: self._update_ui(start_date))
                else:
                    self.after(100, self._handle_no_data)
            except Exception as e:
                self.after(100, lambda: self._handle_error(f"Ошибка при загрузке данных: {str(e)}"))

        threading.Thread(target=fetch_data).start()

    def _update_ui(self, filter_date):
        self._clear_orders_list()

        processed_orders = self._process_orders_data()
        filtered_orders = self._filter_orders(processed_orders, filter_date)

        self._update_summary(filtered_orders)
        self._display_orders(filtered_orders)

        self._hide_loading_spinner()

    def _process_orders_data(self):
        processed = []
        for order in self._orders_data:
            try:
                order_copy = order.copy()
                if isinstance(order_copy['date'], str):
                    order_copy['date'] = datetime.strptime(order_copy['date'], '%Y-%m-%d')
                processed.append(order_copy)
            except Exception:
                continue
        return processed

    def _filter_orders(self, orders, filter_date):
        if filter_date:
            return [o for o in orders if o['date'].date() >= filter_date]
        return orders

    def _clear_orders_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def _update_summary(self, orders):
        total_orders = len(orders)
        total_revenue = sum(float(o['total_price']) for o in orders)

        self.lbl_orders.configure(text=f"📦 {total_orders} заказов")
        self.lbl_revenue.configure(text=f"💰 {total_revenue:,.2f} ₽")

    def _display_orders(self, orders):
        if not orders:
            self._show_no_orders_message()
            return

        for order in sorted(orders, key=lambda o: o['date'], reverse=True):
            self._create_order_widget(order)

    def _show_no_orders_message(self):
        empty_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#252525",
            corner_radius=12,
            height=100
        )
        empty_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            empty_frame,
            text="📭 Нет данных о заказах",
            font=ctk.CTkFont(size=16),
            text_color="#777777"
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _create_order_widget(self, order):
        container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#333333",
            corner_radius=12,
            border_width=1,
            border_color="#444444"
        )
        container.pack(fill="x", padx=10, pady=8)
        
        top_frame = ctk.CTkFrame(container, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        ctk.CTkLabel(
            top_frame,
            text=f"🆔 Заказ #{order['id']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4d8af0",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            top_frame,
            text=f"📅 {order['date'].strftime('%d.%m.%Y')}",
            font=ctk.CTkFont(size=14),
            text_color="#aaaaaa",
            anchor="e"
        ).pack(side="right")
        
        bottom_frame = ctk.CTkFrame(container, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            bottom_frame,
            text=f"👤 Сотрудник ID: {order['pharmacist_id']}",
            font=ctk.CTkFont(size=13),
            text_color="#cccccc",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            bottom_frame,
            text=f"💰 {float(order['total_price']):,.2f} ₽",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4d8af0",
            anchor="e"
        ).pack(side="right")

    def _handle_no_data(self):
        self._orders_data = []
        self._update_ui(None)
        messagebox.showwarning("Предупреждение", "Нет данных о заказах")

    def _handle_error(self, message):
        self._orders_data = []
        self._update_ui(None)
        messagebox.showerror("Ошибка", message)

    def refresh_orders_list(self):
        filter_text = self.entry_filter_date.get().strip()

        if not filter_text:
            self.load_orders_data()
            return

        dt = self.parse_date(filter_text)
        if not dt:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте дд.мм.ГГГГ")
            return

        self.load_orders_data(start_date=dt.date())

    def _show_loading_spinner(self):
        self._clear_orders_list()
        
        spinner_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#252525",
            corner_radius=12,
            height=100
        )
        spinner_frame.pack(fill="x", padx=10, pady=10)
        
        self.loading_spinner = ctk.CTkLabel(
            spinner_frame,
            text="⏳ Загрузка данных...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#7a7a7a"
        )
        self.loading_spinner.place(relx=0.5, rely=0.5, anchor="center")

    def _hide_loading_spinner(self):
        if self.loading_spinner:
            self.loading_spinner.destroy()
            self.loading_spinner = None