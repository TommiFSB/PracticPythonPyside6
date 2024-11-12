from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QLineEdit, QComboBox, QTableWidget,QTableWidgetItem,QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, BigInteger, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from models import session, Partner, TypeCompany, Address, PartnerProduct, Product, Material,ProductType, MaterialProduct
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSpacerItem, QSizePolicy
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
# Функция для расчета скидки
def calculate_discount(total_sales_quantity):
    if total_sales_quantity <= 10000:
        return 0
    elif total_sales_quantity <= 50000:
        return 5
    elif total_sales_quantity <= 300000:
        return 10
    else:
        return 15
class PartnerWidget(QFrame):
    def __init__(self, partner_data, update_callback):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("background-color: #67BA80; padding: 10px; border-radius: 5px;")
        layout = QVBoxLayout()
        # Получаем ID партнера для расчета скидки
        partner_id = partner_data.get("id")
        
        # Получаем данные о продажах партнера
        total_sales_quantity = session.query(func.sum(PartnerProduct.quantity)).filter(PartnerProduct.id_partner == partner_id).scalar()
        
        # Рассчитываем скидку
        if total_sales_quantity:
            discount = calculate_discount(total_sales_quantity)
        else:
            discount = 0

        # Добавляем скидку в данные партнера
        partner_data['discount'] = discount
        # Параметры партнера
        partner_type = QLabel(f"Тип партнера: {partner_data['type']}")
        partner_name = QLabel(f"Наименование партнера: {partner_data['name']}")
        director_name = QLabel(f"Директор: {partner_data['director']}")
        phone = QLabel(f"Телефон: {partner_data['phone']}")
        rating = QLabel(f"Рейтинг: {partner_data['rating']}")
        discount_label=QLabel(f"Скидка: {discount}")

        # Кнопка редактирования
        self.edit_button = QPushButton("")
        self.edit_button.setIcon(QIcon("pen.png"))
        self.edit_button.clicked.connect(self.show_partner)
        
        # Кнопка для вызова истории продаж
        self.history_button = QPushButton("История реализации продукции")
        self.history_button.clicked.connect(self.history)

        # Добавляем элементы в layout
        layout.addWidget(partner_type)
        layout.addWidget(partner_name)
        layout.addWidget(director_name)
        layout.addWidget(phone)
        layout.addWidget(rating)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.history_button)
        layout.addWidget(discount_label)
        self.setLayout(layout)

        self.update_callback = update_callback
        self.partner_data = partner_data

    def show_partner(self):
        # Открытие окна редактирования партнера
        self.red_partner_form = RedPartner(self.partner_data, self.update_callback)
        self.red_partner_form.show()

    def history(self):
        # Открытие истории продаж
        id_partner=self.partner_data['id']
        self.history_partner = SalesHistory(id_partner)
        self.history_partner.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: #F4E8D3")
        # Заголовок с логотипами
        header_layout = QHBoxLayout()
        left_logo_label = QLabel()
        left_logo_path = "icon.png"  
        left_pixmap = QPixmap(left_logo_path)
        left_logo_label.setPixmap(left_pixmap.scaled(50, 50, Qt.KeepAspectRatio))  # Масштабируем изображение
        header_layout.addWidget(left_logo_label)
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        right_logo_label = QLabel()
        right_logo_path = "icon.png"  
        right_pixmap = QPixmap(right_logo_path)
        right_logo_label.setPixmap(right_pixmap.scaled(50, 50, Qt.KeepAspectRatio))  # Масштабируем изображение
        header_layout.addWidget(right_logo_label)

        # Добавляем горизонтальный макет с логотипами и заголовком в основной макет
        main_layout.addLayout(header_layout)
        title = QLabel("Список партнеров")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        main_layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Инициализация данных о партнерах
        self.update_partner_list()

        scroll_area.setWidget(self.scroll_content)
        scroll_area.setStyleSheet("background-color: #FFFFFF")
        main_layout.addWidget(scroll_area)

        add_partner_button = QPushButton("Добавить партнера")
        add_partner_button.setStyleSheet("background-color: #67BA80")
        add_partner_button.setFixedSize(150, 30)
        add_partner_button.clicked.connect(self.add_partner)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(add_partner_button)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def fetch_partners_data(self):
        partners = session.query(Partner).join(TypeCompany).join(Address).order_by(Partner.id_partner).all()
        result = []
        for partner in partners:
            result.append({
                'id': partner.id_partner,
                'type': partner.type_company.name,
                'name': partner.company_name,
                'director': partner.director_name,
                'phone': partner.phone,
                'rating': partner.rating,
                'email': partner.email,
                'index': partner.address.index,
                'region': partner.address.region,
                'city': partner.address.city,
                'street': partner.address.street,
                'number': partner.address.number,
                'inn':partner.inn
            })
        return result

    def add_partner(self):
        # Открытие формы для добавления нового партнера
        self.add_partners_form = AddPartners(self.update_partner_list)
        self.add_partners_form.show()


    def update_partner_list(self):
        # Обновление списка партнеров
        partner_data_list = self.fetch_partners_data()
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        for partner_data in partner_data_list:
            partner_widget = PartnerWidget(partner_data, self.update_partner_list)
            self.scroll_layout.addWidget(partner_widget)


