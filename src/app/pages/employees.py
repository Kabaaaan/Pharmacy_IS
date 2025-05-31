import customtkinter as ctk
from tkinter import messagebox, StringVar
import threading
from datetime import datetime
from .home import api


class EmployeesPage(ctk.CTkFrame):
    """Страница управления сотрудниками с улучшенным дизайном"""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1a1a1a")
        self.controller = controller
        self._employees_data = []
        self._pharmacies = []
        self._roles = []
        self.loading_spinner = None

        self._setup_ui()
        self.load_initial_data()

    def _setup_ui(self):
        """Инициализация UI компонентов"""
        self._create_header()
        self._create_controls_panel()
        self._create_scrollable_area()

    def _create_header(self):
        """Создание заголовка страницы с акцентным оформлением"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=200)

        ctk.CTkLabel(
            header_frame,
            text="Управление сотрудниками",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color="#ffffff"
        ).pack(side="bottom")

    def _create_controls_panel(self):
        """Панель управления с улучшенным дизайном"""
        actions_panel = ctk.CTkFrame(
            self,
            fg_color="#252525",
            corner_radius=14,
            border_width=1,
            border_color="#333333"
        )
        actions_panel.pack(fill="x", padx=20, pady=(0, 20))

        header_frame = ctk.CTkFrame(actions_panel, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 5))

        ctk.CTkLabel(
            header_frame,
            text="⚡ Действия с сотрудниками",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#7a7a7a"
        ).pack(expand=True)

        controls_frame = ctk.CTkFrame(actions_panel, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))

        btn_style = {
            "height": 40,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 8,
            "border_width": 1
        }

        btn_add_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        btn_add_frame.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.btn_add = ctk.CTkButton(
            btn_add_frame,
            text="➕ Добавить сотрудника",
            fg_color="#2e8b57",
            hover_color="#3cb371",
            border_color="#3a7a50",
            text_color="white",
            command=self._open_add_dialog,
            **btn_style
        )
        self.btn_add.pack(fill="x")

        filter_container = ctk.CTkFrame(
            controls_frame,
            fg_color="#303030",
            corner_radius=8,
            border_width=1,
            border_color="#404040"
        )
        filter_container.pack(side="right", expand=True, fill="both")

        filter_frame = ctk.CTkFrame(filter_container, fg_color="transparent")
        filter_frame.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(
            filter_frame,
            text="🔍 Фильтр по аптеке:",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(side="left", padx=(0, 5))

        self.pharmacy_filter = StringVar(value="Все")
        self.pharmacy_combobox = ctk.CTkComboBox(
            filter_frame,
            values=["Все"],
            variable=self.pharmacy_filter,
            state="disabled",
            width=180,
            font=ctk.CTkFont(size=14),
            fg_color="#383838",
            button_color="#4d4d4d",
            dropdown_fg_color="#252525",
            dropdown_text_color="white",
            dropdown_hover_color="#3a3a3a",
            text_color="white",
            command=self._refresh_employees
        )
        self.pharmacy_combobox.pack(side="left", fill="x", expand=True)

    def _create_scrollable_area(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(0, 10), fill="x", padx=20)

        ctk.CTkLabel(
            header_frame,
            text="СПИСОК СОТРУДНИКОВ",
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
        self.scrollable_frame.pack(
            padx=20, pady=(0, 20), fill="both", expand=True)

    def load_initial_data(self):
        """Загрузка начальных данных (аптеки, роли, сотрудники)"""
        self._show_loading()

        def fetch_data():
            pharmacies = api.get("pharmacy")
            if pharmacies:
                self._pharmacies = [(p["id"], p["address"])
                                    for p in pharmacies]
                self.after(100, lambda: self._update_pharmacy_filter(
                    ["Все"] + [addr for _, addr in self._pharmacies]
                ))

            roles = api.get("worker/role")
            if roles:
                self._roles = [(r["id"], r["name"]) for r in roles]

            self._refresh_employees()

        threading.Thread(target=fetch_data, daemon=True).start()

    def _update_pharmacy_filter(self, values):
        """Обновление списка аптек в фильтре"""
        if not self.winfo_exists():
            return
        if self.pharmacy_combobox and self.pharmacy_combobox.winfo_exists():
            self.pharmacy_combobox.configure(values=values, state="readonly")
        self._hide_loading()

    def _refresh_employees(self, *args):
        """Обновление списка сотрудников"""
        if not self.winfo_exists():
            return
        self._show_loading()

        def fetch_employees():
            response = api.get("worker")
            if response:
                for emp in response:
                    if isinstance(emp.get('role'), str):
                        emp['role'] = {'name': emp['role'],
                                       'id': emp.get('role_id', 0)}
                    elif not emp.get('role'):
                        emp['role'] = {'name': 'Неизвестно', 'id': 0}

                self._employees_data = response
                self.after(100, self._display_employees)
            else:
                self.after(100, lambda: messagebox.showerror(
                    "Ошибка", "Не удалось загрузить данные сотрудников"
                ))
                self._hide_loading()

        threading.Thread(target=fetch_employees, daemon=True).start()

    def _display_employees(self):
        """Отображение списка сотрудников"""
        if not self.winfo_exists():
            return
        self._clear_scrollable_area()

        selected_pharmacy = self.pharmacy_filter.get()
        if selected_pharmacy != "Все":
            pharmacy_id = next(
                (pid for pid, addr in self._pharmacies if addr ==
                 selected_pharmacy), None
            )
            employees = [
                e for e in self._employees_data if e["pharmacy_id"] == pharmacy_id]
        else:
            employees = self._employees_data

        if not employees:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="Сотрудники не найдены",
                font=ctk.CTkFont(size=14),
                text_color="white"
            ).pack(pady=20)
            self._hide_loading()
            return

        for emp in employees:
            self._create_employee_card(emp)

        self._hide_loading()

    def _create_employee_card(self, employee):
        """Создание карточки сотрудника в новом стиле"""
        if not self.scrollable_frame or not self.scrollable_frame.winfo_exists():
            return
        pharmacy_name = next(
            (addr for pid, addr in self._pharmacies if pid ==
             employee["pharmacy_id"]), "Неизвестно"
        )
        role_name = next(
            (name for rid, name in self._roles if rid ==
             employee["role_id"]), "Неизвестно"
        )

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
            text=f"👤 ID: {employee['id']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4d8af0",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            top_frame,
            text=f"📅 {employee['enter_date']}",
            font=ctk.CTkFont(size=13),
            text_color="#aaaaaa",
            anchor="e"
        ).pack(side="right")

        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(5, 0))

        ctk.CTkLabel(
            info_frame,
            text=f"🆔 {employee['FIO']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff",
            anchor="w"
        ).pack(fill="x", pady=2)

        ctk.CTkLabel(
            info_frame,
            text=f"📞 {employee['phone_number']}",
            font=ctk.CTkFont(size=13),
            text_color="#cccccc",
            anchor="w"
        ).pack(fill="x", pady=2)

        ctk.CTkLabel(
            info_frame,
            text=f"🏠 {employee['home_address']}",
            font=ctk.CTkFont(size=13),
            text_color="#cccccc",
            anchor="w"
        ).pack(fill="x", pady=2)

        ctk.CTkLabel(
            info_frame,
            text=f"💊 Аптека: {pharmacy_name}",
            font=ctk.CTkFont(size=13),
            text_color="#4d8af0",
            anchor="w"
        ).pack(fill="x", pady=2)

        ctk.CTkLabel(
            info_frame,
            text=f"👔 Должность: {role_name} | 💰 Зарплата: {employee['salary']:,} ₽",
            font=ctk.CTkFont(size=13),
            text_color="#4d8af0",
            anchor="w"
        ).pack(fill="x", pady=2)

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkButton(
            btn_frame,
            text="✏️ Контакты",
            width=120,
            height=30,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=lambda e=employee: self._open_edit_dialog(e)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="🏢 Место работы",
            width=140,
            height=30,
            fg_color="#5a5a8a",
            hover_color="#6a6a9a",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=lambda e=employee: self._open_change_pharmacy_dialog(e)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="🗑️ Удалить",
            width=100,
            height=30,
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=lambda e=employee: self._delete_employee(e)
        ).pack(side="right")

    def _open_change_pharmacy_dialog(self, employee):
        """Диалог изменения места работы сотрудника"""
        if not self._pharmacies:
            messagebox.showwarning("Ошибка", "Данные аптек не загружены")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.transient(self)  # Модальное поверх основного окна
        dialog.title(f"Изменение аптеки для {employee['FIO']}")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.focus_set()  # Устанавливаем фокус
        dialog.configure(fg_color="#1a1a1a")

        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=20)

        ctk.CTkLabel(
            header_frame,
            text="Смена аптеки",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")

        current_pharmacy = next(
            (addr for pid, addr in self._pharmacies if pid ==
             employee["pharmacy_id"]), "Неизвестно"
        )

        info_frame = ctk.CTkFrame(dialog, fg_color="#252525", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            info_frame,
            text=f"Текущая аптека: {current_pharmacy}",
            font=ctk.CTkFont(size=14),
            text_color="#ffffff"
        ).pack(padx=10, pady=8)

        ctk.CTkLabel(
            dialog,
            text="Новая аптека:",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(anchor="w", padx=20, pady=(10, 2))

        pharmacy_var = StringVar(value=current_pharmacy)
        pharmacy_combobox = ctk.CTkComboBox(
            dialog,
            values=[addr for _, addr in self._pharmacies],
            variable=pharmacy_var,
            width=380,
            fg_color="#333333",
            button_color="#444444",
            dropdown_fg_color="#252525",
            dropdown_text_color="white",
            dropdown_hover_color="#3a3a3a",
            text_color="white"
        )
        pharmacy_combobox.pack(padx=20, pady=(0, 20))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(0, 20), padx=20, fill="x")

        def submit():
            new_pharmacy_name = pharmacy_var.get()
            new_pharmacy_id = next(
                pid for pid, addr in self._pharmacies if addr == new_pharmacy_name
            )

            data = {"new_pharmacy_id": new_pharmacy_id}
            response = api.put(
                f"worker/work_place/{employee['id']}",
                json_data=data
            )

            if response:
                messagebox.showinfo(
                    "Успех", "Аптека сотрудника успешно изменена")
                dialog.destroy()
                self._refresh_employees()
            else:
                messagebox.showerror(
                    "Ошибка", "Не удалось изменить аптеку сотрудника")

        ctk.CTkButton(
            btn_frame,
            text="Сохранить",
            height=40,
            fg_color="#5a5a8a",
            hover_color="#6a6a9a",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            command=submit
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="Отмена",
            height=40,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            command=dialog.destroy
        ).pack(side="right", fill="x", expand=True)

    def _open_add_dialog(self):
        """Диалог добавления нового сотрудника"""
        if not self._pharmacies or not self._roles:
            messagebox.showwarning(
                "Ошибка", "Данные не загружены, попробуйте позже")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.transient(self)  # Модальное поверх основного окна
        dialog.title("Добавить сотрудника")
        dialog.geometry("500x750")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.focus_set()  # Устанавливаем фокус
        dialog.configure(fg_color="#1a1a1a")

        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=20)

        ctk.CTkLabel(
            header_frame,
            text="▌",
            font=ctk.CTkFont(size=24),
            text_color="#2e8b57"
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="Новый сотрудник",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text="▐",
            font=ctk.CTkFont(size=24),
            text_color="#2e8b57"
        ).pack(side="right")

        fields = [
            ("FIO", "ФИО", "text", ""),
            ("salary", "Зарплата", "number", "0"),
            ("enter_date", "Дата приёма", "date",
             datetime.now().strftime("%Y-%m-%d")),
            ("phone_number", "Телефон", "tel", "+7"),
            ("home_address", "Адрес", "text", ""),
        ]

        entries = {}
        for field, label, field_type, default in fields:
            ctk.CTkLabel(
                dialog, text=f"{label}:", text_color="white"
            ).pack(anchor="w", padx=20, pady=(10, 2))

            if field_type == "date":
                entry = ctk.CTkEntry(
                    dialog, placeholder_text="YYYY-MM-DD", width=380
                )
            else:
                entry = ctk.CTkEntry(
                    dialog, width=380
                )

            entry.insert(0, default)
            entry.pack(padx=20)
            entries[field] = entry

        ctk.CTkLabel(
            dialog, text="Аптека:", text_color="white"
        ).pack(anchor="w", padx=20, pady=(10, 2))

        pharmacy_var = StringVar(value=self._pharmacies[0][1])
        pharmacy_combobox = ctk.CTkComboBox(
            dialog,
            values=[addr for _, addr in self._pharmacies],
            variable=pharmacy_var,
            width=380,
            fg_color="#333333",
            button_color="#444444",
            dropdown_fg_color="#252525",
            dropdown_text_color="white",
            dropdown_hover_color="#3a3a3a",
            text_color="white"
        )
        pharmacy_combobox.pack(padx=20)

        ctk.CTkLabel(
            dialog, text="Должность:", text_color="white"
        ).pack(anchor="w", padx=20, pady=(10, 2))

        role_var = StringVar(value=self._roles[0][1])
        role_combobox = ctk.CTkComboBox(
            dialog,
            values=[name for _, name in self._roles],
            variable=role_var,
            width=380,
            fg_color="#333333",
            button_color="#444444",
            dropdown_fg_color="#252525",
            dropdown_text_color="white",
            dropdown_hover_color="#3a3a3a",
            text_color="white"
        )
        role_combobox.pack(padx=20, pady=(0, 15))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

        def submit():

            # Валидация зарплаты
            try:
                salary = float(entries["salary"].get())
                if salary < 0:
                    raise ValueError("Зарплата не может быть отрицательной")
            except ValueError:
                messagebox.showerror(
                    "Ошибка",
                    "Некорректное значение зарплаты\n"
                    "Введите положительное число (например: 45000 или 45000.50)"
                )
                entries["salary"].focus_set()
                return

            data = {
                "FIO": entries["FIO"].get().strip(),
                "salary": float(entries["salary"].get()),
                "enter_date": entries["enter_date"].get().strip(),
                "phone_number": entries["phone_number"].get().strip(),
                "home_address": entries["home_address"].get().strip(),
                "role_id": next(rid for rid, name in self._roles if name == role_var.get()),
                "pharmacy_id": next(pid for pid, addr in self._pharmacies if addr == pharmacy_var.get())
            }

            # Валидация
            if not all(data.values()):
                messagebox.showwarning(
                    "Ошибка", "Все поля обязательны для заполнения")
                return

            response = api.post("worker", json_data=data)
            if response:
                messagebox.showinfo("Успех", "Сотрудник успешно добавлен")
                dialog.destroy()
                self._refresh_employees()
            else:
                messagebox.showerror(
                    "Ошибка", "Не удалось добавить сотрудника")

        ctk.CTkButton(
            btn_frame,
            text="Добавить",
            width=120, height=36,
            fg_color="#2e8b57",
            hover_color="#3cb371",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=submit
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="Отмена",
            width=120, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=dialog.destroy
        ).pack(side="left")

    def _open_edit_dialog(self, employee):
        """Диалог редактирования сотрудника"""
        dialog = ctk.CTkToplevel(self)
        dialog.transient(self)  # Модальное поверх основного окна
        dialog.title(f"Редактирование сотрудника ID={employee['id']}")
        dialog.geometry("550x500")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.focus_set()  # Устанавливаем фокус
        dialog.configure(fg_color="#1a1a1a")

        header_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=20)

        ctk.CTkLabel(
            header_frame,
            text=f"Редактирование: {employee['FIO']}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")

        info_frame = ctk.CTkFrame(dialog, fg_color="#252525", corner_radius=8)
        info_frame.pack(fill="x", padx=20, pady=10)

        role_name = next(
            (name for rid, name in self._roles if rid == employee["role_id"]), "Неизвестно")
        ctk.CTkLabel(
            info_frame,
            text=f"Должность: {role_name} | Зарплата: {employee['salary']:,} ₽",
            font=ctk.CTkFont(size=14),
            text_color="#ffffff"
        ).pack(padx=10, pady=8)

        fields = [
            ("phone_number", "Телефон", employee["phone_number"]),
            ("home_address", "Адрес", employee["home_address"]),
        ]

        entries = {}
        for field, label, value in fields:
            ctk.CTkLabel(
                dialog, text=f"{label}:", text_color="white"
            ).pack(anchor="w", padx=20, pady=(10, 2))

            entry = ctk.CTkEntry(dialog, width=380)
            entry.insert(0, value)
            entry.pack(padx=20)
            entries[field] = entry

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(20, 20))

        def submit():
            data = {
                "phone_number": entries["phone_number"].get().strip,
                "home_address": entries["home_address"].get().strip()
            }

            if not all(data.values()):
                messagebox.showwarning(
                    "Ошибка", "Все поля обязательны для заполнения")
                return

            response = api.put(f"worker/{employee['id']}", json_data=data)
            if response:
                messagebox.showinfo("Успех", "Данные сотрудника обновлены")
                dialog.destroy()
                self._refresh_employees()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить данные")

        ctk.CTkButton(
            btn_frame,
            text="Сохранить",
            width=120, height=36,
            fg_color="#4d8af0",
            hover_color="#3a7ae0",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=submit
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="Отмена",
            width=120, height=36,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            command=dialog.destroy
        ).pack(side="left")

    def _delete_employee(self, employee):
        """Удаление сотрудника с подтверждением"""
        if not messagebox.askyesno(
            "Подтверждение",
            f"Вы точно хотите удалить сотрудника {employee['FIO']}?",
            parent=self
        ):
            return

        def perform_delete():
            response = api.delete(f"worker/{employee['id']}")

            if response is not None:
                self.after(100, lambda: messagebox.showinfo(
                    "Успех", "Сотрудник удалён"))
                self.after(100, self._refresh_employees)
            else:
                self.after(100, lambda: messagebox.showerror(
                    "Ошибка",
                    response.get('detail', 'Не удалось удалить сотрудника')
                ))

        self._show_loading()
        threading.Thread(target=perform_delete, daemon=True).start()

    def _show_loading(self):
        """Показать индикатор загрузки"""
        self._clear_scrollable_area()
        if self.scrollable_frame and self.scrollable_frame.winfo_exists():
            self.loading_spinner = ctk.CTkLabel(
                self.scrollable_frame,
                text="⏳ Загрузка данных...",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#7a7a7a"
            )
            self.loading_spinner.pack(pady=40)

    def _hide_loading(self):
        """Скрыть индикатор загрузки"""
        if self.loading_spinner and self.loading_spinner.winfo_exists():
            self.loading_spinner.destroy()
            self.loading_spinner = None

    def _clear_scrollable_area(self):
        """Очистить область с сотрудниками"""
        if self.scrollable_frame and self.scrollable_frame.winfo_exists():
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
