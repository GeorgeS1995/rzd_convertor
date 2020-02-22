import json
import unittest
from rzd_converter import main
import os
import os.path as op
import exception as ex


class RZDconverterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_directory = op.join(os.getcwd(), "./testdata")
        self.test_directory = op.normpath(self.test_directory)

        self.input = op.join(self.test_directory, "./data.xlsm")
        self.input = op.normpath(self.input)

        self.input_old = op.join(self.test_directory, "./data.xls")
        self.input_old = op.normpath(self.input_old)

        self.output = "newname.json"

        self.result = {
            "ASOUP": [
                {
                    "SER_LOC": 530,
                    "ZNS_LOC": 1339,
                    "PRS_LOC": 1,
                    "DOR_PRIP": 76,
                    "DEPO_PRIP": 7,
                    "DATE_OP": "2019-09-17T09:35:00Z",
                    "KOD_SOST": 535,
                    "KOP_LMD": 0,
                    "PROBEG_LIN": 0,
                    "PROBEG_USL": 0,
                    "VREM_OPER": 0,
                    "EXPL_TYPE_CODE": 2
                }
            ],
            "loco_1": [
                {
                    "KOD_FIRM_PRIP": 317607,
                    "KOD_FIRM_REPAIR": 317637,
                    "REPAIR_KIND": 308,
                    "WAIT_DATE": "2019-10-06T19:09:00Z",
                    "REPAIR_DATE": "2019-10-06T20:03:00Z",
                    "FINISH_DATE": "2019-10-15T12:02:00Z",
                    "TCHD_REASON": "НЕИСПРАВНОСТЬ ВОДЯНОЙ СИСТЕМЫ ОХЛАЖДЕНИЯ ДИЗЕЛЯ",
                    "FINAL_REASON": "НЕИСПРАВНОСТЬ НЕ ПОДТВЕРЖДЕНА",
                    "FAIL_PLACE": "Водяные переходники выпускного коллектора",
                    "FINAL_GUILTY_FIRM": 317637,
                    "GUILTY_DRIVER": None,
                    "FINAL_DATE": "2019-10-28T17:28:14Z",
                    "SER_LOC": 506,
                    "ZNS_LOC": 65,
                    "PRS_LOC": 0
                }
            ],
            "loco_26": [
                {
                    "SER_LOC": 606,
                    "ZNS_LOC": 3,
                    "PRS_LOC": 0,
                    "REPAIR_DATE": "2019-10-01T00:00:00Z",
                    "REPAIR_TIME": "1899-12-31T07:00:00Z",
                    "REPAIR_KIND": "ТР-1",
                    "KOD_SLD": 317635
                }
            ],
            "acts_31L": [
                {
                    "ID": 219100060,
                    "ID_ETD": None,
                    "INDEX_NUM": "31-7635-191022195410",
                    "REG_DEPOT": 317607,
                    "REP_DEPOT": 317635,
                    "REP_CODE": 14,
                    "REP_NAME": "ТО-2",
                    "MOD_NUM": None,
                    "K_INDEX": 0,
                    "K_IND_ON_BODY": 0,
                    "LOCO_FUEL": 0,
                    "EKASUD_ID": None,
                    "IT_SECTIONS": {
                        "CTIME": "2019-10-22 21:26:41.680",
                        "section": {
                            "CTIME": "2019-10-22 21:26:41.680",
                            "SERIE": "506",
                            "SERIE_NAME": "ТЭП70",
                            "SER_NUM": "00000542",
                            "SEC_CODE": "0",
                            "EL_COUNT": 0,
                            "FUEL_LIT": 0,
                            "FUEL_DENS": 0.8,
                            "FUEL_KG": 0,
                            "IS_NEED": "1"
                        }
                    },
                    "IT_INVENT": {
                        "CTIME": "2019-10-22 21:26:41.680",
                        "inv": {
                            "CTIME": "2019-10-22 21:26:41.680",
                            "INVENT_NAME": "Пенька",
                            "UNIT": "шт.",
                            "NORMA": 0,
                            "FACT": 0,
                            "INFO_TYPE": "0"
                        }
                    }
                }
            ],
            "LocoSeries": [
                {
                    "OBJECT_ID": 702774,
                    "CLASS_ID": 418,
                    "OBJECT_KOD": 0,
                    "OBJECT_KODSTR": None,
                    "OBJECT_VNAME": None,
                    "OBJECT_NAME": "040-DHC",
                    "OBJECT_SNAME": None,
                    "REFER": None,
                    "S1": None,
                    "I1": None,
                    "KOMM": None,
                    "COR_TIP": "I",
                    "DATE_ND": "2012-08-07T00:00:00Z",
                    "DATE_KD": "9999-12-31T00:00:00Z",
                    "COR_TIME": "2012-08-08T11:19:42.639000Z",
                    "OPER_ID": 1143418,
                    "REPL_FL": 1,
                    "KOL_SEK": None,
                    "TYPE_GROUP_ID": None,
                    "TIP_TPS": None,
                    "ROD_SL": None
                }
            ]
        }

    def tearDown(self) -> None:
        for root, dirs, files in os.walk(self.test_directory):
            for file in files:
                if op.splitext(op.join(root, file))[1] == ".json":
                    os.remove(op.join(root, file))
            if root != self.test_directory:
                os.rmdir(root)

    def test_default_output(self):
        main(self.input)
        with open(op.join(self.test_directory, "data.json"), "r", encoding='utf-8') as f:
            data = json.load(f)
        self.assertTrue(op.isfile(op.join(self.test_directory, "data.json")))
        self.assertEqual(data, self.result)

    def test_outfile(self):
        main(self.input, self.output)
        self.assertTrue(op.isfile(op.join(self.test_directory, "newname.json")))

    def test_outfile_with_path(self):
        main(self.input, op.join(self.test_directory, "newdir", self.output))
        self.assertTrue(op.isfile(op.join(self.test_directory, "newdir", self.output)))

    def test_outfile_only_path(self):
        main(self.input, self.test_directory)
        self.assertTrue(op.isfile(op.join(self.test_directory, "data.json")))

    def test_outfile_exist(self):
        main(self.input)
        self.assertTrue(op.isfile(op.join(self.test_directory, "data.json")))
        self.assertRaisesRegex(ex.ConvertErr, "Can't convert file: output file exist", main, self.input)

        main(self.input, self.output)
        self.assertTrue(op.isfile(op.join(self.test_directory, "newname.json")))
        self.assertRaisesRegex(ex.ConvertErr, "Can't convert file: output file exist", main, self.input, self.output)

    def test_old_format(self):
        main(self.input_old)
        with open(op.join(self.test_directory, "data.json"), "r", encoding='utf-8') as f:
            data = json.load(f)
        self.assertTrue(op.isfile(op.join(self.test_directory, "data.json")))
        self.assertEqual(data, self.result)


if __name__ == '__main__':
    unittest.main()
