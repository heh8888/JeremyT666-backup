# GitHub 账号 JeremyT666 (Jeremy Ting) 仓库分析报告

> 分析日期：2026-11-21
> 账号主页：https://github.com/JeremyT666
> 公开仓库数：3 个（全部 Python 项目）

---

## 总览

| # | 仓库名 | 语言 | 最后更新 | 定位 |
|---|--------|------|----------|------|
| 1 | data_mapping | Python | 2022-05-05 | Excel 数据比对工具 |
| 2 | game-automation | Python | 2025-08~09 | 游戏客户端协议级自动化测试框架 |
| 3 | opennet-qa-test | Python | 2025-11-07 | Web UI 自动化测试（Page Object 模式） |

账号持有人为 QA/自动化测试工程师，技术栈纯 Python，涵盖协议级测试、Web UI 测试、数据比对三个方向。

---

## 1. data_mapping

- 仓库地址：https://github.com/JeremyT666/data_mapping
- 最后提交：2022-05-05（4 commits）
- 文件：`data_mapping.py`（单文件脚本）+ `example/` + `README.md`

### 功能

数据比对工具，用于对冲检测（Hedging Detection）场景。对比 `Old/` 和 `New/` 两个目录下的 Excel 文件，逐层比对差异：

1. **文件名比对** — 检查两个目录的文件列表是否一致
2. **Sheet 名比对** — 同名文件的 sheet 是否对齐
3. **单元格值比对** — 用 pandas + numpy 做逐格 diff，记录所有不一致的行号列号和前后值

### 技术实现

- 用 `os.listdir` 遍历目录，`sorted()` 排序后做交叉比对
- `cross_comparsion(source, target)` 函数返回两个列表的差集
- pandas 读取 xlsx，`to_numpy()` 转 ndarray 后用 `==` 矩阵比对
- `np.where(comparsion_values == False)` 定位差异单元格
- 特殊处理 `NaN == NaN` 为 False 的边界情况
- 结果写入两个日志文件：
  - `mapping_result.log`：差异记录
  - `success_mapping.log`：完全一致的文件

### 输出日志格式

```
# 差异日志示例
[Data Mapping Error]file.xlsx - sheet1 row:5 col:2 is different old_value ---> new_value - 2022/05/05 12:00:00

# 成功日志示例
subdir - file.xlsx >>> mapping is successful - 2022/05/05 12:00:00
```

### 依赖

- pandas
- numpy
- openpyxl（pandas 读 xlsx 隐式依赖）
- logging（标准库）

---

## 2. game-automation

- 仓库地址：https://github.com/JeremyT666/game-automation
- 最后提交：2025-08-26 ~ 2025-09-11（2 commits）
- 这是最完整、工作量最大的项目

### 定位

游戏客户端自动化测试框架，针对**百家乐（Baccarat）和龙虎（Dragon Tiger）**游戏的线上服务端协议测试。

### 技术栈

- 语言：Python 3.10+
- 测试框架：pytest
- 异步处理：asyncio
- WebSocket：websockets
- 配置管理：PyYAML
- 报告生成：pytest-html
- 日志管理：自定义 logger 模块
- 位运算：自定义 bitmap 解析工具

### 项目架构

