import os
from pathlib import Path
import yaml

class ProjectConfigs:
    """
    Class containing methods relating to project configurations.  
    
    Instantiate with: \n
        project=ProjectConfigs() \n

          .root_dir() \n
          .configs_from_yaml() \n
          .print_global_configs() \n
          .yaml_to_dict(filename) \n
          .dict_to_yaml(data_dict, filename, append=False)
    """

    
    def root_dir(self):
        path = Path().absolute()
        markers = ['data', 'src', 'notebooks', '.git', 'configs', 'scripts']
        
        while path != path.parent:
            if any((path / marker).exists() for marker in markers):
                return path
            path = path.parent
        return None


    def configs_from_yaml(self):
        return self.yaml_to_dict(self.root_dir() / 'configs' / 'settings.yaml')


    def print_global_configs(self):
        project_dir = self.root_dir()
        global_configs = self.configs_from_yaml()
        for k,v in global_configs.items():
            print(f'{k} <- {v}')

            if isinstance(v, dict):
                for k2,v2 in v.items():
                    print(f'  {k2} <- {v2}')
                    if k2.endswith('_dir'):     
                        print(f'     contains:{[f for f in os.listdir(project_dir / v2) if not f.startswith(".")]}')

            print('\n')

    def yaml_to_dict(self,filename):
        """
        Reads a YAML file and returns data in form of dictionary.
        """
        try:
            with open(filename, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        
 
    def dict_to_yaml(self,data_dict, filename, append=False):
        """
        Takes a data_dict and writes data out to filename.yaml
        """

        with open(filename, 'a' if append else 'w') as f:

            if append:
                print(f'appending to {filename}...')
            else:
                print(f'writing to {filename}...')

            for k,v in data_dict.items():
                if isinstance(v, list):
                    f.write(f'{k}:\n')
                    for item in v:
                        f.write(f'  - {item}\n')
                    f.write('\n')
                
                if isinstance(v,dict):
                    f.write(f'{k}:\n')
                    for col,attrbutes in v.items():
                        f.write(f'  {col}: {attrbutes}\n')
                    f.write('\n')
