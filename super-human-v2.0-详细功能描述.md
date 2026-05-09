# super-human v2.0 - 全能超人 详细功能描述

## 📋 基本信息

- **技能名称**: super-human (全能超人)
- **版本**: 2.0.0
- **最后更新**: 2026-05-10
- **状态**: 生产就绪（BMAD + Open Design 集成完成，核心功能完整）
- **作者**: ClawdBot Community
- **技能类型**: 融合型元技能（Meta Skill）

---

## 🎯 核心理念

**不是简单的技能堆叠，而是智能融合** - super-human v2.0 将多个顶级 AI 工作流系统无缝集成，让 AI 真正理解用户需求，智能选择最佳工作流，动态加载专业角色，并无缝管理记忆。

### 设计原则

1. **模式自动识别** - 根据任务类型自动选择最佳工作流（开发 vs 商业）
2. **无冲突集成** - 多个技能系统协同工作，无重复、无矛盾
3. **动态角色加载** - 从 193 个专业角色库中按需加载最适合的专家
4. **双轨记忆系统** - 内置快速记忆 + 扩展深度记忆，快慢结合
5. **设计智能执行** - 自动学习视觉偏好，生成符合品味的作品

---

## 🚀 五大工作模式

### 1. 开发模式（superpowers 流程）

**自动触发词**: 「开发」、「写代码」、「做个XX」、「实现XX功能」、「帮我做」

#### 五阶段强制工作流

```
1. 澄清需求 (Clarify)
   ↓
2. 制定设计 (Plan)
   ↓
3. 执行开发 (Execute with TDD)
   ↓
4. 系统调试 (Debug)
   ↓
5. 完成分支 (Finish)
```

#### 阶段1：澄清需求 (Clarify)

**硬门规则**: 在设计获批之前，禁止编写任何代码！

**必问问题**（一次只问一个）:
- 你真正想做什么？（目的）
- 有什么限制？（时间、技术栈、依赖）
- 成功是什么样子的？（成功标准）
- 这个不应该做什么？（范围边界）

**提问策略**:
- 优先使用选择题，而非开放性问题
- 每个项目都要经过此流程
- 探索项目上下文（文件、文档、最近提交）

#### 阶段2：制定设计 (Plan)

**设计文档包含**:
- 架构概览
- 组件及其职责
- 数据流
- 错误处理方法
- 测试策略

**输出**: `docs/plans/YYYY-MM-DD-<topic>-design.md`

**规则**:
- 分节呈现设计，每节获得批准后再继续
- 提出 2-3 个方案，包含权衡分析和推荐
- "太简单不需要设计" 永远是错误的

#### 阶段3：执行开发 (Execute with TDD)

**强制规则**:
- **TDD 必须** - 先写失败的测试，再实现代码
- **小步迭代** - 每个任务 2-5 分钟
- **频繁提交** - 每次测试通过后提交
- **YAGNI** - 从所有设计中删除不必要的功能
- **DRY** - 无重复代码

**子代理驱动开发模式**:
```
1. sessions_spawn 一个实现者子代理（带任务和完整计划上下文）
2. 等待完成通知
3. sessions_spawn 一个规范审查者子代理 → 必须确认代码符合规范
4. sessions_spawn 一个代码质量审查者子代理 → 必须批准质量
5. 修复任何问题，必要时重新审查
6. 标记任务完成，移动到下一个
```

#### 阶段4：系统调试 (Debug)

**硬门规则**: 没有根因调查，禁止修复！

**四个阶段**:
1. **根因调查** - 读取错误、重现、检查最近更改、追踪数据流
2. **模式分析** - 找到工作示例、比较、识别差异
3. **假设+测试** - 一次一个假设，测试证明/反驳
4. **修复+验证** - 修复根因，而非症状；验证修复不会破坏任何东西

#### 阶段5：完成分支 (Finish)

**触发条件**: 所有任务完成，所有测试通过

**步骤**:
1. 验证所有测试通过
2. 确定基础分支
3. 提供 4 个选项：本地合并 / 推送+PR / 保持 / 丢弃
4. 执行选择
5. 清理

---

### 2. BMAD 敏捷开发模式

**触发词**: 「BMAD」、「敏捷开发」、「产品规划」、「架构设计」

#### BMAD 角色系统（6 个专业角色）

