#!/usr/bin/env python3
"""
capability-evolver v2.0 - 轻量级自我进化引擎
纯Python实现，无外部依赖
"""

import json
import os
import re
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from pathlib import Path
import subprocess

# ============== 配置 ==============
HOME = Path.home()
EVOLVER_DIR = HOME / ".openclaw" / "skills" / "capability-evolver"
MEMORY_DIR = HOME / ".openclaw" / "skills" / "ontology-clawra" / "memory"
WORKSPACE_DIR = HOME / ".openclaw" / "workspace"
LOGS_DIR = HOME / ".openclaw" / "logs"

@dataclass
class EvolutionEvent:
    ts: str
    type: str  # error_analyzed, fix_applied, rule_learned, optimization_suggested
    content: Dict[str, Any]
    status: str  # pending, approved, executed, rejected
    risk: str  # low, medium, high
    parent_id: Optional[str] = None

class ErrorAnalyzer:
    """错误分析器 - 扫描日志，提取失败模式"""
    
    ERROR_PATTERNS = [
        (r"Connection error|ConnectionRefused|Connection timeout", "network_error", 0.8),
        (r"SyntaxError|IndentationError|NameError", "code_error", 0.9),
        (r"FileNotFoundError|Permission denied", "file_error", 0.7),
        (r"Rate limit|RateLimitExceeded", "rate_limit", 0.6),
        (r"AuthenticationError|Auth failed|401", "auth_error", 0.8),
        (r"ImportError|ModuleNotFoundError", "import_error", 0.9),
        (r"Timeout|timeout|Timed out", "timeout_error", 0.6),
        (r"Validation error|Invalid.*input", "validation_error", 0.7),
    ]
    
    def scan_logs(self, log_paths: List[str] = None, since_hours: int = 24) -> List[Dict]:
        """扫描日志，提取错误模式"""
        if log_paths is None:
            log_paths = [str(LOGS_DIR)]
        
        patterns_found = {}
        cutoff = datetime.now() - timedelta(hours=since_hours)
        
        for log_path in log_paths:
            path = Path(log_path)
            if not path.exists():
                continue
                
            for log_file in path.glob("*.log"):
                try:
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            try:
                                # 提取时间戳
                                ts_match = re.match(r"\[?(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2})", line)
                                if ts_match:
                                    ts = datetime.fromisoformat(ts_match.group(1).replace(' ', 'T'))
                                    if ts < cutoff:
                                        continue
                                
                                # 匹配错误模式
                                for pattern, error_type, severity in self.ERROR_PATTERNS:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        if error_type not in patterns_found:
                                            patterns_found[error_type] = {
                                                "pattern": error_type,
                                                "count": 0,
                                                "severity": severity,
                                                "examples": [],
                                                "suggestion": self._generate_suggestion(error_type)
                                            }
                                        patterns_found[error_type]["count"] += 1
                                        if len(patterns_found[error_type]["examples"]) < 3:
                                            patterns_found[error_type]["examples"].append(line.strip()[:200])
                            except:
                                continue
                except:
                    continue
        
        return list(patterns_found.values())
    
    def _generate_suggestion(self, error_type: str) -> str:
        """生成修复建议"""
        suggestions = {
            "network_error": "检查网络连接，考虑增加重试机制和超时处理",
            "code_error": "检查语法和变量命名，确保代码符合Python规范",
            "file_error": "检查文件路径和权限，确保目录存在",
            "rate_limit": "实现指数退避策略，控制请求频率",
            "auth_error": "检查API密钥和认证信息是否正确",
            "import_error": "检查依赖是否正确安装，模块路径是否正确",
            "timeout_error": "增加超时时间，或实现异步处理",
            "validation_error": "增强输入验证，确保数据格式正确"
        }
        return suggestions.get(error_type, "需要进一步分析错误原因")


class SelfRepair:
    """自我修复器 - 生成修复代码"""
    
    def __init__(self, evolver_dir: Path = EVOLVER_DIR):
        self.evolver_dir = evolver_dir
        self.events_file = evolver_dir / "events.jsonl"
    
    def analyze_and_fix(self, error_patterns: List[Dict], target_files: List[str] = None) -> List[Dict]:
        """分析错误并生成修复"""
        fixes = []
        
        for error in error_patterns:
            fix = self._generate_fix(error)
            if fix:
                fixes.append(fix)
        
        return fixes
    
    def _generate_fix(self, error: Dict) -> Optional[Dict]:
        """为单个错误生成修复"""
        error_type = error["pattern"]
        count = error["count"]
        
        # 风险评估
        risk_score = error["severity"] * min(count / 10, 1.0)
        if risk_score < 0.3:
            risk = "low"
        elif risk_score < 0.6:
            risk = "medium"
        else:
            risk = "high"
        
        # 生成修复建议
        fix_templates = {
            "network_error": {
                "description": f"增加网络错误重试机制（{count}次）",
                "template": '''
def retry_on_network_error(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    if i == max_retries - 1:
                        raise
                    time.sleep(delay * (2 ** i))
        return wrapper
    return decorator
'''
            },
            "timeout_error": {
                "description": f"增加超时处理机制（{count}次）",
                "template": '''
import signal

class TimeoutError(Exception):
    pass

def with_timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutError(f"Function timed out after {seconds}s")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapper
    return decorator
'''
            },
            "import_error": {
                "description": f"增加可选依赖处理（{count}次）",
                "template": '''
def safe_import(module_name, fallback=None):
    try:
        return __import__(module_name)
    except ImportError:
        return fallback
'''
            }
        }
        
        template = fix_templates.get(error_type, {
            "description": f"需要人工审查（{error_type}）",
            "template": "# 建议人工检查此错误"
        })
        
        return {
            "error_type": error_type,
            "description": template["description"],
            "count": count,
            "severity": error["severity"],
            "risk": risk,
            "confidence": error["severity"] * 0.8,
            "fix_template": template["template"],
            "suggestion": error.get("suggestion", "")
        }


