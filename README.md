# CLI 工具集

这个仓库包含多个实用的命令行工具。

## GitHub Stars CLI

一个命令行应用，用于查找特定日期范围内GitHub上最受欢迎（按星标数排序）的项目。

## Bulk Rename CLI

一个批量文件重命名工具，支持多种重命名模式。

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

# Bulk Rename CLI

批量文件重命名工具，支持多种重命名模式，如添加前缀、添加后缀、替换文本和正则表达式替换等。

## 使用方法

基本用法：

```bash
python bulk_rename.py <目录> <模式> [选项]
```

### 可用模式

1. **添加前缀**：
   ```bash
   python bulk_rename.py /path/to/directory prefix "新前缀-"
   ```

2. **添加后缀**（在文件名与扩展名之间）：
   ```bash
   python bulk_rename.py /path/to/directory suffix "-新后缀"
   ```

3. **替换文本**：
   ```bash
   python bulk_rename.py /path/to/directory replace "旧文本" "新文本"
   ```

4. **正则表达式替换**：
   ```bash
   python bulk_rename.py /path/to/directory regex "正则模式" "替换文本"
   ```

5. **格式化模式**：
   ```bash
   python bulk_rename.py /path/to/directory pattern "file_{counter:03d}{ext}"
   ```
   
   格式化模式支持以下变量：
   - `{name}` - 原始文件名（不含扩展名）
   - `{ext}` - 文件扩展名（包含点）
   - `{index}` - 文件索引号
   - `{counter}` - 计数器（可使用 Python 格式化，如 `{counter:03d}`）

### 通用选项

`-f, --force` - 强制执行而不询问确认

### 示例

将目录中所有文件添加前缀 "img_"：
```bash
python bulk_rename.py ~/Pictures/vacation prefix "img_"
```

将文件从 "DSC_xxxx.jpg" 改名为 "vacation_xxxx.jpg"：
```bash
python bulk_rename.py ~/Pictures/vacation replace "DSC_" "vacation_"
```

使用格式化模式将所有文件按顺序编号（photo_001.jpg, photo_002.jpg 等）：
```bash
python bulk_rename.py ~/Pictures/vacation pattern "photo_{counter:03d}{ext}"
```

## 许可证

MIT