| 角色 | 职责 | 对应 super-human 组件 |
|------|------|------------------------|
| **bmad-orchestrator** | 编排器，协调整个工作流 | super-human 的编排层 |
| **bmad-product-manager** | 产品经理，需求分析和产品规划 | agency-agents-zh 的产品专家 |
| **bmad-architect** | 系统架构师，设计技术架构 | agency-agents-zh 的系统架构师 |
| **bmad-developer** | 开发者，执行代码实现 | superpowers 的 TDD 流程 |
| **bmad-scrum-master** | Scrum 主管，管理敏捷流程 | agency 的项目跟踪 |
| **bmad-ux-designer** | UX 设计师，优化用户体验 | design 技能的执行层 |

#### BMAD 工作流程

```
1. 产品规划 (Product Manager)
   ↓
2. 架构设计 (Architect)
   ↓
3. 敏捷迭代 (Scrum Master + Developer)
   ↓
4. UX 优化 (UX Designer)
   ↓
5. 编排协调 (Orchestrator)
```

**示例**:
```
用户：用 BMAD 方法开发一个任务管理应用
AI：[BMAD 流程]
  1. [Product Manager] 分析需求：任务 CRUD、用户系统、通知系统
  2. [Architect] 设计架构：React + Node.js + MongoDB
  3. [Scrum Master] 创建用户故事和冲刺计划
  4. [Developer] 开始实现第一个冲刺
  5. [UX Designer] 设计用户界面和交互流程
```

#### BMAD 集成冲突优化

**挑战**: BMAD 有独立的角色系统，与 superpowers 和 agency 的角色可能重叠

