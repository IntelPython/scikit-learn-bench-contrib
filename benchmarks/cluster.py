import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster.k_means_ import _k_init
from sklearn.utils.extmath import row_norms

from .common import Benchmark
from .datasets import _china_dataset, _20newsgroups_highdim_dataset


class KMeans_bench(Benchmark):
    """
    Benchmarks for KMeans.
    """
    # params = (representation, algorithm)
    param_names = ['params'] + Benchmark.param_names
    params = ([('dense', 'full'),
               ('dense', 'elkan'),
               ('sparse', 'full')],) + Benchmark.params

    def setup(self, params, *common):
        representation = params[0]
        algo = params[1]

        n_jobs = common[0]

        if representation is 'sparse':
            self.X, _ = _20newsgroups_highdim_dataset()
            self.n_clusters = 20
        else:
            self.X = _china_dataset()
            self.n_clusters = 64

        self.x_squared_norms = row_norms(self.X, squared=True)

        self.kmeans_params = {'n_clusters': self.n_clusters,
                              'algorithm': algo,
                              'n_init': 1,
                              'n_jobs': n_jobs,
                              'random_state': 0}

    def time_iterations(self, *args):
        kmeans = KMeans(init='random', max_iter=10, tol=0,
                        **self.kmeans_params)
        kmeans.fit(self.X)

    def peakmem_iterations(self, *args):
        kmeans = KMeans(init='random', max_iter=10, tol=0,
                        **self.kmeans_params)
        kmeans.fit(self.X)

    def track_iterations(self, *args):
        kmeans = KMeans(init='random', max_iter=10, tol=0,
                        **self.kmeans_params)
        kmeans.fit(self.X)
        return kmeans.n_iter_

    def time_convergence(self, *args):
        kmeans = KMeans(**self.kmeans_params)
        kmeans.fit(self.X)

    def peakmem_convergence(self, *args):
        kmeans = KMeans(**self.kmeans_params)
        kmeans.fit(self.X)

    def track_convergence(self, *args):
        kmeans = KMeans(**self.kmeans_params)
        kmeans.fit(self.X)
        return kmeans.n_iter_


class KMeansPlusPlus_bench(Benchmark):
    """
    Benchmarks for k-means++ init.
    """
    param_names = []
    params = []

    def setup(self):
        self.X = _china_dataset()
        self.n_clusters = 64
        self.x_squared_norms = row_norms(self.X, squared=True)

    def time_kmeansplusplus(self):
        rng = np.random.RandomState(0)
        _k_init(self.X, self.n_clusters, self.x_squared_norms,
                random_state=rng)

    def peakmem_kmeansplusplus(self):
        rng = np.random.RandomState(0)
        _k_init(self.X, self.n_clusters, self.x_squared_norms,
                random_state=rng)
