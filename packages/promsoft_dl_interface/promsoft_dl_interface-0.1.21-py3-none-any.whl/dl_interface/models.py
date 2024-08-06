#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional

from pydantic import BaseModel, Field, validator

# Включение проверки типов при присваивании
BaseModel.Config.validate_assignment = True


class Order(BaseModel):
    """Модель заказа на доставку груза."""

    class ManualParams(BaseModel):
        manual_length: float = Field(title='Длина отправления')
        manual_width: float = Field(title='Ширина отправления.')
        manual_height: float = Field(title='Высота отправления.')

        @validator('manual_length', 'manual_width', 'manual_height')
        def prevent_zero(cls, v):
            if v == 0:
                raise ValueError(
                    'Переданные размеры отправления не могут быть равны 0.')

            return v

    id: int = Field(title='idmonopolia')
    force: bool = False  # Если true - пересоздать существующую заявку.
    need_create_if_exists: Optional[bool] = False  # Если true - заявка является дополнительной частью заказа.
    hardPacking: bool = False
    insurance: bool = False
    manual_params: Optional[ManualParams] = Field(title='Размеры отправления.')


class Item(BaseModel):
    """Модель входящего запроса на сервис."""

    cargopickup: bool = False
    test: bool = Field(False, title="Режим тестирования.")
    arr: List[Order] = Field(title="Список заказов на доставку груза.")


class Token(BaseModel):
    """Модель токена задач."""

    token_id: str = Field(title="Токен, на получение результатов по созданию заявок.")


class Data(BaseModel):
    """Модель данных заявки."""

    request_id: int = Field(title="id заявки, полученной от Деловых Линий.")
    form: dict = Field(title="Форма заявки отправленная в Деловые Линии.")
    barcode: str = Field(title="Штрихкод, полученный от Деловых Линий.")


class RequestData(BaseModel):
    """Модель данных о результате создания заявки."""

    id: int = Field(title="idmonopolia")
    request_data: Optional[dict] = Field(title="Данные заявки от магазина.")
    query_params: Optional[Order] = Field(title="Параметры запроса на создание заявки от магазина.")
    data: Optional[Data] = Field(title="Данные о создании заявки.")
    error: Optional[str] = Field(title="Причина ошибки создания заявки.")


class Result(BaseModel):
    """Модель результа."""

    success: Optional[List[RequestData]] = Field(
        title="Список успешно созданных заявок."
    )
    fail: Optional[List[RequestData]] = Field(title="Список несозданных заявок.")
    total_pdf: Optional[str] = Field(title="Общий файл заявок на доставку груза.")
    status: Optional[str] = Field(title="Статус процесса создания заявок.")


class Response(BaseModel):
    """Модель ответа сервиса."""

    result: Optional[Result] = Field(title="Результат работы сервиса.")
