# src/app/pages/employees.py

import customtkinter as ctk
from tkinter import messagebox
from tkinter import StringVar


class EmployeesPage(ctk.CTkFrame):
    """
    Страница «Работа с сотрудниками» (тёмная тема).
    - Добавление, редактирование, удаление сотрудников с проверкой связей
    - Фильтрация/сортировка по месту работы (аптеке)
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#2B2B2B")
        self.controller = controller

        # ====== Заглушечные данные «АПТЕКИ» ======
        self._pharmacies = ["Аптека №1", "Аптека №2", "Аптека №3", "Аптека №4"]

        # ====== Заглушечные данные «ДОЛЖНОСТИ» ======
        self._positions = ["Фармацевт", "Провизор",
                           "Администратор", "Кассир", "Менеджер"]

        # ====== Заглушечные данные «СОТРУДНИКИ» ======
        self._employees_data = [
            {"id": 1, "name": "Иванов П.П.",
                "phone": "+7 (900) 123-45-67", "address": "ул. Ленина, д. 10",
                "pharmacy": "Аптека №1", "position": "Фармацевт"},
            {"id": 2, "name": "Смирнова А.В.",
                "phone": "+7 (900) 234-56-78", "address": "пр. Мира, д. 5",
                "pharmacy": "Аптека №2", "position": "Провизор"},
            {"id": 3, "name": "Петров С.С.",
                "phone": "+7 (900) 345-67-89", "address": "ул. Гагарина, д. 7",
                "pharmacy": "Аптека №1", "position": "Администратор"},
        ]

        # ====== Заглушечные данные «ЗАКАЗЫ» ======
        self._orders_data = [
            {"order_id": 101, "employee_id": 1},
            {"order_id": 102, "employee_id": 2},
            # сотрудник с id=3 не имеет заказов
        ]

        # ====== Дизайн страницы ======

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="Управление сотрудниками",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        self.label_title.pack(pady=(20, 10))

        # Верхняя панель
        top_frame = ctk.CTkFrame(self, fg_color="#3A3A3A", corner_radius=8)
        top_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Кнопка «Добавить сотрудника»
        self.btn_add = ctk.CTkButton(
            top_frame,
            text="Добавить сотрудника",
            width=180, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=self.open_add_modal
        )
        self.btn_add.pack(side="left", padx=(15, 10), pady=10)

        # Метка + Combobox для фильтрации по аптеке
        lbl_filter = ctk.CTkLabel(
            top_frame,
            text="Сортировать по аптеке:",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        lbl_filter.pack(side="left", padx=(10, 5))

        self.selected_pharmacy = StringVar(value="Все")
        self.combo_pharmacies = ctk.CTkComboBox(
            top_frame,
            values=["Все"] + self._pharmacies,
            variable=self.selected_pharmacy,
            font=ctk.CTkFont(size=14),
            width=180,
            fg_color="#444444",
            button_color="#555555",
            dropdown_fg_color="#3A3A3A",
            dropdown_text_color="white",
            dropdown_hover_color="#555555",
            text_color="white",
            command=self.refresh_employees_list
        )
        self.combo_pharmacies.pack(side="left", padx=(0, 15), pady=10)

        # Прокручиваемый фрейм для списка сотрудников
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

        # Заполнение списка сотрудников
        self.refresh_employees_list()

    def refresh_employees_list(self, *args):
        """
        Перестраивает список сотрудников согласно выбранному фильтру.
        """
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        selected = self.selected_pharmacy.get()
        if selected == "Все":
            data = self._employees_data.copy()
        else:
            data = [
                emp for emp in self._employees_data if emp["pharmacy"] == selected]

        if not data:
            lbl_empty = ctk.CTkLabel(
                self.scrollable_frame,
                text="Сотрудники не найдены.",
                font=ctk.CTkFont(size=14),
                text_color="white"
            )
            lbl_empty.pack(pady=20)
            return

        for emp in data:
            container = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color="#3A3A3A",
                corner_radius=6,
                border_width=1,
                border_color="#555555"
            )
            container.pack(fill="x", padx=15, pady=8)

            # Основная информация
            txt_main = (
                f"ID: {emp['id']}    |    Имя: {emp['name']}    |    "
                f"Телефон: {emp['phone']}    |    Адрес: {emp['address']}    |    "
                f"Аптека: {emp['pharmacy']}"
            )
            lbl_main = ctk.CTkLabel(
                container,
                text=txt_main,
                font=ctk.CTkFont(size=13),
                text_color="white",
                wraplength=700,
                anchor="w"
            )
            # Уменьшен отступ снизу
            lbl_main.pack(fill="x", padx=10, pady=(8, 0))

            # Должность с дополнительным отступом сверху
            txt_position = f"Должность: {emp['position']}"
            lbl_position = ctk.CTkLabel(
                container,
                text=txt_position,
                font=ctk.CTkFont(size=13),
                text_color="white",
                wraplength=700,
                anchor="w"
            )
            lbl_position.pack(fill="x", padx=10, pady=(5, 4)
                              )  # Добавлен отступ сверху

            btn_frame = ctk.CTkFrame(container, fg_color="transparent")
            btn_frame.pack(pady=(0, 8), anchor="e", padx=10)

            btn_edit = ctk.CTkButton(
                btn_frame,
                text="Редактировать",
                width=120, height=30,
                fg_color="#555555",
                hover_color="#666666",
                text_color="white",
                font=ctk.CTkFont(size=12),
                command=lambda e=emp: self.open_edit_modal(e)
            )
            btn_edit.pack(side="left", padx=(0, 10))

            btn_delete = ctk.CTkButton(
                btn_frame,
                text="Удалить",
                width=100, height=30,
                fg_color="#555555",
                hover_color="#666666",
                text_color="white",
                font=ctk.CTkFont(size=12),
                command=lambda e=emp: self.delete_employee(e)
            )
            btn_delete.pack(side="left")

    def open_add_modal(self):
        """
        Модальное окно для добавления нового сотрудника.
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Добавить сотрудника")
        modal.geometry("450x450")
        modal.configure(fg_color="#2B2B2B")
        modal.grab_set()

        lbl_title = ctk.CTkLabel(
            modal,
            text="Новый сотрудник",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        lbl_title.pack(pady=(20, 15))

        lbl_name = ctk.CTkLabel(modal, text="ФИО:", text_color="white")
        lbl_name.pack(anchor="w", padx=20, pady=(10, 2))
        entry_name = ctk.CTkEntry(modal, placeholder_text="ФИО", width=380)
        entry_name.pack(padx=20)

        lbl_phone = ctk.CTkLabel(modal, text="Телефон:", text_color="white")
        lbl_phone.pack(anchor="w", padx=20, pady=(10, 2))
        entry_phone = ctk.CTkEntry(
            modal, placeholder_text="+7 (___) ___-__-__", width=380)
        entry_phone.pack(padx=20)

        lbl_address = ctk.CTkLabel(modal, text="Адрес:", text_color="white")
        lbl_address.pack(anchor="w", padx=20, pady=(10, 2))
        entry_address = ctk.CTkEntry(
            modal, placeholder_text="г. ..., ул. ..., д. ...", width=380)
        entry_address.pack(padx=20)

        lbl_pharmacy = ctk.CTkLabel(
            modal, text="Выберите аптеку:", text_color="white")
        lbl_pharmacy.pack(anchor="w", padx=20, pady=(10, 2))
        var_pharmacy = StringVar(value=self._pharmacies[0])
        combo_pharmacy = ctk.CTkComboBox(
            modal,
            values=self._pharmacies,
            variable=var_pharmacy,
            width=200,
            fg_color="#444444",
            button_color="#555555",
            text_color="white",
            dropdown_fg_color="#3A3A3A",
            dropdown_text_color="white",
            dropdown_hover_color="#555555"
        )
        combo_pharmacy.pack(padx=20, pady=(0, 5))

        lbl_position = ctk.CTkLabel(
            modal, text="Выберите должность:", text_color="white")
        lbl_position.pack(anchor="w", padx=20, pady=(10, 2))
        var_position = StringVar(value=self._positions[0])
        combo_position = ctk.CTkComboBox(
            modal,
            values=self._positions,
            variable=var_position,
            width=200,
            fg_color="#444444",
            button_color="#555555",
            text_color="white",
            dropdown_fg_color="#3A3A3A",
            dropdown_text_color="white",
            dropdown_hover_color="#555555"
        )
        combo_position.pack(padx=20, pady=(0, 15))

        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

        def on_confirm():
            name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            address = entry_address.get().strip()
            pharmacy = var_pharmacy.get().strip()
            position = var_position.get().strip()

            if not name or not phone or not address or not pharmacy or not position:
                messagebox.showwarning("Ошибка", "Все поля обязательны.")
                return

            new_id = max(emp["id"] for emp in self._employees_data) + \
                1 if self._employees_data else 1
            new_emp = {
                "id": new_id,
                "name": name,
                "phone": phone,
                "address": address,
                "pharmacy": pharmacy,
                "position": position
            }
            self._employees_data.append(new_emp)
            print(f"[Заглушка] Добавлен сотрудник ID={new_id}")
            modal.destroy()
            self.refresh_employees_list()

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

    def open_edit_modal(self, employee):
        """
        Модальное окно для редактирования сотрудника.
        Редактируются: телефон, адрес, аптека.
        Должность не редактируется.
        """
        modal = ctk.CTkToplevel(self)
        modal.title(f"Редактировать сотрудника ID={employee['id']}")
        modal.geometry("450x400")  # Уменьшена высота окна
        modal.configure(fg_color="#2B2B2B")
        modal.grab_set()

        lbl_title = ctk.CTkLabel(
            modal,
            text="Редактирование сотрудника",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        lbl_title.pack(pady=(20, 15))

        # Блок информации о сотруднике (не редактируется)
        info_frame = ctk.CTkFrame(modal, fg_color="#3A3A3A", corner_radius=6)
        info_frame.pack(fill="x", padx=20, pady=10)

        lbl_name = ctk.CTkLabel(
            info_frame,
            text=f"ФИО: {employee['name']}",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        lbl_name.pack(anchor="w", padx=10, pady=(8, 2))

        lbl_position = ctk.CTkLabel(
            info_frame,
            text=f"Должность: {employee['position']}",
            font=ctk.CTkFont(size=14),
            text_color="white"
        )
        lbl_position.pack(anchor="w", padx=10, pady=(0, 8))

        # Поля для редактирования
        lbl_phone = ctk.CTkLabel(modal, text="Телефон:", text_color="white")
        lbl_phone.pack(anchor="w", padx=20, pady=(10, 2))
        entry_phone = ctk.CTkEntry(modal, width=380)
        entry_phone.insert(0, employee["phone"])
        entry_phone.pack(padx=20)

        lbl_address = ctk.CTkLabel(modal, text="Адрес:", text_color="white")
        lbl_address.pack(anchor="w", padx=20, pady=(10, 2))
        entry_address = ctk.CTkEntry(modal, width=380)
        entry_address.insert(0, employee["address"])
        entry_address.pack(padx=20)

        lbl_pharmacy = ctk.CTkLabel(modal, text="Аптека:", text_color="white")
        lbl_pharmacy.pack(anchor="w", padx=20, pady=(10, 2))
        var_pharmacy = StringVar(value=employee["pharmacy"])
        combo_pharmacy = ctk.CTkComboBox(
            modal,
            values=self._pharmacies,
            variable=var_pharmacy,
            width=200,
            fg_color="#444444",
            button_color="#555555",
            text_color="white",
            dropdown_fg_color="#3A3A3A",
            dropdown_text_color="white",
            dropdown_hover_color="#555555"
        )
        combo_pharmacy.pack(padx=20, pady=(0, 15))

        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

        def on_save():
            new_phone = entry_phone.get().strip()
            new_address = entry_address.get().strip()
            new_pharmacy = var_pharmacy.get().strip()

            if not new_phone or not new_address or not new_pharmacy:
                messagebox.showwarning("Ошибка", "Все поля обязательны.")
                return

            for emp in self._employees_data:
                if emp["id"] == employee["id"]:
                    emp["phone"] = new_phone
                    emp["address"] = new_address
                    emp["pharmacy"] = new_pharmacy
                    break

            print(f"[Заглушка] Сотрудник ID={employee['id']} отредактирован")
            modal.destroy()
            self.refresh_employees_list()

        btn_save = ctk.CTkButton(
            btn_frame,
            text="Сохранить",
            width=100, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=on_save
        )
        btn_save.pack(side="left", padx=(0, 10))

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

    def delete_employee(self, employee):
        """
        Удаление сотрудника с проверкой наличия у него заказов.
        """
        has_orders = any(o["employee_id"] == employee["id"]
                         for o in self._orders_data)
        if has_orders:
            messagebox.showerror(
                "Ошибка удаления",
                "Невозможно удалить сотрудника,\nтак как на его имя уже создан заказ."
            )
            return

        self._employees_data = [
            emp for emp in self._employees_data if emp["id"] != employee["id"]
        ]
        print(f"[Заглушка] Сотрудник ID={employee['id']} удалён")
        self.refresh_employees_list()
