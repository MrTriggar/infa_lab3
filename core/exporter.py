import sqlalchemy.orm
import json
import csv
import xml.etree.ElementTree as ET
import yaml
from io import StringIO
from pathlib import Path
from datetime import date
from decimal import Decimal
from core.models import *


class DatabaseExporter:
    def __init__(self):
        self.output_dir = Path("out")
        self.create_output_dir()

    def create_output_dir(self):
        """Создает папку out если её нет"""
        self.output_dir.mkdir(exist_ok=True)

    def get_model_data(self, model_class, include_relations=False):
        """
        Получает данные из модели SQLAlchemy
        """
        with localsession() as session:
            query = session.query(model_class)

            if include_relations:
                # Добавляем joined load для связанных данных
                if model_class == Buyer:
                    query = query.options(*[sqlalchemy.orm.joinedload(Buyer.orders)])
                elif model_class == Product:
                    query = query.options(*[
                        sqlalchemy.orm.joinedload(Product.category),
                        sqlalchemy.orm.joinedload(Product.seller)
                    ])
                elif model_class == Order:
                    query = query.options(*[
                        sqlalchemy.orm.joinedload(Order.buyer),
                        sqlalchemy.orm.joinedload(Order.products)
                    ])
                elif model_class == Seller:
                    query = query.options(*[sqlalchemy.orm.joinedload(Seller.products)])
                elif model_class == Categories:
                    query = query.options(*[sqlalchemy.orm.joinedload(Categories.products)])

            results = query.all()

            # Преобразуем объекты SQLAlchemy в словари
            data = []
            for obj in results:
                obj_dict = self.object_to_dict(obj, include_relations)
                data.append(obj_dict)

            return data

    def object_to_dict(self, obj, include_relations=False):
        """
        Рекурсивно преобразует объект SQLAlchemy в словарь
        """
        if obj is None:
            return None

        result = {}

        # Получаем все колонки таблицы
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)

            # Обрабатываем специальные типы данных
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)

            result[column.name] = value

        # Добавляем связанные данные если требуется
        if include_relations:
            for relationship in obj.__mapper__.relationships:
                related_obj = getattr(obj, relationship.key)

                if related_obj is not None:
                    if relationship.uselist:  # One-to-Many или Many-to-Many
                        result[relationship.key] = [
                            self.object_to_dict(item, False) for item in related_obj
                        ]
                    else:  # Many-to-One или One-to-One
                        result[relationship.key] = self.object_to_dict(related_obj, False)

        return result

    def serialize_json(self, data, filename="data.json"):
        """Сериализация в JSON"""
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return filepath

    def serialize_csv(self, data, filename="data.csv"):
        """Сериализация в CSV"""
        if not data:
            return None

        filepath = self.output_dir / filename

        # Получаем все возможные поля (включая вложенные)
        all_fields = set()
        for item in data:
            self._collect_fields(item, "", all_fields)

        fieldnames = sorted(all_fields)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in data:
                row = self._flatten_dict(item)
                writer.writerow(row)

        return filepath

    def _collect_fields(self, data, prefix, fields_set):
        """Рекурсивно собирает все поля из данных"""
        if isinstance(data, dict):
            for key, value in data.items():
                field_name = f"{prefix}{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    self._collect_fields(value, f"{field_name}_", fields_set)
                else:
                    fields_set.add(field_name)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._collect_fields(item, f"{prefix}{i}_", fields_set)

    def _flatten_dict(self, data, prefix=""):
        """Рекурсивно преобразует вложенный словарь в плоский"""
        flat_dict = {}

        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{prefix}{key}" if prefix else key

                if isinstance(value, dict):
                    flat_dict.update(self._flatten_dict(value, f"{full_key}_"))
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        list_prefix = f"{full_key}_{i}_"
                        if isinstance(item, dict):
                            flat_dict.update(self._flatten_dict(item, list_prefix))
                        else:
                            flat_dict[f"{full_key}_{i}"] = item
                else:
                    flat_dict[full_key] = value

        return flat_dict

    def serialize_xml(self, data, filename="data.xml"):
        """Сериализация в XML"""

        def dict_to_xml(element, data):
            for key, value in data.items():
                if isinstance(value, dict):
                    child = ET.SubElement(element, key)
                    dict_to_xml(child, value)
                elif isinstance(value, list):
                    list_elem = ET.SubElement(element, key)
                    for item in value:
                        if isinstance(item, dict):
                            item_elem = ET.SubElement(list_elem, "item")
                            dict_to_xml(item_elem, item)
                        else:
                            item_elem = ET.SubElement(list_elem, "item")
                            item_elem.text = str(item)
                else:
                    child = ET.SubElement(element, key)
                    child.text = str(value)

        root = ET.Element("data")
        for item in data:
            record_elem = ET.SubElement(root, "record")
            dict_to_xml(record_elem, item)

        filepath = self.output_dir / filename
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)

        return filepath

    def serialize_yaml(self, data, filename="data.yaml"):
        """Сериализация в YAML"""
        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

        return filepath

    def export_table(self, table_name, include_relations=False, base_filename=None):
        """
        Экспортирует указанную таблицу во всех форматах
        """
        # Определяем модель по имени таблицы
        model_map = {
            'buyers': Buyer,
            'sellers': Seller,
            'categories': Categories,
            'products': Product,
            'orders': Order
        }

        if table_name not in model_map:
            raise ValueError(f"Таблица {table_name} не найдена")

        model_class = model_map[table_name]

        if base_filename is None:
            base_filename = table_name

        # Получаем данные
        data = self.get_model_data(model_class, include_relations)

        # Экспортируем во все форматы
        results = {
            'json': self.serialize_json(data, f"{base_filename}.json"),
            'csv': self.serialize_csv(data, f"{base_filename}.csv"),
            'xml': self.serialize_xml(data, f"{base_filename}.xml"),
            'yaml': self.serialize_yaml(data, f"{base_filename}.yaml")
        }

        return results

        # Упрощенный интерфейс для быстрого использования
    def export_all_tables(self):
        """Экспортирует все таблицы во всех форматах"""
        exporter = DatabaseExporter()

        tables = ['buyers', 'sellers', 'categories', 'products', 'orders']
        all_results = {}

        for table in tables:
            print(f"Экспортирую {table}...")
            try:
                # Для основных таблиц включаем связанные данные
                include_relations = table in ['buyers', 'products', 'orders']
                results = exporter.export_table(table, include_relations)
                all_results[table] = results
                print(f" {table} успешно экспортирована")
            except Exception as e:
                 print(f" Ошибка при экспорте {table}: {e}")

        return all_results