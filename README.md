# GitHub Stars CLI

一个命令行应用，用于查找特定日期范围内GitHub上最受欢迎（按星标数排序）的项目。

## 安装

1. 确保已安装Python 3.6+
2. 安装依赖项：

```bash
pip install -r requirements.txt
```

## 使用方法

基本用法：

```bash
python github_stars.py
```

这将显示过去30天内创建的GitHub上最受欢迎的10个项目。

### 参数选项

- `--from DATE`: 开始日期，格式为 YYYY-MM-DD（默认为30天前）
- `--to DATE`: 结束日期，格式为 YYYY-MM-DD（默认为今天）
- `--count COUNT`: 要显示的仓库数量（默认为10）
- `--language LANGUAGE`: 按编程语言筛选仓库（例如 Python、JavaScript）
- `--export FILENAME`: 将结果导出到JSON文件（提供文件名）

### 示例

显示2023年全年创建的最受欢迎的20个项目：

```bash
python github_stars.py --from 2023-01-01 --to 2023-12-31 --count 20
```

显示本月创建的最受欢迎的5个项目：

```bash
python github_stars.py --from 2025-05-01 --count 5
```

显示Python语言的最受欢迎项目：

```bash
python github_stars.py --language Python --count 10
```

将结果导出到JSON文件：

```bash
python github_stars.py --language JavaScript --count 15 --export js_stars
```

## GitHub API 限制

请注意，GitHub API对未认证请求有速率限制（每小时60次请求）。如果需要更高的限制，可以设置环境变量`GITHUB_TOKEN`：

```bash
export GITHUB_TOKEN="your_github_personal_access_token"
```

## 许可证

MIT
