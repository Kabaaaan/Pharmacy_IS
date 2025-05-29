import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from .home import api
from openpyxl import Workbook
import os
import pathlib

class PrescriptionsPage(ctk.CTkFrame):
    """Страница «Работа с рецептами»"""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1a1a1a")
        self.controller = controller

        self._prescriptions_data = []
        self._medicines_list = []
        self._medicines_dict = {} 
        self.loading = False  

        self._setup_ui()
        self.load_medicines()
        self.refresh_prescriptions_list()

    def _setup_ui(self):
        # self._create_back_button()
        self._create_header()
        self._create_filters_panel()
        self._create_prescriptions_list()
        
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

    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=200)
        
        ctk.CTkLabel(
            header_frame,
            text="Работа с рецептами",
            font=ctk.CTkFont(size=26, weight="bold", family="Arial"),
            text_color="#ffffff"
        ).pack(side="bottom")
        
    def _create_filters_panel(self):
        actions_panel = ctk.CTkFrame(
            self, 
            fg_color="#252525",
            corner_radius=14,
            border_width=1,
            border_color="#333333"
        )
        actions_panel.pack(fill="x", padx=20, pady=(0, 20))
        
        header_frame = ctk.CTkFrame(actions_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="⚡ Действия с рецептами",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#7a7a7a"
        ).pack(side="left")
        
        buttons_frame = ctk.CTkFrame(actions_panel, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        btn_style = {
            "height": 40,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 8,
            "border_width": 1
        }
        
        self.btn_add = ctk.CTkButton(
            buttons_frame,
            text="➕ Создать новый рецепт",
            fg_color="#2e8b57",
            hover_color="#3cb371",
            border_color="#3a7a50",
            text_color="white",
            command=self.open_add_modal,
            **btn_style
        )
        self.btn_add.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        self.btn_export = ctk.CTkButton(
            buttons_frame,
            text="📁 Экспорт в Excel",
            fg_color="#4d8af0",
            hover_color="#3a7ae0",
            border_color="#3a5f8a",
            text_color="white",
            command=self.export_to_excel,
            **btn_style
        )
        self.btn_export.pack(side="left", expand=True, fill="x")
    
    def export_to_excel(self):
        """Экспорт списка рецептов в Excel"""
        if not self._prescriptions_data:
            messagebox.showwarning("Предупреждение", "Нет данных для экспорта")
            return
            
        self._show_loading_spinner()
        
        try:   
            # Определяем путь к папке reports (на 2 уровня выше текущего файла)
            current_dir = pathlib.Path(__file__).parent
            reports_dir = current_dir.parent.parent.parent / "reports"
            
            # Создаем папку, если ее нет
            os.makedirs(reports_dir, exist_ok=True)
            
            # Создаем новую книгу Excel
            wb = Workbook()
            ws = wb.active
            ws.title = "Рецепты"
            
            # Заголовки столбцов
            headers = ["ID", "Дата", "Врач", "Пациент", "Препарат"]
            ws.append(headers)
            
            # Заполняем данными
            for pres in self._prescriptions_data:
                ws.append([
                    pres["id"],
                    pres["date"].strftime("%d.%m.%Y"),
                    pres["doctor"],
                    pres["patient"],
                    pres["medicine"]
                ])
            
            # Автоматическая ширина столбцов
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                ws.column_dimensions[column].width = adjusted_width
            
            # Сохраняем файл в папку reports
            filename = f"рецепты_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
            filepath = reports_dir / filename
            wb.save(filepath)
            
            messagebox.showinfo(
                "Успех", 
                f"Данные успешно экспортированы в файл:\n{filepath}"
            )
            
        except ImportError:
            messagebox.showerror(
                "Ошибка", 
                "Для экспорта требуется установить openpyxl\n"
                "Установите его командой: pip install openpyxl"
            )
        except Exception as e:
            messagebox.showerror(
                "Ошибка", 
                f"Не удалось экспортировать данные: {str(e)}"
            )
        finally:
            self.refresh_prescriptions_list()

    def _create_prescriptions_list(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(0, 10), fill="x", padx=20)
        
        ctk.CTkLabel(
            header_frame,
            text="СПИСОК РЕЦЕПТОВ",
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

    def parse_date(self, date_str):
        """Парсит строку «дд.мм.ГГГГ» в datetime. Если некорректно — возвращает None."""
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except Exception:
            return None

    def reset_filter(self):
        """Сброс фильтра (очистка поля) и перерисовка списка."""
        self.entry_filter_date.delete(0, "end")
        self.refresh_prescriptions_list()

    def load_medicines(self):
        """Загружает список лекарств из API"""
        try:
            response = api.get(endpoint='medicine')
            
            if response and isinstance(response, list):
                self._medicines_list = [med["name"] for med in response]
                self._medicines_dict = {med["name"]: med["id"] for med in response}
            else:
                messagebox.showwarning("Предупреждение", "Не удалось загрузить список лекарств")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке лекарств: {str(e)}")

    def refresh_prescriptions_list(self):
        """Загружает и отображает список рецептов"""
        if self.loading:
            return
            
        self.loading = True
        self._show_loading_spinner()
        
        try:
            response = api.get(endpoint='order/recipe/date')
            
            if response and isinstance(response, list):
                processed = []
                for pres in response:
                    try:
                        processed.append({
                            "id": pres["id"],
                            "doctor": pres["doctor_name"],
                            "patient": pres["client_name"],
                            "medicine": pres["medicine_name"],
                            "date": datetime.strptime(pres["issue_date"], "%Y-%m-%d")
                        })
                    except Exception:
                        continue
                
                self._prescriptions_data = sorted(
                    processed, 
                    key=lambda p: p["date"], 
                    reverse=True
                )
                self._update_prescriptions_list()
            else:
                self._handle_no_data()
        except Exception as e:
            self._handle_error(f"Ошибка при загрузке рецептов: {str(e)}")
        finally:
            self.loading = False

    def _update_prescriptions_list(self):
        """Обновляет список рецептов на основе загруженных данных"""
        self._clear_orders_list()
        
        self.scrollable_frame._parent_canvas.yview_moveto(0)

        if not self._prescriptions_data:
            self._show_no_orders_message()
            return

        for pres in self._prescriptions_data:
            self._create_prescription_card(pres)

        self._hide_loading_spinner()

    def _clear_orders_list(self):
        """Очищает список рецептов"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def _show_loading_spinner(self):
        """Показывает индикатор загрузки"""
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
        """Скрывает индикатор загрузки"""
        if hasattr(self, 'loading_spinner') and self.loading_spinner:
            self.loading_spinner.destroy()

    def _show_no_orders_message(self):
        """Показывает сообщение об отсутствии рецептов"""
        empty_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#252525",
            corner_radius=12,
            height=100
        )
        empty_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            empty_frame,
            text="📭 Рецепты не найдены",
            font=ctk.CTkFont(size=16),
            text_color="#777777"
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _handle_no_data(self):
        """Обрабатывает отсутствие данных"""
        self._prescriptions_data = []
        self._update_prescriptions_list()
        messagebox.showwarning("Предупреждение", "Нет данных о рецептах")

    def _handle_error(self, message):
        """Обрабатывает ошибки"""
        self._prescriptions_data = []
        self._update_prescriptions_list()
        messagebox.showerror("Ошибка", message)

    def _create_prescription_card(self, prescription):
        """Создает карточку рецепта."""
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
            text=f"📋 Рецепт #{prescription['id']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4d8af0",
            anchor="w"
        ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            top_frame,
            text=f"📅 {prescription['date'].strftime('%d.%m.%Y')}",
            font=ctk.CTkFont(size=13),
            text_color="#aaaaaa",
            anchor="e"
        ).pack(side="right")
        
        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(5, 0))

        ctk.CTkLabel(
            info_frame,
            text=f"👨‍⚕️ Врач: {prescription['doctor']}",
            font=ctk.CTkFont(size=13),
            text_color="#cccccc",
            anchor="w"
        ).pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            info_frame,
            text=f"👤 Пациент: {prescription['patient']}",
            font=ctk.CTkFont(size=13),
            text_color="#cccccc",
            anchor="w"
        ).pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            info_frame,
            text=f"💊 Препарат: {prescription['medicine']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4d8af0",
            anchor="w"
        ).pack(fill="x", pady=2)
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Удалить",
            width=100,
            height=30,
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=lambda p=prescription: self.delete_prescription(p)
        ).pack(side="right")

    def delete_prescription(self, prescription):
        """Удаляет рецепт после подтверждения."""
        answer = messagebox.askyesno(
            "Удаление рецепта",
            f"Вы действительно хотите удалить рецепт ID={prescription['id']}?"
        )
        if not answer:
            return

        self._show_loading_spinner()
        
        try:
            response = api.delete(endpoint=f'order/recipe/{prescription["id"]}')
            if response:
                self._handle_delete_success()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить рецепт")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении: {str(e)}")
        finally:
            self.scrollable_frame._parent_canvas.yview_moveto(0)
            self.refresh_prescriptions_list()

    def _handle_delete_success(self):
        """Обрабатывает успешное удаление рецепта"""
        messagebox.showinfo("Успех", "Рецепт успешно удалён")

    def open_add_modal(self):
        """Модальное окно для создания нового рецепта."""
        if not self._medicines_list:
            messagebox.showwarning("Предупреждение", "Список лекарств ещё не загружен")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Добавить новый рецепт")
        modal.geometry("500x750")
        modal.configure(fg_color="#1a1a1a")
        modal.grab_set()
        modal.transient(self)
        modal.resizable(False, False)

        header_frame = ctk.CTkFrame(modal, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x", padx=20)
        
        ctk.CTkLabel(
            header_frame,
            text="▌",
            font=ctk.CTkFont(size=28),
            text_color="#4d8af0"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="Новый рецепт",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header_frame,
            text="▐",
            font=ctk.CTkFont(size=28),
            text_color="#4d8af0"
        ).pack(side="right")

        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(pady=(0, 20), padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            form_frame,
            text="ФИО врача:",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(anchor="w", pady=(10, 2))
        
        entry_doctor = ctk.CTkEntry(
            form_frame,
            placeholder_text="Введите ФИО врача",
            height=40,
            fg_color="#333333",
            border_color="#444444",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        entry_doctor.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            form_frame,
            text="Номер лицензии врача:",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(anchor="w", pady=(10, 2))
        
        entry_licence = ctk.CTkEntry(
            form_frame,
            placeholder_text="Введите номер лицензии врача",
            height=40,
            fg_color="#333333",
            border_color="#444444",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        entry_licence.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            form_frame,
            text="ФИО пациента:",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(anchor="w", pady=(10, 2))
        
        entry_patient = ctk.CTkEntry(
            form_frame,
            placeholder_text="Введите ФИО пациента",
            height=40,
            fg_color="#333333",
            border_color="#444444",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        entry_patient.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            form_frame,
            text="Дата выписки (дд.мм.ГГГГ):",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(anchor="w", pady=(10, 2))
        
        entry_date = ctk.CTkEntry(
            form_frame,
            placeholder_text="дд.мм.ГГГГ",
            height=40,
            fg_color="#333333",
            border_color="#444444",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        entry_date.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            form_frame,
            text="Лекарственный препарат:",
            font=ctk.CTkFont(size=14),
            text_color="#d6d6d6"
        ).pack(anchor="w", pady=(10, 2))
        
        combo_med = ctk.CTkComboBox(
            form_frame,
            values=sorted(self._medicines_list),
            state="readonly",
            height=40,
            dropdown_fg_color="#333333",
            button_color="#555555",
            corner_radius=8,
            font=ctk.CTkFont(size=14)
        )
        combo_med.pack(fill="x", pady=(0, 20))
        combo_med.set(self._medicines_list[0] if self._medicines_list else "")

        btn_frame = ctk.CTkFrame(modal, fg_color="transparent")
        btn_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        def on_confirm():
            doctor = entry_doctor.get().strip()
            license = entry_licence.get().strip()
            patient = entry_patient.get().strip()
            date_text = entry_date.get().strip()
            medicine = combo_med.get().strip()

            if not all([doctor, license, patient, date_text, medicine]):
                messagebox.showwarning("Ошибка", "Все поля обязательны.")
                return

            try:
                dt = datetime.strptime(date_text, "%d.%m.%Y")
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте дд.мм.ГГГГ")
                return

            try:
                license_number = int(license)
            except ValueError:
                messagebox.showerror("Ошибка", "Номер лицензии должен быть числом")
                return

            medicine_id = self._medicines_dict.get(medicine)
            if not medicine_id:
                messagebox.showerror("Ошибка", "Выбранное лекарство не найдено")
                return

            prescription_data = {
                "doctor_name": doctor,
                "license_number": license_number, 
                "client_name": patient,
                "medicine_id": medicine_id,
                "issue_date": dt.date().isoformat()
            }

            modal.destroy()
            self._show_loading_spinner()
            
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                
                response = api.post(
                    endpoint='order/recipe', 
                    json_data=prescription_data,
                    headers=headers
                )
                
                if response and response.get("id"):
                    messagebox.showinfo("Успех", "Рецепт успешно создан")
                    self.refresh_prescriptions_list()
                else:
                    error_msg = response.get("detail", "Не удалось создать рецепт")
                    messagebox.showerror("Ошибка", error_msg)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при создании рецепта: {str(e)}")
            finally:
                self._hide_loading_spinner()

        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="Добавить",
            height=40,
            fg_color="#2e8b57",
            hover_color="#3cb371",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            command=on_confirm
        )
        btn_confirm.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Отмена",
            height=40,
            fg_color="#555555",
            hover_color="#666666",
            text_color="white",
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            command=modal.destroy
        )
        btn_cancel.pack(side="right", fill="x", expand=True)

        modal.update_idletasks()
        width = modal.winfo_width()
        height = modal.winfo_height()
        x = (modal.winfo_screenwidth() // 2) - (width // 2)
        y = (modal.winfo_screenheight() // 2) - (height // 2)
        modal.geometry(f"{width}x{height}+{x}+{y}")