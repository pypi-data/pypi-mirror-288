# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen', 'pipen.cli']

package_data = \
{'': ['*']}

install_requires = \
['argx>=0.2.10,<0.3.0',
 'enlighten>=1,<2',
 'liquidpy>=0.8.2,<0.9.0',
 'pandas>=2.0,<3.0',
 'pipda>=0.13,<0.14',
 'python-simpleconf[toml]>=0.6,<0.7',
 'rtoml>=0.8,<0.9',
 'varname>=0.13,<0.14',
 'xqute>=0.5.1,<0.6.0']

entry_points = \
{'console_scripts': ['pipen = pipen.cli:main']}

setup_kwargs = {
    'name': 'pipen',
    'version': '0.15.2',
    'description': 'A pipeline framework for python',
    'long_description': '<div align="center">\n    <img src="./pipen.png" width="320px">\n\n**A pipeline framework for python**\n\n</div>\n\n______________________________________________________________________\n\n[![Pypi][6]][7] [![Github][8]][9] ![Building][10] [![Docs and API][11]][1] [![Codacy][12]][13] [![Codacy coverage][14]][13] [![Deps][5]][23]\n\n[Documentation][1] | [ChangeLog][2] | [Examples][3] | [API][4]\n\n## Features\n\n- Easy to use\n- Nearly zero-configuration\n- Nice logging\n- Highly extendable\n\n## Installation\n\n```bash\npip install -U pipen\n```\n\n## Quickstart\n\n`example.py`\n\n```python\nfrom pipen import Proc, Pipen\n\nclass P1(Proc):\n    """Sort input file"""\n    input = "infile"\n    input_data = ["/tmp/data.txt"]\n    output = "outfile:file:intermediate.txt"\n    script = "cat {{in.infile}} | sort > {{out.outfile}}"\n\nclass P2(Proc):\n    """Paste line number"""\n    requires = P1\n    input = "infile"\n    output = "outfile:file:result.txt"\n    script = "paste <(seq 1 3) {{in.infile}} > {{out.outfile}}"\n\nclass MyPipeline(Pipen):\n    starts = P1\n\nif __name__ == "__main__":\n    MyPipeline().run()\n```\n\n```shell\n> echo -e "3\\n2\\n1" > /tmp/data.txt\n> python example.py\n```\n\n```log\n06-09 23:15:29 I core                  _____________________________________   __\n06-09 23:15:29 I core                  ___  __ \\___  _/__  __ \\__  ____/__  | / /\n06-09 23:15:29 I core                  __  /_/ /__  / __  /_/ /_  __/  __   |/ /\n06-09 23:15:29 I core                  _  ____/__/ /  _  ____/_  /___  _  /|  /\n06-09 23:15:29 I core                  /_/     /___/  /_/     /_____/  /_/ |_/\n06-09 23:15:29 I core\n06-09 23:15:29 I core                              version: 0.14.5\n06-09 23:15:29 I core\n06-09 23:15:29 I core    ╔═══════════════════════════════════════════════════╗\n06-09 23:15:29 I core    ║                            MYPIPELINE                            ║\n06-09 23:15:29 I core    ╚═══════════════════════════════════════════════════╝\n06-09 23:15:29 I core    plugins         : verbose v0.11.0\n06-09 23:15:29 I core    # procs         : 2\n06-09 23:15:29 I core    profile         : default\n06-09 23:15:29 I core    outdir          : /home/pwwang/github/pipen/MyPipeline-output\n06-09 23:15:29 I core    cache           : True\n06-09 23:15:29 I core    dirsig          : 1\n06-09 23:15:29 I core    error_strategy  : ignore\n06-09 23:15:29 I core    forks           : 1\n06-09 23:15:29 I core    lang            : bash\n06-09 23:15:29 I core    loglevel        : info\n06-09 23:15:29 I core    num_retries     : 3\n06-09 23:15:29 I core    scheduler       : local\n06-09 23:15:29 I core    submission_batch: 8\n06-09 23:15:29 I core    template        : liquid\n06-09 23:15:29 I core    workdir         : /home/pwwang/github/pipen/.pipen/MyPipeline\n06-09 23:15:29 I core    plugin_opts     :\n06-09 23:15:29 I core    template_opts   :\n06-09 23:15:31 I core\n06-09 23:15:31 I core    ╭──────────────────────── P1 ───────────────────────╮\n06-09 23:15:31 I core    │ Sort input file                                                  │\n06-09 23:15:31 I core    ╰──────────────────────────────────────────────────╯\n06-09 23:15:31 I core    P1: Workdir: \'/home/pwwang/github/pipen/.pipen/MyPipeline/P1\'\n06-09 23:15:31 I core    P1: <<< [START]\n06-09 23:15:31 I core    P1: >>> [\'P2\']\n06-09 23:15:31 I verbose P1: size: 1\n06-09 23:15:31 I verbose P1: [0/0] in.infile: /tmp/data.txt\n06-09 23:15:31 I verbose P1: [0/0] out.outfile:\n                 /home/pwwang/github/pipen/.pipen/MyPipeline/P1/0/output/intermediate.txt\n06-09 23:15:33 I verbose P1: Time elapsed: 00:00:02.018s\n06-09 23:15:33 I core\n06-09 23:15:33 I core    ╭════════════════════════ P2 ═══════════════════════╮\n06-09 23:15:33 I core    ║ Paste line number                                                ║\n06-09 23:15:33 I core    ╰══════════════════════════════════════════════════╯\n06-09 23:15:33 I core    P2: Workdir: \'/home/pwwang/github/pipen/.pipen/MyPipeline/P2\'\n06-09 23:15:33 I core    P2: <<< [\'P1\']\n06-09 23:15:33 I core    P2: >>> [END]\n06-09 23:15:33 I verbose P2: size: 1\n06-09 23:15:33 I verbose P2: [0/0] in.infile:\n                 /home/pwwang/github/pipen/.pipen/MyPipeline/P1/0/output/intermediate.txt\n06-09 23:15:33 I verbose P2: [0/0] out.outfile:\n                 /home/pwwang/github/pipen/MyPipeline-output/P2/result.txt\n06-09 23:15:35 I verbose P2: Time elapsed: 00:00:02.009s\n06-09 23:15:35 I core\n\n              MYPIPELINE: 100%|█████████████████████████████| 2/2 [00:06<00:00, 0.36 procs/s]\n```\n\n```shell\n> cat ./MyPipeline-output/P2/result.txt\n1       1\n2       2\n3       3\n```\n\n## Examples\n\nSee more examples at `examples/` and a more realcase example at:\nhttps://github.com/pwwang/pipen-report/tree/master/example\n\n## Plugin gallery\n\nPlugins make `pipen` even better.\n\n- [`pipen-annotate`][26]: Use docstring to annotate pipen processes\n- [`pipen-args`][19]: Command line argument parser for pipen\n- [`pipen-board`][27]: Visualize configuration and running of pipen pipelines on the web\n- [`pipen-diagram`][18]: Draw pipeline diagrams for pipen\n- [`pipen-dry`][20]: Dry runner for pipen pipelines\n- [`pipen-filters`][17]: Add a set of useful filters for pipen templates.\n- [`pipen-lock`][25]: Process lock for pipen to prevent multiple runs at the same time.\n- [`pipen-log2file`][28]: Save running logs to file for pipen\n- [`pipen-poplog`][30]: Populate logs from jobs to running log of the pipeline\n- [`pipen-report`][16]: Generate report for pipen\n- [`pipen-runinfo`][29]: Save running information to file for pipen\n- [`pipen-verbose`][15]: Add verbosal information in logs for pipen.\n- [`pipen-gcs`][32]: A plugin for pipen to handle files in Google Cloud Storage.\n- [`pipen-cli-init`][21]: A pipen CLI plugin to create a pipen project (pipeline)\n- [`pipen-cli-ref`][31]: Make reference documentation for processes\n- [`pipen-cli-require`][24]: A pipen cli plugin check the requirements of a pipeline\n- [`pipen-cli-run`][22]: A pipen cli plugin to run a process or a pipeline\n\n\n[1]: https://pwwang.github.io/pipen\n[2]: https://pwwang.github.io/pipen/CHANGELOG\n[3]: https://pwwang.github.io/pipen/examples\n[4]: https://pwwang.github.io/pipen/api/pipen\n[5]: https://img.shields.io/librariesio/release/pypi/pipen?style=flat-square\n[6]: https://img.shields.io/pypi/v/pipen?style=flat-square\n[7]: https://pypi.org/project/pipen/\n[8]: https://img.shields.io/github/v/tag/pwwang/pipen?style=flat-square\n[9]: https://github.com/pwwang/pipen\n[10]: https://img.shields.io/github/actions/workflow/status/pwwang/pipen/build.yml?style=flat-square\n[11]: https://img.shields.io/github/actions/workflow/status/pwwang/pipen/docs.yml?label=docs&style=flat-square\n[12]: https://img.shields.io/codacy/grade/cf1c6c97e5c4480386a05b42dec10c6e?style=flat-square\n[13]: https://app.codacy.com/gh/pwwang/pipen\n[14]: https://img.shields.io/codacy/coverage/cf1c6c97e5c4480386a05b42dec10c6e?style=flat-square\n[15]: https://github.com/pwwang/pipen-verbose\n[16]: https://github.com/pwwang/pipen-report\n[17]: https://github.com/pwwang/pipen-filters\n[18]: https://github.com/pwwang/pipen-diagram\n[19]: https://github.com/pwwang/pipen-args\n[20]: https://github.com/pwwang/pipen-dry\n[21]: https://github.com/pwwang/pipen-cli-init\n[22]: https://github.com/pwwang/pipen-cli-run\n[23]: https://libraries.io/github/pwwang/pipen#repository_dependencies\n[24]: https://github.com/pwwang/pipen-cli-require\n[25]: https://github.com/pwwang/pipen-lock\n[26]: https://github.com/pwwang/pipen-annotate\n[27]: https://github.com/pwwang/pipen-board\n[28]: https://github.com/pwwang/pipen-log2file\n[29]: https://github.com/pwwang/pipen-runinfo\n[30]: https://github.com/pwwang/pipen-poplog\n[31]: https://github.com/pwwang/pipen-cli-ref\n[32]: https://github.com/pwwang/pipen-gcs\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwwang/pipen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
