import sys
import mysql.connector
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLineEdit, QTextEdit, QComboBox, QDateEdit,
                             QSpinBox, QDoubleSpinBox, QFormLayout, QGroupBox,
                             QTabWidget, QMessageBox, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPalette, QColor

# test
class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Подключение к базе данных"""
        try:
            self.connection = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='Snejok2015',
                database='master_pol'
            )
            print("Успешное подключение к базе данных")
        except mysql.connector.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def execute_query(self, query, params=None):
        """Выполнение запроса к базе данных"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    def execute_update(self, query, params=None):
        """Выполнение запроса на обновление данных"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return False


class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("Производственная компания «Мастер пол»")
        self.setGeometry(100, 100, 1400, 800)

        # Установка стиля
        self.setup_styles()

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Боковая панель навигации
        self.create_sidebar(main_layout)

        # Основная область контента
        self.create_content_area(main_layout)

    def setup_styles(self):
        """Настройка стилей приложения"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QWidget {
                font-family: 'Segoe UI';
                font-size: 9pt;
                color: #333333;
            }
            /* Стили для боковой панели */
            .sidebar {
                background-color: #F4E8D3;
            }
            .sidebar-button {
                background-color: transparent;
                border: none;
                border-radius: 0px;
                padding: 12px 20px;
                text-align: left;
                color: #333333;
                font-weight: normal;
                border-left: 4px solid transparent;
            }
            .sidebar-button:hover {
                background-color: #E8D9C0;
                color: #333333;
            }
            .sidebar-button.active {
                background-color: #E8D9C0;
                color: #2C3E50;
                border-left: 4px solid #67BA80;
                font-weight: bold;
            }
            /* Основные кнопки */
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #DCDFE6;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #F5F7FA;
                border-color: #C0C4CC;
            }
            QPushButton.primary {
                background-color: #67BA80;
                color: #FFFFFF;
                border: 1px solid #67BA80;
                font-weight: bold;
            }
            QPushButton.primary:hover {
                background-color: #5AA870;
                border-color: #5AA870;
            }
            QPushButton.secondary {
                background-color: #F4E8D3;
                color: #8B7355;
                border: 1px solid #E8D9C0;
            }
            QPushButton.secondary:hover {
                background-color: #E8D9C0;
                border-color: #DCC9A8;
            }
            /* Таблицы */
            QTableWidget {
                border: 1px solid #DCDFE6;
                border-radius: 6px;
                background-color: #FFFFFF;
                gridline-color: #EBEEF5;
                outline: 0;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #EBEEF5;
                color: #606266;
            }
            QTableWidget::item:selected {
                background-color: #F0F9EB;
                color: #67BA80;
            }
            QHeaderView::section {
                background-color: #FAFAFA;
                padding: 12px 8px;
                border: none;
                border-bottom: 1px solid #EBEEF5;
                font-weight: bold;
                color: #303133;
            }
            /* Поля ввода */
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                border: 1px solid #DCDFE6;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: #FFFFFF;
                color: #606266;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, 
            QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #67BA80;
                background-color: #F0F9EB;
            }
            /* Группы */
            QGroupBox {
                font-weight: bold;
                border: 1px solid #E4E7ED;
                border-radius: 6px;
                margin-top: 16px;
                padding-top: 16px;
                color: #303133;
                background-color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #303133;
            }
            /* Вкладки */
            QTabWidget::pane {
                border: 1px solid #E4E7ED;
                border-radius: 6px;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #FAFAFA;
                padding: 12px 24px;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                color: #606266;
                border: 1px solid #E4E7ED;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                color: #67BA80;
                font-weight: bold;
                border-color: #67BA80;
            }
            QTabBar::tab:hover:!selected {
                background-color: #F5F7FA;
                color: #303133;
            }
        """)

    def create_sidebar(self, main_layout):
        """Создание боковой панели навигации"""
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setProperty("class", "sidebar")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Логотип
        logo_container = QWidget()
        logo_container.setFixedHeight(80)
        logo_container.setStyleSheet("background-color: #1A252F; border-bottom: 1px solid #34495E;")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 0, 20, 0)

        logo_label = QLabel("МАСТЕР ПОЛ")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            color: #67BA80;
            font-size: 18px;
            font-weight: bold;
            padding: 20px 0;
        """)
        logo_layout.addWidget(logo_label)

        sidebar_layout.addWidget(logo_container)

        # Кнопки навигации
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 20, 0, 20)
        nav_layout.setSpacing(2)

        nav_buttons = [
            ("Главная панель", self.show_main),
            ("Партнеры", self.show_partners),
            ("Продукция", self.show_products),
            ("Производство", self.show_production),
            ("Заявки", self.show_orders),
            ("Сотрудники", self.show_employees),
            ("Материалы", self.show_materials),
            ("Склад", self.show_warehouse),
            ("Поставщики", self.show_suppliers),
            ("Аналитика", self.show_analytics)
        ]

        self.nav_buttons = []
        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setProperty("class", "sidebar-button")
            btn.clicked.connect(callback)
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()

        # Кнопка выхода
        exit_btn = QPushButton("Выход")
        exit_btn.setProperty("class", "sidebar-button")
        exit_btn.clicked.connect(self.close)
        exit_btn.setStyleSheet("color: #E74C3C;")
        nav_layout.addWidget(exit_btn)

        sidebar_layout.addWidget(nav_container)

        main_layout.addWidget(sidebar)

    def create_content_area(self, main_layout):
        """Создание основной области контента"""
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #F5F7FA;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Верхняя панель
        top_bar = QWidget()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E4E7ED;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(30, 0, 30, 0)

        self.title_label = QLabel("Главная панель")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #303133;")

        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(0, 0, 0, 0)

        user_name = QLabel("Администратор")
        user_name.setStyleSheet("color: #606266; margin-right: 15px;")

        user_layout.addWidget(user_name)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(user_widget)

        content_layout.addWidget(top_bar)

        # Основной контент
        content_container = QWidget()
        content_container_layout = QVBoxLayout(content_container)
        content_container_layout.setContentsMargins(30, 30, 30, 30)
        content_container_layout.setSpacing(0)

        # Stacked widget для переключения между экранами
        self.stacked_widget = QStackedWidget()
        content_container_layout.addWidget(self.stacked_widget)

        content_layout.addWidget(content_container)

        # Создание всех экранов
        self.create_main_screen()
        self.create_partners_screen()
        self.create_products_screen()
        self.create_orders_screen()
        self.create_employees_screen()
        self.create_materials_screen()
        self.create_suppliers_screen()  # Новый экран поставщиков
        self.create_analytics_screen()

        main_layout.addWidget(content_widget)

    def create_stat_card(self, title, value, trend=None):
        """Создание карточки статистики"""
        card = QWidget()
        card.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #E4E7ED;
            border-radius: 8px;
            padding: 20px;
        """)
        card.setFixedHeight(120)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #303133;")

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #909399; margin-top: 8px;")

        layout.addWidget(value_label)
        layout.addWidget(title_label)

        if trend:
            trend_label = QLabel(trend)
            trend_label.setStyleSheet("color: #67BA80; font-size: 12px; margin-top: 5px;")
            layout.addWidget(trend_label)

        return card

    def create_main_screen(self):
        """Создание главного экрана"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Статистика из базы данных
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setSpacing(15)

        # Получение данных из БД
        partners_count = self.db.execute_query("SELECT COUNT(*) as count FROM partners")[0]['count']
        active_orders = self.db.execute_query("SELECT COUNT(*) as count FROM orders WHERE Status != 'Выполнена'")[0][
            'count']
        products_count = self.db.execute_query("SELECT COUNT(*) as count FROM products")[0]['count']
        low_stock = self.db.execute_query("SELECT COUNT(*) as count FROM materials WHERE StockQuantity < MinStock")[0][
            'count']

        stats_data = [
            ("Активные партнеры", str(partners_count), "+12%"),
            ("Заявки в работе", str(active_orders), "+5%"),
            ("Виды продукции", str(products_count), "+3%"),
            ("Материалы с низким запасом", str(low_stock), "Требуют заказа")
        ]

        for title, value, trend in stats_data:
            stats_layout.addWidget(self.create_stat_card(title, value, trend))

        layout.addWidget(stats_widget)

        # Две колонки
        columns_widget = QWidget()
        columns_layout = QHBoxLayout(columns_widget)
        columns_layout.setSpacing(20)

        # Последние заявки из БД
        orders_group = QGroupBox("Последние заявки")
        orders_layout = QVBoxLayout(orders_group)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Партнер", "Статус", "Сумма", "Дата"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Получение заявок из БД
        orders = self.db.execute_query("""
            SELECT o.OrderID, p.CompanyName, o.Status, o.TotalAmount, o.OrderDate 
            FROM orders o 
            LEFT JOIN partners p ON o.PartnerID = p.PartnerID 
            ORDER BY o.OrderDate DESC LIMIT 10
        """)

        table.setRowCount(len(orders))
        for i, order in enumerate(orders):
            table.setItem(i, 0, QTableWidgetItem(str(order['OrderID'])))
            table.setItem(i, 1, QTableWidgetItem(order['CompanyName']))
            table.setItem(i, 2, QTableWidgetItem(order['Status']))
            table.setItem(i, 3, QTableWidgetItem(f"{order['TotalAmount']:,.0f} ₽"))
            table.setItem(i, 4, QTableWidgetItem(str(order['OrderDate'])))

        orders_layout.addWidget(table)

        # Активность
        activity_group = QGroupBox("Последняя активность")
        activity_layout = QVBoxLayout(activity_group)

        # Получение последних продаж
        recent_sales = self.db.execute_query("""
            SELECT p.CompanyName, SUM(s.Quantity) as quantity 
            FROM saleshistory s 
            LEFT JOIN partners p ON s.PartnerID = p.PartnerID 
            GROUP BY p.CompanyName 
            ORDER BY quantity DESC LIMIT 5
        """)

        for sale in recent_sales:
            label = QLabel(f"• {sale['CompanyName']}: {sale['quantity']} ед.")
            label.setStyleSheet("padding: 8px 0; color: #606266; border-bottom: 1px solid #EBEEF5;")
            activity_layout.addWidget(label)

        columns_layout.addWidget(orders_group, 2)
        columns_layout.addWidget(activity_group, 1)

        layout.addWidget(columns_widget)

        self.stacked_widget.addWidget(widget)

    def create_partners_screen(self):
        """Создание экрана партнеров"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Панель управления
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        self.partner_search = QLineEdit()
        self.partner_search.setPlaceholderText("Поиск партнеров...")
        self.partner_search.setMinimumWidth(300)
        self.partner_search.textChanged.connect(self.search_partners)
        control_layout.addWidget(self.partner_search)

        control_layout.addStretch()

        add_btn = StyledButton("Добавить партнера")
        add_btn.setProperty("class", "primary")
        add_btn.clicked.connect(self.add_partner)
        control_layout.addWidget(add_btn)

        layout.addWidget(control_panel)

        # Таблица партнеров
        self.partners_table = QTableWidget()
        self.partners_table.setColumnCount(7)
        self.partners_table.setHorizontalHeaderLabels([
            "ID", "Название компании", "Тип", "Рейтинг", "Телефон",
            "Объем продаж", "Действия"
        ])
        self.partners_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_partners_data()
        layout.addWidget(self.partners_table)

        self.stacked_widget.addWidget(widget)

    def load_partners_data(self):
        """Загрузка данных партнеров из БД"""
        partners = self.db.execute_query("""
            SELECT p.*, COALESCE(SUM(s.TotalAmount), 0) as total_sales
            FROM partners p 
            LEFT JOIN saleshistory s ON p.PartnerID = s.PartnerID 
            GROUP BY p.PartnerID
        """)

        self.partners_table.setRowCount(len(partners))
        for i, partner in enumerate(partners):
            self.partners_table.setItem(i, 0, QTableWidgetItem(str(partner['PartnerID'])))
            self.partners_table.setItem(i, 1, QTableWidgetItem(partner['CompanyName']))
            self.partners_table.setItem(i, 2, QTableWidgetItem(partner['Type']))

            rating_item = QTableWidgetItem("★" * partner['Rating'])
            rating_item.setForeground(QColor("#E6A23C"))
            self.partners_table.setItem(i, 3, rating_item)

            self.partners_table.setItem(i, 4, QTableWidgetItem(partner['Phone']))
            self.partners_table.setItem(i, 5, QTableWidgetItem(f"{partner['total_sales']:,.0f} ₽"))

            # Кнопка действий
            action_btn = QPushButton("Редактировать")
            action_btn.setProperty("class", "secondary")
            action_btn.setFixedWidth(100)
            action_btn.clicked.connect(lambda checked, pid=partner['PartnerID']: self.edit_partner(pid))
            self.partners_table.setCellWidget(i, 6, action_btn)

    def search_partners(self):
        """Поиск партнеров"""
        search_text = self.partner_search.text()
        if search_text:
            partners = self.db.execute_query("""
                SELECT p.*, COALESCE(SUM(s.TotalAmount), 0) as total_sales
                FROM partners p 
                LEFT JOIN saleshistory s ON p.PartnerID = s.PartnerID 
                WHERE p.CompanyName LIKE %s OR p.Type LIKE %s
                GROUP BY p.PartnerID
            """, (f"%{search_text}%", f"%{search_text}%"))
        else:
            partners = self.db.execute_query("""
                SELECT p.*, COALESCE(SUM(s.TotalAmount), 0) as total_sales
                FROM partners p 
                LEFT JOIN saleshistory s ON p.PartnerID = s.PartnerID 
                GROUP BY p.PartnerID
            """)

        self.partners_table.setRowCount(len(partners))
        for i, partner in enumerate(partners):
            self.partners_table.setItem(i, 0, QTableWidgetItem(str(partner['PartnerID'])))
            self.partners_table.setItem(i, 1, QTableWidgetItem(partner['CompanyName']))
            self.partners_table.setItem(i, 2, QTableWidgetItem(partner['Type']))

            rating_item = QTableWidgetItem("★" * partner['Rating'])
            rating_item.setForeground(QColor("#E6A23C"))
            self.partners_table.setItem(i, 3, rating_item)

            self.partners_table.setItem(i, 4, QTableWidgetItem(partner['Phone']))
            self.partners_table.setItem(i, 5, QTableWidgetItem(f"{partner['total_sales']:,.0f} ₽"))

            action_btn = QPushButton("Редактировать")
            action_btn.setProperty("class", "secondary")
            action_btn.setFixedWidth(100)
            action_btn.clicked.connect(lambda checked, pid=partner['PartnerID']: self.edit_partner(pid))
            self.partners_table.setCellWidget(i, 6, action_btn)

    def add_partner(self):
        """Добавление нового партнера"""
        QMessageBox.information(self, "Добавление партнера", "Функция добавления партнера")

    def edit_partner(self, partner_id):
        """Редактирование партнера"""
        QMessageBox.information(self, "Редактирование", f"Редактирование партнера ID: {partner_id}")

    def create_products_screen(self):
        """Создание экрана продукции"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Вкладки
        tabs = QTabWidget()

        # Вкладка каталога
        catalog_tab = QWidget()
        catalog_layout = QVBoxLayout(catalog_tab)
        catalog_layout.setSpacing(15)

        # Фильтры
        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)

        self.product_type_combo = QComboBox()
        self.product_type_combo.addItems(["Все типы", "Ламинат", "Паркет", "Линолеум", "Ковролин"])
        self.product_type_combo.currentTextChanged.connect(self.filter_products)
        filter_layout.addWidget(QLabel("Тип:"))
        filter_layout.addWidget(self.product_type_combo)

        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText("Поиск продукции...")
        self.product_search.textChanged.connect(self.filter_products)
        filter_layout.addWidget(self.product_search)

        filter_layout.addStretch()

        catalog_layout.addWidget(filter_widget)

        # Таблица продукции
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(6)
        self.products_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Тип", "Минимальная цена",
            "Время производства", "Себестоимость"
        ])

        self.load_products_data()
        catalog_layout.addWidget(self.products_table)

        tabs.addTab(catalog_tab, "Каталог продукции")

        layout.addWidget(tabs)
        self.stacked_widget.addWidget(widget)

    def load_products_data(self):
        """Загрузка данных продукции из БД"""
        products = self.db.execute_query("SELECT * FROM products")

        self.products_table.setRowCount(len(products))
        for i, product in enumerate(products):
            self.products_table.setItem(i, 0, QTableWidgetItem(product['Article']))
            self.products_table.setItem(i, 1, QTableWidgetItem(product['Name']))
            self.products_table.setItem(i, 2, QTableWidgetItem(product['Type']))

            price_item = QTableWidgetItem(f"{product['MinPrice']:,.0f} ₽")
            price_item.setForeground(QColor("#67BA80"))
            self.products_table.setItem(i, 3, price_item)

            self.products_table.setItem(i, 4, QTableWidgetItem(f"{product['ProductionTime']} дней"))
            self.products_table.setItem(i, 5, QTableWidgetItem(f"{product['CostPrice']:,.0f} ₽"))

    def filter_products(self):
        """Фильтрация продукции"""
        product_type = self.product_type_combo.currentText()
        search_text = self.product_search.text()

        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if product_type != "Все типы":
            query += " AND Type = %s"
            params.append(product_type)

        if search_text:
            query += " AND (Name LIKE %s OR Article LIKE %s)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])

        products = self.db.execute_query(query, params)

        self.products_table.setRowCount(len(products))
        for i, product in enumerate(products):
            self.products_table.setItem(i, 0, QTableWidgetItem(product['Article']))
            self.products_table.setItem(i, 1, QTableWidgetItem(product['Name']))
            self.products_table.setItem(i, 2, QTableWidgetItem(product['Type']))

            price_item = QTableWidgetItem(f"{product['MinPrice']:,.0f} ₽")
            price_item.setForeground(QColor("#67BA80"))
            self.products_table.setItem(i, 3, price_item)

            self.products_table.setItem(i, 4, QTableWidgetItem(f"{product['ProductionTime']} дней"))
            self.products_table.setItem(i, 5, QTableWidgetItem(f"{product['CostPrice']:,.0f} ₽"))

    def create_orders_screen(self):
        """Создание экрана заявок"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Статус заявок
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setSpacing(10)

        # Получение статистики по статусам
        status_stats = self.db.execute_query("""
            SELECT Status, COUNT(*) as count 
            FROM orders 
            GROUP BY Status
        """)

        status_counts = {stat['Status']: stat['count'] for stat in status_stats}

        statuses = [
            ("Новые", status_counts.get('Новая', 0)),
            ("В работе", status_counts.get('В производстве', 0)),
            ("Ожидают оплаты", status_counts.get('Ожидает оплаты', 0)),
            ("Выполненные", status_counts.get('Выполнена', 0)),
            ("Отмененные", status_counts.get('Отменена', 0))
        ]

        for status, count in statuses:
            status_btn = QPushButton(f"{status} ({count})")
            status_btn.setProperty("class", "secondary")
            status_btn.setStyleSheet("font-weight: bold;")
            status_btn.setFixedHeight(50)
            status_btn.clicked.connect(lambda checked, s=status: self.filter_orders_by_status(s))
            status_layout.addWidget(status_btn)

        layout.addWidget(status_widget)

        # Детали заявки
        splitter = QSplitter(Qt.Horizontal)

        # Список заявок
        self.orders_list = QTableWidget()
        self.orders_list.setColumnCount(4)
        self.orders_list.setHorizontalHeaderLabels(["ID", "Партнер", "Статус", "Сумма"])
        self.orders_list.itemSelectionChanged.connect(self.show_order_details)

        self.load_orders_data()
        splitter.addWidget(self.orders_list)

        # Детали выбранной заявки
        self.order_details_widget = QWidget()
        self.order_details_layout = QVBoxLayout(self.order_details_widget)

        splitter.addWidget(self.order_details_widget)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)
        self.stacked_widget.addWidget(widget)

    def load_orders_data(self):
        """Загрузка данных заявок из БД"""
        orders = self.db.execute_query("""
            SELECT o.*, p.CompanyName 
            FROM orders o 
            LEFT JOIN partners p ON o.PartnerID = p.PartnerID 
            ORDER BY o.OrderDate DESC
        """)

        self.orders_list.setRowCount(len(orders))
        for i, order in enumerate(orders):
            self.orders_list.setItem(i, 0, QTableWidgetItem(str(order['OrderID'])))
            self.orders_list.setItem(i, 1, QTableWidgetItem(order['CompanyName']))

            status_item = QTableWidgetItem(order['Status'])
            if "производстве" in order['Status']:
                status_item.setForeground(QColor("#409EFF"))
            elif "ожидает" in order['Status']:
                status_item.setForeground(QColor("#E6A23C"))
            elif "выполнена" in order['Status']:
                status_item.setForeground(QColor("#67BA80"))
            self.orders_list.setItem(i, 2, status_item)

            self.orders_list.setItem(i, 3, QTableWidgetItem(f"{order['TotalAmount']:,.0f} ₽"))

    def filter_orders_by_status(self, status):
        """Фильтрация заявок по статусу"""
        status_map = {
            "Новые": "Новая",
            "В работе": "В производстве",
            "Ожидают оплаты": "Ожидает оплаты",
            "Выполненные": "Выполнена",
            "Отмененные": "Отменена"
        }

        db_status = status_map.get(status, status)

        orders = self.db.execute_query("""
            SELECT o.*, p.CompanyName 
            FROM orders o 
            LEFT JOIN partners p ON o.PartnerID = p.PartnerID 
            WHERE o.Status = %s
            ORDER BY o.OrderDate DESC
        """, (db_status,))

        self.orders_list.setRowCount(len(orders))
        for i, order in enumerate(orders):
            self.orders_list.setItem(i, 0, QTableWidgetItem(str(order['OrderID'])))
            self.orders_list.setItem(i, 1, QTableWidgetItem(order['CompanyName']))

            status_item = QTableWidgetItem(order['Status'])
            if "производстве" in order['Status']:
                status_item.setForeground(QColor("#409EFF"))
            elif "ожидает" in order['Status']:
                status_item.setForeground(QColor("#E6A23C"))
            elif "выполнена" in order['Status']:
                status_item.setForeground(QColor("#67BA80"))
            self.orders_list.setItem(i, 2, status_item)

            self.orders_list.setItem(i, 3, QTableWidgetItem(f"{order['TotalAmount']:,.0f} ₽"))

    def show_order_details(self):
        """Показать детали выбранной заявки"""
        current_row = self.orders_list.currentRow()
        if current_row >= 0:
            order_id = int(self.orders_list.item(current_row, 0).text())

            # Очистка предыдущих деталей
            for i in reversed(range(self.order_details_layout.count())):
                self.order_details_layout.itemAt(i).widget().setParent(None)

            # Получение деталей заявки
            order_details = self.db.execute_query("""
                SELECT o.*, p.CompanyName, p.Phone, p.Email 
                FROM orders o 
                LEFT JOIN partners p ON o.PartnerID = p.PartnerID 
                WHERE o.OrderID = %s
            """, (order_id,))[0]

            order_items = self.db.execute_query("""
                SELECT oi.*, p.Name as ProductName 
                FROM orderitems oi 
                LEFT JOIN products p ON oi.ProductID = p.ProductID 
                WHERE oi.OrderID = %s
            """, (order_id,))

            details_group = QGroupBox(f"Детали заявки #{order_id}")
            details_form = QFormLayout(details_group)

            details_form.addRow("ID заявки:", QLabel(str(order_details['OrderID'])))
            details_form.addRow("Партнер:", QLabel(order_details['CompanyName']))
            details_form.addRow("Статус:", QLabel(order_details['Status']))
            details_form.addRow("Сумма:", QLabel(f"{order_details['TotalAmount']:,.0f} ₽"))
            details_form.addRow("Дата создания:", QLabel(str(order_details['OrderDate'])))
            details_form.addRow("Телефон:", QLabel(order_details['Phone']))
            details_form.addRow("Email:", QLabel(order_details['Email']))

            # Продукция в заявке
            if order_items:
                products_table = QTableWidget()
                products_table.setColumnCount(4)
                products_table.setHorizontalHeaderLabels(["Продукция", "Количество", "Цена", "Сумма"])
                products_table.setRowCount(len(order_items))

                for i, item in enumerate(order_items):
                    products_table.setItem(i, 0, QTableWidgetItem(item['ProductName']))
                    products_table.setItem(i, 1, QTableWidgetItem(str(item['Quantity'])))
                    products_table.setItem(i, 2, QTableWidgetItem(f"{item['Price']:,.0f} ₽"))
                    products_table.setItem(i, 3, QTableWidgetItem(f"{item['Quantity'] * item['Price']:,.0f} ₽"))

                products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                details_form.addRow("Продукция:", products_table)

            self.order_details_layout.addWidget(details_group)

    def create_employees_screen(self):
        """Создание экрана сотрудников"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Таблица сотрудников
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "ФИО", "Должность", "Дата рождения", "Контакты", "Здоровье", "Категория"
        ])

        # Загрузка данных из БД
        employees = self.db.execute_query("""
            SELECT e.*, c.CategoryName 
            FROM employees e 
            LEFT JOIN employeecategories c ON e.CategoryID = c.CategoryID
        """)

        table.setRowCount(len(employees))
        for i, employee in enumerate(employees):
            table.setItem(i, 0, QTableWidgetItem(employee['FullName']))
            table.setItem(i, 1, QTableWidgetItem(employee['CategoryName']))
            table.setItem(i, 2, QTableWidgetItem(str(employee['BirthDate'])))
            table.setItem(i, 3, QTableWidgetItem("Контакты"))
            table.setItem(i, 4, QTableWidgetItem(employee['HealthStatus']))
            table.setItem(i, 5, QTableWidgetItem(employee['CategoryName']))

        layout.addWidget(table)
        self.stacked_widget.addWidget(widget)

    def create_materials_screen(self):
        """Создание экрана материалов"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Вкладки
        tabs = QTabWidget()

        # Материалы на складе
        materials_tab = QWidget()
        materials_layout = QVBoxLayout(materials_tab)
        materials_layout.setSpacing(15)

        # Панель управления
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        self.material_search = QLineEdit()
        self.material_search.setPlaceholderText("Поиск материалов...")
        self.material_search.setMinimumWidth(300)
        self.material_search.textChanged.connect(self.search_materials)
        control_layout.addWidget(self.material_search)

        control_layout.addStretch()

        add_btn = StyledButton("Добавить материал")
        add_btn.setProperty("class", "primary")
        add_btn.clicked.connect(self.add_material)
        control_layout.addWidget(add_btn)

        materials_layout.addWidget(control_panel)

        # Таблица материалов
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(8)
        self.materials_table.setHorizontalHeaderLabels([
            "ID", "Наименование", "Тип", "Поставщик", "Количество",
            "Мин. запас", "Стоимость", "Статус"
        ])
        self.materials_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_materials_data()
        materials_layout.addWidget(self.materials_table)

        tabs.addTab(materials_tab, "Материалы на складе")

        # Вкладка низких запасов
        low_stock_tab = QWidget()
        low_stock_layout = QVBoxLayout(low_stock_tab)

        low_stock_label = QLabel("Материалы с низким запасом")
        low_stock_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        low_stock_layout.addWidget(low_stock_label)

        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(6)
        self.low_stock_table.setHorizontalHeaderLabels([
            "Наименование", "Тип", "Текущий запас", "Мин. запас", "Разница", "Статус"
        ])
        self.load_low_stock_data()
        low_stock_layout.addWidget(self.low_stock_table)

        tabs.addTab(low_stock_tab, "Низкие запасы")

        layout.addWidget(tabs)
        self.stacked_widget.addWidget(widget)

    def load_materials_data(self):
        """Загрузка данных материалов из БД"""
        materials = self.db.execute_query("""
            SELECT m.*, p.CompanyName as SupplierName 
            FROM materials m 
            LEFT JOIN partners p ON m.SupplierID = p.PartnerID
            ORDER BY m.StockQuantity ASC
        """)

        self.materials_table.setRowCount(len(materials))
        for i, material in enumerate(materials):
            self.materials_table.setItem(i, 0, QTableWidgetItem(str(material['MaterialID'])))
            self.materials_table.setItem(i, 1, QTableWidgetItem(material['Name']))
            self.materials_table.setItem(i, 2, QTableWidgetItem(material['Type']))
            self.materials_table.setItem(i, 3, QTableWidgetItem(material['SupplierName'] or "Не указан"))
            self.materials_table.setItem(i, 4, QTableWidgetItem(f"{material['StockQuantity']} {material['Unit']}"))
            self.materials_table.setItem(i, 5, QTableWidgetItem(f"{material['MinStock']} {material['Unit']}"))
            self.materials_table.setItem(i, 6, QTableWidgetItem(f"{material['Cost']:,.2f} ₽"))

            status = "В норме" if material['StockQuantity'] >= material['MinStock'] else "Мало"
            status_item = QTableWidgetItem(status)
            if status == "В норме":
                status_item.setForeground(QColor("#67BA80"))
            else:
                status_item.setForeground(QColor("#E6A23C"))
            self.materials_table.setItem(i, 7, status_item)

    def load_low_stock_data(self):
        """Загрузка данных о материалах с низким запасом"""
        low_stock_materials = self.db.execute_query("""
            SELECT m.*, p.CompanyName as SupplierName 
            FROM materials m 
            LEFT JOIN partners p ON m.SupplierID = p.PartnerID
            WHERE m.StockQuantity < m.MinStock
            ORDER BY (m.StockQuantity - m.MinStock) ASC
        """)

        self.low_stock_table.setRowCount(len(low_stock_materials))
        for i, material in enumerate(low_stock_materials):
            self.low_stock_table.setItem(i, 0, QTableWidgetItem(material['Name']))
            self.low_stock_table.setItem(i, 1, QTableWidgetItem(material['Type']))
            self.low_stock_table.setItem(i, 2, QTableWidgetItem(f"{material['StockQuantity']} {material['Unit']}"))
            self.low_stock_table.setItem(i, 3, QTableWidgetItem(f"{material['MinStock']} {material['Unit']}"))

            difference = material['StockQuantity'] - material['MinStock']
            difference_item = QTableWidgetItem(f"{difference} {material['Unit']}")
            difference_item.setForeground(QColor("#E6A23C"))
            self.low_stock_table.setItem(i, 4, difference_item)

            status_item = QTableWidgetItem("Требует заказа")
            status_item.setForeground(QColor("#F56C6C"))
            self.low_stock_table.setItem(i, 5, status_item)

    def search_materials(self):
        """Поиск материалов"""
        search_text = self.material_search.text()
        if search_text:
            materials = self.db.execute_query("""
                SELECT m.*, p.CompanyName as SupplierName 
                FROM materials m 
                LEFT JOIN partners p ON m.SupplierID = p.PartnerID
                WHERE m.Name LIKE %s OR m.Type LIKE %s OR p.CompanyName LIKE %s
                ORDER BY m.StockQuantity ASC
            """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        else:
            materials = self.db.execute_query("""
                SELECT m.*, p.CompanyName as SupplierName 
                FROM materials m 
                LEFT JOIN partners p ON m.SupplierID = p.PartnerID
                ORDER BY m.StockQuantity ASC
            """)

        self.materials_table.setRowCount(len(materials))
        for i, material in enumerate(materials):
            self.materials_table.setItem(i, 0, QTableWidgetItem(str(material['MaterialID'])))
            self.materials_table.setItem(i, 1, QTableWidgetItem(material['Name']))
            self.materials_table.setItem(i, 2, QTableWidgetItem(material['Type']))
            self.materials_table.setItem(i, 3, QTableWidgetItem(material['SupplierName'] or "Не указан"))
            self.materials_table.setItem(i, 4, QTableWidgetItem(f"{material['StockQuantity']} {material['Unit']}"))
            self.materials_table.setItem(i, 5, QTableWidgetItem(f"{material['MinStock']} {material['Unit']}"))
            self.materials_table.setItem(i, 6, QTableWidgetItem(f"{material['Cost']:,.2f} ₽"))

            status = "В норме" if material['StockQuantity'] >= material['MinStock'] else "Мало"
            status_item = QTableWidgetItem(status)
            if status == "В норме":
                status_item.setForeground(QColor("#67BA80"))
            else:
                status_item.setForeground(QColor("#E6A23C"))
            self.materials_table.setItem(i, 7, status_item)

    def add_material(self):
        """Добавление нового материала"""
        QMessageBox.information(self, "Добавление материала", "Функция добавления материала")

    def create_suppliers_screen(self):
        """Создание экрана поставщиков"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)

        # Панель управления
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        self.supplier_search = QLineEdit()
        self.supplier_search.setPlaceholderText("Поиск поставщиков...")
        self.supplier_search.setMinimumWidth(300)
        self.supplier_search.textChanged.connect(self.search_suppliers)
        control_layout.addWidget(self.supplier_search)

        control_layout.addStretch()

        add_btn = StyledButton("Добавить поставщика")
        add_btn.setProperty("class", "primary")
        add_btn.clicked.connect(self.add_supplier)
        control_layout.addWidget(add_btn)

        layout.addWidget(control_panel)

        # Таблица поставщиков
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(8)
        self.suppliers_table.setHorizontalHeaderLabels([
            "ID", "Название компании", "Директор", "ИНН", "Телефон",
            "Email", "Рейтинг", "Поставляемые материалы"
        ])
        self.suppliers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_suppliers_data()
        layout.addWidget(self.suppliers_table)

        self.stacked_widget.addWidget(widget)

    def load_suppliers_data(self):
        """Загрузка данных поставщиков из БД"""
        suppliers = self.db.execute_query("""
            SELECT p.*, 
                   GROUP_CONCAT(DISTINCT m.Name SEPARATOR ', ') as SuppliedMaterials,
                   COUNT(m.MaterialID) as MaterialsCount
            FROM partners p 
            LEFT JOIN materials m ON p.PartnerID = m.SupplierID
            WHERE p.Type = 'Поставщик'
            GROUP BY p.PartnerID
            ORDER BY p.Rating DESC
        """)

        self.suppliers_table.setRowCount(len(suppliers))
        for i, supplier in enumerate(suppliers):
            self.suppliers_table.setItem(i, 0, QTableWidgetItem(str(supplier['PartnerID'])))
            self.suppliers_table.setItem(i, 1, QTableWidgetItem(supplier['CompanyName']))
            self.suppliers_table.setItem(i, 2, QTableWidgetItem(supplier['DirectorName']))
            self.suppliers_table.setItem(i, 3, QTableWidgetItem(supplier['INN']))
            self.suppliers_table.setItem(i, 4, QTableWidgetItem(supplier['Phone']))
            self.suppliers_table.setItem(i, 5, QTableWidgetItem(supplier['Email']))

            rating_item = QTableWidgetItem("★" * supplier['Rating'])
            rating_item.setForeground(QColor("#E6A23C"))
            self.suppliers_table.setItem(i, 6, rating_item)

            materials_text = supplier['SuppliedMaterials'] or "Не указаны"
            materials_count = f"{materials_text} ({supplier['MaterialsCount']} видов)"
            self.suppliers_table.setItem(i, 7, QTableWidgetItem(materials_count))

    def search_suppliers(self):
        """Поиск поставщиков"""
        search_text = self.supplier_search.text()
        if search_text:
            suppliers = self.db.execute_query("""
                SELECT p.*, 
                       GROUP_CONCAT(DISTINCT m.Name SEPARATOR ', ') as SuppliedMaterials,
                       COUNT(m.MaterialID) as MaterialsCount
                FROM partners p 
                LEFT JOIN materials m ON p.PartnerID = m.SupplierID
                WHERE p.Type = 'Поставщик' 
                  AND (p.CompanyName LIKE %s OR p.DirectorName LIKE %s OR m.Name LIKE %s)
                GROUP BY p.PartnerID
                ORDER BY p.Rating DESC
            """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        else:
            suppliers = self.db.execute_query("""
                SELECT p.*, 
                       GROUP_CONCAT(DISTINCT m.Name SEPARATOR ', ') as SuppliedMaterials,
                       COUNT(m.MaterialID) as MaterialsCount
                FROM partners p 
                LEFT JOIN materials m ON p.PartnerID = m.SupplierID
                WHERE p.Type = 'Поставщик'
                GROUP BY p.PartnerID
                ORDER BY p.Rating DESC
            """)

        self.suppliers_table.setRowCount(len(suppliers))
        for i, supplier in enumerate(suppliers):
            self.suppliers_table.setItem(i, 0, QTableWidgetItem(str(supplier['PartnerID'])))
            self.suppliers_table.setItem(i, 1, QTableWidgetItem(supplier['CompanyName']))
            self.suppliers_table.setItem(i, 2, QTableWidgetItem(supplier['DirectorName']))
            self.suppliers_table.setItem(i, 3, QTableWidgetItem(supplier['INN']))
            self.suppliers_table.setItem(i, 4, QTableWidgetItem(supplier['Phone']))
            self.suppliers_table.setItem(i, 5, QTableWidgetItem(supplier['Email']))

            rating_item = QTableWidgetItem("★" * supplier['Rating'])
            rating_item.setForeground(QColor("#E6A23C"))
            self.suppliers_table.setItem(i, 6, rating_item)

            materials_text = supplier['SuppliedMaterials'] or "Не указаны"
            materials_count = f"{materials_text} ({supplier['MaterialsCount']} видов)"
            self.suppliers_table.setItem(i, 7, QTableWidgetItem(materials_count))

    def add_supplier(self):
        """Добавление нового поставщика"""
        QMessageBox.information(self, "Добавление поставщика", "Функция добавления поставщика")

    def create_analytics_screen(self):
        """Создание экрана аналитики"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        label = QLabel("Раздел аналитики в разработке")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #909399; padding: 100px;")
        layout.addWidget(label)

        self.stacked_widget.addWidget(widget)

    # Методы переключения между экранами
    def show_main(self):
        self.stacked_widget.setCurrentIndex(0)
        self.title_label.setText("Главная панель")
        self.update_nav_buttons(0)
        self.create_main_screen()

    def show_partners(self):
        self.stacked_widget.setCurrentIndex(1)
        self.title_label.setText("Управление партнерами")
        self.update_nav_buttons(1)
        self.load_partners_data()

    def show_products(self):
        self.stacked_widget.setCurrentIndex(2)
        self.title_label.setText("Каталог продукции")
        self.update_nav_buttons(2)
        self.load_products_data()

    def show_production(self):
        self.show_main()

    def show_orders(self):
        self.stacked_widget.setCurrentIndex(3)
        self.title_label.setText("Управление заявками")
        self.update_nav_buttons(4)
        self.load_orders_data()

    def show_employees(self):
        self.stacked_widget.setCurrentIndex(4)
        self.title_label.setText("Сотрудники")
        self.update_nav_buttons(5)

    def show_materials(self):
        self.stacked_widget.setCurrentIndex(5)
        self.title_label.setText("Управление материалами")
        self.update_nav_buttons(6)
        self.load_materials_data()
        self.load_low_stock_data()

    def show_warehouse(self):
        self.show_main()

    def show_suppliers(self):
        self.stacked_widget.setCurrentIndex(6)
        self.title_label.setText("Поставщики")
        self.update_nav_buttons(8)
        self.load_suppliers_data()

    def show_analytics(self):
        self.stacked_widget.setCurrentIndex(7)
        self.title_label.setText("Аналитика")
        self.update_nav_buttons(9)

    def update_nav_buttons(self, active_index):
        """Обновление стиля кнопок навигации"""
        for i, btn in enumerate(self.nav_buttons):
            if i == active_index:
                btn.setProperty("class", "sidebar-button active")
            else:
                btn.setProperty("class", "sidebar-button")


def main():
    app = QApplication(sys.argv)

    # Установка шрифта
    font = QFont("Segoe UI")
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()