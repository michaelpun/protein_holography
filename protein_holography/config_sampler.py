import yaml
import os
import datetime
import getpass
import itertools
from argparse import ArgumentParser
import numpy as np

class Config:
    def __parse_args(self):
        parser = ArgumentParser()
        parser.add_argument('parameters', metavar='param', type=str, nargs='*',
                            help='parameters')
        parser.add_argument('limits', metavar='lim', type=str, nargs='*',
                            help='parameters')
        parser.add_argument('--config', dest='name', type=str, help='config name')
        ns = parser.parse_args()
        self.__runtime_name = ns.name
        self.__parameters = ns.parameters
    
    def __init__(self):
        self.__parse_args()
        with open('config/static.yaml') as f_config_static:
            with open('config/runtime/{runtime_name}.yaml'.format(runtime_name = self.__runtime_name)) as f_config_runtime:
                self.config_static = yaml.load(f_config_static, Loader=yaml.FullLoader)
                self.config_runtime = yaml.load(f_config_runtime, Loader=yaml.FullLoader)
                print(self.config_runtime)
                self.config_runtime['date'] = datetime.date.today()
                self.config_runtime['config'] = self.__runtime_name

                if 'chdir' not in self.config_runtime:
                    self.config_runtime['chdir'] = os.path.dirname(os.path.realpath(__file__))

                if 'user' not in self.config_runtime:
                    self.config_runtime['user'] = getpass.getuser()

    def sample_parameters(self):
        n = self.config_runtime['n']
        for k,v in self.config_runtime['parameters'].items():
            self.config_runtime['parameters'][k] = v*n
        for k,v in self.config_runtime['limits'].items():
            mode = v[2]
            high = v[1]
            low = v[0]

            
            print('Sampling',k,v,n)

            # uniform sampling
            if mode == 0:
                self.config_runtime['parameters'][k] = np.random.uniform(low=low,high=high,size=n)
            # log-uniform sampling
            if mode == 1:
                self.config_runtime['parameters'][k] = np.power(10,np.random.uniform(low=low,high=high,size=n))
            #uniform discrete
            if mode == 2:
               self.config_runtime['parameters'][k] = np.random.randint(low=low,high=high+1,size=n)

    def generate_sbatch_scripts(self):
        self.sample_parameters()
        parameters = self.config_runtime['parameters']
        for el in zip(* parameters.values()):
            cr = self.config_runtime.copy() # shallow copy
            i = 0
            for k in parameters.keys():
                cr[k] = el[i]
                i = i + 1
            cr['jobname'] = cr['jobname'].format(** cr)
            yield cr['jobname'], '\n'.join([
                self.config_static.get('sbatch').format(** cr),
                self.config_runtime.get('command').format(** cr)])

    def get(self, name):
        return self.config_runtime[name]
    
def test():
    config = Config()
    
    for s in config.generate_sbatch_scripts():
        pass

    print(config.get('datadir'))
            
if __name__ == "__main__":
    test()
