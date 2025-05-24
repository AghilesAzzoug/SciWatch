<p align="center">
    <img src="docs/_static/logo.png?raw=true" width="400" title="SciWatch">
</p>

<p align="center">
  <!-- Unit Tests -->
  <a href="https://github.com/AghilesAzzoug/SciWatch/actions/workflows/github-ci.yaml">
    <img src="https://github.com/AghilesAzzoug/SciWatch/actions/workflows/github-ci.yaml/badge.svg" alt="tests">
  </a>
  <!-- Documentation -->
  <a href="https://aghilesazzoug.github.io/SciWatch/">
    <img src="https://img.shields.io/website?label=docs&style=flat-square&url=https%3A%2F%2Faghilesazzoug.github.io%2FSciWatch%2F" alt="docs">
  </a>
  <!-- License -->
  <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/github/license/AghilesAzzoug/SciWatch" alt="mit_license">
  </a>
</p>

**SciWatch** is a Python package designed to facilitate scientific monitoring
for data scientists and AI researchers (mainly). It serves as a useful tool for staying up-to-date
with the latest developments in the ever-evolving world of science and technology.
By effortlessly retrieving relevant scientific papers and technical blogs,
**SciWatch** empowers researchers to keep their knowledge current and expand their
horizons in their respective fields.

# Usage

1. Setup senders

See [senders](https://aghilesazzoug.github.io/SciWatch/senders.html) documentation for details

Example for with Gmail, setup the following env variables:

```sh
export GMAIL_SENDER=test@gmail.com
export GMAIL_TOKEN=your_token
```

2. Write a config (`scrapping_config.toml`)

```toml 
title = "LLM & AL Watch" # Will be used as email title

end_date = "now" # will search content up to now (exec. time)
time_delta = "02:00:00:00" # will look for content up to two days ago

recipients = ["aghiles.ahmed.azzoug@gmail.com"]

# define your queries
[[query]]
title = "LLM" # LLM query
raw_content = """intitle:(GPT* OR LLM* OR prompt* OR "Large language models"~2) AND incontent:(survey OR review OR evaluation* OR benchmark* OR optimization*)"""

[[query]]
title = "AL" # Active Learning on VRD (or benchmarks/surveys)
raw_content = """intitle:("active learning") AND incontent:(VRD OR documents OR survey* OR benchmark*)"""

# define your sources
[[source]]
type = "arxiv" # check for Computer Science papers on Arxiv
use_abstract_as_content = true
search_topic = "cs"
max_documents = 200

[[source]]
type = "openai_blog" # check for latest blogs on OpenAI blog (mainly for GPT updates)
max_documents = 20

[[source]]
type = "reddit"
sub_reddits = ["ChatGPTJailbreak", "PromptEngineering"]
min_submission_score = 2
max_documents_per_sub_reddit = 10
```

3. Run the watcher

```python
from sci_watch.sci_watcher import SciWatcher

watcher = SciWatcher.from_toml("scrapping_config.toml")

watcher.exec()  # if some relevant content is retrieved, recipients will receive an Email
```

You might get an email like this:
<p align="center">
    <img src="docs/_static/email_sample.png?raw=true" width="800" title="email sample">
</p>

# Documentation

For full documentation, including grammar syntax, check
the [docs](https://aghilesazzoug.github.io/SciWatch/).

# Contributing

Contribution are welcome by finding issues or by pull requests. For major changes, please open an issue first to
discuss/explain what you would like to change.

1. Fork the project
2. Create your feature branch following the convention feature/feature-name (`git checkout -b feature/feature-name`)
3. **Run pre-commit** (`make pre-commit`)
4. Commit your changes (`git commit -m "a meaningful message please"`)
5. Push to the branch (`git push origin feature/feature-name`)
6. Open a Pull Request

# Roadmap

- [x] (feat) Add GPT support for papers summarization
- [ ] (feat) Add better error handling (while scrapping, calling OpenAI API, etc.)
- [ ] (refactor) Refactor configuration file parsing (and a lot of other things)
- [ ] (perf) Add [short-circuit evaluation](https://en.wikipedia.org/wiki/Short-circuit_evaluation) for queries
- [ ] (perf) Run sources only once for all queries
- [ ] (perf) Process queries asynchronously

Feel free to post an issue or send an email if you have any idea :)

# License

Copyright 2024 Aghiles Azzoug

SciWatch is free and open-source software distributed under the terms of the [**MIT**](LICENSE) license.

# Contact

Aghiles Azzoug - [LinkedIn](https://www.linkedin.com/in/aghiles-azzoug/) - aghiles.ahmed.azzoug@gmail.com