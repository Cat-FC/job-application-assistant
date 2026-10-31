# Job Application Assistant

一个面向求职准备和转岗规划的 Codex Skill。

输入目标岗位名称和岗位要求后，它会通过 5–10 轮一问一答的选项式诊断，评估当前能力与岗位要求之间的具体差距，并生成有优先级、可验收的学习路线和经过核验的学习资料。

## 功能

- 将 JD 拆解为硬性门槛、核心能力和加分项
- 使用单题选项框逐步诊断，支持自由输入
- 区分知识、实践、工程和证据差距
- 给出“现在投递 / 边学边投 / 暂缓准备”的行动建议
- 生成分阶段路线、实践项目和验收标准
- 推荐与具体差距对应的书籍、课程、视频和官方资料
- 支持完成学习阶段后的进度复评与路线调整

## 安装

### 让 Codex 安装

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

## 使用

```text
使用 $job-application-assistant

岗位名称：Python 后端开发工程师

岗位要求：
1. 熟悉 Python 和 FastAPI
2. 熟悉 MySQL、Redis
3. 了解 Docker 和 Linux
4. 有 REST API 开发经验
5. 具备测试和工程化能力
```

Skill 会逐次提出一个问题。支持原生选项框时会显示三个可点击选项和自由输入入口；不支持时会自动使用 A/B/C/D 文本选项。

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
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── assessment-roadmap.md
    ├── question-design.md
    ├── reassessment.md
    └── resource-research.md
```

## 限制

- 所有能力判断都基于用户自述和提供的证据，不等同于招聘方认证。
- Skill 不虚构经历、技能、成果或证书。
- 学习路线和匹配分析不构成录用保证。
- 具体学习资料需要可用的联网搜索能力才能进行实时核验。

## License

[MIT](LICENSE)
