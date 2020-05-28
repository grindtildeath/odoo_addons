# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class TestEmployee(models.Model):

    _name = 'test.employee'
    _table = 'test_employee_text'
    _auto = False
    _sql = r"""
        CREATE TABLE test_employee_text (
            id INT4 NOT NULL,
            content text NULL,
            CONSTRAINT test_employee_text_pkey PRIMARY KEY (id)
        );
        CREATE TABLE test_employee_json (
            id INT4 NOT NULL,
            content jsonb NULL,
            CONSTRAINT test_employee_json_pkey PRIMARY KEY (id)
        );
    """
