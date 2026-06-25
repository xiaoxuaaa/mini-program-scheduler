# 📚 更新日志文档规范

本文档定义项目更新日志文件的命名和组织规范。

---

## 📁 文件命名规范

### 1. 版本发布说明
**格式**: `V{版本号}_RELEASE_NOTES.md`  
**示例**: 
- `V0.3.0_RELEASE_NOTES.md`
- `V0.7.2_RELEASE_NOTES.md`

**内容要求**:
- 发布日期
- 版本类型（重大功能/功能增强/问题修复）
- 新增功能详细说明
- 技术改进
- 使用示例
- 文件变更清单
- 向后兼容性说明

---

### 2. 升级指南
**格式**: `UPGRADE_TO_V{版本号}.md`  
**示例**: 
- `UPGRADE_TO_V0.7.0.md`

**内容要求**:
- 升级前准备
- 升级步骤
- 数据迁移（如需要）
- 验证方法
- 回滚方案
- 常见问题

---

### 3. Bug 修复记录
**格式**: `BUGFIX_V{版本号}_{简短描述}.md`  
**示例**: 
- `BUGFIX_V0.6.0_COORDINATE_COUNTDOWN.md`
- `BUGFIX_V0.7.0_JS_SYNTAX.md`

**内容要求**:
- 问题描述
- 原因分析
- 修复方案
- 修复代码对比
- 验证步骤
- 影响范围

---

### 4. 版本总结
**格式**: `V{版本号}_SUMMARY.md`  
**示例**: 
- `V0.6.0_SUMMARY.md`

**内容要求**:
- 版本概述
- 完成的功能清单
- 技术亮点
- 测试结果
- 下一步计划

---

### 5. 统一变更日志
**格式**: `CHANGELOG.md`（唯一文件）

**内容要求**:
- 按版本倒序排列（最新在最上面）
- 每个版本包含：版本号、日期、分类变更（新增/改进/修复）
- 遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范

---

## 🗂️ 文件组织结构

```
mini-program-scheduled-tasks/
├── CHANGELOG.md                           # 统一变更日志
│
├── V0.3.0_RELEASE_NOTES.md               # 版本发布说明
├── V0.4.0_RELEASE_NOTES.md
├── V0.5.0_RELEASE_NOTES.md
├── V0.6.0_RELEASE_NOTES.md
├── V0.7.0_RELEASE_NOTES.md
├── V0.7.1_RELEASE_NOTES.md
├── V0.7.2_RELEASE_NOTES.md
│
├── UPGRADE_TO_V0.7.0.md                  # 升级指南
│
├── BUGFIX_V0.6.0_COORDINATE_COUNTDOWN.md # Bug 修复
├── BUGFIX_V0.7.0_JS_SYNTAX.md
│
└── V0.6.0_SUMMARY.md                     # 版本总结
```

---

## ✅ 规范要点

### 版本号格式
- ✅ 大写 `V` 开头（不是小写 `v`）
- ✅ 使用点号分隔：`V0.7.2`
- ✅ 三位版本号：主版本.次版本.修订号

### 文件名要求
- ✅ 使用下划线 `_` 分隔（不是短横线 `-`）
- ✅ 英文描述使用大写：`RELEASE_NOTES`、`UPGRADE`、`BUGFIX`
- ✅ 简短描述使用下划线连接：`JS_SYNTAX`、`COORDINATE_COUNTDOWN`
- ✅ 不使用日期或"FINAL"前缀

### 内容规范
- ✅ 使用 Markdown 格式
- ✅ 使用 emoji 提升可读性（适度）
- ✅ 包含代码示例和对比
- ✅ 添加版本信息和发布日期

---

## 🔄 版本关系

### 主要文档
- **CHANGELOG.md** - 所有版本的简要记录（必读）
- **V{版本号}_RELEASE_NOTES.md** - 某版本的详细说明

### 补充文档
- **UPGRADE_TO_V{版本号}.md** - 重大版本的升级指南
- **BUGFIX_V{版本号}_{描述}.md** - 重要 Bug 的修复记录
- **V{版本号}_SUMMARY.md** - 里程碑版本的总结

---

## 📝 文档更新流程

### 发布新版本时
1. ✅ 更新 `CHANGELOG.md`（添加新版本条目）
2. ✅ 创建 `V{版本号}_RELEASE_NOTES.md`（详细发布说明）
3. ⚠️ 如果是重大更新，创建 `UPGRADE_TO_V{版本号}.md`
4. ⚠️ 如果是里程碑版本，创建 `V{版本号}_SUMMARY.md`

### 修复 Bug 时
1. ✅ 更新 `CHANGELOG.md`（记录修复）
2. ⚠️ 如果是重要 Bug，创建 `BUGFIX_V{版本号}_{描述}.md`

---

## 🚫 不符合规范的示例

❌ `v0.7.0_release.md` - 小写 v，使用短横线  
❌ `FINAL_V0.6.0_SUMMARY.md` - 不必要的 FINAL 前缀  
❌ `UPGRADE_v0.7.0.md` - 小写 v  
❌ `bugfix-coordinate.md` - 缺少版本号  
❌ `UPGRADE_SUMMARY.md` - 缺少版本号  
❌ `2026-06-24_RELEASE.md` - 不使用日期命名  

---

## ✅ 符合规范的示例

✅ `V0.7.2_RELEASE_NOTES.md` - 正确格式  
✅ `UPGRADE_TO_V0.7.0.md` - 清晰表达升级目标版本  
✅ `BUGFIX_V0.7.0_JS_SYNTAX.md` - 版本号+简短描述  
✅ `V0.6.0_SUMMARY.md` - 简洁的总结文档  
✅ `CHANGELOG.md` - 统一变更日志  

---

## 🔍 快速查找指南

### 想了解某个版本的功能
👉 查看 `V{版本号}_RELEASE_NOTES.md`

### 想升级到某个版本
👉 查看 `UPGRADE_TO_V{版本号}.md`

### 想了解某个 Bug 修复
👉 查看 `BUGFIX_V{版本号}_{描述}.md`

### 想浏览所有变更
👉 查看 `CHANGELOG.md`

---

## 📅 维护说明

### 定期检查
- 每次发布后验证文件命名是否符合规范
- 删除过时的临时文档（如 `*_CHECKLIST.md`、`*_SUMMARY.md` 临时文件）
- 合并重复的文档

### 归档策略
- 保留所有正式版本的发布说明
- 保留重要 Bug 的修复记录
- 删除临时验证文档

---

## 📖 相关文档

- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [语义化版本](https://semver.org/lang/zh-CN/)

---

**创建日期**: 2026-06-24  
**最后更新**: 2026-06-24  
**维护者**: 项目团队
