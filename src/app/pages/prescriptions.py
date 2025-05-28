import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox


class PrescriptionsPage(ctk.CTkFrame):
    """
    Страница «Работа с рецептами» (тёмная тема).
    - Просмотр всех рецептов
    - Добавление нового рецепта (модальное окно)
    - Удаление рецепта
    - Фильтрация по дате с возможностью сброса
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#2B2B2B")
        self.controller = controller

        # ====== Заглушечные данные «РЕЦЕПТЫ» ======
        # Поля: id, doctor, patient, medicine, date
        self._prescriptions_data = [
            {
                "id": 1,
                "doctor": "Смирнов В.В.",
                "patient": "Иванов И.И.",
                "medicine": "Аспирин",
                "date": datetime(2023, 9, 10, 14, 30)
            },
            {
                "id": 2,
                "doctor": "Петрова Е.Е.",
                "patient": "Петрова А.А.",
                "medicine": "Ибупрофен",
                "date": datetime(2023, 9, 11, 9, 15)
            },
            {
                "id": 3,
                "doctor": "Кузнецова М.М.",
                "patient": "Сидоров К.К.",
                "medicine": "Парацетамол",
                "date": datetime(2023, 9, 12, 16, 0)
            }
        ]

        # ====== Заглушечные данные «СПИСОК ЛЕКАРСТВ» (для автокомплита) ======
        self._medicines_list = [
            "Аспирин", "Ибупрофен", "Парацетамол", "Цитрамон", "Амоксиклав", "Но-шпа",
            "Ибупрофен Форте", "Ибупром", "Ибуклин", "Парацетамол Некст", "Аспирин Кардио"
        ]

        # ====== Дизайн страницы ======

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self,
            text="Работа с рецептами",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        self.label_title.pack(pady=(20, 10))

        # Верхняя панель: фильтр по дате + кнопки
        top_frame = ctk.CTkFrame(self, fg_color="#3A3A3A", corner_radius=8)
        top_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Метка «Дата с:»
        lbl_filter = ctk.CTkLabel(
            top_frame,
            text="Показать рецепты с даты (дд.мм.ГГГГ):",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        lbl_filter.pack(side="left", padx=(15, 5), pady=10)

        # Поле для ввода даты
        self.entry_filter_date = ctk.CTkEntry(
            top_frame,
            placeholder_text="дд.мм.ГГГГ",
            width=120
        )
        self.entry_filter_date.pack(side="left", padx=(0, 5), pady=10)

        # Кнопка «Применить»
        self.btn_apply_filter = ctk.CTkButton(
            top_frame,
            text="Применить",
            width=100, height=30,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=self.refresh_prescriptions_list
        )
        self.btn_apply_filter.pack(side="left", padx=(0, 10), pady=10)

        # Кнопка «Сбросить»
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
        self.btn_reset_filter.pack(side="left", padx=(0, 10), pady=10)

        # Кнопка «Добавить рецепт»
        self.btn_add = ctk.CTkButton(
            top_frame,
            text="Добавить рецепт",
            width=140, height=30,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=12),
            command=self.open_add_modal
        )
        self.btn_add.pack(side="right", padx=(0, 15), pady=10)

        # Прокручиваемый фрейм для списка рецептов
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, width=800, height=420, corner_radius=8, fg_color="#2B2B2B"
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

        # Изначально отображаем все рецепты
        self.refresh_prescriptions_list()

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
        Сброс фильтра (очистка поля) и перерисовка списка.
        """
        self.entry_filter_date.delete(0, "end")
        self.refresh_prescriptions_list()

    def refresh_prescriptions_list(self):
        """
        Перерисовывает список рецептов, применяя фильтр по дате, если указан.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        filter_text = self.entry_filter_date.get().strip()
        if filter_text:
            dt = self.parse_date(filter_text)
            if dt is None:
                messagebox.showerror(
                    "Ошибка", "Некорректный формат даты. Используйте дд.мм.ГГГГ")
                return
            filtered = [
                p for p in self._prescriptions_data if p["date"].date() >= dt.date()]
        else:
            filtered = self._prescriptions_data.copy()

        if not filtered:
            lbl_empty = ctk.CTkLabel(
                self.scrollable_frame,
                text="Рецепты не найдены.",
                font=ctk.CTkFont(size=14),
                text_color="white"
            )
            lbl_empty.pack(pady=20)
            return

        # Сортируем по дате от новых к старым
        sorted_list = sorted(filtered, key=lambda p: p["date"], reverse=True)

        for pres in sorted_list:
            container = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#3A3A3A",
                corner_radius=6,
                border_width=1,
                border_color="#555555"
            )
            container.pack(fill="x", padx=15, pady=8)

            txt = (
                f"ID: {pres['id']}    |    Врач: {pres['doctor']}    |    "
                f"Пациент: {pres['patient']}    |    Препарат: {pres['medicine']}    |    "
                f"Дата: {pres['date'].strftime('%d.%m.%Y')}"
            )
            lbl = ctk.CTkLabel(
                container,
                text=txt,
                font=ctk.CTkFont(size=13),
                text_color="white",
                wraplength=700,
                anchor="w"
            )
            lbl.pack(fill="x", padx=10, pady=(8, 4))

            btn_delete = ctk.CTkButton(
                container,
                text="Удалить",
                width=100, height=30,
                fg_color="#555555",
                hover_color="#666666",
                text_color="white",
                font=ctk.CTkFont(size=12),
                command=lambda p=pres: self.delete_prescription(p)
            )
            btn_delete.pack(anchor="e", padx=10, pady=(0, 8))

    def delete_prescription(self, prescription):
        """
        Удаляет рецепт после подтверждения.
        """
        answer = messagebox.askyesno(
            "Удаление рецепта",
            f"Вы действительно хотите удалить рецепт ID={prescription['id']}?"
        )
        if not answer:
            return

        self._prescriptions_data = [
            p for p in self._prescriptions_data if p["id"] != prescription["id"]
        ]
        print(f"[Заглушка] Рецепт ID={prescription['id']} удалён")
        self.refresh_prescriptions_list()

    def open_add_modal(self):
        """
        Модальное окно для создания нового рецепта.
        Поля: Врач, Клиент, Дата, Выбор препарата (выпадающий список).
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Добавить новый рецепт")
        modal.geometry("400x300")
        modal.configure(fg_color="#2B2B2B")
        modal.grab_set()
        modal.transient(self)
        modal.minsize(500, 500)

        lbl_title = ctk.CTkLabel(
            modal,
            text="Новый рецепт",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        lbl_title.pack(pady=(20, 10))

        # Врач
        lbl_doctor = ctk.CTkLabel(modal, text="Врач:", text_color="white")
        lbl_doctor.pack(anchor="w", padx=20, pady=(10, 2))
        entry_doctor = ctk.CTkEntry(
            modal, placeholder_text="ФИО врача", width=440)
        entry_doctor.pack(padx=20)

        # Пациент
        lbl_patient = ctk.CTkLabel(modal, text="Пациент:", text_color="white")
        lbl_patient.pack(anchor="w", padx=20, pady=(10, 2))
        entry_patient = ctk.CTkEntry(
            modal, placeholder_text="ФИО пациента", width=440)
        entry_patient.pack(padx=20)

        # Дата (дд.мм.ГГГГ)
        lbl_date = ctk.CTkLabel(
            modal, text="Дата (дд.мм.ГГГГ):", text_color="white")
        lbl_date.pack(anchor="w", padx=20, pady=(10, 2))
        entry_date = ctk.CTkEntry(
            modal, placeholder_text="дд.мм.ГГГГ", width=200)
        entry_date.pack(padx=20)

        # Лекарство - выпадающий список вместо автокомплита
        lbl_med = ctk.CTkLabel(modal, text="Лекарство:", text_color="white")
        lbl_med.pack(anchor="w", padx=20, pady=(10, 2))

        # Создаем выпадающий список с лекарствами
        self.combo_med = ctk.CTkComboBox(
            modal,
            values=sorted(self._medicines_list),  # сортируем по алфавиту
            state="readonly",   # только выбор из списка
            width=440,
            dropdown_fg_color="#3A3A3A",  # цвет выпадающего списка
            button_color="#555555",        # цвет кнопки
        )
        self.combo_med.pack(padx=20)
        self.combo_med.set("")  # начальное значение - пустое

        # Кнопки «Добавить» и «Отмена»
        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=(30, 20))

        def on_confirm():
            doctor = entry_doctor.get().strip()
            patient = entry_patient.get().strip()
            date_text = entry_date.get().strip()
            medicine = self.combo_med.get().strip()  # получаем выбранное значение

            if not all([doctor, patient, date_text, medicine]):
                messagebox.showwarning("Ошибка", "Все поля обязательны.")
                return

            try:
                dt = datetime.strptime(date_text, "%d.%m.%Y")
            except ValueError:
                messagebox.showerror(
                    "Ошибка", "Некорректный формат даты. Используйте дд.мм.ГГГГ")
                return

            new_id = max((p["id"] for p in self._prescriptions_data),
                         default=0) + 1
            new_pres = {
                "id": new_id,
                "doctor": doctor,
                "patient": patient,
                "medicine": medicine,
                "date": dt
            }
            self._prescriptions_data.append(new_pres)
            print(f"[Заглушка] Добавлен рецепт ID={new_id}")
            modal.destroy()
            self.refresh_prescriptions_list()

        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="Добавить",
            width=100, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=on_confirm
        )
        btn_confirm.pack(side="left", padx=(0, 10))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Отмена",
            width=100, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=modal.destroy
        )
        btn_cancel.pack(side="left")

        # Центрируем модальное окно
        modal.update_idletasks()
        width = modal.winfo_width()
        height = modal.winfo_height()
        x = (modal.winfo_screenwidth() // 2) - (width // 2)
        y = (modal.winfo_screenheight() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")
