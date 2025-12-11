
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, List, Union
import yaml
import configparser
import datetime as dt
import pandas as pd


def get_project_root() -> Optional[Path]:

    """
    Return the absolute path to the project root directory by walking parents
    until a marker file/directory (e.g., ``pyproject.toml``) is found.
    """
    path = Path().absolute()
    markers = ['data', 'src', 'notebooks', '.git', 'configs', 'scripts']


    while path != path.parent:
            if any((path / marker).exists() for marker in markers):
                return path
            path = path.parent
    return None


def configs_from_yaml(dir: str = 'configs', filename: str = 'settings.yaml') -> Dict[str, Any]:
        root = get_project_root()
        if root is None:
            raise RuntimeError('Unable to determine project root directory.')
        return yaml_to_dict(root / dir / filename)


def yaml_to_dict(filepath: Union[str, Path]) -> Dict[str, Any]:
        """
        Reads a YAML file and returns data in form of dictionary.
        """
        try:
            with open(filepath, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print('config file: {filepath} not found!')
            return {}
        

def load_credentials(credentials_json: Dict[str, str]) -> Dict[str, Dict[str, Dict[str, str]]]:
        creds = credentials_json
        result = {}

        for key, path in creds.items():

            path = os.path.expanduser(path)

            credential_files = [f for f in os.listdir(path) if f.startswith('credentials')]
            
            for file in credential_files:
                parser = configparser.ConfigParser()
                file_path = f'{path}/{file}'

                try:
                    parser.read(file_path)

                    if not parser.sections():
                         raise ValueError(f"No sections found in credential file: {file_path}")

                    section_data = {section: dict(parser[section]) for section in parser.sections()}

                    if key=='other':
                        file_key = file.split('_')[1]

                    else:
                        file_key = key

                    result[file_key] = section_data

                except FileNotFoundError:
                    raise FileNotFoundError(f"Credential file for {key} not found at: {path}")
                
                except Exception as e:
                    raise ValueError(f"Error parsing credentials for {key} from {path}: {e}")

        return result



 
def set_env_from_creds(
    target: Optional[Union[str, List[str]]] = None, verbose: bool = False,
    ) -> None:

    # Need to add special handling for LangFuse
    
    if target == None:
        print(f'no environ credentials set')
        target_list=[]

    elif target == ['all'] or target == 'all':
        target_list = ['all']
    elif isinstance(target, str):
        target_list = [target]
    else:
        target_list = list(target)

    target_list = [t.lower() for t in target_list]
    process_all = 'all' in target_list

    configs = configs_from_yaml()
    credentials = load_credentials(configs.get('credentials', {}))

    skipped = []

    for k, v in credentials.items():
        service = k.lower()

        if not process_all and service not in target_list:
            for section in v.keys():
                skipped.append(f'{k}[{section}]')
            continue

        for k2, v2 in v.items():
            if service == 'kaggle' and k2 == 'default': # handle kaggle format
                username = v2.get('username')
                key = v2.get('key')

                if isinstance(username, str):
                    os.environ['KAGGLE_USERNAME'] = username
                    print('set environment variable for default: KAGGLE_USERNAME')

                if isinstance(key, str):
                    os.environ['KAGGLE_KEY'] = key
                    print('set environment variable for default: KAGGLE_KEY')

                if not isinstance(username, str) and not isinstance(key, str):
                    skipped.append(f'{k}[{k2}]')

            elif service not in ['aws'] and k2 == 'default' and isinstance(v2.get('api_key'), str):
                os.environ[f'{k.upper()}_API_KEY'] = v2.get('api_key')
                print(f'set environment variable for default: {k.upper()}_API_KEY')

            else:
                skipped.append(f'{k}[{k2}]')

    if verbose:
        print('skipping:')
        print(skipped)



class Timer:
    """
    Convenience timer methods.
    Instantiate with:
       timer=Timer()
         .start(message='')
         .elapsed(message='', periodicity='s')
         .end(periodicity='s')
    """
    
    def __init__(self) -> None:
        self.start_time: Optional[dt.datetime] = None
        self.timestamp: Optional[dt.datetime] = None
        self.end_time: Optional[dt.datetime] = None

    @staticmethod
    def format_time(time_obj: dt.datetime) -> str:
        return time_obj.strftime('%Y-%m-%d %H:%M:%S')


    def start(self, message: str = '') -> None:
        """Start the timer."""
        self.start_time = dt.datetime.now()
        self.timestamp = self.start_time
        print(f'Start time: {self.format_time(self.start_time)}')
        if message:
            print(f'{message}\n')


    def elapsed(self, message: str = '', periodicity: str = 's') -> None:
        """Print the elapsed time since the last timestamp."""
        if self.timestamp is None:
            print("Timer hasn't been started yet. Use `start()` first.")
            return

        new_timestamp = dt.datetime.now()
        if message:
            print(message)

        if periodicity.lower() in ['m', 'min', 'mins', 'minutes', 'minute']:
            elapsed_minutes = (new_timestamp - self.timestamp).total_seconds() / 60
            print(f'Elapsed time: {elapsed_minutes:.1f} mins since last timestamp at {new_timestamp}\n')
        else:
            elapsed_seconds = (new_timestamp - self.timestamp).total_seconds()
            print(f'Elapsed time: {elapsed_seconds:.0f} seconds since last timestamp at {new_timestamp}\n')

        self.timestamp = new_timestamp

    def end(self, periodicity: str = 's') -> None:
        """End the timer and print total elapsed time."""
        if self.start_time is None:
            print("Timer hasn't been started yet. Use `start()` first.")
            return

        else:
            self.end_time = dt.datetime.now()
            print(f'\nEnd time: {self.format_time(self.end_time)}')

            total_elapsed = (self.end_time - self.start_time).total_seconds()
            since_last_timestamp = (self.end_time - self.timestamp).total_seconds()

            if periodicity.lower() in ['m', 'min', 'mins', 'minutes', 'minute']:
                print(f'Wall time: {total_elapsed / 60:.1f} minutes '
                    f'({since_last_timestamp / 60:.1f} mins since last timestamp)\n')
            else:
                print(f'Wall time: {total_elapsed:.0f} seconds '
                    f'({since_last_timestamp:.0f} seconds since last timestamp)\n')

    @staticmethod            
    def get_timestamp(timestamp_format: str = 'YYYY-MM-DD_HHMMSS') -> str:
        """
        Returns a conveniently formated timestamp for use in filenames, logs etc
        """
        if timestamp_format == 'YYYY-MM-DD_HHMMSS':
            return dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        
        else:
            try:
                return dt.datetime.now().strftime(str(timestamp_format))
            
            except:
                return dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            

def pd_format(maxRows=50, maxCols=20, maxColWidth=50, displayWidth=250):
    """
    Convenience function for setting dataframe defaults
    """

    pd.set_option('display.max_rows', maxRows) #pd.get_option("display.max_rows")
    pd.set_option('display.max_columns', maxCols)
    pd.set_option('display.max_colwidth', maxColWidth)
    pd.set_option('display.width', displayWidth)
