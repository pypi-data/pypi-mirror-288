# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_cogvideox']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.2.0,<3.0.0',
 'zhipuai>=2.1.4.20230731,<3.0.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-cogvideox',
    'version': '0.1.3',
    'description': 'A nonebot plugin for cogvideox',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-chatgpt-turbo\n</div>\n\n# 介绍\n- 本插件适配智谱清言的cogvideox视频生成模型API，具有文字生成视频和图文生成视频的功能。\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_cogvideox.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot_plugin_cogvideox.git"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-cogvideox.git\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\nzhipu_key = ""  # （必填）智谱清言清影API KEY\n```\n[API KEY获取地址](https://open.bigmodel.cn/usercenter/apikeys)\n# 效果\n![](demo1.jpg)\n![](demo2.jpg)\n\n# 使用方法\n\n- AI视频 文字提示词(图片)\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@alpaca.kim',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