```
game-automation/
├── src/
│   ├── conf/                       # 配置文件
│   ├── connection/
│   │   └── wss_handler.py          # WebSocket 连线与封包收发
│   ├── game/
│   │   ├── bet.py                  # 下注功能
│   │   ├── card_parser.py          # 扑克牌解析（bitmap → 牌面信息）
│   │   ├── game_result_parser.py   # 游戏结果解析（bitmap → 游戏状态）
│   │   ├── get_result.py           # 游戏结果接收处理
│   │   ├── odds_tables.py          # 赔率表配置
│   │   ├── playtype_enums.py       # 游戏玩法枚举定义
│   │   ├── settle.py               # 派彩相关协议处理
│   │   └── payout/
│   │       ├── payout_calculator.py  # 赔率计算逻辑
│   │       └── payout_verifier.py    # 赔率验证逻辑
│   ├── gateserver/
│   │   └── gateserver_handler.py   # GateServer 连线处理
│   ├── gameapi/
│   │   └── gameapi_handler.py      # GameAPI 连线处理
│   ├── heartbeat/
│   │   └── heartbeat.py            # 连线心跳包处理
│   ├── loginserver/
│   │   └── loginserver_handler.py  # 登入与取得 GateServer Token
│   ├── packet/
│   │   └── packet_handler.py       # 封包打包与解包
│   ├── protocols/
│   │   ├── generate_protocol_format.py  # 格式化协议字串
│   │   └── protocols.py            # 所有对接协议定义与格式
│   ├── user/
│   │   ├── balance.py              # 额度相关协议处理
│   │   └── enter_table.py          # 进桌功能
│   ├── utils/
│   │   ├── balance_checker.py      # 额度检查工具
│   │   ├── bitmap_mapping.py       # 位元运算工具
│   │   ├── config_loader.py        # 配置加载
│   │   ├── encryption.py           # 加密函数
│   │   ├── logger.py               # 日志模块
│   │   └── random_string.py        # 随机字串生成
│   └── main_test.py                # 模拟客户端测试程式
├── tests/
│   ├── conftest.py                 # pytest 配置和 fixtures
│   ├── test_login.py               # 登入测试
│   ├── test_enter_table.py         # 进桌测试
│   ├── bac/                        # 百家乐测试
│   │   ├── test_bac_balance_check.py
│   │   └── single_table/
│   │       ├── test_bac_betting.py
│   │       └── test_bac_odds.py
│   └── dtb/                        # 龙虎测试
│       ├── test_dtb_balance_check.py
│       └── single_table/
│           ├── test_dtb_betting.py
│           └── test_dtb_odds.py
├── test_data/
│   ├── config.yaml                 # 测试服务器配置
│   └── player_info/                # 各币别测试玩家配置
├── reports/
│   ├── report.html                 # HTML 测试报告
│   └── logs/
├── pytest.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

### 核心模块说明

| 模块 | 作用 |
|------|------|
| loginserver_handler | 登录服务器，获取 GateServer Token |
| gateserver_handler | 连接 GateServer，建立游戏会话 |
| wss_handler | WebSocket 封包收发，异步处理 |
| packet_handler | 协议封包打包与解包 |
| card_parser | 把服务端返回的 bitmap 位运算数据解析成扑克牌面 |
| game_result_parser | bitmap → 游戏状态（输赢、点数等） |
| payout_calculator | 根据赔率表计算派彩金额 |
| payout_verifier | 验证服务端实际派彩与预期是否一致 |
| bet.py | 下注协议封装 |
| settle.py | 结算/派彩协议处理 |
| heartbeat | WebSocket 连线保活心跳 |

### 测试用例统计

| Pytest Marker | 用例数 | 说明 |
|---------------|--------|------|
| login | 2 | 登入测试 |
| table | 52 | 进桌测试 |
| bac_bet | 2496 | 百家乐投注（含 bac_balancecheck） |
| bac_balancecheck | 718 | 百家乐余额检查 |
| bac_odds | 14 | 百家乐赔率验证（全玩法输赢场景） |
| dtb_bet | 928 | 龙虎投注（含 dtb_balancecheck） |
| dtb_balancecheck | 232 | 龙虎余额检查 |
| dtb_odds | 11 | 龙虎赔率验证（全玩法输赢场景） |
| single_table | 2474 | 单桌全部投注测试 |

### 运行方式

```bash
# 克隆并安装
git clone <repo-url>
cd game-automation
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 编辑测试配置
nano test_data/config.yaml
nano test_data/player_info/<currency>_player_info.yaml

# 执行测试
python -m pytest -v -m "login"
python -m pytest -v --player-id=rel_usd_single_player -m "bac_bet"
python -m pytest -v --player-id=rel_usd_single_player -m "dtb_bet"
python -m pytest -v --player-id=rel_usd_single_player -m "bac_balancecheck"

# 生成 HTML 报告
python -m pytest --html=reports/report.html --self-contained-html

# 并行执行
python -m pytest -v -n 4 -m "single_table"
```

### 测试环境要求

- 测试账号需加入 Operator 热加载永不踢桌列表
- 桌台设定：结算秒数 5 秒，延迟 0 秒，特定玩法限制 60 局
- AutoDealer 设定：换靴局数 60 局

### 开发规范

- Branch 命名：`feature/<功能>` / `fix/<问题>` / `test/<测试>` / `docs/<文档>` / `refactor/<范围>`
- Commit Message：遵循 Conventional Commits（feat / fix / refactor / chore / test / style / docs / perf / ci）

---

## 3. opennet-qa-test

- 仓库地址：https://github.com/JeremyT666/opennet-qa-test
- 最后提交：2025-11-07（init commit + 1 update）

### 定位

Web UI 自动化测试项目，采用 Page Object 模式。从代码文件名推断，测试目标包含 **Twitch 搜索频道功能**。

### 项目架构

```
opennet-qa-test/
├── config/          # 配置文件
├── pages/           # 页面对象（Page Object）
│   └── twitch_search_channels_tab_page.py  # Twitch 搜索频道页面对象
├── tests/           # 测试用例
├── utils/           # 工具函数
├── result_gif/      # 测试运行演示 GIF
├── __init__.py
├── pytest.ini       # pytest 配置
├── requirements.txt # Python 依赖
└── README.md        # 仅含一行 Demo Gif
```

### 特点

- 标准 Page Object Model 架构
- pytest 驱动
- 有可视化运行结果演示（result_gif/result.gif）
- 项目较新（2025-11），README 尚未完善

---

## 三个仓库的关系

```
                    JeremyT666 GitHub
                         |
          +--------------+--------------+
          |              |              |
    data_mapping   game-automation  opennet-qa-test
    (2022)         (2025 8-9月)     (2025 11月)
          |              |              |
     Excel 数据比对   游戏协议测试    Web UI 测试
     单文件脚本       完整框架        POM 架构
          |              |              |
     早期工具          主力项目        新项目
```

技术演进路线：从单文件数据比对脚本 → 到完整的游戏协议级测试框架 → 再到 Web UI 自动化测试，覆盖了 QA 工程师工作的三个核心场景。
