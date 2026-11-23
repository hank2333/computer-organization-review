# 计算机组成 · 复习与自测

基于 Week 1–8 的 37 份课程 PDF（996 页）与 C 辅助文本，整理知识框架、Tutorial 例题与自测。

**在线阅读：[打开复习网站](https://hank2333.github.io/computer-organization-review/)**

- 知识册：27 个知识节点，按依赖关系组织，链接到对应例题。
- 讲解册：44 组例题、原题图、分步解析、36 道自动评分题。
- 原课件：保留 Week 目录结构，正文可直接回查来源。

## 本地阅读

直接用浏览器打开 `index.html`。两册内容和插图支持离线阅读；打开来源 PDF 需要保留 Week 文件夹。
自测答案和草稿不会上传或持久保存，刷新后清空。

## 修改与检查

使用 Python 3.12 或更高版本：

```sh
python -m pip install -r requirements.txt
python tools/build.py
python tools/check.py
```

修改讲解内容时编辑 `tools/build.py`，再重新生成两册 HTML。`tools/inventory.json` 保存课件路径和页数。
校验脚本检查本地链接、跨册锚点、重复 ID、自测数据、BCD 与状态标志计算，以及有符号乘除边界。

## CI/CD

工作流位于 `.github/workflows/pages.yml`：

1. 向 `main` 提交 PR：生成网页并执行校验。
2. 推送到 `main` 或手动运行：校验通过后上传静态站点并部署 GitHub Pages。
3. 部署目录仅包含 HTML 和 Week 课件目录，不包含工具、Git 元数据、本地提取文本或截图。

仓库 Pages 的发布源需设为 **GitHub Actions**。不需要配置个人访问令牌等仓库 Secrets。

原始课件的权利属于各自权利人；本仓库没有为原始课件额外授予开源许可。汇编示例采用 MASM 风格，未在 DOSBox 实机汇编运行。
