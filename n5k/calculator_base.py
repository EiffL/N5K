import numpy as np


class N5KCalculatorBase(object):
    name = 'Base'
    needed_fields = ['output_prefix']
    nb_g = 10
    nb_s = 5
    cosmo = {'OmegaM': 0.3156,
             'OmegaB': 0.0492,
             'w0': -1.0,
             'h': 0.6727,
             'A_s': 2.12107E-9,
             'n_s': 0.9645}

    def __init__(self, fname_config):
        import yaml

        with open(fname_config) as f:
            self.config = yaml.safe_load(f)

        self._check_config_sanity()

    def _check_config_sanity(self):
        for name in self.needed_fields:
            if not self.config.get(name):
                raise ValueError(f"You must provide {name}")

    def get_bias(self):
        b = np.array([1.376695,
                      1.451179,
                      1.528404,
                      1.607983,
                      1.689579,
                      1.772899,
                      1.857700,
                      1.943754,
                      2.030887,
                      2.118943])
        return b

    def get_A_IA(self):
        return 0.15
        
    def get_nz_g(self):
        d = np.loadtxt('input/dNdz_clust_LSSTSRD_zb0_sigz0.03.dat', unpack=True)
        return d[0], d[1:]

    def get_nz_s(self):
        d = np.loadtxt('input/dNdz_srcs_LSSTSRD_zb0_sigz0.05.dat', unpack=True)
        return d[0], d[1:]

    def get_ells(self):
        return np.unique(np.geomspace(2, 2000, 128).astype(int)).astype(float)

    def get_num_cls(self):
        ngg = (self.nb_g * (self.nb_g + 1)) // 2
        nss = (self.nb_s * (self.nb_s + 1)) // 2
        ngs = self.nb_g * self.nb_s
        return ngg, ngs, nss

    def write_output(self):
        ls = self.get_ells()
        nl = len(ls)
        ngg, ngs, nss = self.get_num_cls()
        print(self.cls_gg.shape)
        print(self.cls_gs.shape)
        print(self.cls_ss.shape)
        if self.cls_gg.shape != (ngg, nl):
            raise ValueError("Incorrect G-G spectra shape")
        if self.cls_gs.shape != (ngs, nl):
            raise ValueError("Incorrect G-S spectra shape")
        if self.cls_ss.shape != (nss, nl):
            raise ValueError("Incorrect S-S spectra shape")

        np.savez(self.config['output_prefix'] + '_clgg.npz',
                 ls=ls, cls=self.cls_gg)
        np.savez(self.config['output_prefix'] + '_clgs.npz',
                 ls=ls, cls=self.cls_gs)
        np.savez(self.config['output_prefix'] + '_clss.npz',
                 ls=ls, cls=self.cls_ss)

    def teardown(self):
        pass

    def setup(self):
        pass

    def run(self):
        nl = len(self.get_ells())
        ngg, ngs, nss = self.get_num_cls()
        self.cls_gg = np.zeros((ngg, nl))
        self.cls_gs = np.zeros((ngs, nl))
        self.cls_ss = np.zeros((nss, nl))