class RedPartner(QWidget):
    def __init__(self, partner_data, update_callback):
        super().__init__()
        self.setWindowTitle("Редактировать партнера")
        self.setWindowIcon(QIcon("icon.png"))
        title=QLabel("Редактирование партнера")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 12))
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #F4E8D3")
        layout = QVBoxLayout()
        self.partner_data = partner_data
        self.update_callback = update_callback
        header_layout = QHBoxLayout()
        right_logo_label = QLabel()
        right_logo_path = "icon.png"  
        right_pixmap = QPixmap(right_logo_path)
        right_logo_label.setPixmap(right_pixmap.scaled(50, 50, Qt.KeepAspectRatio))  # Масштабируем изображение
        header_layout.addWidget(right_logo_label)
        header_layout.addWidget(title)
        layout.addLayout(header_layout)
        # Основной контейнер для левой и правой части
        container_layout = QHBoxLayout()
    
        # Левая часть формы (название, тип партнёра, рейтинг, директор)
        left_layout = QVBoxLayout()
        self.name_input = QLineEdit(self.partner_data['name'])
        self.name_input.setStyleSheet("background-color:#FFFFFF")

        # Выпадающий список для типа партнёра
        self.type_combobox = QComboBox()
        self.type_combobox.setStyleSheet("background-color:#FFFFFF")
        self.load_type_company()
        self.set_selected_type(self.partner_data['type'])  # Устанавливаем текущий тип партнера
        self.rating_input = QLineEdit(str(self.partner_data['rating']))
        self.rating_input.setStyleSheet("background-color:#FFFFFF")
        self.director_input = QLineEdit(self.partner_data['director'])
        self.director_input.setStyleSheet("background-color:#FFFFFF")
        self.inn_input=QLineEdit(str(self.partner_data['inn']))
        self.inn_input.setStyleSheet("background-color:#FFFFFF")

        left_layout.addWidget(QLabel("Название партнера"))
        left_layout.addWidget(self.name_input)
        left_layout.addWidget(QLabel("Тип партнера"))
        left_layout.addWidget(self.type_combobox)
        left_layout.addWidget(QLabel("Рейтинг"))
        left_layout.addWidget(self.rating_input)
        left_layout.addWidget(QLabel("Директор"))
        left_layout.addWidget(self.director_input)
        left_layout.addWidget(QLabel("ИНН"))
        left_layout.addWidget(self.inn_input)

        # Правая часть формы (адрес, телефон, email)
        right_layout = QVBoxLayout()
        self.index_input = QLineEdit(str(self.partner_data['index']))
        self.index_input.setStyleSheet("background-color:#FFFFFF")
        self.region_input = QLineEdit(self.partner_data['region'])
        self.region_input.setStyleSheet("background-color:#FFFFFF")
        self.city_input = QLineEdit(self.partner_data['city'])
        self.city_input.setStyleSheet("background-color:#FFFFFF")
        self.street_input = QLineEdit(self.partner_data['street'])
        self.street_input.setStyleSheet("background-color:#FFFFFF")
        self.number_input = QLineEdit(str(self.partner_data['number']))
        self.number_input.setStyleSheet("background-color:#FFFFFF")
        self.phone_input = QLineEdit(self.partner_data['phone'])
        self.phone_input.setStyleSheet("background-color:#FFFFFF")
        self.email_input = QLineEdit(self.partner_data['email'])
        self.email_input.setStyleSheet("background-color:#FFFFFF")

        right_layout.addWidget(QLabel("Индекс"))
        right_layout.addWidget(self.index_input)
        right_layout.addWidget(QLabel("Регион"))
        right_layout.addWidget(self.region_input)
        right_layout.addWidget(QLabel("Город"))
        right_layout.addWidget(self.city_input)
        right_layout.addWidget(QLabel("Улица"))
        right_layout.addWidget(self.street_input)
        right_layout.addWidget(QLabel("Номер"))
        right_layout.addWidget(self.number_input)
        right_layout.addWidget(QLabel("Телефон"))
        right_layout.addWidget(self.phone_input)
        right_layout.addWidget(QLabel("Email"))
        right_layout.addWidget(self.email_input)

        # Размещение левой и правой частей
        container_layout.addLayout(left_layout)
        container_layout.addLayout(right_layout)

        # Кнопка сохранения
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_partner)
        self.red_message=QMessageBox()
        self.red_message.setIcon(QMessageBox.Information)
        self.red_message.setText("Отредактированные данные успешно сохранены!")
        self.red_message.setWindowTitle("Успех!")
        save_button.setStyleSheet("background-color: #67BA80; color: white;")
        save_button.setFixedSize(150, 40)

        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addStretch(stretch=4)

        layout.addLayout(container_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)
    def load_type_company(self):
        types = session.query(TypeCompany).all()
        for type_company in types:
            self.type_combobox.addItem(type_company.name, userData=type_company.id)

    def set_selected_type(self, type_name):
        index = self.type_combobox.findText(type_name)
        if index >= 0:
            self.type_combobox.setCurrentIndex(index)

    def save_partner(self):
        partner = session.query(Partner).filter_by(id_partner=self.partner_data['id']).first()
        if partner:
            partner.company_name = self.name_input.text()
            partner.type_partner_id = self.type_combobox.currentData()
            partner.director_name = self.director_input.text()
            partner.rating = int(self.rating_input.text())
            partner.phone = self.phone_input.text()
            partner.email = self.email_input.text()
            partner.inn=int(self.inn_input.text())

            address = session.query(Address).filter_by(id=partner.ur_adress).first()
            if address:
                address.index = int(self.index_input.text())
                address.region = self.region_input.text()
                address.city = self.city_input.text()
                address.street = self.street_input.text()
                address.number = int(self.number_input.text())

            session.commit()
            self.red_message.exec()
        self.update_callback()
        self.close()
        
