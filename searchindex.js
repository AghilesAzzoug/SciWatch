Search.setIndex({"docnames": ["debugging_queries", "grammar", "index", "installation", "query", "sci_watch", "sci_watch.core", "sci_watch.core.exceptions", "sci_watch.core.settings", "sci_watch.parser", "sci_watch.parser.query", "sci_watch.parser.query_evaluator", "sci_watch.parser.query_parser", "sci_watch.parser.tree_node", "sci_watch.sci_watcher", "sci_watch.senders", "sci_watch.senders.gmail_sender", "sci_watch.senders.local_dir_sender", "sci_watch.senders.slack_sender", "sci_watch.senders.teams_sender", "sci_watch.source_wrappers", "sci_watch.source_wrappers.abstract_wrapper", "sci_watch.source_wrappers.arxiv_wrapper", "sci_watch.source_wrappers.document", "sci_watch.source_wrappers.openai_wrapper", "sci_watch.source_wrappers.techcrunch_wrapper", "sci_watch.summarizers", "sci_watch.summarizers.openai_summarizers", "sci_watch.summarizers.summarizer", "sci_watch.utils", "sci_watch.utils.logger", "sci_watch.watcher", "sci_watch.watcher.watcher", "senders", "usage"], "filenames": ["debugging_queries.rst", "grammar.rst", "index.rst", "installation.rst", "query.rst", "sci_watch.rst", "sci_watch.core.rst", "sci_watch.core.exceptions.rst", "sci_watch.core.settings.rst", "sci_watch.parser.rst", "sci_watch.parser.query.rst", "sci_watch.parser.query_evaluator.rst", "sci_watch.parser.query_parser.rst", "sci_watch.parser.tree_node.rst", "sci_watch.sci_watcher.rst", "sci_watch.senders.rst", "sci_watch.senders.gmail_sender.rst", "sci_watch.senders.local_dir_sender.rst", "sci_watch.senders.slack_sender.rst", "sci_watch.senders.teams_sender.rst", "sci_watch.source_wrappers.rst", "sci_watch.source_wrappers.abstract_wrapper.rst", "sci_watch.source_wrappers.arxiv_wrapper.rst", "sci_watch.source_wrappers.document.rst", "sci_watch.source_wrappers.openai_wrapper.rst", "sci_watch.source_wrappers.techcrunch_wrapper.rst", "sci_watch.summarizers.rst", "sci_watch.summarizers.openai_summarizers.rst", "sci_watch.summarizers.summarizer.rst", "sci_watch.utils.rst", "sci_watch.utils.logger.rst", "sci_watch.watcher.rst", "sci_watch.watcher.watcher.rst", "senders.rst", "usage.rst"], "titles": ["Debugging queries", "Grammar", "Welcome to SciWatch\u2019s documentation!", "Installation", "Query syntax", "sci_watch package", "sci_watch.core package", "sci_watch.core.exceptions module", "sci_watch.core.settings module", "sci_watch.parser package", "sci_watch.parser.query module", "sci_watch.parser.query_evaluator module", "sci_watch.parser.query_parser module", "sci_watch.parser.tree_node module", "sci_watch.sci_watcher module", "sci_watch.senders package", "sci_watch.senders.gmail_sender module", "sci_watch.senders.local_dir_sender module", "sci_watch.senders.slack_sender module", "sci_watch.senders.teams_sender module", "sci_watch.source_wrappers package", "sci_watch.source_wrappers.abstract_wrapper module", "sci_watch.source_wrappers.arxiv_wrapper module", "sci_watch.source_wrappers.document module", "sci_watch.source_wrappers.openai_wrapper module", "sci_watch.source_wrappers.techcrunch_wrapper module", "sci_watch.summarizers package", "sci_watch.summarizers.openai_summarizers module", "sci_watch.summarizers.summarizer module", "sci_watch.utils package", "sci_watch.utils.logger module", "sci_watch.watcher package", "sci_watch.watcher.watcher module", "Senders", "Usage"], "terms": {"For": [0, 33, 34], "i": [0, 1, 4], "e": [0, 3, 4], "know": 0, "which": [0, 1], "part": 0, "match": [0, 2, 4, 10], "evalu": [0, 4, 10, 11, 34], "true": [0, 4, 10, 12, 22, 34], "versu": 0, "didn": 0, "t": [0, 33], "you": [0, 2, 33, 34], "can": [0, 1, 2, 4, 23, 33, 34], "us": [0, 1, 2, 13, 27, 30, 34], "script": 0, "01_visualize_query_evalu": 0, "py": 0, "follow": [0, 1, 4, 33], "python": [0, 2], "hello": [0, 4], "AND": [0, 1, 4, 11, 34], "world": [0, 2, 4], "OR": [0, 1, 4, 11, 34], "titl": [0, 4, 10, 23, 34], "content": [0, 4, 23, 27, 34], "print": [0, 13], "tree": [0, 11, 12, 13], "show": 0, "graph": 0, "get": [0, 34], "becaus": 0, "argument": 0, "your": [0, 34], "browser": 0, "veri": [0, 4], "long": 0, "might": [0, 34], "unread": 0, "prefer": 0, "option": [0, 8, 13, 16, 17, 18, 19, 30], "alon": 0, "also": 0, "termin": 0, "path": [0, 14, 17, 33], "file": [0, 2, 8, 14, 17, 30, 33], "contain": [0, 4], "The": [1, 10, 11, 30, 33], "pars": 1, "tool": [1, 2], "lark": [1, 12, 13], "we": [1, 34], "gener": 1, "lalr": 1, "1": 1, "parser": [1, 5], "found": [1, 4, 14], "sci_watch": [1, 34], "asset": 1, "queri": [1, 2, 5, 7, 9, 11, 12, 13, 14, 32, 34], "factor": 1, "and_claus": [1, 11, 12], "or_claus": [1, 11, 12], "NOT": [1, 4, 11], "not_claus": [1, 11, 12], "token": [1, 12, 33], "intitle_kw": 1, "colon": 1, "scoped_token": [1, 12], "in_title_claus": [1, 11, 12], "incontent_kw": 1, "in_content_claus": [1, 11, 12], "begin_kw": 1, "begin_claus": [1, 11, 12], "word_with_wildcard": [1, 11, 12], "expr": 1, "left_par": 1, "right_par": 1, "parenthesis_claus": [1, 11, 12], "scoped_queri": [1, 12], "quot": 1, "A": [1, 4, 14, 30], "za": 1, "z0": 1, "9": 1, "express": [1, 4, 11, 12], "tild": 1, "distanc": [1, 4, 12], "proxim": [1, 4, 11, 12], "0": 1, "space": [1, 4], "s": [1, 4], "intitl": [1, 4, 34], "incont": [1, 4, 34], "begin": [1, 4, 11], "ignor": 1, "entri": 1, "point": 1, "packag": 2, "design": 2, "facilit": 2, "scientif": 2, "monitor": [2, 32, 34], "data": 2, "scientist": 2, "ai": [2, 25], "research": 2, "mainli": [2, 34], "It": 2, "serv": 2, "stai": 2, "up": [2, 4, 34], "date": [2, 23], "latest": [2, 22, 24, 25, 34], "develop": 2, "ever": 2, "evolv": 2, "scienc": [2, 34], "technolog": 2, "By": 2, "effortlessli": 2, "retriev": [2, 16, 34], "relev": [2, 14, 19, 32, 34], "paper": [2, 22, 23, 28, 34], "technic": 2, "blog": [2, 23, 24, 25, 28, 34], "empow": 2, "keep": 2, "knowledg": 2, "current": [2, 4, 13, 27], "expand": 2, "horizon": 2, "respect": 2, "field": [2, 33], "come": 2, "equip": 2, "an": [2, 14, 30, 33, 34], "advanc": 2, "keyword": [2, 4, 10], "base": [2, 7, 8, 10, 11, 12, 13, 14, 21, 22, 23, 24, 25, 27, 28, 32], "languag": [2, 34], "specif": 2, "implement": [2, 4], "thi": [2, 4, 34], "user": 2, "now": [2, 34], "effici": 2, "search": [2, 12, 34], "criteria": 2, "whether": 2, "relat": 2, "cut": 2, "edg": 2, "machin": 2, "learn": [2, 34], "techniqu": 2, "deep": 2, "framework": 2, "natur": 2, "process": 2, "ani": [2, 30, 33], "other": 2, "interest": 2, "public": 2, "from": [2, 4, 8, 14, 32, 34], "arxiv": [2, 22, 34], "openai": [2, 24, 34], "techcrunch": 2, "instal": 2, "directli": 2, "github": 2, "local": 2, "repositori": 2, "onli": [2, 4, 27], "depend": 2, "usag": 2, "setup": 2, "sender": [2, 5], "creat": [2, 12, 14], "configur": [2, 33], "run": [2, 14], "watcher": [2, 5, 17], "syntax": [2, 34], "atom": 2, "logic": 2, "oper": 2, "scope": [2, 12], "wildcard": [2, 11], "prioriti": 2, "gmail": [2, 34], "microsoft": 2, "team": [2, 14, 19], "untest": 2, "yet": 2, "slack": [2, 18], "directori": [2, 17], "debug": [2, 8, 30, 33], "grammar": [2, 4], "index": 2, "modul": [2, 5, 6, 9, 15, 20, 26, 29, 31], "page": [2, 33], "pip": 3, "git": 3, "http": [3, 33], "com": [3, 33, 34], "aghilesazzoug": 3, "sciwatch": [3, 14, 34], "clone": 3, "cd": 3, "make": 3, "defin": [4, 34], "compon": 4, "more": [4, 33, 34], "detail": [4, 33], "see": [4, 33, 34], "repres": [4, 23], "basic": 4, "each": [4, 12, 16], "own": 4, "type": [4, 10, 13, 14, 16, 26, 27, 28, 30, 32, 33, 34], "descript": 4, "simpl": [4, 34], "word": [4, 11], "without": 4, "normal": 4, "special": 4, "charact": 4, "present": 4, "first": 4, "second": 4, "third": 4, "list": [4, 8, 13, 16, 17, 18, 19, 21, 27, 28, 32, 33], "separ": 4, "white": 4, "cannot": 4, "exact": 4, "g": 4, "2": [4, 34], "all": [4, 14, 32], "ar": [4, 7, 14, 30, 33], "same": 4, "order": [4, 30], "most": 4, "note": 4, "case": 4, "insensit": 4, "intend": 4, "left": 4, "right": 4, "both": 4, "condit": 4, "must": [4, 18, 33], "satisfi": 4, "At": 4, "least": 4, "one": [4, 16, 27, 28], "exclus": 4, "equival": 4, "boolean": 4, "To": [4, 33], "fals": [4, 8, 10], "subqueri": 4, "document": [4, 5, 10, 14, 16, 17, 18, 19, 20, 21, 22, 24, 25, 27, 28, 32, 33, 34], "global": 4, "default": [4, 11, 16, 17, 18, 19], "If": [4, 10, 33], "noth": 4, "specifi": 4, "anoth": 4, "soon": 4, "look": [4, 22, 24, 25, 33, 34], "two": [4, 34], "behavior": 4, "differ": 4, "regex": 4, "Will": [4, 34], "everyth": 4, "hell": 4, "would": 4, "helloo": 4, "hellfir": 4, "neither": 4, "highest": 4, "lower": 4, "parenthesi": [4, 11], "exampl": [4, 33, 34], "short": 4, "fake": 4, "core": 5, "except": [5, 6, 25, 30], "set": [5, 6, 18, 33], "query_evalu": [5, 9], "query_pars": [5, 9], "tree_nod": [5, 9], "gmail_send": [5, 8, 15, 33], "local_dir_send": [5, 15], "slack_send": [5, 15], "teams_send": [5, 15], "source_wrapp": [5, 16, 17, 18, 19, 27, 28, 32], "abstract_wrapp": [5, 20, 32], "arxiv_wrapp": [5, 20], "openai_wrapp": [5, 20], "techcrunch_wrapp": [5, 20], "summar": 5, "openai_summar": [5, 26], "util": 5, "logger": [5, 29], "querysyntaxerror": 7, "messag": [7, 14, 18, 19, 33], "str": [7, 8, 10, 11, 13, 16, 17, 18, 19, 22, 23, 25, 26, 27, 28, 30], "sourc": [7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 30, 32, 34], "rais": [7, 30], "when": 7, "syntact": 7, "wrong": 7, "class": [8, 10, 11, 12, 13, 14, 21, 22, 23, 24, 25, 27, 28, 32], "_env_fil": 8, "union": [8, 30], "pathlik": [8, 14, 30], "tupl": 8, "object": [8, 10, 11, 13, 14, 21, 23, 30, 32], "_env_file_encod": 8, "none": [8, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 24, 30], "_env_nested_delimit": 8, "_secrets_dir": 8, "log_level": 8, "liter": [8, 30], "notset": [8, 30], "info": [8, 30], "warn": [8, 30], "error": [8, 30], "fatal": [8, 30], "critic": [8, 30], "gmail_token": [8, 33], "grammar_path": 8, "http_proxi": 8, "https_proxi": 8, "log_file_path": [8, 30], "baseset": 8, "load": 8, "env": [8, 18, 33], "config": [8, 14, 33], "allow_mut": 8, "raw_cont": [10, 34], "eval_with_docu": 10, "bool": [10, 12, 22], "given": [10, 12, 19, 32], "return": [10, 13, 14, 27, 28, 30, 32], "otherwis": 10, "paramet": [10, 11, 12, 13, 14, 17, 18, 19, 27, 28, 30], "queryevalu": 11, "content_text": 11, "title_text": 11, "node": [11, 12, 13], "callback": 11, "method": [11, 12, 13], "claus": [11, 12], "eval_tre": 11, "place": [11, 12], "root": [11, 12], "in_cont": 11, "in_titl": 11, "createcustomtre": 12, "visit_token": 12, "transform": 12, "custom": [12, 13], "below": [12, 34], "call": 12, "correspond": 12, "valu": [12, 13], "int": [12, 13, 22, 24, 25], "update_search_scop": 12, "travers": 12, "updat": [12, 21, 22, 24, 25, 34], "start_po": 13, "end_po": 13, "children": 13, "search_scop": 13, "replac": 13, "pretti": 13, "_indent": 13, "indent": 13, "level": [13, 30], "raw": 13, "string": 13, "represent": 13, "dict": [14, 26], "exec": [14, 32, 34], "send": [14, 16, 18, 19, 33], "email": [14, 16, 33, 34], "classmethod": 14, "from_toml": [14, 34], "os": 14, "pathlib": 14, "scrapper": 14, "toml": [14, 34], "send_email": 16, "subject": 16, "recipi": [16, 33, 34], "doc": [16, 17, 19, 27, 28], "summari": [16, 17, 18, 19], "convert": 16, "html": [16, 17, 33], "them": 16, "thought": 16, "smtp": 16, "param": 16, "write_on_fil": 17, "output_dir": 17, "write": 17, "output": 17, "send_slack": 18, "channel_id": [18, 33], "through": [18, 33, 34], "slack_oauth_token": [18, 33], "channel": [18, 33], "name": [18, 30, 34], "send_team": 19, "webhook_url": [19, 33], "webhook": [19, 33], "group": 19, "url": [19, 23, 33], "sourcewrapp": [21, 22, 24, 25, 32], "abc": [21, 28], "abstract": [21, 28], "wrapper": [21, 22, 24, 27], "update_docu": [21, 22, 24, 25], "self": [21, 22, 24, 25], "arxivwrapp": 22, "search_top": [22, 25, 34], "max_docu": [22, 24, 25, 34], "start_dat": [22, 24, 25], "datetim": [22, 23, 24, 25], "end_dat": [22, 24, 25, 34], "use_abstract_as_cont": [22, 34], "between": [22, 24, 25], "end": [22, 24, 25], "from_queri": 23, "etc": 23, "openaiblogwrapp": 24, "post": [24, 25], "notablogpost": 25, "techcrunchwrapp": 25, "tech": 25, "crunch": 25, "get_summar": 26, "summarizer_kwarg": 26, "abstractsummar": [26, 27, 28], "gptsummar": 27, "kwarg": 27, "gpt": [27, 34], "model": [27, 34], "batch_summar": [27, 28], "get_logg": 30, "logger_nam": 30, "getter": 30, "function": [30, 33], "should": 30, "import": [30, 34], "minimum": 30, "log": 30, "readi": 30, "logging_wrapp": 30, "callabl": 30, "wrap": 30, "entir": 30, "try": 30, "block": [30, 33], "catch": 30, "propag": 30, "caller": 30, "decor": 30, "multipl": 32, "execut": 32, "avail": 33, "format": 33, "address": 33, "variabl": 33, "check": [33, 34], "support": 33, "googl": 33, "account": 33, "answer": 33, "185833": 33, "hl": 33, "en": 33, "enabl": 33, "simpli": 33, "add": 33, "scrap": 33, "alongsid": 33, "aghil": [33, 34], "ahm": [33, 34], "azzoug": [33, 34], "second_email": 33, "outlook": 33, "fr": 33, "access": 33, "ha": 33, "undergon": 33, "real": 33, "test": 33, "encount": 33, "issu": 33, "pleas": 33, "don": 33, "hesit": 33, "submit": 33, "pull": 33, "request": 33, "test_webhook": 33, "123xyz": 33, "although": 33, "mai": 33, "visual": 33, "appeal": 33, "activ": [33, 34], "along": 33, "addition": 33, "ensur": 33, "environ": 33, "bot": 33, "oauth": 33, "start": 33, "xoxb": 33, "api": 33, "authent": 33, "my": 33, "isn": 33, "exactli": 33, "Its": 33, "primari": 33, "maintain": 33, "purpos": 33, "In": 33, "local_dir": 33, "tmp": 33, "save": 33, "cwd": 33, "how": 34, "llm": 34, "augment": 34, "let": 34, "suppos": 34, "scrapping_config": 34, "al": 34, "watch": 34, "time": 34, "time_delta": 34, "02": 34, "00": 34, "dai": 34, "ago": 34, "prompt": 34, "larg": 34, "survei": 34, "review": 34, "benchmark": 34, "optim": 34, "vrd": 34, "comput": 34, "cs": 34, "200": 34, "openai_blog": 34, "20": 34, "inform": 34, "about": 34, "some": 34, "receiv": 34, "like": 34, "code": 34, "crontab": 34, "daili": 34, "weekli": 34}, "objects": {"": [[5, 0, 0, "-", "sci_watch"]], "sci_watch": [[6, 0, 0, "-", "core"], [9, 0, 0, "-", "parser"], [14, 0, 0, "-", "sci_watcher"], [15, 0, 0, "-", "senders"], [20, 0, 0, "-", "source_wrappers"], [26, 0, 0, "-", "summarizers"], [29, 0, 0, "-", "utils"], [31, 0, 0, "-", "watcher"]], "sci_watch.core": [[7, 0, 0, "-", "exceptions"], [8, 0, 0, "-", "settings"]], "sci_watch.core.exceptions": [[7, 1, 1, "", "QuerySyntaxError"]], "sci_watch.core.settings": [[8, 2, 1, "", "Settings"]], "sci_watch.core.settings.Settings": [[8, 2, 1, "", "Config"], [8, 3, 1, "", "gmail_sender"], [8, 3, 1, "", "gmail_token"], [8, 3, 1, "", "grammar_path"], [8, 3, 1, "", "http_proxy"], [8, 3, 1, "", "https_proxy"], [8, 3, 1, "", "log_file_path"], [8, 3, 1, "", "log_level"]], "sci_watch.core.settings.Settings.Config": [[8, 3, 1, "", "allow_mutation"]], "sci_watch.parser": [[10, 0, 0, "-", "query"], [11, 0, 0, "-", "query_evaluator"], [12, 0, 0, "-", "query_parser"], [13, 0, 0, "-", "tree_node"]], "sci_watch.parser.query": [[10, 2, 1, "", "Query"]], "sci_watch.parser.query.Query": [[10, 4, 1, "", "eval_with_document"]], "sci_watch.parser.query_evaluator": [[11, 2, 1, "", "QueryEvaluator"]], "sci_watch.parser.query_evaluator.QueryEvaluator": [[11, 4, 1, "", "and_clause"], [11, 4, 1, "", "begin_clause"], [11, 4, 1, "", "default"], [11, 4, 1, "", "eval_tree"], [11, 4, 1, "", "expression"], [11, 4, 1, "", "in_content_clause"], [11, 4, 1, "", "in_title_clause"], [11, 4, 1, "", "not_clause"], [11, 4, 1, "", "or_clause"], [11, 4, 1, "", "parenthesis_clause"], [11, 4, 1, "", "proximity"], [11, 4, 1, "", "word_with_wildcard"]], "sci_watch.parser.query_parser": [[12, 2, 1, "", "CreateCustomTree"], [12, 5, 1, "", "update_search_scope"]], "sci_watch.parser.query_parser.CreateCustomTree": [[12, 4, 1, "", "and_clause"], [12, 4, 1, "", "begin_clause"], [12, 4, 1, "", "distance"], [12, 4, 1, "", "expression"], [12, 4, 1, "", "in_content_clause"], [12, 4, 1, "", "in_title_clause"], [12, 4, 1, "", "not_clause"], [12, 4, 1, "", "or_clause"], [12, 4, 1, "", "parenthesis_clause"], [12, 4, 1, "", "proximity"], [12, 4, 1, "", "query"], [12, 4, 1, "", "scoped_query"], [12, 4, 1, "", "scoped_token"], [12, 4, 1, "", "token"], [12, 4, 1, "", "word_with_wildcard"]], "sci_watch.parser.tree_node": [[13, 2, 1, "", "Node"]], "sci_watch.parser.tree_node.Node": [[13, 4, 1, "", "pretty"]], "sci_watch.sci_watcher": [[14, 2, 1, "", "SciWatcher"]], "sci_watch.sci_watcher.SciWatcher": [[14, 4, 1, "", "exec"], [14, 4, 1, "", "from_toml"]], "sci_watch.senders": [[16, 0, 0, "-", "gmail_sender"], [17, 0, 0, "-", "local_dir_sender"], [18, 0, 0, "-", "slack_sender"], [19, 0, 0, "-", "teams_sender"]], "sci_watch.senders.gmail_sender": [[16, 5, 1, "", "send_email"]], "sci_watch.senders.local_dir_sender": [[17, 5, 1, "", "write_on_file"]], "sci_watch.senders.slack_sender": [[18, 5, 1, "", "send_slack"]], "sci_watch.senders.teams_sender": [[19, 5, 1, "", "send_teams"]], "sci_watch.source_wrappers": [[21, 0, 0, "-", "abstract_wrapper"], [22, 0, 0, "-", "arxiv_wrapper"], [23, 0, 0, "-", "document"], [24, 0, 0, "-", "openai_wrapper"], [25, 0, 0, "-", "techcrunch_wrapper"]], "sci_watch.source_wrappers.abstract_wrapper": [[21, 2, 1, "", "SourceWrapper"]], "sci_watch.source_wrappers.abstract_wrapper.SourceWrapper": [[21, 3, 1, "", "documents"], [21, 4, 1, "", "update_documents"]], "sci_watch.source_wrappers.arxiv_wrapper": [[22, 2, 1, "", "ArxivWrapper"]], "sci_watch.source_wrappers.arxiv_wrapper.ArxivWrapper": [[22, 4, 1, "", "update_documents"]], "sci_watch.source_wrappers.document": [[23, 2, 1, "", "Document"]], "sci_watch.source_wrappers.openai_wrapper": [[24, 2, 1, "", "OpenAIBlogWrapper"]], "sci_watch.source_wrappers.openai_wrapper.OpenAIBlogWrapper": [[24, 4, 1, "", "update_documents"]], "sci_watch.source_wrappers.techcrunch_wrapper": [[25, 1, 1, "", "NotABlogPost"], [25, 2, 1, "", "TechCrunchWrapper"]], "sci_watch.source_wrappers.techcrunch_wrapper.TechCrunchWrapper": [[25, 4, 1, "", "update_documents"]], "sci_watch.summarizers": [[26, 5, 1, "", "get_summarizer"], [27, 0, 0, "-", "openai_summarizers"], [28, 0, 0, "-", "summarizer"]], "sci_watch.summarizers.openai_summarizers": [[27, 2, 1, "", "GPTSummarizer"]], "sci_watch.summarizers.openai_summarizers.GPTSummarizer": [[27, 4, 1, "", "batch_summarize"], [27, 4, 1, "", "summarize"]], "sci_watch.summarizers.summarizer": [[28, 2, 1, "", "AbstractSummarizer"]], "sci_watch.summarizers.summarizer.AbstractSummarizer": [[28, 4, 1, "", "batch_summarize"], [28, 4, 1, "", "summarize"]], "sci_watch.utils": [[30, 0, 0, "-", "logger"]], "sci_watch.utils.logger": [[30, 5, 1, "", "get_logger"], [30, 5, 1, "", "logging_wrapper"]], "sci_watch.watcher": [[32, 0, 0, "-", "watcher"]], "sci_watch.watcher.watcher": [[32, 2, 1, "", "Watcher"]], "sci_watch.watcher.watcher.Watcher": [[32, 4, 1, "", "exec"]]}, "objtypes": {"0": "py:module", "1": "py:exception", "2": "py:class", "3": "py:attribute", "4": "py:method", "5": "py:function"}, "objnames": {"0": ["py", "module", "Python module"], "1": ["py", "exception", "Python exception"], "2": ["py", "class", "Python class"], "3": ["py", "attribute", "Python attribute"], "4": ["py", "method", "Python method"], "5": ["py", "function", "Python function"]}, "titleterms": {"debug": 0, "queri": [0, 4, 10], "grammar": 1, "welcom": 2, "sciwatch": 2, "s": 2, "document": [2, 23], "content": 2, "indic": 2, "tabl": 2, "instal": 3, "directli": 3, "from": 3, "github": 3, "local": [3, 33], "repositori": 3, "onli": 3, "depend": 3, "syntax": 4, "atom": 4, "logic": 4, "oper": 4, "search": 4, "scope": 4, "wildcard": 4, "prioriti": 4, "sci_watch": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], "packag": [5, 6, 9, 15, 20, 26, 29, 31], "subpackag": 5, "submodul": [5, 6, 9, 15, 20, 26, 29, 31], "core": [6, 7, 8], "except": 7, "modul": [7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25, 27, 28, 30, 32], "set": 8, "parser": [9, 10, 11, 12, 13], "query_evalu": 11, "query_pars": 12, "tree_nod": 13, "sender": [15, 16, 17, 18, 19, 33, 34], "gmail_send": 16, "local_dir_send": 17, "slack_send": 18, "teams_send": 19, "source_wrapp": [20, 21, 22, 23, 24, 25], "abstract_wrapp": 21, "arxiv_wrapp": 22, "openai_wrapp": 24, "techcrunch_wrapp": 25, "summar": [26, 27, 28], "openai_summar": 27, "util": [29, 30], "logger": 30, "watcher": [31, 32, 34], "gmail": 33, "microsoft": 33, "team": 33, "untest": 33, "yet": 33, "slack": 33, "directori": 33, "usag": 34, "setup": 34, "creat": 34, "configur": 34, "file": 34, "run": 34}, "envversion": {"sphinx.domains.c": 2, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 6, "sphinx.domains.index": 1, "sphinx.domains.javascript": 2, "sphinx.domains.math": 2, "sphinx.domains.python": 3, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.viewcode": 1, "sphinx": 56}})