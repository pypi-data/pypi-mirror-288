import os
import pynibs
import numpy as np
import unittest
import yaml
from inspect import getmembers, isfunction, getfullargspec

import pynibs


class TestRegressData(unittest.TestCase):
    """
    Test pynibs.regress_data()
    """
    np.random.seed(1)

    n_elm_small = 10
    # n_elm_large = 100000
    n_mep_small = 10
    # n_mep_large = 100
    n_signed = 25  # because function run_select_signed_data needs > 20 data points

    e_small = np.zeros((n_mep_small, n_elm_small))
    e_small[:] = 1
    e_small *= np.linspace(0.1, 5, n_mep_small)[:, np.newaxis]
    e_small *= np.linspace(0.1, 5, n_elm_small)

    e_signed = np.zeros((n_signed, n_signed))
    e_signed[:] = 1
    e_signed[0] = -1
    e_signed *= np.linspace(0.1, 5, n_signed)[:, np.newaxis]
    e_signed *= np.linspace(0.1, 5, n_signed)

    mep_small = np.linspace(0.1, 5, n_mep_small)

    mep_signed = np.linspace(0.1, 5, n_signed)

    con_small = np.array([[i, i + 1, i + 2] for i in range(n_elm_small)])

    def test_raise_assert_if_no_con(self):
        """
        When refit_discontinuities=True, con cannot be None
        """
        with self.assertRaises(AssertionError):
            pynibs.regress_data(self.e_small, self.mep_small)

    def test_all_default(self):
        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)

    def test_return_fits(self):
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       return_fits=True)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)
        assert len(fits) == self.n_elm_small
        assert type(fits[0]) == dict
        for k in ['x0', 'r', 'amp', 'y0']:
            assert k in fits[0]

    def test_elm_idx_list(self):
        elm_idx_list = list(range(0, int(self.n_elm_small / 2)))
        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                 elm_idx_list=elm_idx_list)
        assert r2.max() > .9
        assert r2.shape == (len(elm_idx_list),)

    def test_zap_idx(self):
        zap_idx = range(int(self.n_mep_small / 2), self.n_mep_small)
        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                 zap_idx=zap_idx)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)

    def test_element_list_linear(self):
        """
        Gives regress_data() an element_list AND fun=linear
        """
        element_list = [pynibs.Element(x=self.e_small[:, ele_id],
                                       y=self.mep_small,
                                       ele_id=ele_id,
                                       fun=pynibs.expio.fit_funs.linear,
                                       score_type="R2",
                                       select_signed_data=False,
                                       constants=None) for ele_id in range(self.n_elm_small)]
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       element_list=element_list, return_fits=True)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)
        # let's check if really linear fits have been used
        assert 'm' in fits[0]
        assert 'n' in fits[0]

    def test_refit_discontinuities(self):
        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=True, n_cpu=1,
                                 con=self.con_small)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)

    def test_n_refit(self):
        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                 n_refit=0)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)

    def test_workhorses(self):  # and verbose
        # Suppress output message in run_select_signed_data()
        # suppress_text = io.StringIO()
        # sys.stdout = suppress_text

        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=4,
                                 n_refit=0, verbose=True)
        assert r2.max() > .9
        assert r2.shape == (self.n_elm_small,)

        # Enable output messages again
        # sys.stdout = sys.__stdout__

    def test_score_type(self):
        sr = pynibs.regress_data(self.e_small, self.mep_small, score_type='SR', refit_discontinuities=False, n_cpu=1,
                                 n_refit=0)
        assert sr.max() > .9
        assert sr.shape == (self.n_elm_small,)

        rho = pynibs.regress_data(self.e_small, self.mep_small, score_type='rho', refit_discontinuities=False, n_cpu=1,
                                  n_refit=0)
        assert rho.max() > .9
        assert rho.shape == (self.n_elm_small, 2)

        with self.assertRaises(NotImplementedError):
            pynibs.regress_data(self.e_small, self.mep_small, score_type='abc', refit_discontinuities=False, n_cpu=1,
                                n_refit=0)

    def test_select_signed_data(self):
        # Suppress output message in run_select_signed_data()
        # suppress_text = io.StringIO()
        # sys.stdout = suppress_text

        # Test with mostly positive data
        r2_pos = pynibs.regress_data(self.e_signed, self.mep_signed, select_signed_data=True,
                                     refit_discontinuities=False, n_refit=0)
        assert r2_pos.max() > 0.9
        assert r2_pos.shape == (self.n_signed,)

        # Test with mostly negative data
        r2_neg = pynibs.regress_data(-self.e_signed, self.mep_signed, select_signed_data=True,
                                     refit_discontinuities=False, n_refit=0)
        assert r2_neg.max() > 0.9
        assert r2_neg.shape == (self.n_signed,)

        # Enable output messages again
        # sys.stdout = sys.__stdout__

    # ***** Testing all regression functions: *****

    def test_dummy_fun(self):
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.dummy_fun, return_fits=True)
        assert r2.shape == (self.n_elm_small,)
        assert 'a' in fits[0]

    def test_sigmoid(self):
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.sigmoid, return_fits=True)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)
        assert 'x0' in fits[0]
        assert 'r' in fits[0]
        assert 'amp' in fits[0]

    def test_sigmoid_negative_values(self):
        r2 = pynibs.regress_data(-self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                 n_refit=0, fun=pynibs.expio.fit_funs.sigmoid)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)

    def test_sigmoid_log(self):
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.sigmoid_log, return_fits=True)
        assert r2.max() > 0.9
        assert r2.shape == (self.n_elm_small,)
        assert 'x0' in fits[0]
        assert 'r' in fits[0]
        assert 'amp' in fits[0]

    def test_sigmoid4_log(self):
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.sigmoid4_log, return_fits=True)
        assert r2.max() > 0.9
        assert r2.shape == (self.n_elm_small,)
        assert 'x0' in fits[0]
        assert 'r' in fits[0]
        assert 'amp' in fits[0]
        assert 'y0' in fits[0]

    def test_exp(self):
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.exp0, return_fits=True)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)
        assert 'x0' in fits[0]
        assert 'r' in fits[0]

    def test_raise_assert_if_false_fun(self):
        with self.assertRaises(NotImplementedError):
            pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                n_refit=0, fun=pynibs.expio.fit_funs.linear_log)

    # ***** Testing use of yaml-configuration files: *****

    def test_yaml_sigmoid4(self):
        yaml_config = os.path.join(pynibs.__datadir__, 'configuration_sigmoid4.yaml')
        with open(yaml_config, "r") as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        r2 = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                 n_refit=0, fun=pynibs.expio.fit_funs.sigmoid4, **config)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)

    def test_yaml_linear_MEP(self):
        yaml_config = os.path.join(pynibs.__datadir__, 'configuration_linear_MEP.yaml')
        with open(yaml_config, "r") as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.linear, return_fits=True, **config)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)
        assert 'm' in fits[0]
        assert 'n' in fits[0]

    def test_yaml_linear_RT(self):
        yaml_config = os.path.join(pynibs.__datadir__, 'configuration_linear_RT.yaml')
        with open(yaml_config, "r") as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.linear, return_fits=True, **config)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)
        assert 'm' in fits[0]
        assert 'n' in fits[0]

    def test_yaml_exp(self):
        yaml_config = os.path.join(pynibs.__datadir__, 'configuration_exp0.yaml')
        with open(yaml_config, "r") as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        r2, fits = pynibs.regress_data(self.e_small, self.mep_small, refit_discontinuities=False, n_cpu=1,
                                       n_refit=0, fun=pynibs.expio.fit_funs.exp0, return_fits=True, **config)
        assert r2.max() > 0.90
        assert r2.shape == (self.n_elm_small,)
        assert 'x0' in fits[0]
        assert 'r' in fits[0]


class TestSingleFit(unittest.TestCase):

    def setUp(self):
        self.x = x = np.array(range(1, 100))
        self.args = {'a': 1,
                     'x0': 0,
                     'r': .2,
                     'amp': 5,
                     'y0': 0,
                     'm': 5,
                     'n': 1}

    def test_single_fit(self):
        for fun_id, fun in getmembers(pynibs.expio.fit_funs):
            if isfunction(fun):
                if fun_id == 'dummy_fun':
                    continue

                fun_params = getfullargspec(fun)[0]
                print(f"Testing {fun_id} with: {fun_params}")
                fun_args = {k: self.args[k] for k in fun_params if k != 'x'}
                y = fun(self.x, **fun_args)

                fit = pynibs.single_fit(self.x, y, fun)
                for k in fun_params:
                    if k != 'x':
                        print(
                            f"\t{k}: org: {self.args[k]} | "
                            f"fit: {fit.params[k].value} | "
                            f"{np.isclose(self.args[k], fit.params[k].value, atol=.1)}")
                print(f"R2: {fit.rsquared}")


if __name__ == '__main__':
    unittest.main()
