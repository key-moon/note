import readline
from typing import Callable, Dict, List

def option_getter(
    keys: List[str],
    default_vals: Dict[str, str],
    candidates: Dict[str, List[str]],
    candidates_fetcher: Dict[str, Callable[[Dict[str, str]], str]]
):
    try:
        cur_candidates = []
        def completer(text, state):
            options = [i for i in cur_candidates if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)
        opts = {}
        for key in keys:
            cur_candidates = []
            if key in candidates:
                cur_candidates = candidates[key]
            elif key in candidates_fetcher:
                cur_candidates = candidates_fetcher[key](opts)
            prompt = f'{key}?'
            
            if key in default_vals and 0 < len(default_vals[key]):
                prompt += f' default: {repr(default_vals[key])}'

            MAX_LEN = 80
            if len(cur_candidates) != 0 and MAX_LEN < len(prompt):
                show_cands = cur_candidates
                truncated = False
                while True:
                    s = f' cands: {(", ".join(map(repr, show_cands)))}'
                    if truncated: s += " ..."
                    if 80 <= len(prompt + s):
                        show_cands = show_cands[:-1]
                        truncated = True
                        continue
                    prompt += s
                    break
            print(prompt)
            opt = input("> ")

            if opt == "" and key in default_vals:
                opt = default_vals[key]
            
            opts[key] = opt
        return opts
    finally:
        readline.set_completer(None)
    