**优化方案**:
- **角色映射**: 将 BMAD 的 6 个角色映射到现有系统（见上表）
- **工作流集成**: BMAD 流程作为"敏捷开发模式"，与 superpowers 的"严格 TDD 模式"并存
- **记忆共享**: BMAD 的项目状态（bmad/*.yaml）同步到 `~/.workbuddy/memory/agile/`

---

### 3. 商业管理模式（agency 流程）

**触发词**: 「客户」、「项目」、「定价」、「提案」、「机构」

#### 核心操作流程

```
1. 客户接入 (Client Onboarding)
   ↓
2. 定价提案 (Pricing & Proposals)
   ↓
3. 项目跟踪 (Project Tracking)
   ↓
4. 交付物管理 (Deliverables)
   ↓
5. 团队协调 (Team Coordination)
   ↓
6. 学习系统 (Learning System)
   ↓
7. 按类型定制 (Agency Type Specifics)
```

#### 详细操作

**客户接入**:
- 简介到达（音频、邮件、文档）
- 提取范围、预算、时间线
- 生成结构化简介
- 标记危险信号（范围蔓延、不切实际的截止日期）
- 创建客户文件夹

**定价**:
- 给定范围 → 应用配置中的价目表
- 计算带有复杂性乘数的估算
- 生成提案 PDF
- 与历史类似项目比较

**项目跟踪**:
- 维护所有活跃项目的统一看板
- 截止日期警报
- 检测停滞项目
- 按客户生成每周状态

**交付物管理**:
- 转换粗略笔记/输入 → 结构化交付物
- 对照简介审查
- 如需要适应多种格式

#### 工作空间结构

```
~/.workbuddy/skills/agency/
├── clients/           # 每个客户一个文件
│   ├── index.md       # 客户列表（含状态）
│   └── [name].md      # 客户档案、历史、偏好
├── projects/          # 活跃项目跟踪
├── templates/         # 可重用的提案、简介、报告
├── knowledge/         # SOP、学习、案例研究
└── config.md          # 费率、利润、团队结构
```

#### 商业管理模式原则

- **绝不在没有人类批准的情况下** 发送提案或与客户沟通
- **跟踪时间/成本 vs 估算** - 当项目亏损时警报
- **从纠正中学习** - 更新模板和知识库
- **跨会话维护客户上下文** - 参考历史

---

### 4. Open Design 快速原型模式

**触发词**: 「落地页」、「editorial site」、「杂志风」、「品牌页」

#### 可用技能（真实存在的 2 个）

| 技能 | 功能 | 设计系统 |
|------|------|----------|
| **open-design-landing** | 编辑级品牌落地页 | Atelier Zero |
| **open-design-landing-deck** | 配套幻灯片原型 | Atelier Zero |

#### Atelier Zero 设计语言

**视觉特征**:
- Warm paper background（温暖纸张背景）
- Inter Tight + Playfair Display 字体组合
- Italic serif emphasis spans（斜体衬线强调）
- Dotted hairline rules（点状细线）
- Coral terminating dots（珊瑚色终止点）
- Scroll-reveal motion（滚动显示动画）
- 16 surreal collage plates（超现实拼贴画）

**适用场景**:
- 编辑/杂志风格网站
- 品牌落地页
- 设计工作室作品集
- 独立出版社

#### Open Design 工作流程

```
1. 收集品牌信息（brief → inputs.json）
   ↓
2. 选择图片策略（placeholder / generate / bring-your-own）
   ↓
3. 生成单页 HTML（自包含，CSS 内联）
   ↓
4. 预览并迭代
```

**图片策略对比**:

| 策略 | 使用场景 | 成本/延迟 |
|------|----------|------------|
| `placeholder` | 首次通过、演示、内部幻灯片、无图片预算 | $0, <1s |
| `generate` | 最终交付、品牌需要原创拼贴画 | ~$0.40, ~6 min |
| `bring-your-own` | 用户有艺术指导 PNG | $0, 0s |

#### 输入参数（inputs.json）

| ID | 标签 | 描述 | Schema 路径 |
|----|------|------|-------------|
| `brand` | Brand identity | 名称、标记、标语、位置、语言、许可证、仓库 URL | `schema.ts#BrandBlock` |
| `nav` | Navigation links | 最多 5 个导航条目，每个可选计数徽章 | `schema.ts#NavLink` |
| `hero` | Hero block | 标题 + 3 个统计环 + 4 步索引 | `schema.ts#HeroBlock` |
| `about` | About block | 宣言/关于块 | `schema.ts#AboutBlock` |
| `capabilities` | 4 capability cards | 4 个能力卡片 | `schema.ts#CapabilitiesBlock` |
| `labs` | 5 lab cards + filter pills | 5 个实验室卡片 + 过滤药丸 | `schema.ts#LabsBlock` |
| `method` | 4 method steps | 4 个方法步骤（带缩略图） | `schema.ts#MethodBlock` |
| `work` | 2 selected-work cards | 2 个精选作品卡片（深色底板） | `schema.ts#WorkBlock` |
| `testimonial` | Pull quote + 5 partner glyphs | 引文 + 5 个合作伙伴标志 | `schema.ts#TestimonialBlock` |
| `cta` | Closing CTA + ribbon | 结束 CTA + 丝带 | `schema.ts#CTABlock` |
| `footer` | Footer | 品牌描述 + 4 个链接列 + 巨型踢脚板 | `schema.ts#FooterBlock` |
| `imagery` | Image strategy | 图片策略（生成/占位符/自带） | `schema.ts#ImageryConfig` |

#### Open Design 集成冲突优化

**挑战**: Open Design 技能可能与 design 技能的偏好学习冲突

**优化方案**:
- **技能分层**:
  - Open Design 作为**快速原型层**（生成初始原型）
  - design 技能作为**偏好优化层**（迭代和优化）
- **工作流集成**:
  - 开发模式：Open Design 生成原型 → design 技能优化 → superpowers 实现
  - 商业模式：Open Design 生成交付物 → agency 管理客户反馈

---

### 5. 专业角色加载模式

**触发词**: 「作为XX专家」、「我需要XX师」、「用XX的角色」

#### 193 个专业角色库（agency-agents-zh）

**角色分类**:

| 领域 | 示例角色 | 数量 |
|------|----------|------|
| 学术领域 (academic) | 研究员、教授、学术编辑 | 待统计 |
| 设计领域 (design) | UI 设计师、UX 研究员、视觉故事讲述者 | 待统计 |
| 工程领域 (engineering) | 安全工程师、后端架构师、前端开发者、DevOps 自动化师、数据工程师 | 最大类别 |
| 金融领域 (finance) | 金融分析师、投资顾问、风险管理师 | 待统计 |
| 游戏开发 (game-development) | 游戏设计师、关卡设计师、游戏引擎程序员 | 待统计 |
| 市场营销 (marketing) | 市场营销专家、SEO 专家、社交媒体经理 | 待统计 |
| 产品管理 (product) | 产品经理、产品负责人、产品营销经理 | 待统计 |
| **中国市场原创** | 小红书运营专家、抖音内容策略师、微信小程序开发者 | 待统计 |

#### 角色加载流程

```
1. 识别需求 - 确定需要哪种专家
   ↓
2. 加载角色 - 从 `agency-agents-zh/` 加载对应的角色定义
   ↓
3. 执行任务 - AI 按照专家的工作流程执行
   ↓
4. 交付成果 - 输出符合专业标准的成果
```

#### 角色定义位置

```
~/.workbuddy/skills/agency-agents-zh/
├── academic/          # 学术领域
├── design/           # 设计领域
├── engineering/      # 工程领域（最大）
├── finance/          # 金融领域
├── game-development/ # 游戏开发
├── marketing/        # 市场营销
├── product/          # 产品管理
└── ...
```

#### 快速开始

```bash
# 查看所有可用的专家角色
cat ~/.workbuddy/skills/agency-agents-zh/AGENT-LIST.md

# 查看特定角色定义
cat ~/.workbuddy/skills/agency-agents-zh/engineering/engineering-security-engineer.md
```

---

## 🧠 记忆系统协同

### 双轨记忆系统架构

```
┌─────────────────────────┐       ┌─────────────────────────────┐
│   内置 Agent 记忆       │       │   本技能扩展记忆             │
│   (~/.workbuddy/)      │   +   │   (~/.workbuddy/memory/)    │
│   - MEMORY.md          │       │   - 无限分类存储             │
│   - memory/ (daily)   │       │   - 任何你想要的结构         │
│   - 基本回忆能力       │       │   - 完美组织                 │
└─────────────────────────┘       └─────────────────────────────┘
         ↓                                  ↓
   快速上下文（自动工作）           深度和长期存储（按需扩展）
```

### 写入策略

**立即写入** - 当用户分享重要信息时：
1. 写入 `~/.workbuddy/memory/` 中的适当文件
2. 更新类别 `INDEX.md`
3. 然后回应

**不要等待。不要批处理。立即写入。**

### 搜索策略

**对于小记忆（<50 文件）**:
```bash
# Grep 足够快
grep -r "keyword" ~/.workbuddy/memory/
```

**对于大记忆（50+ 文件）**:
```
1. ~/.workbuddy/memory/INDEX.md → 找到类别
2. ~/.workbuddy/memory/{category}/INDEX.md → 找到项目
3. ~/.workbuddy/memory/{category}/{item}.md → 读取详情
```

### 记忆系统原则

- **分离于内置记忆** - 本系统在 `~/.workbuddy/memory/` 中。永远不要修改：Agent 的 `MEMORY.md`（工作空间根目录），Agent 的 `memory/` 文件夹（如果在工作空间中）
- **用户定义结构** - 在设置期间，询问他们想存储什么
- **每个类别有一个索引** - 维护 `INDEX.md`
- **立即写入** - 当用户分享信息时，立即写入
- **通过分裂扩展** - 当类别增长很大时，分裂成子类别

---

## 🎨 设计智能执行

### 自动学习视觉偏好

**规则**:
- 从选择、反馈和反应中检测模式
- 支持所有设计类型（UI、图形、视频、打印、任何视觉）
- 在 2+ 一致偏好后确认
- 保持条目超级紧凑
- 检查 `dimensions.md` 获取类别，`criteria.md` 获取格式

### 设计偏好结构

```markdown
### 美学
<!-- 通用视觉品味。格式: "特质" -->

### 按媒介
<!-- 不同偏好按类型。格式: "媒介: 特质" -->

### 品牌
<!-- 命名项目/品牌 with 独特风格。格式: "名称: 特质" -->

### 永不
<!-- 用户拒绝或视觉上不喜欢的东西 -->
```

### 设计流程冲突优化

**挑战**: design 技能自动学习偏好，superpowers 有固定设计阶段

**优化方案**:
- 将 design 技能作为**设计执行层**
- superpowers 的设计阶段调用 design 技能执行
- design 技能学习到的偏好反馈到 superpowers 的设计模板

---

## ⚙️ 配置

### 首次使用设置

1. **选择模式** - 让系统自动识别，或手动指定
2. **配置文件结构** - 为记忆系统定义类别
3. **加载角色库** - 确认 agency-agents-zh 已安装
4. **设置设计偏好** - 让 design 技能自动学习，或手动配置

### 配置文件

| 配置文件 | 用途 |
|----------|------|
| `~/.workbuddy/skills/agency/config.md` | 商业管理模式配置（费率、利润、团队结构） |
| `~/.workbuddy/memory/config.md` | 记忆系统配置 |
| `skills/super-human/design-preferences.md` | 设计偏好配置 |

---

## 🔧 疑难解答

### 问题1：模式识别错误

**症状**: 系统选择了错误的工作流模式

**修复**:
1. 明确指定模式：「用开发模式」、「用商业管理模式」
2. 检查触发词是否清晰
3. 重新训练模式识别系统

### 问题2：角色加载失败

**症状**: 无法加载请求的专业角色

**修复**:
1. 检查 agency-agents-zh 是否正确安装
2. 查看 `~/.workbuddy/skills/agency-agents-zh/AGENT-LIST.md` 确认角色名称
3. 手动指定角色文件路径

### 问题3：记忆系统混乱

**症状**: 找不到存储的信息，或内置记忆与扩展记忆冲突

**修复**:
1. 检查 `~/.workbuddy/memory/INDEX.md` 是否最新
2. 验证内置记忆和扩展记忆的分离
3. 运行记忆系统诊断

---

## 📚 已融合的技能

### 核心技能

| 技能 | 功能 | 来源 |
|------|------|------|
| `superpowers` | 开发工作流（TDD、子代理驱动） | obra/superpowers |
| `agency` | 商业管理机构（客户、项目、定价） | agency skill |
| `agency-agents-zh` | 193 个专业角色库 | Chinese market adaptation |
| `design` | 设计执行和偏好学习 | design skill |
| `memory` | 扩展记忆系统 | memory skill |

### BMAD 敏捷开发技能

| 技能 | 角色 | 状态 |
|------|------|------|
| `bmad-orchestrator` | 编排器（协调整个工作流） | ✅ 已集成 |
| `bmad-product-manager` | 产品经理（需求分析、产品规划） | ✅ 已集成 |
| `bmad-architect` | 系统架构师（技术架构设计） | ✅ 已集成 |
| `bmad-developer` | 开发者（代码实现） | ✅ 已集成 |
| `bmad-scrum-master` | Scrum 主管（敏捷流程管理） | ✅ 已集成 |
| `bmad-ux-designer` | UX 设计师（用户体验优化） | ✅ 已集成 |

### Open Design 快速原型技能

| 技能 | 功能 | 设计系统 |
|------|------|----------|
| `open-design-landing` | 编辑级品牌落地页 | Atelier Zero |
| `open-design-landing-deck` | 配套幻灯片原型 | Atelier Zero |

### 推荐安装的补充技能

| 技能 | 功能 | 使用场景 |
|------|------|----------|
| `workflow-runner` | 多智能体协作工作流 | 复杂项目 |
| `security-auditor` | 安全审计 | 与安全工程师角色互补 |
| `decide` | 决策跟踪模式 | 重要决策记录 |
| `escalate` | 何时涉及人类 | 升级机制 |
| `learn` | 自适应学习 | 持续改进 |

---

## 🎯 关键原则总结

### 开发模式原则（来自 superpowers）

- **一次一个问题** 在头脑风暴期间
- **TDD 始终** - 先写失败的测试，删除在测试前写的代码
- **YAGNI** - 从所有设计中删除不必要的功能
- **DRY** - 无重复
- **系统化优于临时** - 遵循流程，特别是在时间压力下
- **证据优于主张** - 在声明成功之前验证
- **频繁提交** - 每次测试通过后

### 商业管理模式原则（来自 agency）

- **绝不在没有人类批准的情况下** 发送提案或与客户沟通
- **跟踪时间/成本 vs 估算** - 当项目亏损时警报
- **从纠正中学习** - 更新模板和知识库
- **跨会话维护客户上下文** - 参考历史

### 记忆系统原则（来自 memory）

- **分离于内置记忆** - 本系统在 `~/.workbuddy/memory/` 中
- **用户定义结构** - 在设置期间，询问他们想存储什么
- **每个类别有一个索引** - 维护 `INDEX.md`
- **立即写入** - 当用户分享信息时，立即写入
- **通过分裂扩展** - 当类别增长很大时，分裂成子类别

---

## 🚀 使用示例

### 示例1：开发模式

```
用户：帮我做一个网站
AI：[澄清] 网站是什么类型的？个人站还是企业站？
用户：个人博客
AI：[设计] 我计划用 HTML+CSS+JS，3个文件搞定
用户：好的
AI：[执行] 
1. 创建 index.html
2. 创建 style.css  
3. 创建 script.js
[审核] 博客功能完整，符合需求
```

### 示例2：BMAD 敏捷开发模式

```
用户：用 BMAD 方法开发一个任务管理应用
AI：[BMAD 流程]
  1. [Product Manager] 分析需求：任务 CRUD、用户系统、通知系统
  2. [Architect] 设计架构：React + Node.js + MongoDB
  3. [Scrum Master] 创建用户故事和冲刺计划
  4. [Developer] 开始实现第一个冲刺
  5. [UX Designer] 设计用户界面和交互流程
```

### 示例3：Open Design 快速原型模式

```
用户：做一个编辑风格的落地页，品牌叫"Lumen Field"
AI：[Open Design 流程]
  1. 收集品牌信息（名称、标语、坐标、联系方式）
  2. 使用 placeholder 图片策略（快速预览）
  3. 生成 index.html（Atelier Zero 风格）
  4. 提供预览链接
```

### 示例4：专业角色加载

```
用户：作为安全工程师，请审查这段代码
AI：[加载角色] 从 agency-agents-zh 加载安全工程师角色定义
    [执行] 按照安全工程师的工作流程执行任务...
```

---

## 📊 技术规格

### 系统要求

| 项目 | 要求 |
|------|------|
| OS | Linux, macOS, Windows (win32) |
| AI 模型 | Claude, GPT, 或其他支持工具调用的 LLM |
| 依赖二进制 | 无强制依赖 |
| 内存需求 | 建议 4GB+ RAM |

### 文件结构

```
~/.workbuddy/skills/super-human/
├── SKILL.md              # 主技能文档（已修复）
├── design-preferences.md # 设计偏好配置
├── references/           # 参考文档
│   ├── brainstorming.md
│   ├── writing-plans.md
│   ├── subagent-development.md
│   ├── systematic-debugging.md
│   └── finishing-branch.md
└── examples/            # 使用示例
```

---

## 🔄 版本历史

### v2.0.0 (2026-05-10)

**重大更新**:
- ✅ 集成 BMAD 敏捷开发方法（6 个专业角色）
- ✅ 集成 Open Design 快速原型（2 个技能，Atelier Zero 设计语言）
- ✅ 修复虚假描述（"31种设计原型"、"72个设计系统"）
- ✅ 优化冲突策略（6 个冲突优化方案）
- ✅ 更新文档以反映实际情况

**修复内容**:
- 第 5 行（description）：移除虚假的 "31种"、"72个"
- 第 20 行（核心理念）：修正 Open Design 描述
- 第 118-164 行（Open Design 模式）：替换为准确的 2 个技能说明
- 第 426-438 行（冲突优化）：移除虚假引用
- 第 535-543 行（已融合技能）：替换为真实存在的技能名称

### v1.0.0 (假设)

- 初始版本
- 融合 superpowers + agency + design + memory
- 包含 193 个专业角色库（agency-agents-zh）

---

## 📞 反馈和改进

**这个融合技能正在建设中**。你的反馈很重要：

- **如果有用**: `clawhub star super-human`
- **获取更新**: `clawhub sync`
- **报告问题**: 描述什么没按预期工作
- **建议改进**: 描述可以增强什么

---

## 📝 结语

super-human v2.0 是一个强大的 AI 工作流融合系统，通过智能集成多个顶级技能，让 AI 能够：
- ✅ 根据任务类型自动选择最佳工作流
- ✅ 动态加载 193 个专业角色
- ✅ 管理双轨记忆系统（快速 + 深度）
- ✅ 学习并应用视觉设计偏好
- ✅ 无缝协调多个工作流，无冲突、无重复

**现在就开始使用 super-human，体验 AI 工作流的终极融合！** 🚀

---

**版本**: 2.0.0  
**最后更新**: 2026-05-10  
**状态**: 生产就绪（BMAD + Open Design 集成完成，核心功能完整）  
**作者**: ClawdBot Community  
**许可证**: MIT（假设）
