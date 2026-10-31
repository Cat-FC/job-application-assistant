# Job Application Assistant

一个面向求职准备和转岗规划的 Agent Skill，采用 `SKILL.md + references/` 的可移植结构，并针对 Codex 的安装与交互体验进行了优化。

输入目标岗位名称和岗位要求后，它会通过 5–10 轮一问一答的选项式诊断，评估当前能力与岗位要求之间的具体差距，并生成有优先级、可验收的学习路线和经过核验的学习资料。

## 功能

- 将 JD 拆解为硬性门槛、核心能力和加分项
- 使用单题选项框逐步诊断，支持自由输入
- 区分知识、实践、工程和证据差距
- 给出“现在投递 / 边学边投 / 暂缓准备”的行动建议
- 生成分阶段路线、实践项目和验收标准
- 推荐与具体差距对应的书籍、课程、视频和官方资料
- 支持完成学习阶段后的进度复评与路线调整
- 默认提供精简报告，也可按需生成详细模式
- 输出可复制到新聊天的隐私安全诊断快照
- 对简历、作品和联网检索执行数据最小化与脱敏规则

## 平台兼容性

| 平台 | 当前支持情况 | 使用方式 |
|---|---|---|
| Codex | 可直接安装 | 从本仓库根目录安装 Skill |
| OpenAI Responses API | 可直接接入核心 Skill | 上传目录或 ZIP，并挂载为 Skill |
| OpenAI Agents API | 可直接接入核心 Skill | 放入 Agent sandbox，并注册 capability directory |
| Claude Code / Claude | 核心内容可用，需要平台包装 | 将 `SKILL.md` 和 `references/` 放入 Claude Plugin/Skill 结构 |
| Cursor | 核心内容可用，需要平台包装 | 将核心 Skill 放入 Cursor 支持的 Plugin/Skill 结构 |
| ChatGPT | 需要打包为 skills-only Plugin | 发布到 ChatGPT/Codex Plugins Directory 后安装 |
| 其他支持 Agent Skills 的工具 | 视工具实现而定 | 导入 `SKILL.md` 与引用文件，或转换成该工具的 rules/instructions |

核心诊断逻辑不依赖 Codex。`agents/openai.yaml` 是 OpenAI/Codex 的界面元数据，其他工具可以忽略。原生选项框不可用时，Skill 会自动退化为 A/B/C/D 文本问答。

## 安装与接入

### Codex：直接安装

把下面这段话发送给 Codex：

```text
请从 GitHub 仓库 Cat-FC/job-application-assistant 的根目录安装
job-application-assistant Skill。
```

### 使用安装脚本

在 PowerShell 中运行：

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" `
  --repo Cat-FC/job-application-assistant `
  --path . `
  --name job-application-assistant
```

安装后建议新建一个 Codex 聊天。如果 Skill 没有立即出现，请重启 Codex。

### OpenAI Responses API

可以把整个仓库目录或 ZIP 上传为版本化 Skill，再将它挂载到支持 Skill 的运行环境。具体请求格式参见 [OpenAI Skills 文档](https://developers.openai.com/api/docs/guides/tools-skills)。

### OpenAI Agents API

把本 Skill 放进 Agent sandbox 中，将其父目录注册到 `environment.capability_directories`。Agent 会发现其中的 `SKILL.md`，并按名称和描述决定何时加载。

### Claude Code / Claude

当前仓库提供可移植的 Skill 核心，但尚未包含 Claude Marketplace 清单，因此不是一键安装包。适配时保留：

```text
SKILL.md
references/
```

再按照 Claude Plugin 的目录和 Marketplace 格式添加平台清单。`agents/openai.yaml` 可以忽略。

### Cursor

当前仓库尚未包含 Cursor Plugin 清单。可以复用 `SKILL.md` 和 `references/`，将它们包装到 Cursor 支持的 Plugin/Skill 结构中；如果只使用项目规则，也可以把核心行为转换为 Cursor 的项目 instructions。

### ChatGPT

需要先将本仓库打包成 skills-only Plugin，并提交到 ChatGPT/Codex 共用的 Plugins Directory。GitHub 仓库本身不能直接作为 ChatGPT 公共插件安装。

## 使用

```text
使用 job-application-assistant Skill

岗位名称：Python 后端开发工程师

岗位要求：
1. 熟悉 Python 和 FastAPI
2. 熟悉 MySQL、Redis
3. 了解 Docker 和 Linux
4. 有 REST API 开发经验
5. 具备测试和工程化能力
```

在 Codex 中也可以显式写成 `$job-application-assistant`。Skill 会逐次提出一个问题；支持原生选项框时会显示三个可点击选项和自由输入入口，不支持时会自动使用 A/B/C/D 文本选项。

## 工作流

1. 解析岗位要求并建立能力模型
2. 通过证据导向的问题了解当前水平
3. 识别并排列关键差距
4. 制定与时间预算匹配的学习路线
5. 核验并推荐学习资料
6. 提供最低可申请标准和未来 7 天行动
7. 根据后续作品和学习成果进行复评

## 文件结构

```text
job-application-assistant/
├── .github/workflows/validate.yml
├── CHANGELOG.md
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── assessment-roadmap.md
│   ├── question-design.md
│   ├── privacy.md
│   ├── reassessment.md
│   └── resource-research.md
├── scripts/validate_release.py
└── tests/behavior-cases.json
```

## 验证

仓库包含零依赖发布校验器和 10 个行为回归场景：

```bash
python scripts/validate_release.py
```

GitHub Actions 会在每次 push 和 pull request 时运行相同检查。行为案例描述应满足和禁止出现的结果，不锁定模型的具体措辞。

## 限制

- 所有能力判断都基于用户自述和提供的证据，不等同于招聘方认证。
- Skill 不虚构经历、技能、成果或证书。
- 学习路线和匹配分析不构成录用保证。
- 具体学习资料需要可用的联网搜索能力才能进行实时核验。
- 上传简历或项目材料前仍建议主动移除联系方式、证件信息、详细住址和公司机密。

## License

[MIT](LICENSE)
