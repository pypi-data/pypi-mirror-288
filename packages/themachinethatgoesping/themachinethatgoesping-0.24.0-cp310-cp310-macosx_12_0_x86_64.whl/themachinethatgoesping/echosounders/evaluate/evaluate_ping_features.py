import themachinethatgoesping as Ping
from tqdm.auto import tqdm

# evaluate if all specified features can be called without crashing
# also evaluate that all possible features exist (even if the function may throw an exception)
def __eval_all_features_can_be_called__(feature_group, name, verbose):
    for f in feature_group.possible_features():
        if feature_group.has_feature(f):
            get_feature = f'feature_group.get_{f.name}()'
            if verbose: print('[success]      ', get_feature.replace("feature_group", name))
            try:
                eval(get_feature)
            except Exception as e:
                raise RuntimeError(f'Error: {get_feature.replace("feature_group", name)} failed with error: {e}')
        else:
            get_feature = f'feature_group.get_{f.name}()'
            if verbose: print('[not available]', get_feature.replace("feature_group", name))
            if not hasattr(feature_group,f'get_{f.name}'):
                raise RuntimeError(f'Error: {get_feature.replace("feature_group", name)} function does not exist!')
            
    for f in feature_group.possible_feature_groups():
        if feature_group.has_feature(f):
            if verbose: print()
            __eval_all_features_can_be_called__(eval(f'feature_group.{f.name}'), f'{name}.{f.name}', verbose)
        else:
            if verbose: print()
            get_feature = f'feature_group.{f.name}'
            if verbose: print('[not available]', get_feature.replace("feature_group", name))
            
            try:
                has_attr = hasattr(feature_group,f'{f.name}')
            except:
                has_attr = True # hasattr returns false if the attribute does not exist, but it sometimes throw san exceptions for attributes that to exist

            if not has_attr:
                raise RuntimeError(f'Error: {get_feature.replace("feature_group", name)} function does not exist!')

def evaluate_ping_features_can_be_called(ping, verbose=False):
    if not isinstance(ping, Ping.echosounders.filetemplates.I_Ping):
        if hasattr(ping, '__iter__') or hasattr(ping, '__getitem__'):
            items = tqdm(ping, desc='Evaluating pings', unit='ping', leave=True) if verbose else ping
            for item in items:
                evaluate_ping_features_can_be_called(item, verbose=False) # don't be verbose in individual pings when handling lists
        else:
            raise ValueError('ping must be a single I_Ping object or a list of I_Ping objects')            
    else:
        # here pings is a single ping
        __eval_all_features_can_be_called__(ping, name='ping', verbose=verbose)
