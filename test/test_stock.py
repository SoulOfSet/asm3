#!/usr/bin/python env

import unittest
import base

import stock
import utils

class TestStock(unittest.TestCase):
 
    nid = 0

    def setUp(self):
        data = {
            "name": "Test Stock",
            "description": "Test Description",
            "location": "1",
            "unitname": "Tablet",
            "total": "50",
            "balance": "50",
            "expiry": "2014-01-01",
            "batchnumber": "00001",
            "usagetype": "1",
            "usagedate": base.today_display()
        }
        post = utils.PostedData(data, "en")
        self.nid = stock.insert_stocklevel_from_form(base.get_dbo(), post, "test")

    def tearDown(self):
        base.execute("DELETE FROM stockusage WHERE StockLevelID = %d" % self.nid)
        stock.delete_stocklevel(base.get_dbo(), "test", self.nid)

    def test_get_stocklevel(self):
        assert None is not stock.get_stocklevel(base.get_dbo(), self.nid)

    def test_get_stocklevels(self):
        assert len(stock.get_stocklevels(base.get_dbo())) > 0

    def test_update_stocklevel_from_form(self):
        data = {
            "stocklevelid": str(self.nid),
            "name": "Test Stock",
            "description": "Test Description",
            "location": "1",
            "unitname": "Tablet",
            "total": "50",
            "balance": "50",
            "expiry": "2014-01-01",
            "batchnumber": "00001",
            "usagetype": "1",
            "usagedate": base.today_display()
        }
        post = utils.PostedData(data, "en")
        stock.update_stocklevel_from_form(base.get_dbo(), post, "test")

    def test_deduct_stocklevel_from_form(self):
        data = {
            "item": str(self.nid),
            "quantity": "1",
            "usagetype": "1",
            "usagedate": base.today_display(),
            "comments": "test"
        }
        post = utils.PostedData(data, "en")
        stock.deduct_stocklevel_from_form(base.get_dbo(), "test", post)

    def test_stock_take_from_mobile_form(self):
        data = {
            "sl%d" % self.nid: "5",
            "usagetype": "1"
        }
        post = utils.PostedData(data, "en")
        stock.stock_take_from_mobile_form(base.get_dbo(), "test", post)
       
