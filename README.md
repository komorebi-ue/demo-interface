# OrangeHRM 接口自动化

基于 Python 的 OrangeHRM 演示环境接口自动化：pytest 组织用例，Playwright 完成浏览器登录并获取 Cookie，requests 发起后续 API 调用。

## 依赖

- Python
- pytest
- playwright
- requests
- allure-pytest
- pyyaml
- loguru

## 项目结构

```text
demo-interface/
├── common/           # 日志、HTTP 客户端封装
├── config/           # 多环境配置
├── data/             # 测试数据（YAML 等）
├── pages/            # 接口层封装
├── tests/            # 测试用例
├── logs/             # 运行日志
├── conftest.py       # 全局 fixture（登录、会话等）
├── pytest.ini
├── requirements.txt
└── README.md
```

## 环境准备

在项目根目录使用 PowerShell：

```powershell
# 1. 创建虚拟环境（已存在可跳过）
python -m venv .venv

# 2. 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 3. 安装依赖
pip install -r .\requirements.txt

# 4. 安装 Playwright Chromium
playwright install chromium
```

若激活脚本被策略拦截：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

亦可不激活环境，直接使用 `.venv\Scripts\python.exe` 执行下文中的 pytest 命令。

## 配置

配置文件：

- `config/config.dev.yaml`
- `config/config.test.yaml`
- `config/config.yaml`（环境专用文件缺项时的回退）

在对应环境中填写：

- `base_url`：站点根地址
- `username` / `password`：登录凭据

## 运行测试

```powershell
# 全部用例
.\.venv\Scripts\python.exe -m pytest -s

# 指定 test 环境配置
.\.venv\Scripts\python.exe -m pytest -s --env=test

# 指定文件
.\.venv\Scripts\python.exe -m pytest -q tests/test_employee_management.py -s

# 按 marker
.\.venv\Scripts\python.exe -m pytest -s -m smoke
.\.venv\Scripts\python.exe -m pytest -s -m pim
```

## Allure 报告

`pytest.ini` 已配置 `--alluredir=./allure-results`。需本机安装 [Allure CLI](https://github.com/allure-framework/allure2/releases) 后执行：

```powershell
allure serve .\allure-results
```

## 日志

- 控制台：loguru 输出
- 文件：`logs/test.log`

## 业务流程概要

1. Playwright 无头登录，提取浏览器 Cookie  
2. 将 Cookie 注入 `requests.Session`，后续请求携带会话  
3. 覆盖新增员工、列表校验；fixture teardown 中删除测试数据，保证清理  
