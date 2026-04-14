# PhD 科研开发者 Claude Code 配置包

一套可跨项目复用的 Claude Code 最佳实践配置，专为 AI 科研开发设计。

## 快速使用

```bash
# 复制到新项目
cp -r .claude_personal/rules/     your-project/.claude/rules/
cp -r .claude_personal/agents/    your-project/.claude/agents/
cp -r .claude_personal/skills/    your-project/.claude/skills/
cp -r .claude_personal/commands/  your-project/.claude/commands/

# 然后编辑 CLAUDE.md 的 "Project-Specific" 部分，填入项目特有信息
```

## 包含什么

### Rules — 自动防护栏
| 规则 | 匹配文件 | 作用 |
|------|---------|------|
| `data-protection` | `data/**`, `checkpoints/**`, `weights/**` | 禁止修改数据和权重 |
| `python-research` | `**/*.py` | Python 科研代码规范 |
| `experiment-logs` | `results/**`, `experiments/**` | 实验记录只追加不修改 |

### Agents — 专用代理
| 代理 | 权限 | Memory | 用途 |
|------|------|--------|------|
| `paper-analyst` | 只读 | `user`（跨项目） | 论文分析 |
| `code-explorer` | 只读 | `user`（跨项目） | 代码理解 |
| `experiment-runner` | 读写 | `local`（项目私有） | 实验执行 |

### Skills — 领域知识（预加载到 Agent）
| 技能 | 预加载给 | 内容 |
|------|---------|------|
| `paper-reading` | paper-analyst | 论文分析方法论和输出模板 |
| `code-review` | code-explorer | 论文↔代码对比方法论 |
| `experiment-tracking` | experiment-runner | 实验记录规范和格式 |

### Commands — 工作流入口
| 命令 | 用法 | 做什么 |
|------|------|--------|
| `/read-paper` | `/read-paper [url]` | 分析论文，保存到 notes/ |
| `/reproduce-check` | `/reproduce-check` | 对比论文和代码实现 |
| `/run-experiment` | `/run-experiment [config]` | 执行实验并自动记录 |

## 使用后别忘了

2. **积累知识**：每次讨论后把结论写入 CLAUDE.md
3. **及时 compact**：上下文用到 ~50% 时 `/compact`
4. **Agent Memory 会自动积累**：paper-analyst 和 code-explorer 会越用越懂你的领域
