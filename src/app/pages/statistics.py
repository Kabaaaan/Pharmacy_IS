# src/app/pages/statistics.py

import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox


class StatisticsPage(ctk.CTkFrame):
    """
    Страница «Статистика прибыли сети по заказам» (тёмная тема).
    - Фильтр «Дата с»
    - Кнопка «Применить» и «Сбросить»
    - Сводка (orders, revenue)
    - Список заказов
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#2B2B2B")
        self.controller = controller

        # ====== Заглушечные данные «Заказы» ======
        # Поля: order_id, employee_id, date, amount
        self._orders_data = [
            {"order_id": 101, "employee_id": 1, "date": datetime(
                2023, 7,  1, 11, 30), "amount": 1500.0},
            {"order_id": 102, "employee_id": 2, "date": datetime(
                2023, 7,  5, 13, 45), "amount": 2570.5},
            {"order_id": 103, "employee_id": 3, "date": datetime(
                2023, 8, 10, 15, 10), "amount": 980.0},
            {"order_id": 104, "employee_id": 1, "date": datetime(
                2023, 8, 20, 9, 5),   "amount": 1120.75},
            {"order_id": 105, "employee_id": 2, "date": datetime(
                2023, 9,  1, 10, 20), "amount": 1750.0},
            {"order_id": 106, "employee_id": 3, "date": datetime(
                2023, 9, 15, 14, 55), "amount": 620.0},
            {"order_id": 107, "employee_id": 1, "date": datetime(
                2023, 9, 25, 10, 15), "amount": 2330.9},
        ]

        # ====== Дизайн страницы ======

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self,
            text="Статистика прибыли сети",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        self.label_title.pack(pady=(20, 10))

        # Верхняя панель: фильтр «Дата с», кнопки «Применить» и «Сбросить»
        top_frame = ctk.CTkFrame(self, fg_color="#3A3A3A", corner_radius=8)
        top_frame.pack(fill="x", padx=20, pady=(0, 10))

        lbl_filter = ctk.CTkLabel(
            top_frame,
            text="Показать заказы с даты (дд.мм.ГГГГ):",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        lbl_filter.pack(side="left", padx=(15, 5), pady=10)

        self.entry_filter_date = ctk.CTkEntry(
            top_frame,
            placeholder_text="дд.мм.ГГГГ",
            width=120
        )
        # Оставляем пустым по умолчанию
        self.entry_filter_date.pack(side="left", padx=(0, 5), pady=10)

        self.btn_apply_filter = ctk.CTkButton(
            top_frame,
            text="Применить",
            width=100, height=30,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=self.refresh_orders_list
        )
        self.btn_apply_filter.pack(side="left", padx=(0, 10), pady=10)

        self.btn_reset_filter = ctk.CTkButton(
            top_frame,
            text="Сбросить",
            width=100, height=30,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=self.reset_filter
        )
        self.btn_reset_filter.pack(side="left", padx=(0, 15), pady=10)

        # ====== Блок «Сводка» ======
        self.summary_frame = ctk.CTkFrame(
            self, fg_color="#3A3A3A", corner_radius=8)
        self.summary_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.lbl_orders = ctk.CTkLabel(
            self.summary_frame,
            text="Всего заказов: 0",
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        self.lbl_orders.pack(anchor="w", padx=15, pady=(10, 5))

        self.lbl_revenue = ctk.CTkLabel(
            self.summary_frame,
            text="Общая выручка: 0.00 ₽",
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        self.lbl_revenue.pack(anchor="w", padx=15, pady=(0, 10))

        # Метка «Последние заказы»
        self.lbl_recent = ctk.CTkLabel(
            self,
            text="Последние заказы:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.lbl_recent.pack(pady=(0, 10))

        # Прокручиваемый фрейм для списка заказов
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, width=800, height=400, corner_radius=8, fg_color="#2B2B2B"
        )
        self.scrollable_frame.pack(
            padx=20, pady=(0, 15), fill="both", expand=True)

        # Кнопка «Назад»
        self.btn_back = ctk.CTkButton(
            self,
            text="← Назад",
            width=100, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=lambda: controller.show_page("HomePage")
        )
        self.btn_back.place(x=20, y=20)

        # Первоначальное заполнение
        self.refresh_orders_list()

    def parse_date(self, date_str):
        """
        Парсит строку «дд.мм.ГГГГ» в datetime. Если некорректно — возвращает None.
        """
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except Exception:
            return None

    def reset_filter(self):
        """
        Сбрасывает фильтр: очищает поле и показывает все заказы.
        """
        self.entry_filter_date.delete(0, "end")
        self.refresh_orders_list()

    def refresh_orders_list(self):
        """
        Перерисовывает сводку и список заказов с учётом фильтра «Дата с».
        """
        # Чищаем список внутри scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        filter_text = self.entry_filter_date.get().strip()
        if filter_text:
            dt = self.parse_date(filter_text)
            if dt is None:
                messagebox.showerror(
                    "Ошибка", "Некорректный формат даты. Используйте дд.мм.ГГГГ")
                return
            filtered = [o for o in self._orders_data if o["date"].date()
                        >= dt.date()]
        else:
            filtered = self._orders_data.copy()

        # Считаем сводку на отфильтрованных данных
        total_orders = len(filtered)
        total_revenue = sum(o["amount"] for o in filtered)

        self.lbl_orders.configure(text=f"Всего заказов: {total_orders}")
        self.lbl_revenue.configure(
            text=f"Общая выручка: {total_revenue:,.2f} ₽")

        if not filtered:
            lbl_empty = ctk.CTkLabel(
                self.scrollable_frame,
                text="Заказы не найдены.",
                font=ctk.CTkFont(size=14),
                text_color="white"
            )
            lbl_empty.pack(pady=20)
            return

        # Сортируем по дате (новые первыми)
        sorted_orders = sorted(filtered, key=lambda o: o["date"], reverse=True)

        for order in sorted_orders:
            container = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#3A3A3A",
                corner_radius=6,
                border_width=1,
                border_color="#555555"
            )
            container.pack(fill="x", padx=15, pady=8)

            txt = (
                f"Заказ ID: {order['order_id']}    |    "
                f"Сотрудник ID: {order['employee_id']}    |    "
                f"Дата: {order['date'].strftime('%d.%m.%Y')}    |    "
                f"Сумма: {order['amount']:,.2f} ₽"
            )
            lbl = ctk.CTkLabel(
                container,
                text=txt,
                font=ctk.CTkFont(size=13),
                text_color="white",
                wraplength=700,
                anchor="w"
            )
            lbl.pack(fill="x", padx=10, pady=8)
