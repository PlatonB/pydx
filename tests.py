# autopep8: off
import sys; sys.dont_write_bytecode = True
# autopep8: on
import unittest
import os
from src.antidb.srt import *
from src.antidb.idx import *
from src.antidb.prs import *

__version__ = 'v4.0.0'
__authors__ = [{'name': 'Platon Bykadorov',
                'email': 'platon.work@gmail.com',
                'years': '2023-2025'}]


class AntidbTests(unittest.TestCase):
    src_bed = ['1\t116545156\t116545157\trs12044852\n',
               '1\t241782991\t241782992\trs952084\n',
               '1\t154527612\t154527613\trs4131514\n',
               '1\t201015351\t201015352\trs12122721\n',
               '1\t92515681\t92515682\trs17371561\n',
               '1\t92543755\t92543756\trs11804321\n',
               '1\t92580419\t92580420\trs17380378\n',
               '1\t24977084\t24977085\trs10903122\n',
               '1\t92516860\t92516861\trs11581176\n',
               '1\t92543755\t92543756\trs11804321\n',
               '1\t92516860\t92516861\trs11581176\n',
               '1\t86877126\t86877127\trs581405\n',
               '1\t237115473\t237115474\trs10925318\n',
               '1\t86876786\t86876787\trs479341\n',
               '1\t66265029\t66265030\trs1321172\n',
               '1\t92543755\t92543756\trs11804321\n']
    src_file_path = os.path.join(os.getcwd(),
                                 'bed.bed')
    db_zst_path = os.path.join(os.getcwd(),
                               'bed.bed.zst')

    def test_common(self):
        adb_path = os.path.join(os.getcwd(),
                                'bed.bed.rsids.adb')
        with open(self.src_file_path, 'w') as src_file_opened:
            for src_line in self.src_bed:
                src_file_opened.write(src_line)
        self.assertTrue(os.path.isfile(self.src_file_path))
        if os.path.exists(self.db_zst_path):
            os.remove(self.db_zst_path)
        if os.path.exists(adb_path):
            os.remove(adb_path)
        idx_obj = Idx(db_file_path=self.src_file_path,
                      idx_prefix='rsids',
                      your_line_prs=lambda line:
                      line.split('\t')[-1],
                      presrt_chunk_elems_quan=5,
                      idx_chunk_elems_quan=5)
        idx_obj.idx()
        self.assertEqual(len(idx_obj.presrtd_idxs_opened), 4)
        self.assertTrue(os.path.isfile(self.src_file_path))
        self.assertTrue(os.path.isfile(self.db_zst_path))
        self.assertTrue(os.path.isfile(adb_path))
        with ZipFile(adb_path) as adb_opened_r:
            adb_content = adb_opened_r.namelist()
            idx_names = []
            idx_begins = []
            b_names = []
            for file_name in adb_content:
                if file_name.endswith('.idx'):
                    idx_names.append(file_name)
                    idx_begins.append(eval(file_name.replace('.idx',
                                                             '')))
                elif file_name.endswith('.b'):
                    b_names.append(file_name)
            srtd_idx_names = sorted(idx_names)
            self.assertEqual(srtd_idx_names[0],
                             "[[inf, 'rs', 10903122]].idx")
            self.assertEqual(srtd_idx_names[1],
                             "[[inf, 'rs', 11804321]].idx")
            self.assertEqual(srtd_idx_names[2],
                             "[[inf, 'rs', 17380378]].idx")
            self.assertEqual(srtd_idx_names[3],
                             "[[inf, 'rs', 479341]].idx")
            self.assertEqual(len(srtd_idx_names),
                             4)
            srtd_b_names = sorted(b_names)
            self.assertEqual(srtd_b_names[0],
                             "[[inf, 'rs', 10903122]].b")
            self.assertEqual(srtd_b_names[1],
                             "[[inf, 'rs', 11804321]].b")
            self.assertEqual(srtd_b_names[2],
                             "[[inf, 'rs', 17380378]].b")
            self.assertEqual(srtd_b_names[3],
                             "[[inf, 'rs', 479341]].b")
            self.assertEqual(len(srtd_b_names),
                             4)
            srtd_idx_begins = sorted(idx_begins)
            self.assertEqual(srtd_idx_begins[0],
                             [[float('+inf'),
                               'rs', 479341]])
            self.assertEqual(srtd_idx_begins[1],
                             [[float('+inf'),
                               'rs', 10903122]])
            self.assertEqual(srtd_idx_begins[2],
                             [[float('+inf'),
                               'rs', 11804321]])
            self.assertEqual(srtd_idx_begins[3],
                             [[float('+inf'),
                               'rs', 17380378]])
            self.assertEqual(len(srtd_idx_begins),
                             4)
            self.assertTrue('meta.txt' in adb_content)
            self.assertEqual(len(adb_content),
                             9)
            with ZstdFile(adb_opened_r.open("[[inf, 'rs', 479341]].idx")) as fir_idx_opened:
                fir_idx = load(fir_idx_opened)
                self.assertEqual(fir_idx[0],
                                 [[inf, 'rs', 479341]])
                self.assertEqual(fir_idx[1],
                                 [[inf, 'rs', 581405]])
                self.assertEqual(fir_idx[2],
                                 [[inf, 'rs', 952084]])
                self.assertEqual(fir_idx[3],
                                 [[inf, 'rs', 1321172]])
                self.assertEqual(fir_idx[4],
                                 [[inf, 'rs', 4131514]])
                self.assertEqual(len(fir_idx),
                                 5)
            with ZstdFile(adb_opened_r.open("[[inf, 'rs', 10903122]].idx")) as sec_idx_opened:
                sec_idx = load(sec_idx_opened)
                self.assertEqual(sec_idx[0],
                                 [[inf, 'rs', 10903122]])
                self.assertEqual(sec_idx[1],
                                 [[inf, 'rs', 10925318]])
                self.assertEqual(sec_idx[2],
                                 [[inf, 'rs', 11581176]])
                self.assertEqual(sec_idx[3],
                                 [[inf, 'rs', 11581176]])
                self.assertEqual(sec_idx[4],
                                 [[inf, 'rs', 11804321]])
                self.assertEqual(len(sec_idx),
                                 5)
            with ZstdFile(adb_opened_r.open("[[inf, 'rs', 11804321]].idx")) as thi_idx_opened:
                thi_idx = load(thi_idx_opened)
                self.assertEqual(thi_idx[0],
                                 [[inf, 'rs', 11804321]])
                self.assertEqual(thi_idx[1],
                                 [[inf, 'rs', 11804321]])
                self.assertEqual(thi_idx[2],
                                 [[inf, 'rs', 12044852]])
                self.assertEqual(thi_idx[3],
                                 [[inf, 'rs', 12122721]])
                self.assertEqual(thi_idx[4],
                                 [[inf, 'rs', 17371561]])
                self.assertEqual(len(thi_idx),
                                 5)
            with ZstdFile(adb_opened_r.open("[[inf, 'rs', 17380378]].idx")) as fou_idx_opened:
                fou_idx = load(fou_idx_opened)
                self.assertEqual(fou_idx[0],
                                 [[inf, 'rs', 17380378]])
                self.assertEqual(len(fou_idx),
                                 1)
        prs_obj = Prs(db_file_path=self.src_file_path,
                      idx_prefix='rsids')
        self.assertEqual(list(prs_obj.eq('rs12044852')),
                         ['1\t116545156\t116545157\trs12044852\n'])
        self.assertEqual(list(prs_obj.eq('rs952084')),
                         ['1\t241782991\t241782992\trs952084\n'])
        self.assertEqual(list(prs_obj.eq('rs4131514')),
                         ['1\t154527612\t154527613\trs4131514\n'])
        self.assertEqual(list(prs_obj.eq('rs12122721')),
                         ['1\t201015351\t201015352\trs12122721\n'])
        self.assertEqual(list(prs_obj.eq('rs17371561')),
                         ['1\t92515681\t92515682\trs17371561\n'])
        self.assertEqual(list(prs_obj.eq('rs11804321')),
                         ['1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n'])
        self.assertEqual(list(prs_obj.eq('rs17380378')),
                         ['1\t92580419\t92580420\trs17380378\n'])
        self.assertEqual(list(prs_obj.eq('rs10903122')),
                         ['1\t24977084\t24977085\trs10903122\n'])
        self.assertEqual(list(prs_obj.eq('rs11581176')),
                         ['1\t92516860\t92516861\trs11581176\n',
                          '1\t92516860\t92516861\trs11581176\n'])
        self.assertEqual(list(prs_obj.eq('rs581405')),
                         ['1\t86877126\t86877127\trs581405\n'])
        self.assertEqual(list(prs_obj.eq('rs10925318')),
                         ['1\t237115473\t237115474\trs10925318\n'])
        self.assertEqual(list(prs_obj.eq('rs479341')),
                         ['1\t86876786\t86876787\trs479341\n'])
        self.assertEqual(list(prs_obj.eq('rs1321172')),
                         ['1\t66265029\t66265030\trs1321172\n'])
        self.assertEqual(list(prs_obj.eq('rs00000')),
                         [])
        self.assertEqual(list(prs_obj.eq('rs11804321',
                                         'rs11581176',
                                         'hz12345')),
                         ['1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92516860\t92516861\trs11581176\n',
                          '1\t92516860\t92516861\trs11581176\n'])
        self.assertEqual(list(prs_obj.rng('rs479341',
                                          'rs952084')),
                         ['1\t86876786\t86876787\trs479341\n',
                          '1\t86877126\t86877127\trs581405\n',
                          '1\t241782991\t241782992\trs952084\n'])
        self.assertEqual(list(prs_obj.rng('rs4131514',
                                          'rs10903122')),
                         ['1\t154527612\t154527613\trs4131514\n',
                          '1\t24977084\t24977085\trs10903122\n'])
        self.assertEqual(list(prs_obj.rng('rs11804321',
                                          'rs11804321')),
                         ['1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n'])
        self.assertEqual(list(prs_obj.rng('rs12122721',
                                          'rs17380378')),
                         ['1\t201015351\t201015352\trs12122721\n',
                          '1\t92515681\t92515682\trs17371561\n',
                          '1\t92580419\t92580420\trs17380378\n'])
        self.assertEqual(list(prs_obj.rng('rs00000',
                                          'rs480000')),
                         ['1\t86876786\t86876787\trs479341\n'])
        self.assertEqual(list(prs_obj.rng('rs4000000',
                                          'rs11900000')),
                         ['1\t154527612\t154527613\trs4131514\n',
                          '1\t24977084\t24977085\trs10903122\n',
                          '1\t237115473\t237115474\trs10925318\n',
                          '1\t92516860\t92516861\trs11581176\n',
                          '1\t92516860\t92516861\trs11581176\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n'])
        self.assertEqual(list(prs_obj.rng('rs17380000',
                                          'rs99999999')),
                         ['1\t92580419\t92580420\trs17380378\n'])
        self.assertRaises(QueryStartGtEndError,
                          lambda query_start, query_end:
                          list(prs_obj.rng(query_start,
                                           query_end)),
                          'rs11900000',
                          'rs4000000')
        os.remove(self.src_file_path)
        os.remove(self.db_zst_path)
        os.remove(adb_path)

    def test_coords(self):
        adb_path = os.path.join(os.getcwd(),
                                'bed.bed.coords.adb')
        with open(self.src_file_path, 'w') as src_file_opened:
            for src_line in self.src_bed:
                src_file_opened.write(src_line)
        if os.path.exists(self.db_zst_path):
            os.remove(self.db_zst_path)
        if os.path.exists(adb_path):
            os.remove(adb_path)

        def get_coords(src_bed_line: str):
            src_bed_row = src_bed_line.rstrip().split('\t')
            coords = [f'chr{src_bed_row[0]}',
                      int(src_bed_row[1]),
                      int(src_bed_row[2])]
            return coords

        idx_obj = Idx(db_file_path=self.src_file_path,
                      idx_prefix='coords',
                      your_line_prs=get_coords,
                      presrt_chunk_elems_quan=8,
                      idx_chunk_elems_quan=8,
                      srt_rule=lambda val: val)
        idx_obj.idx()
        with ZipFile(adb_path) as adb_opened_r:
            with ZstdFile(adb_opened_r.open("['chr1', 24977084, 24977085].idx")) as fir_idx_opened:
                fir_idx = load(fir_idx_opened)
                self.assertEqual(fir_idx[0],
                                 ['chr1', 24977084, 24977085])
                self.assertEqual(fir_idx[1],
                                 ['chr1', 66265029, 66265030])
                self.assertEqual(fir_idx[2],
                                 ['chr1', 86876786, 86876787])
                self.assertEqual(fir_idx[3],
                                 ['chr1', 86877126, 86877127])
                self.assertEqual(fir_idx[4],
                                 ['chr1', 92515681, 92515682])
                self.assertEqual(fir_idx[5],
                                 ['chr1', 92516860, 92516861])
                self.assertEqual(fir_idx[6],
                                 ['chr1', 92516860, 92516861])
                self.assertEqual(fir_idx[7],
                                 ['chr1', 92543755, 92543756])
                self.assertEqual(len(fir_idx),
                                 8)
            with ZstdFile(adb_opened_r.open("['chr1', 92543755, 92543756].idx")) as sec_idx_opened:
                sec_idx = load(sec_idx_opened)
                self.assertEqual(sec_idx[0],
                                 ['chr1', 92543755, 92543756])
                self.assertEqual(sec_idx[1],
                                 ['chr1', 92543755, 92543756])
                self.assertEqual(sec_idx[2],
                                 ['chr1', 92580419, 92580420])
                self.assertEqual(sec_idx[3],
                                 ['chr1', 116545156, 116545157])
                self.assertEqual(sec_idx[4],
                                 ['chr1', 154527612, 154527613])
                self.assertEqual(sec_idx[5],
                                 ['chr1', 201015351, 201015352])
                self.assertEqual(sec_idx[6],
                                 ['chr1', 237115473, 237115474])
                self.assertEqual(sec_idx[7],
                                 ['chr1', 241782991, 241782992])
                self.assertEqual(len(sec_idx),
                                 8)
        prs_obj = Prs(db_file_path=self.src_file_path,
                      idx_prefix='coords',
                      srt_rule=lambda val: val)
        self.assertEqual(list(prs_obj.eq(['chr1', 24977084, 24977085])),
                         ['1\t24977084\t24977085\trs10903122\n'])
        self.assertEqual(list(prs_obj.eq(['chr1', 92543755, 92543756])),
                         ['1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n'])
        self.assertEqual(list(prs_obj.eq(['chr1', 237115473, 237115474],
                                         ['chr1', 241782991, 241782992])),
                         ['1\t237115473\t237115474\trs10925318\n',
                          '1\t241782991\t241782992\trs952084\n'])
        self.assertEqual(list(prs_obj.rng(['chr1', 92516000, 92516001],
                                          ['chr1', 92543800, 92543801])),
                         ['1\t92516860\t92516861\trs11581176\n',
                          '1\t92516860\t92516861\trs11581176\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n',
                          '1\t92543755\t92543756\trs11804321\n'])
        os.remove(self.src_file_path)
        os.remove(self.db_zst_path)
        os.remove(adb_path)


