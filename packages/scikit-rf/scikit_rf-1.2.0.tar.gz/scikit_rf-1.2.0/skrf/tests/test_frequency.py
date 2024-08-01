import os
import unittest

import numpy as np

import skrf as rf
from skrf.frequency import InvalidFrequencyWarning


class FrequencyTestCase(unittest.TestCase):
    """

    """
    def setUp(self):
        """
        """
        self.test_dir = os.path.dirname(os.path.abspath(__file__))+'/'

    def test_create_linear_sweep(self):
        freq = rf.Frequency(1,10,10,'ghz')
        self.assertTrue((freq.f == np.linspace(1,10,10)*1e9).all())
        self.assertTrue((freq.f_scaled ==np.linspace(1,10,10)).all())
        self.assertTrue(freq.sweep_type == 'lin')

    def test_create_log_sweep(self):
        freq = rf.Frequency(1,10,10,'ghz', sweep_type='log')
        #Check end points
        self.assertTrue(freq.f[0] == 1e9)
        self.assertTrue(freq.f[-1] == 10e9)
        spacing = [freq.f[i+1]/freq.f[i] for i in range(len(freq.f)-1)]
        #Check that frequency is increasing
        self.assertTrue(all(s > 1 for s in spacing))
        #Check that ratio of adjacent frequency points is identical
        self.assertTrue(all(abs(spacing[i] - spacing[0]) < 1e-10 for i in range(len(spacing))))
        self.assertTrue(freq.sweep_type == 'log')

    def test_create_rando_sweep(self):
        f = np.array([1,5,200])
        freq = rf.Frequency.from_f(f,unit='khz')
        self.assertTrue((freq.f ==f*1e3).all())
        self.assertTrue((freq.f_scaled== f).all())

        # TODO : in next release
        # with self.assertRaises(AttributeError):
        #     # number of point is a property and can't be set
        #     freq.npoints = 10

    def test_rando_sweep_from_touchstone(self):
        """
        this also tests the ability to read a touchstone file.
        """
        rando_sweep_ntwk = rf.Network(os.path.join(self.test_dir, 'ntwk_arbitrary_frequency.s2p'))
        self.assertTrue((rando_sweep_ntwk.f == \
            np.array([1,4,10,20])).all())

    def test_slicer(self):
        a = rf.Frequency.from_f([1,2,4,5,6], unit='GHz')

        b = a['2-5ghz']
        tinyfloat = 1e-12
        self.assertTrue((abs(b.f - [2e9,4e9,5e9]) < tinyfloat).all())

    def test_frequency_check(self):
        with self.assertWarns(InvalidFrequencyWarning):
            freq = rf.Frequency.from_f([2,1], unit='Hz')

        with self.assertWarns(InvalidFrequencyWarning):
            freq = rf.Frequency.from_f([1,2,2], unit='Hz')

        with self.assertWarns(InvalidFrequencyWarning):
            freq = rf.Frequency.from_f([1,2,2], unit='Hz')
            inv = freq.drop_non_monotonic_increasing()
            self.assertListEqual(inv, [2])
            self.assertTrue(np.allclose(freq.f, [1,2]))

    def test_immutability(self):
        """
        To avoid corner cases, it is not be possible to change the
        frequency points directly.
        """
        a = rf.Frequency.from_f([1,2,4,5,6], unit='Hz')
        with self.assertRaises(AttributeError):
            a.f = [1, 2]
        with self.assertRaises(AttributeError):
            a.npoints = 10
        with self. assertRaises(AttributeError):
            a.start = 2
        with self. assertRaises(AttributeError):
            a.stop = 10

suite = unittest.TestLoader().loadTestsFromTestCase(FrequencyTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
