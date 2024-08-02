import inspect

def whoami(msg="", verbose=True):
    fun_name = inspect.currentframe().f_back.f_code.co_name
    ret_val = f"[{fun_name}] -> {msg}"

    if verbose:
        print(ret_val)

    return ret_val

def whereami(msg="", verbose=True, obsolete_path = False, path_depth = 2):
    pf = inspect.currentframe().f_back
    file_n_path = pf.f_code.co_filename
    fun_name = pf.f_code.co_name
    lineno = pf.f_lineno
    
    dir_list = []

    fpath = file_n_path
    if (obsolete_path == False):
        dir_depth = file_n_path.split('/')
        
        try:
            for i in range(1, path_depth+1):
                dir_list.insert(0, dir_depth[-i])
        except IndexError as e:
            pass
        fpath = "/".join(dir_list)
        
    retval = f"[{fpath}:{lineno}]:{fun_name} -> {msg}"
    
    if verbose:
        print(retval)

    return retval

def whocalledme(verbose=True, obsolete_path = False, path_depth = 2):
    dir_list = []   
    pparent_frame = inspect.getouterframes(inspect.currentframe())[2]
    
    file_n_path = pparent_frame.filename
    fun_name = pparent_frame.function
    lineno = pparent_frame.lineno
    
    fpath = file_n_path
    if (obsolete_path == False):
        dir_depth = file_n_path.split('/')
        
        try:
            for i in range(1, path_depth+1):
                dir_list.insert(0, dir_depth[-i])
        except IndexError as e:
            pass
        fpath = "/".join(dir_list)

    retval = f"[{fpath}:{lineno}]:{fun_name} -> "
    if verbose:
        print(retval)

    return retval

def calledtree(tree_depth=3, verbose=True):
    data = inspect.stack()
    tree = ""
    
    frame_len = len(data)
    
    if (tree_depth >= frame_len):
        tree_depth = frame_len-1
    
    for (i, sf) in enumerate(data):
        if (i == 0):
            continue
        if (i > tree_depth):
            break
        tree = tree + f"#{tree_depth-i}[{data[i][1]}:{data[i][2]}]:{data[i][3]} <-- \n"

    if (verbose):
        print(tree)

    return tree

def whosdaddy(msg="", versbose=True):
    pparent_frame = inspect.getouterframes(inspect.currentframe())[2]
    fun_name = f"[{pparent_frame.function}] -> {msg}"
    
    if (versbose):
        print(fun_name)
        
    return fun_name

