# yutto 贡献快速指南

很高兴你对参与 yutto 的贡献感兴趣，在提交你的贡献之前，请花一点点时间阅读本指南

## 开发工具链

为了获得最佳的开发体验，希望你能够安装一些开发工具

这些工具都是可选的，都有一定的替代方案，不过可能会稍微麻烦些……

### 依赖管理工具 poetry

[poetry](https://github.com/python-poetry/poetry) 是 yutto 用来进行依赖管理的工具，通过 pip 就可以很方便地安装它：

```bash
pip install poetry
```

> 替代方案（非常不建议）：自行使用 pip 安装依赖，依赖项在 pyproject.toml 中可以找到。

### 命令执行工具 just

[just](https://github.com/casey/just) 是一款用 rust 编写的简单易用的命令执行工具，通过它可以方便地执行一些开发时常用的命令。安装方法请参考[它的文档](https://github.com/casey/just#installation)

> 替代方案（不方便安装或者 Windows 上无法运行这些命令时建议使用）：自行查看 justfile 中对应的详细命令。

### 编辑器 Visual Studio Code

[VSCode](https://github.com/microsoft/vscode) 是一款功能强大的编辑器，由于 yutto 全面使用了 [Type Hints](https://docs.python.org/3/library/typing.html)，所以这里建议使用 VSCode + 扩展 pylance 来保证类型提示的准确性，同时配置格式化工具 black 以保证代码格式的一致性。

当然，如果你有更熟悉的编辑器或 IDE 的话，也是完全可以的。

## 本地调试

如果你想要本地调试，最佳实践是从 github 上下载最新的源码来运行

```bash
git clone git@github.com:SigureMo/yutto.git
cd yutto/
poetry install
poetry run yutto -v
```

注意本地调试请不要直接使用 `yutto` 命令，那只会运行从 pip 安装的 yutto，而不是本地调试的 yutto。

另外请注意如果你确定想为 yutto 做贡献请 fork 之后 clone 自己的 repo 再修改，以便发起 PR。

## 架构设计

这部分内容带你了解下 yutto 的主要模块结构与工作流程。

> 本部分内容可能略有滞后，这里列出的是 2022-02-11 时 [0fd5e0820e5c476ae696bf95db0ccc9ff205b5f7](https://github.com/SigureMo/yutto/tree/0fd5e0820e5c476ae696bf95db0ccc9ff205b5f7) 的模块结构，

### 模块结构

```text
.
├── Dockerfile                         # 一个轻量的 yutto docker
├── justfile                           # just 命令启动文件
├── pyproject.toml                     # poetry 依赖清单
├── tests                              # 测试文件
│   ├── __init__.py
│   ├── test_api                       # API 测试模块，对应 yutto/api
│   ├── test_downloader.py             # downloader 测试模块，对应 yutto/
│   └── test_e2e.py                    # 端到端测试
└── yutto
    ├── __init__.py
    ├── __main__.py                    # 命令行入口，含所有命令选项
    ├── __version__.py
    ├── _typing.py                     # yutto 的主要类型声明（非全部，部分类型是定义在自己模块之内的）
    ├── api                            # bilibili API 的基本函数封装，输入输出转换为 yutto 的主要类型
    │   ├── __init__.py
    │   ├── acg_video.py               # 投稿视频相关
    │   ├── bangumi.py                 # 番剧相关
    │   ├── danmaku.py                 # 弹幕相关（xml、protobuf）
    │   ├── info.py                    # 基本信息相关
    │   └── space.py                   # 个人空间相关（收藏夹、合集、列表）
    ├── bilibili_typing                # bilibili 自己的一些数据类型绑定
    │   ├── __init__.py
    │   ├── codec.py                   # bilibili 的 codec
    │   └── quality.py                 # bilibili 的 qn
    ├── exceptions.py                  # yutto 异常声明模块
    ├── extractor                      # 页面提取器（每种入口 url 对应一个 extractor）
    │   ├── __init__.py
    │   ├── _abc.py                    # 基本抽象类
    │   ├── acg_video.py               # 投稿视频单集
    │   ├── acg_video_batch.py         # 投稿视频批量
    │   ├── bangumi.py                 # 番剧单话
    │   ├── bangumi_batch.py           # 番剧全集
    │   ├── common.py                  # 低阶提取器（投稿视频、番剧），每种视频类型对应一个低阶提取器
    │   ├── favourites.py              # 收藏夹
    │   ├── favourites_all.py          # 全部收藏夹
    │   ├── series.py                  # 合集、视频列表
    │   └── uploader_all_videos.py     # 个人空间全部
    ├── processor                      # 一些在提取/下载过程中用到的基本处理方法（该部分很可能进一步重构）
    │   ├── __init__.py
    │   ├── downloader.py              # 下载器
    │   ├── filter.py                  # 选集、内容过滤器（本部分可修改成支持交互的）
    │   ├── parser.py                  # 文件解析器（解析任务列表、alias 文件）
    │   ├── path_resolver.py           # 路径处理器（需处理路径变量）
    │   └── progressbar.py             # 进度条（本部分可替换成为其他行为以支持更丰富的进度显示方式）
    ├── utils                          # yutto 无关或弱相关模块，不应依赖 yutto 强相关模块（api、extrator、processor），含部分类型资源的基本封装（弹幕、字幕、描述文件）
    │   ├── __init__.py
    │   ├── asynclib.py                # 封装部分异步相关方法
    │   ├── console                    # 命令行打印相关
    │   │   ├── __init__.py
    │   │   ├── attributes.py
    │   │   ├── colorful.py
    │   │   ├── formatter.py
    │   │   ├── logger.py              # 其中的 Logger 是 yutto 主要的打印方式，yutto 中只应使用这一种打印方式
    │   │   └── status_bar.py          # 底部状态栏（主要用于显示进度条）
    │   ├── danmaku.py                 # 「资源文件」弹幕基本封装
    │   ├── fetcher.py                 # 基本抓取器
    │   ├── ffmpeg.py                  # FFmpeg 驱动单例模块
    │   ├── file_buffer.py             # 文件缓冲器（yutto 下载原理的核心）
    │   ├── functools                  # yutto 需要用的一些实用基本函数（很多是直接参考 StackOverflow 的）
    │   ├── metadata.py                # 「资源文件」描述文件基本封装
    │   ├── priority.py                # 资源优先级判定（用于 codec、quality 判定）
    │   ├── subtitle.py                # 「资源文件」字幕基本封装
    │   └── time.py                    # 时间基本模块
    └── validator.py                   # 命令参数验证器（内含初期全局状态的设置）
```

### 工作流程

切入代码的最好方式自然是从入口开始啦～ yutto 的命令行入口是 [yutto/\_\_main\_\_.py](./yutto/__main__.py)，这里列出了 yutto 整个的工作流程：

1. 解析参数并利用 [yutto/validator.py](./yutto/validator.py) 验证参数的正确性，虽然 argparse 已经做了基本的验证，但 validator 会进一步的验证。另外目前 validator 还会顺带做全局状态的设置的工作，这部分以后可能修改。
2. 利用 [yutto/processor/parser.py](./yutto/processor/parser.py) 解析 alias 和任务列表
3. 遍历任务列表下载：
   1. 初始化提取器 [yutto/extrator/](./yutto/extractor/)
   2. 利用所有提取器处理 id 为可识别的 url
   3. 重定向一下入口 url 到可识别的 url
   4. 从入口 url 提取 `EpisodeData` 列表
      1. 如果是单话下载（继承 `yutto.extrator._abc.SingleExtrator`）
         1. 解析有用信息以提供给路径变量
         2. 使用 `yutto.extrator.common` 里的低阶提取器直接提取
      2. 如果是批量下载（继承 `yutto.extrator._abc.BatchExtrator`）
         1. 循环解析列表
         2. 展平列表
         3. 选集（如果支持的话）
         4. 根据列表构造协程任务（任务包含了解析信息和利用低阶提取器提取）
         5. 并行执行解析任务
         6. 任务重排序
   5. 将 `EpisodeData` 列表依次传入 [yutto/utils/downloader.py](yutto/utils/../processor/downloader.py) 进行下载
      1. 选择清晰度
      2. 显示详细信息
      3. 字幕、弹幕、描述文件等额外资源下载
      4. 下载音频、视频
      5. 合并音频、视频

## 改动

嗯，你现在已经基本了解 yutto 的结构了，可以尝试去修改部分源码了。

## 测试

yutto 已经编写好了一些测试，请确保在改动后仍能通过测试

```bash
just test
```

当然，如果你修改的内容需要对测试用例进行修改和增加，请尽管修改。

## 代码格式化

yutto 使用 black 对代码进行格式化，如果你的编辑器或 IDE 没有自动使用 black 进行格式化，请使用下面的命令对代码进行格式化

```bash
just fmt
```

## 提交 PR

提交 PR 的最佳实践是 fork 一个新的 repo 到你的账户下，并创建一个新的分支，在该分支下进行改动后提交到 GitHub 上，并发起 PR（请注意在发起 PR 时不要取消掉默认已经勾选的 `Allow edits from maintainers` 选项）

```bash
# 首先在 GitHub 上 fork
git clone git@github.com:<YOUR_USER_NAME>/yutto.git         # 将你的 repo clone 到本地
cd yutto/                                                   # cd 到该目录
git remote add upstream git@github.com:SigureMo/yutto.git   # 将原分支绑定在 upstream
git checkout -b <NEW_BRANCH>                                # 新建一个分支，名称随意，最好含有你本次改动的语义
git push origin <NEW_BRANCH>                                # 将该分支推送到 origin （也就是你 fork 后的 repo）
# 对源码进行修改、并通过测试
# 此时可以在 GitHub 发起 PR
```

如果你的贡献需要继续修改，直接继续向该分支提交新的 commit 即可，并推送到 GitHub，PR 也会随之更新

如果你的 PR 已经被合并，就可以放心地删除这个分支了

```bash
git checkout main                                           # 切换到 main
git fetch upstream                                          # 将原作者分支下载到本地
git merge upstream/main                                     # 将原作者 main 分支最新内容合并到本地 main
git branch -d <NEW_BRANCH>                                  # 删除本地分支
git push origin --delete <NEW_BRANCH>                       # 同时删除远程分支
```

## PR 规范

### 标题

表明你所作的更改即可，没有太过苛刻的格式（合并时会重命名）

如果可能，可以按照 `<gitmoji> <type>: <subject>` 来进行命名

这里的 `<type>` 采取和 vite 一样的可选值

> Vite Git Commit Message Convention 参考：<https://github.com/vitejs/vite/blob/main/.github/commit-convention.md>
>
> Gitmoji 参考：<https://gitmoji.dev/>

### 内容

尽可能按照模板书写

## 版本发布

> 本章节内容仅针对有发布权限的维护者

### 更新版本号

现阶段书写版本号的代码包括以下几个文件，发布版本前需要全部更改：

-  [Dockerfile](./Dockerfile)
-  [pyproject.toml](./pyproject.toml)
-  [yutto/\_\_version\_\_.py](./yutto/__version__.py)

### 发布到 PyPI

```bash
just publish
```

### 构建镜像并到 DockerHub

⚠️ 必须在发布到 PyPI 之后

> 需预先自行安装 [Docker](https://docs.docker.com/get-docker/) 并安装 [buildx 插件](https://docs.docker.com/buildx/working-with-buildx/) （我这里貌似不需要手动安装插件就有了……）

```bash
just publish-docker
```

### 发布到 Homebrew Tap

⚠️ 必须在发布到 PyPI 之后

修改 <https://github.com/SigureMo/homebrew-tap/blob/main/Formula/yutto.rb>，按照提示构建新版本 Formula。

**因为有你，yutto 才会更加完善，感谢你的贡献 (・ω< )★**