class AddPartners(QWidget):
    def __init__(self, update_callback):
        super().__init__()
        title=QLabel("Добавление партнера")
        self.setWindowTitle("Добавление партнера")
        self.setWindowIcon(QIcon("icon.png"))
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 12))
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #F4E8D3")
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        header_layout.addWidget(title)
        right_logo_label = QLabel()
        right_logo_path = "icon.png"  
        right_pixmap = QPixmap(right_logo_path)
        right_logo_label.setPixmap(right_pixmap.scaled(100, 50, Qt.KeepAspectRatio))  # Масштабируем изображение
        header_layout.addWidget(right_logo_label)
        layout.addLayout(header_layout)
        self.update_callback = update_callback
        # Основной контейнер для левой и правой части
        container_layout = QHBoxLayout()
 # Левая часть формы (название, тип партнёра, рейтинг, директор)
        left_layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("background-color:#FFFFFF")
        
        # Выпадающий список для типа партнера
        self.type_combobox = QComboBox()
        self.type_combobox.setStyleSheet("background-color:#FFFFFF")
        self.load_type_company()  # Заполняем выпадающий список из базы данных
        
        self.rating_input = QLineEdit()
        self.rating_input.setStyleSheet("background-color:#FFFFFF")
        self.director_input = QLineEdit()
        self.director_input.setStyleSheet("background-color:#FFFFFF")
        self.inn_input=QLineEdit()
        self.inn_input.setStyleSheet("background-color:#FFFFFF")

        left_layout.addWidget(QLabel("Название партнера"))
        left_layout.addWidget(self.name_input)
        left_layout.addWidget(QLabel("Тип партнера"))
        left_layout.addWidget(self.type_combobox)
        left_layout.addWidget(QLabel("Рейтинг"))
        left_layout.addWidget(self.rating_input)
        left_layout.addWidget(QLabel("Директор"))
        left_layout.addWidget(self.director_input)
        left_layout.addWidget(QLabel("ИНН"))
        left_layout.addWidget(self.inn_input)

        # Правая часть формы (адрес, телефон, email)
        right_layout = QVBoxLayout()
        self.index_input = QLineEdit()
        self.index_input.setStyleSheet("background-color:#FFFFFF")
        self.region_input = QLineEdit()
        self.region_input.setStyleSheet("background-color:#FFFFFF")
        self.city_input = QLineEdit()
        self.city_input.setStyleSheet("background-color:#FFFFFF")
        self.street_input = QLineEdit()
        self.street_input.setStyleSheet("background-color:#FFFFFF")
        self.number_input = QLineEdit()
        self.number_input.setStyleSheet("background-color:#FFFFFF")
        self.phone_input = QLineEdit()
        self.phone_input.setStyleSheet("background-color:#FFFFFF")
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("background-color:#FFFFFF")
        

        right_layout.addWidget(QLabel("Индекс"))
        right_layout.addWidget(self.index_input)
        right_layout.addWidget(QLabel("Регион"))
        right_layout.addWidget(self.region_input)
        right_layout.addWidget(QLabel("Город"))
        right_layout.addWidget(self.city_input)
        right_layout.addWidget(QLabel("Улица"))
        right_layout.addWidget(self.street_input)
        right_layout.addWidget(QLabel("Номер"))
        right_layout.addWidget(self.number_input)
        right_layout.addWidget(QLabel("Телефон"))
        right_layout.addWidget(self.phone_input)
        right_layout.addWidget(QLabel("Email"))
        right_layout.addWidget(self.email_input)

        # Размещение левой и правой частей
        container_layout.addLayout(left_layout)
        container_layout.addLayout(right_layout)

        # Кнопка добавления
        save_button = QPushButton("Добавить")
        save_button.clicked.connect(self.save_partner)
        self.add_message=QMessageBox()
        self.add_message.setIcon(QMessageBox.Information)
        self.add_message.setText("Партнер успешно добавлен!")
        self.add_message.setWindowTitle("Успех!")
        
        save_button.setStyleSheet("background-color: #67BA80; color: white;")
        save_button.setFixedSize(150, 40)

        button_layout = QHBoxLayout()
        button_layout.addWidget(save_button)
        button_layout.addStretch(stretch=4)

        layout.addLayout(container_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_type_company(self):
        types = session.query(TypeCompany).all()
        for type_company in types:
            self.type_combobox.addItem(type_company.name, userData=type_company.id)

    def save_partner(self):
        try:
        # Пытаемся преобразовать значение индекса в целое число
            index = int(self.index_input.text())
        except ValueError:
        # Если возникает ошибка, показываем сообщение об ошибке и выходим из функции
            QMessageBox.critical(self, "Ошибка", "Индекс должен быть числом.")
            return
        new_address = Address(
            index=int(self.index_input.text()),
            region=self.region_input.text(),
            city=self.city_input.text(),
            street=self.street_input.text(),
            number=int(self.number_input.text())
            
        )
        session.add(new_address)
        session.flush()

        new_partner = Partner(
            company_name=self.name_input.text(),
            type_partner_id=self.type_combobox.currentData(),
            director_name=self.director_input.text(),
            rating=int(self.rating_input.text()),
            phone=self.phone_input.text(),
            email=self.email_input.text(),
            ur_adress=new_address.id,
            inn=int(self.inn_input.text())
        )
        self.add_message.exec()
        session.add(new_partner)
        session.commit()
        
        self.update_callback()
        self.close()

class SalesHistory(QWidget):
    def __init__(self, id_partner):
        super().__init__()
        self.id_partner=id_partner
        self.setWindowTitle("История продаж партнера")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: #F4E8D3")
        layout = QVBoxLayout()

        # Заголовок формы
        title = QLabel("История реализации продукции")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        header_layout = QHBoxLayout()
        left_logo_label = QLabel()
        left_logo_path = "icon.png"  
        left_pixmap = QPixmap(left_logo_path)
        left_logo_label.setPixmap(left_pixmap.scaled(50, 50, Qt.KeepAspectRatio))  # Масштабируем изображение
        header_layout.addWidget(left_logo_label)
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        right_logo_label = QLabel()
        right_logo_path = "icon.png"  
        right_pixmap = QPixmap(right_logo_path)
        right_logo_label.setPixmap(right_pixmap.scaled(50, 50, Qt.KeepAspectRatio))  # Масштабируем изображение
        header_layout.addWidget(right_logo_label)
        layout.addLayout(header_layout)

        # Таблица для отображения истории продаж
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Наименование продукции, Количество, Дата продажи
        self.table.setHorizontalHeaderLabels(["Продукция", "Количество", "Дата продажи"])
        self.load_sales_history(id_partner)
        self.table.setStyleSheet("background-color: #FFFFFF")

        layout.addWidget(self.table)

        
        report_button = QPushButton("Отчет")
        report_button.clicked.connect(self.generate_report_for_partner)
        self.report_message=QMessageBox()
        self.report_message.setIcon(QMessageBox.Information)
        self.report_message.setText("Отчет успешно создан!")
        self.report_message.setWindowTitle("Успех!")
        report_button.setStyleSheet("background-color: #FFFFFF")
        layout.addWidget(report_button)

        self.setLayout(layout)

    def load_sales_history(self, id_partner):
        # Извлекаем данные о продажах для данного партнера
        sales = session.query(PartnerProduct).filter(PartnerProduct.id_partner == id_partner).all()

        # Устанавливаем количество строк в таблице в зависимости от количества продаж
        self.table.setRowCount(len(sales))

        for row, sale in enumerate(sales):
            # Заполняем таблицу данными
            self.table.setItem(row, 0, QTableWidgetItem(sale.product.description))
            self.table.setItem(row, 1, QTableWidgetItem(str(sale.quantity)))
            self.table.setItem(row, 2, QTableWidgetItem(str(sale.date_of_sale)))
    def calculate_required_material(self, product_type_id, material_type_id, product_quantity, param1, param2):
        if product_quantity <= 0 or param1 <= 0 or param2 <= 0:
            return -1
        
        # Получаем коэффициент типа продукции и процент брака материала из базы данных
        product_type = session.query(ProductType).filter_by(id=product_type_id).first()
        material = session.query(Material).filter_by(id=material_type_id).first()
        
        if not product_type or not material:
            return -1  # Неверные идентификаторы

        # Расчет количества материала на единицу продукции
        material_per_product = param1 * param2 * product_type.coefficient

        # Учет брака материала
        material_with_waste = material_per_product * (1 + material.defect_rate / 100)

        # Общий расчет для заданного количества продукции
        total_material_required = int(material_with_waste * product_quantity)

        return total_material_required

    def generate_report(self, partner_name, product_type_id,product_type_name, material_type_id,material_name, product_quantity, param1, param2):
        required_material = self.calculate_required_material(product_type_id, material_type_id, product_quantity, param1, param2)

        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        
        # Создаем PDF файл
        report_path = f"{partner_name}_MaterialReport_{product_type_name}_{material_name}.pdf"
        c = canvas.Canvas(report_path, pagesize=A4)
        c.setFont("DejaVuSans", 12)  # Устанавливаем размер шрифта
        c.drawString(100, 800, f"Отчет по расчету материала для партнера: {partner_name}")
        c.drawString(100, 780, f"Тип продукции: {product_type_name} (ID: {product_type_id})")
        c.drawString(100, 760, f"Материал: {material_name} (ID: {material_type_id})")
        c.drawString(100, 740, f"Количество продукции: {product_quantity}")
        c.drawString(100, 720, f"Параметр 1: {param1}")
        c.drawString(100, 700, f"Параметр 2: {param2}")
        c.drawString(100, 680, f"Необходимое количество материала: {required_material}")
        
        c.showPage()
        c.save()
        print(f"PDF отчет создан: {report_path}")

    def generate_report_for_partner(self):
        # Получаем имя компании партнёра
        partner = session.query(Partner).filter_by(id_partner=self.id_partner).first()
        if not partner:
            print("Партнёр не найден.")
            return
        partner_name = partner.company_name

        # Извлекаем данные по каждому виду продукции и используемому материалу
        products = (
            session.query(Product, ProductType, Material, PartnerProduct)
            .join(PartnerProduct, PartnerProduct.id_product == Product.id)
            .join(ProductType, Product.type == ProductType.id)
            .join(MaterialProduct, MaterialProduct.id_product == Product.id)
            .join(Material, MaterialProduct.id_material == Material.id)
            .filter(PartnerProduct.id_partner == self.id_partner)
            .all()
        )

        report_data = []
        for product, product_type, material, partner_product in products:
            report_data.append({
                'product_id': product.id,
                'product_name': product.description,
                'product_type_name': product_type.name,
                'product_type_id': product_type.id,
                'material_name': material.name,
                'material_type_id': material.id,
                'product_quantity': partner_product.quantity
            })

        # Генерация PDF отчёта для каждого вида продукции партнёра
        for item in report_data:
            product_type_name = item['product_type_name']
            product_type_id = item['product_type_id']
            material_name = item['material_name']
            material_type_id = item['material_type_id']
            product_quantity = item['product_quantity']
            param1 = 2.0  
            param2 = 1.5  
            
            self.generate_report(partner_name, product_type_id,product_type_name, material_type_id,material_name, product_quantity, param1, param2)
        self.report_message.exec()
        print(f"Отчет для партнера {partner_name} успешно сгенерирован!")
# Запуск приложения
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