class SrtRulesTests(unittest.TestCase):
    srt_rules = SrtRules()

    def test_get_cols_srt_rule(self):
        self.assertEqual(self.srt_rules.cols_delimiter,
                         '\t')
        self.assertIsNone(self.srt_rules.col_inds)
        self.assertEqual(self.srt_rules.get_cols('abc\tdef'),
                         ['abc', 'def'])
        self.assertEqual(self.srt_rules.get_cols('123\t456'),
                         ['123', '456'])
        self.srt_rules.cols_delimiter = ','
        self.assertEqual(self.srt_rules.get_cols('chr10\t1\t100\tA\tC,CC'),
                         ['chr10\t1\t100\tA\tC', 'CC'])
        self.srt_rules.cols_delimiter = None
        self.assertEqual(self.srt_rules.get_cols('chr20\t2\t200\tA\tC,CC'),
                         ['chr20\t2\t200\tA\tC,CC'])
        self.srt_rules.cols_delimiter = '\t'
        self.assertEqual(self.srt_rules.get_cols('chr30\t3\t300\tA\tC,CC'),
                         ['chr30', '3', '300', 'A', 'C,CC'])
        self.srt_rules.col_inds = [0, -1]
        self.assertEqual(self.srt_rules.get_cols('chr40\t4\t400\tA\tC,CC'),
                         ['chr40', 'C,CC'])
        self.srt_rules.col_inds = None

    def test_natur_srt_rule(self):
        self.assertEqual(self.srt_rules.cols_delimiter,
                         '\t')
        self.assertIsNone(self.srt_rules.col_inds)
        self.assertEqual(self.srt_rules.natur('10'),
                         [[10]])
        self.assertEqual(self.srt_rules.natur('01'),
                         [[1]])
        self.assertEqual(self.srt_rules.natur('rs10'),
                         [[float('+inf'), 'rs', 10]])
        self.assertEqual(self.srt_rules.natur('rs01'),
                         [[float('+inf'), 'rs', 1]])
        self.assertEqual(self.srt_rules.natur('val1.5'),
                         [[float('+inf'), 'val', 1.5]])
        self.assertEqual(self.srt_rules.natur('val1.05'),
                         [[float('+inf'), 'val', 1.05]])
        self.assertEqual(self.srt_rules.natur('val1.05suff'),
                         [[float('+inf'), 'val', 1.05, 'suff']])
        self.assertEqual(self.srt_rules.natur('val1,05'),
                         [[float('+inf'), 'val', 1, ',', 5]])
        self.assertEqual(self.srt_rules.natur('val1,05suff'),
                         [[float('+inf'), 'val', 1, ',', 5, 'suff']])
        self.assertEqual(self.srt_rules.natur('I2a2a1b2a2a2-ZS20'),
                         [[float('+inf'), 'I', 2, 'a', 2, 'a',
                           1, 'b', 2, 'a', 2, 'a', 2, '-ZS', 20]])
        self.assertEqual(self.srt_rules.natur('10\t11'),
                         [[10], [11]])
        self.assertEqual(self.srt_rules.natur('rs10\t11'),
                         [[float('+inf'), 'rs', 10], [11]])
        self.srt_rules.cols_delimiter = ','
        self.assertEqual(self.srt_rules.natur('10,11.1'),
                         [[10], [11.1]])
        self.srt_rules.col_inds = None
        self.assertEqual(self.srt_rules.natur('10.1,11'),
                         [[10.1], [11]])
        self.srt_rules.col_inds = 1
        self.assertEqual(self.srt_rules.natur('10,11.1'),
                         [[11.1]])
        self.srt_rules.col_inds = [1, 0]
        self.assertEqual(self.srt_rules.natur('10.1,11'),
                         [[11], [10.1]])
        self.srt_rules.cols_delimiter = '\t'
        self.srt_rules.col_inds = [0]
        self.assertEqual(self.srt_rules.natur('10,11.1'),
                         [[10, ',', 11.1]])
        self.srt_rules.col_inds = None
        self.assertEqual(self.srt_rules.natur('10.1,11',
                                              dec_delimiter=','),
                         [[10, '.', 1.11]])
        self.assertEqual(self.srt_rules.natur('+'),
                         [[float('+inf'), '+']])
        self.assertEqual(self.srt_rules.natur('-'),
                         [[float('+inf'), '-']])
        self.assertEqual(self.srt_rules.natur('1+1'),
                         [[1, '+', 1]])
        self.assertEqual(self.srt_rules.natur('-1-1'),
                         [[-1, -1]])
        self.assertEqual(self.srt_rules.natur('+001-001'),
                         [[float('+inf'), '+', 1, -1]])
        self.assertEqual(self.srt_rules.natur('-1.23e'),
                         [[-1.23, 'e']])
        self.assertEqual(self.srt_rules.natur('123E-3'),
                         [[0.123]])
        self.assertEqual(self.srt_rules.natur('123e-02'),
                         [[1.23]])
        self.assertEqual(self.srt_rules.natur('pref1.23e2suff'),
                         [[float('+inf'), 'pref', 123.0, 'suff']])
        self.assertEqual(self.srt_rules.natur('e1.23e-1e'),
                         [[float('+inf'), 'e', 0.123, 'e']])
        self.assertEqual(self.srt_rules.natur('-E1.23E+01-E'),
                         [[float('+inf'), '-E', 12.3, '-E']])
        self.assertEqual(self.srt_rules.natur('-e-1.23e-1-e'),
                         [[float('+inf'), '-e', -0.123, '-e']])
        self.assertEqual(self.srt_rules.natur('+1230E-1+1'),
                         [[float('+inf'), '+', 123.0, '+', 1]])
        self.assertEqual(self.srt_rules.natur('0.123ee+2'),
                         [[0.123, 'ee+', 2]])
        self.assertEqual(self.srt_rules.natur('-12.3+EE-02'),
                         [[-12.3, '+EE', -2]])
        self.assertEqual(self.srt_rules.natur('-0e10'),
                         [[0]])
        self.assertEqual(self.srt_rules.natur('qwerty\t0.1E2'),
                         [[float('+inf'), 'qwerty'], [10.0]])
        self.assertEqual(self.srt_rules.natur('0,1e+2\tqwerty',
                                              dec_delimiter=','),
                         [[10.0], [float('+inf'), 'qwerty']])
        self.srt_rules.cols_delimiter = ', '
        self.assertEqual(self.srt_rules.natur('1,1, -2,2, str',
                                              dec_delimiter=',',
                                              nums_first=False),
                         [[1.1], [-2.2], [float('-inf'), 'str']])
        self.srt_rules.cols_delimiter = ','
        self.assertRaises(DelimitersMatchError,
                          self.srt_rules.natur,
                          '111,111',
                          dec_delimiter=',')
        self.srt_rules.cols_delimiter = '\t'
        self.srt_rules.col_inds = None

    def test_letts_nums_srt_rule(self):
        self.assertEqual(self.srt_rules.cols_delimiter,
                         '\t')
        self.assertIsNone(self.srt_rules.col_inds)
        self.assertEqual(self.srt_rules.letts_nums('rs1'),
                         [['rs', 1]])
        self.assertEqual(self.srt_rules.letts_nums('rs010'),
                         [['rs', 10]])
        self.srt_rules.col_inds = 0
        self.assertEqual(self.srt_rules.letts_nums('ENSG000\trs000'),
                         [['ENSG', 0]])
        self.srt_rules.col_inds = [1, 0]
        self.assertEqual(self.srt_rules.letts_nums('ENSG000\trs000'),
                         [['rs', 0], ['ENSG', 0]])
        self.srt_rules.col_inds = None
        self.assertRaises(AttributeError,
                          self.srt_rules.letts_nums,
                          'rs')
        self.assertRaises(AttributeError,
                          self.srt_rules.letts_nums,
                          '1dvatri')
        self.assertRaises(AttributeError,
                          self.srt_rules.letts_nums,
                          '123')
        self.assertRaises(AttributeError,
                          self.srt_rules.letts_nums,
                          'id1.1')
        self.assertRaises(AttributeError,
                          self.srt_rules.letts_nums,
                          'id-1')


if __name__ == "__main__":
    unittest.main()
