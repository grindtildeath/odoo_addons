# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SavepointCase

import itertools
import json
import names
from psycopg2.sql import SQL, Identifier


class TestJSONBenchmark(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._populate_employee_tables()

    @classmethod
    def _populate_employee_tables(cls, records_nr=1000):
        names_list = cls._get_json_names(records_nr=records_nr)
        cls._insert_into_table('test_employee_text', names_list)
        cls._insert_into_table("test_employee_json", names_list)

    @classmethod
    def _get_json_names(cls, records_nr=1000):
        res = list()
        for i in range(0, records_nr):
            name = names.get_full_name()
            res.append({"id": i, "name": name})
        return json.dumps(res)

    @classmethod
    def _insert_into_table(cls, table_name, rec_list):
        sql_req = SQL(
            r"""INSERT INTO {} (id, content) VALUES (1, %s);"""
        ).format(Identifier(table_name))
        cls.env.cr.execute(sql_req, tuple([rec_list],))

    def test_read_from_text_table(self):
        self.env.cr.execute("SELECT content FROM test_employee_text;")
        res = self.env.cr.fetchall()
        self.assertEqual(len(res), 1)
        self.assertEqual(len(json.loads(res[0][0])), 1000)

    def test_read_subset_from_json_table(self):
        limit = 10
        res = 0
        fetch_res = [True]
        for i in itertools.takewhile(lambda c: len(fetch_res) > 0,
                                     itertools.count()):
            self.env.cr.execute(
                r"""
                    SELECT jsonb_array_elements(content)
                    FROM test_employee_json 
                    LIMIT %s 
                    OFFSET %s;
                """,
                tuple((limit, i * limit), ),
            )
            fetch_res = [row[0] for row in self.env.cr.fetchall()]
            res += len(fetch_res)
        self.assertEqual(res, 1000)

    def test_read_from_json_table(self):
        self.env.cr.execute(
            r"""
                SELECT content FROM test_employee_json;
            """,
        )
        fetch_res = self.env.cr.fetchall()
        self.assertEqual(len(fetch_res[0][0]), 1000)