class RuleLearner:
    """规则学习器 - 从成功案例中抽取规则"""
    
    def extract_rules(self, from_paths: List[str] = None, min_occurrences: int = 3) -> List[Dict]:
        """从工作记忆提取规则"""
        if from_paths is None:
            from_paths = [str(WORKSPACE_DIR / "memory")]
        
        patterns = {}
        
        for path_str in from_paths:
            path = Path(path_str)
            if not path.exists():
                continue
            
            for md_file in path.glob("**/*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 提取代码块模式
                        code_blocks = re.findall(r'```python\s*(.*?)\s*```', content, re.DOTALL)
                        for block in code_blocks:
                            # 简化模式提取
                            patterns[block[:50]] = {
                                "pattern": block[:100],
                                "count": patterns.get(block[:50], {}).get("count", 0) + 1,
                                "source": str(md_file.name)
                            }
                except:
                    continue
        
        # 过滤高频模式
        rules = []
        for p, data in patterns.items():
            if data["count"] >= min_occurrences:
                rules.append({
                    "pattern": data["pattern"],
                    "count": data["count"],
                    "source": data["source"],
                    "confidence": min(data["count"] / 10, 1.0)
                })
        
        return rules


class ProactiveOptimizer:
    """主动优化器 - 识别低效模式并改进"""
    
    INEFFICIENCY_PATTERNS = [
        (r"for.*in.*:\s*for.*in", "nested_loop", "考虑合并或使用列表推导式"),
        (r"sleep\(\d+\)", "hardcoded_sleep", "考虑使用事件驱动代替sleep"),
        (r"\.append\(.*\).*\.append\(", "repeated_append", "考虑使用列表推导式一次性生成"),
        (r"except:\s*pass", "bare_except", "添加具体异常处理和日志"),
        (r"print\(", "debug_print", "移除调试print或替换为logging"),
    ]
    
    def optimize(self, scope: List[str] = None, strategy: str = "balanced") -> List[Dict]:
        """扫描并提出优化建议"""
        if scope is None:
            scope = ["skills", "workspace"]
        
        suggestions = []
        
        skill_dirs = []
        if "skills" in scope:
            skill_dirs.append(HOME / ".openclaw" / "skills")
        if "workspace" in scope:
            skill_dirs.append(WORKSPACE_DIR)
        
        for skill_dir in skill_dirs:
            if not skill_dir.exists():
                continue
            
            for py_file in skill_dir.glob("**/*.py"):
                # 跳过node_modules等
                if "node_modules" in str(py_file) or "__pycache__" in str(py_file):
                    continue
                
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    for pattern, issue_type, suggestion in self.INEFFICIENCY_PATTERNS:
                        matches = list(re.finditer(pattern, content))
                        if matches:
                            suggestions.append({
                                "file": str(py_file),
                                "issue_type": issue_type,
                                "count": len(matches),
                                "suggestion": suggestion,
                                "priority": "medium" if strategy == "balanced" else "high",
                                "line_preview": content[max(0, matches[0].start()-20):matches[0].start()+50]
                            })
                except:
                    continue
        
        return suggestions


class CapabilityEvolver:
    """主类 - 整合所有功能"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.analyzer = ErrorAnalyzer()
        self.repairer = SelfRepair()
        self.learner = RuleLearner()
        self.optimizer = ProactiveOptimizer()
        self.events_file = EVOLVER_DIR / "events.jsonl"
        self.events_file.parent.mkdir(parents=True, exist_ok=True)
    
    def run(self, mode: str = "passive", interval_hours: int = 1) -> Dict:
        """
        运行进化引擎
        
        modes:
        - passive: 仅当被调用时执行
        - proactive: 定时执行优化
        - review: 生成修改建议（不执行）
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "errors_analyzed": [],
            "fixes_suggested": [],
            "rules_learned": [],
            "optimizations_suggested": []
        }
        
        # 1. 错误分析
        errors = self.analyzer.scan_logs(since_hours=24)
        results["errors_analyzed"] = errors
        
        # 2. 生成修复
        fixes = self.repairer.analyze_and_fix(errors)
        results["fixes_suggested"] = fixes
        
        # 3. 学习规则
        rules = self.learner.extract_rules()
        results["rules_learned"] = rules
        
        # 4. 优化建议
        optimizations = self.optimizer.optimize()
        results["optimizations_suggested"] = optimizations
        
        # 5. 记录事件
        self._log_event("error_analyzed", {"count": len(errors)}, "executed", "low")
        
        return results
    
    def _log_event(self, event_type: str, content: Dict, status: str, risk: str):
        """记录事件到日志"""
        event = EvolutionEvent(
            ts=datetime.now().isoformat(),
            type=event_type,
            content=content,
            status=status,
            risk=risk
        )
        
        with open(self.events_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False) + '\n')


# ============== CLI 入口 ==============
def main():
    import sys
    
    evolver = CapabilityEvolver()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        result = evolver.run(mode=mode)
    else:
        result = evolver.run(mode="passive")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
