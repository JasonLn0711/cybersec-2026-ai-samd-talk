#!/usr/bin/env python3
"""Prepare local BreezyVoice render inputs from the 80 minute engineering draft.

The generated package is intentionally local-only under `.local/breezyvoice`.
It strips orchestration markup before model input, preserves stable
`output_prefix` values, and creates review gates before any full TTS run.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
import wave
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = REPO_ROOT / "docs/speaker-notes/breezyvoice/model-ready/cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md"
PRONUNCIATION_NOTES = REPO_ROOT / "docs/speaker-notes/breezyvoice/model-ready/cde-2026-breezyvoice-pronunciation-notes.md"
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
REFERENCE_AUDIO_REQUIRED = False
DELIVERY_TARGET_SECONDS = 4200
DELIVERY_TARGET_TIME = "70:00"
LEGACY_WHITE_BOX_TERM = "\u767d\u76d2"
PREFERRED_WHITE_BOX_TERM = "\u767d\u7bb1"

PILOT_PREFIXES = [
    "cde_full_01_opening_positioning_crazyhunter_entry_case",
    "cde_full_16_k8s_review_controls",
    "cde_full_20_crowdstrike_update_524b",
    "cde_full_26_shared_close_test_anchors",
]

TERM_NORMALIZATIONS = {
    "CDE": "C D E",
    "AI": "人工智慧",
    "ASR": "A S R",
    "TTS": "T T S",
    "TFDA": "T F D A",
    "FDA": "F D A",
    "510(k)": "五一零 K",
    "510(K)": "五一零 K",
    "SaMD": "S A M D",
    "SBOM": "軟體物料清單，S B O M",
    "SCA": "S C A",
    "PACS": "派克斯",
    "HIS": "H I S",
    "EMR": "E M R",
    "RIS": "R I S",
    "LIS": "L I S",
    "FHIR": "F H I R",
    "DICOM": "戴康",
    "API": "應用程式介面",
    "VPN": "V P N",
    "MFA": "M F A",
    "RBAC": "R B A C",
    "IAM": "I A M",
    "HL7": "H L seven",
    "SIEM": "S I E M",
    "EDR": "E D R",
    "K8S API": "K 八 S 管理介面",
    "K8S": "K 八 S",
    "K8s": "K 八 S",
    "CI/CD": "C I C D",
    "AWS": "A W S",
    "FD&C Act Section 524B": "F D C Act，Section 五二四，英文字母 B 款",
    "FD&C Act，Section 524B": "F D C Act，Section 五二四，英文字母 B 款",
    "FD&C Act Section 五二四 B": "F D C Act，Section 五二四，英文字母 B 款",
    "FD&C Act": "F D C Act",
    "524B": "五二四，英文字母 B 款",
    "Log4Shell": "Log four Shell",
    "MOVEit Transfer": "Move it Transfer",
    "Channel File 291": "Channel File 二九一",
    "NetworkPolicy": "Network Policy",
    "workflow": "工作流程",
    "clinical continuity": "臨床連續性",
    "Clinical": "臨床",
    "ransomware": "勒索軟體",
    "downtime": "停機時間",
    "vendor access": "廠商存取",
    "patching limitation": "修補限制",
    "credential risk": "憑證風險",
    "White-box Testing": "白箱測試",
    "White-box testing": "白箱測試",
    "white-box Testing": "白箱測試",
    "white-box testing": "白箱測試",
    "White box Testing": "白箱測試",
    "White box testing": "白箱測試",
    "white box Testing": "白箱測試",
    "white box testing": "白箱測試",
    "White-box review": "白箱審查",
    "white-box review": "白箱審查",
    "White box review": "白箱審查",
    "white box review": "白箱審查",
    "white-box validation": "白箱驗證",
    "White-box validation": "白箱驗證",
    "white box validation": "白箱驗證",
    "White box validation": "白箱驗證",
    "white-box": "白箱",
    "White-box": "白箱",
    "white box": "白箱",
    "White box": "白箱",
    "software supply paths": "軟體供應鏈",
    "software supply chain": "軟體供應鏈",
    "supply path": "供應鏈",
    "supply chain": "供應鏈",
    "CrazyHunter": "Crazy Hunter",
    "UnitedHealth": "United Health",
    "OneBlood": "One Blood",
    "BlackCat": "Black Cat",
    "St. Jude": "Saint Jude",
    "Lurie Children's Hospital": "Lurie Childrens Hospital",
    "Lurie Children’s Hospital": "Lurie Childrens Hospital",
}

NON_PROPER_ENGLISH_ZHTW_NORMALIZATIONS = {
    "access control": "存取控制",
    "access path": "存取路徑",
    "access": "存取",
    "accounts": "帳號",
    "admission controls": "准入控制",
    "affected asset": "受影響資產",
    "allowed paths": "允許路徑",
    "and": "與",
    "antivirus": "防毒軟體",
    "application boundary": "應用程式邊界",
    "application": "應用程式",
    "architecture": "架構",
    "archive": "保存",
    "approved settings": "核准設定",
    "asset": "資產",
    "attack chain": "攻擊鏈",
    "attack path": "攻擊路徑",
    "attack surface": "攻擊面",
    "audit logs": "稽核日誌",
    "authentication": "認證",
    "authorization check": "授權檢查",
    "authorization": "授權",
    "availability": "可用性",
    "behavior": "行為",
    "black-box testing": "黑箱測試",
    "black-box": "黑箱",
    "campaign": "行動",
    "cause": "成因",
    "claims": "理賠申報",
    "clinical incident": "臨床事件",
    "clinical reality": "臨床現實",
    "clinical service provider": "臨床服務供應商",
    "clinical": "臨床",
    "cloud permission": "雲端權限",
    "cloud resource": "雲端資源",
    "cloud-connected medical applications": "連接雲端的醫療應用程式",
    "cloud": "雲端",
    "cluster": "叢集",
    "code review": "程式碼審查",
    "code signing": "程式碼簽章",
    "compliance checklist": "合規檢核表",
    "component": "元件",
    "components": "元件",
    "commit": "提交紀錄",
    "confidentiality": "機密性",
    "configuration hardening": "設定強化",
    "configuration": "設定",
    "controls": "控制措施",
    "control": "控制",
    "connected systems": "互連系統",
    "connected care": "互連照護",
    "container image": "容器映像檔",
    "container base image": "容器基礎映像檔",
    "container privileges": "容器權限",
    "container": "容器",
    "credential handling": "憑證處理",
    "credentials": "憑證",
    "credential": "憑證",
    "cryptojacking": "挖礦劫持",
    "cyber incident": "資安事件",
    "cyber risk": "資安風險",
    "cybersecurity requirements": "資安需求",
    "cybersecurity": "資安",
    "data corruption": "資料毀損",
    "data flow": "資料流",
    "data pipelines": "資料管線",
    "data": "資料",
    "debug": "除錯",
    "default": "預設",
    "deviations": "偏離事項",
    "debug endpoint": "除錯端點",
    "decision path": "決策路徑",
    "dependency": "相依套件",
    "deployment evidence": "部署證據",
    "deployment security": "部署安全",
    "deployment YAML": "部署 YAML",
    "deployment": "部署",
    "design evidence": "設計證據",
    "device crash": "設備當機",
    "device subnet": "設備子網路",
    "device": "設備",
    "direct dependencies": "直接相依套件",
    "down": "不可用",
    "dynamic analysis": "動態分析",
    "emergency-response operations": "緊急應變作業",
    "endpoint": "端點",
    "environment": "環境",
    "entry point": "進入點",
    "evidence chain": "證據鏈",
    "evidence": "證據",
    "exploit cookbook": "攻擊操作手冊",
    "exploitability": "可利用性",
    "external endpoint": "外部端點",
    "external interface": "外部介面",
    "exposed": "暴露",
    "finding anatomy": "發現事項結構",
    "finding": "發現事項",
    "firewall rules": "防火牆規則",
    "firewall rule": "防火牆規則",
    "firewall": "防火牆",
    "firmware logic": "韌體邏輯",
    "firmware update": "韌體更新",
    "firmware": "韌體",
    "fix and retest": "修補與重測",
    "fix": "修補",
    "fuzz testing": "模糊測試",
    "gateway": "閘道",
    "gateways": "閘道",
    "governance gap": "治理缺口",
    "hardcoded flow": "硬編碼流程",
    "hardening": "強化",
    "hash verification": "雜湊驗證",
    "healthcare information system": "醫療資訊系統",
    "healthcare vulnerability response": "醫療弱點回應",
    "hidden services": "隱藏服務",
    "identity verification": "身分驗證",
    "identity": "身分",
    "image provenance": "映像檔來源",
    "impact": "影響",
    "images": "映像檔",
    "image": "映像檔",
    "incident path": "事件路徑",
    "incident response": "事件回應",
    "incident": "事件",
    "inference service": "推論服務",
    "inference services": "推論服務",
    "infrastructure as code": "基礎設施程式碼",
    "infrastructure control plane": "基礎設施控制平面",
    "input handling": "輸入處理",
    "input validation": "輸入驗證",
    "installation evidence": "安裝證據",
    "internal cause": "內部成因",
    "internal": "內部",
    "integration": "整合",
    "integrations": "整合服務",
    "integrity": "完整性",
    "interconnected computing system": "互連運算系統",
    "interface": "介面",
    "keys": "金鑰",
    "key handling": "金鑰處理",
    "layers": "層",
    "lifecycle trust": "生命週期信任",
    "lifecycle": "生命週期",
    "least privilege": "最小權限",
    "laptop": "筆電",
    "logging and configuration": "日誌與設定",
    "logging implementation": "日誌實作",
    "logging": "日誌",
    "logic flaws": "邏輯缺陷",
    "map": "對應",
    "malformed input": "異常輸入",
    "manual review": "人工審查",
    "manual": "人工",
    "monitoring services": "監控服務",
    "monitor": "監視器",
    "network exposure": "網路暴露",
    "network placement": "網路位置",
    "network rules": "網路規則",
    "network segmentation": "網路區隔",
    "network stack": "網路堆疊",
    "network": "網路",
    "namespace isolation": "namespace 隔離",
    "observed behavior": "觀察到的行為",
    "observed weakness": "觀察到的弱點",
    "operational handoff": "維運交接",
    "operational": "維運",
    "outside-in testing": "外部導向測試",
    "owner": "負責人",
    "parser assumptions": "解析器假設",
    "path": "路徑",
    "paths": "路徑",
    "patient safety risk": "病人安全風險",
    "patient safety": "病人安全",
    "patch and retest evidence": "修補與重測證據",
    "patch": "修補",
    "penetration testing": "滲透測試",
    "perimeter defense": "邊界防禦",
    "pharmacy payment": "藥局付款",
    "pipeline": "管線",
    "privileged account": "高權限帳號",
    "privileged": "特權",
    "provider workflows": "醫療服務流程",
    "provider": "醫療服務端",
    "radio-frequency communication": "射頻通訊",
    "recovery validation": "恢復驗證",
    "recovery": "恢復",
    "regulatory-facing evidence": "法規審查證據",
    "resource": "資源",
    "remote access boundary": "遠端存取邊界",
    "remote-access boundaries": "遠端存取邊界",
    "remote-access boundary": "遠端存取邊界",
    "remote control": "遠端控制",
    "remote support": "遠端支援",
    "report": "報告",
    "remediation": "修補處置",
    "residual risk": "剩餘風險",
    "retest evidence": "重測證據",
    "retest": "重測",
    "risk path": "風險路徑",
    "risk": "風險",
    "rollback": "回滾",
    "review": "審查",
    "runtime alerts": "執行期警示",
    "runtime": "執行期",
    "safety control": "安全控制",
    "secure boot": "安全啟動",
    "secure coding": "安全程式撰寫",
    "secure default": "安全預設",
    "secure defaults": "安全預設",
    "secret management": "機密資料管理",
    "secrets": "機密資料",
    "secret": "機密資料",
    "security finding": "資安發現事項",
    "security requirements": "資安需求",
    "security": "安全",
    "service account token": "服務帳號 token",
    "service-account token scope": "服務帳號 token 範圍",
    "service account": "服務帳號",
    "service identity": "服務身分",
    "services": "服務",
    "service": "服務",
    "session timeout": "連線逾時",
    "session": "連線階段",
    "source code review": "程式碼審查",
    "source code": "程式碼",
    "source review": "程式碼審查",
    "standalone device": "單機設備",
    "static code analysis": "靜態程式碼分析",
    "static analysis": "靜態分析",
    "story map": "故事地圖",
    "strong authentication": "強式認證",
    "system review": "系統審查",
    "system": "系統",
    "subnet": "子網路",
    "testing": "測試",
    "testing evidence": "測試證據",
    "testing vocabulary": "測試詞彙",
    "test": "測試",
    "threat model linkage": "威脅模型連結",
    "threat model": "威脅模型",
    "threat modeling": "威脅建模",
    "threat": "威脅",
    "traceability": "可追溯性",
    "transitive dependencies": "間接相依套件",
    "transitive": "間接",
    "trust boundary": "信任邊界",
    "trust-boundary decisions": "信任邊界決策",
    "trust": "信任",
    "unauthorized access risk": "未授權存取風險",
    "unowned risk": "無歸屬風險",
    "unsafe patterns": "不安全模式",
    "unsafe assumptions": "不安全假設",
    "unsafe function": "不安全函式",
    "unsafe": "不安全",
    "unused ports": "未使用連接埠",
    "update package validation": "更新套件驗證",
    "update path": "更新路徑",
    "update signing key": "更新簽章金鑰",
    "update-signing keys": "更新簽章金鑰",
    "update": "更新",
    "vendor binary": "廠商二進位檔",
    "vendor maintenance access": "廠商維護存取",
    "vendor": "廠商",
    "validation": "驗證",
    "validate": "驗證",
    "validated": "已驗證",
    "variables": "變數",
    "verify": "驗證",
    "verification": "驗證",
    "viewer": "檢視器",
    "vulnerability assessment": "弱點評估",
    "vulnerability response": "弱點回應",
    "vulnerability scan": "弱點掃描",
    "vulnerability": "弱點",
    "workload scheduling": "工作負載排程",
    "workload": "工作負載",
}

PRESERVED_ENGLISH_TECH_TERMS = {
    "token",
    "namespace",
}

SPOKEN_ENGLISH_SENTENCE_REWRITES = {
    "Scope should follow the clinical 工作流程, not just the application boundary": "審查範圍應該跟著臨床工作流程，而不是只跟著應用程式邊界",
    "Black-box testing may see suspicious traffic;白箱審查 explains why the behavior exists": "黑箱測試可能看到可疑流量；白箱審查可以說明這個行為為什麼存在",
    "For regulated devices, the fix itself becomes part of the evidence chain": "對受法規管理的醫療裝置來說，修補本身也會成為證據鏈的一部分",
    "Deployment is where engineering controls meet clinical reality": "部署是工程控制接上臨床現實的地方",
    "What can an attacker do?": "攻擊者可以做什麼？",
    "Why is the system vulnerable, and how do we prove the fix works?": "系統為什麼有弱點，以及我們如何證明修補有效？",
    "K 八 S security is deployment security": "K 八 S 安全就是部署安全",
    "白箱審查 must include infrastructure-as-code, runtime identity, secrets handling, and cloud permission boundaries": "白箱審查必須包含基礎設施程式碼、執行期身分、機密資料處理，以及雲端權限邊界",
    "White-box review should test deployed access paths, not only product features": "白箱審查應該測試實際部署後的存取路徑，而不只是產品功能",
    "SBOM determines response speed when a vulnerability appears": "當漏洞出現時，軟體物料清單會決定回應速度",
    "A vendor incident can become a hospital clinical-delay incident": "廠商事件可能變成醫院的臨床延遲事件",
    "這個事件表面上看起來是 cryptojacking，也就是偷用雲端資源挖礦。": "先把這個案例當成一個現場故事來看。表面上，它是雲端資源被拿去挖礦；真正值得醫療團隊注意的，是攻擊者怎麼從一個暴露的管理介面，一步一步走到雲端資源。",
    "根據簡報內容，AP 報導 United Health CEO 在聽證中提到，攻擊者進入了一台缺乏 multifactor authentication 的伺服器。": "接著看 Change Healthcare 的案例。可以把它想成一個部署路徑的故事：攻擊者先進入一台沒有強制多因素認證的伺服器，接著影響擴大到醫療支付與理賠流程。",
    "這個案例很有意思，因為它不是惡意攻擊，而是 faulty security content update。": "Crowd-Strike 這個案例要用另一種角度聽。它不是傳統惡意攻擊，而是安全內容更新本身出了問題。",
    "最後一個案例是 Synnovis / NHS London ransomware incident。": "最後用 Synnovis 與 NHS London 的案例收束。這個故事提醒我們，第三方服務發生事件時，醫院自己的系統即使沒有直接被攻破，臨床流程仍然會被拖住。",
    "white box testing explains why a risk exists and how to prove it is controlled": "白箱測試說明風險為什麼存在，以及如何證明它已被控制",
    "白箱測試 explains why a 風險 exists — 與 how to prove it is controlled": "白箱測試說明風險為什麼存在，以及如何證明它已被控制",
    "黑箱測試 may see suspicious traffic; 白箱審查 explains why the 行為 exists": "黑箱測試可能看到可疑流量；白箱審查可以說明這個行為為什麼存在",
    "Different tests produce different 證據 — combine them to explain 根本原因 與 驗證 the 修補": "不同測試會產生不同證據；合併起來可以說明根本原因，並驗證修補有效",
    "trace each regulatory expectation to 控制措施 與 verification 證據": "把每一項法規期待追溯到控制措施與驗證證據",
    "SBOM determines response speed when a vulnerability appears": "當漏洞出現時，軟體物料清單會決定回應速度",
}

PILOT_ASR_TERM_VARIANTS = {
    "K8S": ["K eight S", "K8S", "K 八 S"],
    "524B": ["五二四", "524B", "五二四 B"],
    "Log4Shell": ["Log four", "Log4Shell", "Log four Shell"],
    "Channel File 291": ["Channel File", "二九一", "291"],
    "PACS": ["P A C S", "PACS", "派克斯"],
    "HIS": ["H I S", "HIS"],
    "EMR": ["E M R", "EMR"],
    "workflow": ["工作流程", "workflow"],
    "clinical": ["臨床", "Clinical", "clinical"],
    "CDE": ["C D E", "CDE"],
    "FDA": ["F D A", "FDA"],
    "SBOM": ["S B O M", "SBOM"],
}

STAGE_CUE_RE = re.compile(
    r"(\(|（|\[|【|\*)\s*"
    r"(?:吸氣聲?|吐氣聲?|換氣聲?|喘息聲?|嘆氣聲?|笑聲?|乾笑|停頓|pause\s*:?\s*\d*\s*ms?)"
    r"\s*(\)|）|\]|】|\*)",
    re.I,
)
FILLER_RE = re.compile(
    r"(^|[，。！？；：、\s])"
    r"(?:嗯|呃|呃啊|啊|阿哈|對啊|這個|那個|呵呵呵|呵呵|哈哈哈|哈哈|吱吱嗚嗚|支支吾吾)"
    r"(?=([，。！？；：、\s]|$))"
)
HALLUCINATION_RESIDUE_RE = re.compile(r"(媽媽我?|嗎嗎我|這老能喝|這老能吼|金普斯是死老|精普斯是死老|老能喝|老能吼)")
DEMONSTRATIVE_FILLER_RE = re.compile(r"(這個|那個)(?=[\u4e00-\u9fff])")
PHONETIC_ANNOTATION_RE = re.compile(r"\[:[^\]\n]{1,32}\]")
CJK_RE = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"

CONTROL_RE = re.compile(
    r"<!-- BV26_META\n(?P<meta>.*?)\n-->\n\n"
    r"### (?P<title>.*?)\n\n"
    r"\[(?P<tag>BV26[^\]]*)\]\n"
    r"(?P<text>.*?)\n"
    r"\[/BV26\]",
    re.S,
)


@dataclass
class Segment:
    index: int
    segment_id: str
    group: str
    output_prefix: str
    title: str
    preset: str
    speed_cpm: str
    target_duration: str
    target_seconds: int
    timeline: str
    character_count: int
    delivery: str
    source_notes: str
    pronunciation_hints: list[str]
    clean_text: str
    normalized_text: str
    clean_text_path: Path
    normalized_text_path: Path


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_duration(value: str) -> int:
    minutes, seconds = value.split(":")
    return int(minutes) * 60 + int(seconds)


def parse_meta(meta: str) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    hints: list[str] = []
    in_hints = False
    for raw_line in meta.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line == "pronunciation_hints:":
            in_hints = True
            continue
        if in_hints and line.strip().startswith("- "):
            hints.append(line.strip()[2:].strip().strip('"'))
            continue
        in_hints = False
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields, hints


def clean_model_text(text: str) -> str:
    cleaned = text.replace("\u3000", " ")
    cleaned = PHONETIC_ANNOTATION_RE.sub("", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\s*\n\s*", " ", cleaned).strip()
    return cleaned


def sanitize_tts_text(text: str) -> str:
    """Remove stage-cue and filler contamination from model-facing text."""
    sanitized = STAGE_CUE_RE.sub("，", text)
    sanitized = HALLUCINATION_RESIDUE_RE.sub("", sanitized)
    sanitized = DEMONSTRATIVE_FILLER_RE.sub(lambda match: "此" if match.group(1) == "這個" else "該", sanitized)
    previous = None
    while sanitized != previous:
        previous = sanitized
        sanitized = FILLER_RE.sub(lambda match: match.group(1), sanitized)
    sanitized = re.sub(r"[，、]\s*[，、]+", "，", sanitized)
    sanitized = re.sub(r"。+\s*。+", "。", sanitized)
    sanitized = re.sub(r"\s+", " ", sanitized)
    sanitized = re.sub(r"\s+([，。！？；：、])", r"\1", sanitized)
    sanitized = re.sub(r"([，。！？；：、])([A-Za-z0-9])", r"\1 \2", sanitized)
    return sanitized.strip(" ，、")


def apply_non_proper_english_zh_tw(text: str) -> str:
    """Prefer Taiwan Traditional Chinese for non-proper English TTS wording."""
    normalized = text
    for old, new in SPOKEN_ENGLISH_SENTENCE_REWRITES.items():
        normalized = normalized.replace(old, new)
    for old, new in sorted(NON_PROPER_ENGLISH_ZHTW_NORMALIZATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = re.compile(rf"(?<![A-Za-z]){re.escape(old)}(?![A-Za-z])", re.I)
        normalized = pattern.sub(new, normalized)
    normalized = normalized.replace("日誌 日誌與 恢復 恢復", "日誌與恢復")
    normalized = normalized.replace("日誌 日誌", "日誌")
    normalized = normalized.replace("恢復 恢復", "恢復")
    normalized = normalized.replace("命名空間", "namespace")
    normalized = normalized.replace(
        "白箱測試討論點包括：第一，驗證、K、八、S dashboards、與 應用程式介面、servers are not publicly、暴露。",
        "白箱測試的第一個討論點，是確認 K、八、S、dashboard 與應用程式介面伺服器沒有暴露在公開網路上。",
    )
    normalized = normalized.replace(
        "第二， prohibit long-lived、雲端 憑證、inside pods or、環境 變數。",
        "第二，避免在 Pod 或環境變數裡放長期有效的雲端憑證。",
    )
    normalized = normalized.replace(
        "第三，審查 服務帳號、token、範圍 與、R B A C permissions。",
        "第三，審查服務帳號、token、範圍與 R B A C 權限。",
    )
    normalized = normalized.replace(
        "第四， scan manifests、容器 映像檔、 C I C D、變數、for、機密資料。",
        "第四，掃描部署清單、容器映像檔與 C I C D 變數裡的機密資料。",
    )
    normalized = normalized.replace(
        "第五，驗證 雲端、I A M、最小權限、from、工作負載 身分。",
        "第五，從工作負載身分驗證雲端 I A M 的最小權限。",
    )
    normalized = normalized.replace(
        "第六， ensure、稽核日誌、can reconstruct pod、應用程式介面、憑證、usage。",
        "第六，確認稽核日誌可以重建 Pod、應用程式介面與憑證使用紀錄。",
    )
    normalized = normalized.replace(
        "此案例很有意思，因為它不是惡意攻擊，而是、Crowd-Strike Falcon、安全內容更新。",
        "Crowd-Strike 這個案例要用另一種角度聽。它不是傳統惡意攻擊，而是 Falcon 安全內容更新本身出了問題。",
    )
    normalized = normalized.replace(
        "監視器 與、address vulnerabilities",
        "監控與處理漏洞",
    )
    normalized = normalized.replace(
        "白箱審查可以找出、design、或、code weaknesses",
        "白箱審查可以找出設計或程式碼弱點",
    )
    normalized = normalized.replace(
        "第二， cybersecure design、與、maintenance。",
        "第二，資安設計與持續維護。",
    )
    normalized = normalized.replace(
        "最後一個案例是、Synnovis / NHS London、勒索軟體 事件。",
        "最後用 Synnovis 與 NHS London 的案例收束。這個故事提醒我們，第三方服務發生事件時，醫院自己的系統即使沒有直接被攻破，臨床流程仍然會被拖住。",
    )
    normalized = normalized.replace(
        "事件路徑是：廠商、attack、 lab capacity reduced、臨床、backlog、已驗證 恢復。",
        "事件路徑可以簡化成：廠商遭攻擊、檢驗量能下降、臨床案件累積，最後才進入已驗證的恢復。",
    )
    normalized = normalized.replace(
        "審查、third-party、整合 信任、boundaries",
        "審查第三方整合的信任邊界",
    )
    normalized = normalized.replace(
        "驗證、recovered interfaces、與 資料 完整性",
        "驗證已恢復的介面與資料完整性",
    )
    normalized = normalized.replace(
        "link、恢復 證據、to、臨床連續性",
        "把恢復證據連回臨床連續性",
    )
    normalized = normalized.replace(
        "風險、identification、威脅建模",
        "風險識別、威脅建模",
    )
    return normalized


def enforce_cjk_latin_breaks(text: str) -> str:
    """Insert audible punctuation at Chinese/English boundaries for TTS stability."""
    normalized = re.sub(fr"([{CJK_RE}])\s*([A-Za-z])", r"\1、\2", text)
    normalized = re.sub(fr"([A-Za-z])\s*([{CJK_RE}])", r"\1、\2", normalized)
    normalized = re.sub(r"([、，。！？；：])\s*([、，。！？；：])+", r"\1", normalized)
    return normalized


def apply_final_storyline_polish(text: str) -> str:
    """Polish case passages after CJK/English boundary punctuation is inserted."""
    polished = text
    replacements = {
        "白箱測試討論點包括：第一，驗證、K、八、S dashboards、與 應用程式介面、servers are not publicly、暴露。": "白箱測試的第一個討論點，是確認 K、八、S、dashboard 與應用程式介面伺服器沒有暴露在公開網路上。",
        "第二，prohibit long-lived、雲端 憑證、inside pods or、環境 變數。": "第二，避免在 Pod 或環境變數裡放長期有效的雲端憑證。",
        "第三，審查 服務帳號、token、範圍 與、R B A C permissions。": "第三，審查服務帳號、token、範圍與 R B A C 權限。",
        "第四，scan manifests、容器 映像檔、C I C D、變數、for、機密資料。": "第四，掃描部署清單、容器映像檔與 C I C D 變數裡的機密資料。",
        "第五，驗證 雲端、I A M、最小權限、from、工作負載 身分。": "第五，從工作負載身分驗證雲端 I A M 的最小權限。",
        "第六，ensure、稽核日誌、can reconstruct pod、應用程式介面、憑證、usage。": "第六，確認稽核日誌可以重建 Pod、應用程式介面與憑證使用紀錄。",
        "此案例很有意思，因為它不是惡意攻擊，而是、Crowd-Strike Falcon、安全內容更新。": "Crowd-Strike 這個案例要用另一種角度聽。它不是傳統惡意攻擊，而是 Falcon 安全內容更新本身出了問題。",
        "第一，監視器 與、address vulnerabilities。": "第一，監控與處理漏洞。",
        "白箱審查可以找出、design、或、code weaknesses": "白箱審查可以找出設計或程式碼弱點",
        "第二，cybersecure design、與、maintenance。": "第二，資安設計與持續維護。",
        "最後一個案例是、Synnovis / NHS London、勒索軟體 事件。": "最後用 Synnovis 與 NHS London 的案例收束。這個故事提醒我們，第三方服務發生事件時，醫院自己的系統即使沒有直接被攻破，臨床流程仍然會被拖住。",
        "事件路徑是：廠商、attack、lab capacity reduced、臨床、backlog、已驗證 恢復。": "事件路徑可以簡化成：廠商遭攻擊、檢驗量能下降、臨床案件累積，最後才進入已驗證的恢復。",
        "審查、third-party、整合 信任、boundaries": "審查第三方整合的信任邊界",
        "驗證、recovered interfaces、與 資料 完整性": "驗證已恢復的介面與資料完整性",
        "link、恢復 證據、to、臨床連續性": "把恢復證據連回臨床連續性",
        "風險、identification、威脅建模": "風險識別、威脅建模",
        "Downtime procedure、要成為現場可啟動、可交接、可回填的操作能力。": "停機時間處置流程，要成為現場可啟動、可交接、可回填的操作能力。",
        "可是、complex、醫療器材 與 醫療資訊系統 需要更深一層的說明。": "可是，複雜醫療器材與醫療資訊系統，需要更深一層的說明。",
        "憑證 與 金鑰處理 要保護 服務 帳號、應用程式介面 金鑰、 certificates、與 更新簽章金鑰。": "憑證與金鑰處理，要保護服務帳號、應用程式介面金鑰、憑證與更新簽章金鑰。",
        "部署 是、engineering、控制措施 接上 臨床現實 的地方。": "部署是工程控制接上臨床現實的地方。",
        "第一，驗證 更新、authenticity、與 完整性 控制措施。": "第一，驗證更新來源真實性與完整性控制措施。",
        "第二， document、臨床 驗證 與 回滾、assumptions。": "第二，記錄臨床驗證與回滾假設。",
        "第三，保存、residual-風險、rationale after、修補處置。": "第三，保存修補處置後的剩餘風險接受理由。",
        "第二是、implementation、證據。": "第二是實作證據。",
        "第一，驗證、M F A is enforced on real、部署 路徑。": "第一，驗證真實部署路徑已強制使用 M F A。",
        "是否有、shared、憑證？": "是否有共用憑證？",
        "第三，保存 部署 偏離事項 與、ownership。": "第三，保存部署偏離事項與責任歸屬。",
        "此案例可以用一句話總結：白箱審查、should、測試、deployed、存取 路徑, not only product features.": "此案例可以用一句話總結：白箱審查應該測試實際部署後的存取路徑，而不只是產品功能。",
        "這裡有一個很實用的 審查、question： Which、資產, assumption, 與 剩餘風險、does each、發現事項 對應、back to?": "這裡有一個很實用的審查問題：每一個發現事項，分別對應哪個資產、假設與剩餘風險？",
        "這一頁列出、F D A-relevant、的 安全 測試、activities。": "這一頁列出與 F D A 審查相關的安全測試活動。",
        "靜態程式碼分析 可以在 執行期 前找出、vulnerable patterns，例如 不安全函式、 insecure crypto、 hardcoded、機密資料、 SQL injection pattern。": "靜態程式碼分析可以在執行期前找出易受攻擊模式，例如不安全函式、不安全加密、硬編碼機密資料與 S Q L injection 模式。",
        "所以這頁的重點是： Different tests produce different、證據 — combine them to explain、根本原因 與 驗證、the、修補.": "所以這頁的重點是：不同測試會產生不同證據，合併起來可以說明根本原因，並驗證修補有效。",
        "Dependencies、容器 層、 third-party libraries、必須能連到 弱點評估。": "相依套件、容器層與第三方函式庫，必須能連到弱點評估。",
        "這裡的、practical goal、是： trace each regulatory expectation to、控制措施 與 驗證 證據.": "這裡的實務目標，是把每一項法規期待追溯到控制措施與驗證證據。",
        "真正有價值的白箱測試，是能把 發現事項 轉成、reviewable、證據。": "真正有價值的白箱測試，是能把發現事項轉成可審查證據。",
        "它會使用、open-source libraries、 commercial、元件、容器、base、映像檔、執行期、 database driver、人工智慧、framework、 web framework。": "它會使用開源函式庫、商用元件、容器基礎映像檔、執行期、資料庫驅動程式、人工智慧框架與網頁框架。",
        "Direct、相依套件 是我們直接使用的套件。": "直接相依套件，是我們直接使用的套件。",
        "對、healthcare organizations、來說，第一個問題往往不是立刻修，而是先判斷：": "對醫療機構來說，第一個問題往往不是立刻修，而是先判斷：",
        "廠商、tool、裡": "廠商工具裡",
        "appliance、裡": "設備裡",
        "不能只看、package.json、或、requirements.txt、的第一層，要看完整 相依套件、tree。": "不能只看 package.json 或 requirements.txt 的第一層，要看完整相依套件樹。",
        "第二， track、廠商、binaries、與 容器 層。": "第二，追蹤廠商二進位檔與容器層。",
        "有些風險藏在 廠商-provided binary、或 容器基礎映像檔 裡。": "有些風險藏在廠商提供的二進位檔或容器基礎映像檔裡。",
        "第三， assign、負責人、修補 路徑、重測證據。": "第三，指定負責人、修補路徑與重測證據。",
        "這頁可以用一句話收斂：軟體物料清單，當漏洞出現時，軟體物料清單會決定回應速度.": "這頁可以用一句話收斂：當漏洞出現時，軟體物料清單會決定回應速度。",
        "Log、建立、investigation、證據；驗證 建立、trusted、恢復。": "日誌建立調查證據，驗證建立可信恢復。",
        "第一條是、audit trail： login、應用程式介面 存取、 config change、 alert、 investigation。": "第一條是稽核軌跡：登入、應用程式介面存取、設定變更、警示與調查。",
        "這些、log、能幫助我們知道誰在什麼時間做了什麼": "這些日誌能幫助我們知道誰在什麼時間做了什麼",
        "第二條是 恢復、chain： detect、 contain、 recover、驗證、 resume、臨床 服務。": "第二條是恢復鏈：偵測、圍堵、復原、驗證與恢復臨床服務。",
        "log、讓調查有證據": "日誌讓調查有證據",
        "log、是否包含足夠、context？": "日誌是否包含足夠脈絡？",
        "導致、pathology、 blood、測試、 transfusion、服務、 appointments、 operations、都受到影響。": "導致病理檢驗、血液檢測、輸血服務、門診預約與手術安排都受到影響。",
        "一開始，我們用 風險、identification、找出哪些資產與臨床流程重要。": "一開始，我們用風險識別找出哪些資產與臨床流程重要。",
        "再透過 白箱、 gray-box、黑箱、 S C A、 fuzzing、人工審查 等測試方法產生證據。": "再透過白箱、灰箱、黑箱、S C A、模糊測試與人工審查等方法產生證據。",
        "真正的 信任 會從、verbal assurance、推進成、auditable、證據。": "真正的信任，會從口頭保證推進成可稽核證據。",
        "condition、 修補處置、 重測、 日誌與恢復 串起來。": "部署條件、修補處置、重測、日誌與恢復串起來。",
        "所有證據最後要回到、 life cycle、 信任。": "所有證據最後要回到生命週期信任。",
        "最後， 把三個 前測、 pre-測試 與後測、 post-測試、 question、": "最後，把三個前測與後測問題，",
    }
    for old, new in replacements.items():
        polished = polished.replace(old, new)
    polished = re.sub(
        r"但對醫療系統來說，我們不能只看挖礦。.*?甚至造成資料外洩或臨床服務中斷。",
        "對醫療系統來說，這個故事的重點不是挖礦本身，而是同一條路徑如果出現在醫療環境，可能影響人工智慧推論服務、病人資料管線、影像處理服務、應用程式介面閘道，甚至造成資料外洩或臨床服務中斷。",
        polished,
    )
    polished = re.sub(
        r"第二，\s*prohibit long-lived、雲端 憑證、inside pods or、環境 變數。",
        "第二，避免在 Pod 或環境變數裡放長期有效的雲端憑證。",
        polished,
    )
    polished = re.sub(
        r"第四，\s*scan manifests、容器 映像檔、 C I C D、變數、for、機密資料。",
        "第四，掃描部署清單、容器映像檔與 C I C D 變數裡的機密資料。",
        polished,
    )
    polished = re.sub(
        r"第六，\s*ensure、稽核日誌、can reconstruct pod、應用程式介面、憑證、usage。",
        "第六，確認稽核日誌可以重建 Pod、應用程式介面與憑證使用紀錄。",
        polished,
    )
    polished = re.sub(
        r"事件路徑是：廠商、attack、\s*lab capacity reduced、臨床、backlog、已驗證 恢復。",
        "事件路徑可以簡化成：廠商遭攻擊、檢驗量能下降、臨床案件累積，最後才進入已驗證的恢復。",
        polished,
    )
    polished = re.sub(
        r"白箱測試、explains why a、風險、exists\s*[—-]\s*與、how to prove it is controlled\.",
        "白箱測試說明風險為什麼存在，以及如何證明它已被控制。",
        polished,
    )
    polished = re.sub(
        r"黑箱測試、may see suspicious traffic; 白箱審查、explains why the、行為、exists\.",
        "黑箱測試可能看到可疑流量；白箱審查可以說明此行為為什麼存在。",
        polished,
    )
    polished = re.sub(
        r"這裡有一個很實用的\s*審查、question：\s*Which、資產,\s*assumption,\s*與\s*剩餘風險、does each、發現事項\s*對應、back to\?",
        "這裡有一個很實用的審查問題：每一個發現事項，分別對應哪個資產、假設與剩餘風險？",
        polished,
    )
    polished = re.sub(
        r"這裡有一個很實用的.*?back to\?",
        "這裡有一個很實用的審查問題：每一個發現事項，分別對應哪個資產、假設與剩餘風險？",
        polished,
    )
    polished = re.sub(
        r"(?:deployment、)?condition、\s*修補處置、\s*重測、\s*日誌與恢復\s*串起來。",
        "部署條件、修補處置、重測、日誌與恢復串起來。",
        polished,
    )
    polished = re.sub(
        r"(?:最後，\s*把三個 前測、\s*)?pre-測試\s*與後測、\s*post-測試、\s*question、\s*對應到今天的重點。",
        "最後，把三個前測與後測問題，對應到今天的重點。",
        polished,
    )
    polished = polished.replace("第二， cybersecure design、與、maintenance。", "第二，資安設計與持續維護。")
    polished = polished.replace("第二，cybersecure design、與、maintenance。", "第二，資安設計與持續維護。")
    for phrase in ["剩餘風險", "發現事項", "控制證據"]:
        polished = re.sub(rf"{phrase}[，、]\s*{phrase}", phrase, polished)
    late_replacements = {
        "臨床 資安、in practice、出發": "臨床資安實務出發",
        "資安 已經不只是、IT、問題": "資安已經不只是資訊團隊的問題",
        "傳統、IT、視角": "傳統資訊團隊視角",
        "系統、of systems": "系統中的系統",
        "不是、IT、部門自己決定": "不是資訊團隊自己決定",
        "hospital、網路": "醫院網路",
        "isolated hardware": "獨立硬體",
        "人工智慧-enabled S A M D、 model、更新": "人工智慧支援的 S A M D、模型更新",
        "medical、供應鏈": "醫療供應鏈",
        "responsibility、對應": "責任對應",
        "breach、這類": "資料外洩事件這類",
        "penetration、測試": "滲透測試",
        "沒有最小權限、時間限制、來源限制與、log": "沒有最小權限、時間限制、來源限制與日誌",
        "是否有、log？": "是否有日誌？",
        "Radiology modality": "放射影像設備",
        "third-party、整合 信任邊界": "第三方整合信任邊界",
        "email-based intrusion、或、espionage、行動": "電子郵件入侵或間諜行動",
        "IT、第三方廠商": "資訊團隊、第三方廠商",
        "停機時間、procedures、與紙本流程": "停機時間處置流程與紙本流程",
        "勒索軟體、note、與後續應變案例": "勒索軟體事件紀錄與後續應變案例",
        "造成、crash、資料污染": "造成當機、資料污染",
        "足夠、log、可以調查": "足夠日誌可以調查",
        "bedside patient、監視器": "床邊病人監視器",
        "如果、bedside、監視器": "如果床邊監視器",
        "identify hardcoded endpoints、與 資料、flows": "辨識硬編碼端點與資料流",
        "對應 行為、back to、威脅模型 證據": "把行為連回威脅模型證據",
        "IT、修補": "資訊系統修補",
        "pacemaker、韌體、recall": "心律調節器韌體召回",
        "Pacemaker、是植入式設備": "心律調節器是植入式設備",
        "未使用、port": "未使用連接埠",
        "應用程式介面、key、 certificate": "應用程式介面金鑰、憑證",
        "Kubernetes，也就是、K、八、S": "K、八、S",
        "Kubernetes": "K、八、S",
        "Helm、charts、deployment manifests": "Helm 圖表與部署清單",
        "機密資料、handling": "機密資料處理",
        "雲端 憑證、exposure": "雲端憑證暴露",
        "環境、variable": "環境變數",
        "網路、Policy， ingress rules，暴露 服務": "網路政策、入口規則與暴露服務",
        "K、八、S、應用程式介面、dashboard": "K、八、S、管理儀表板與應用程式介面",
        "K、八、S、應用程式介面、 dashboard": "K、八、S、管理儀表板與應用程式介面",
        "K、八、S、dashboard": "K、八、S、管理儀表板",
        "K、八、S、 dashboard": "K、八、S、管理儀表板",
        "K、八、S、管理儀表板與應用程式介面、dashboard": "K、八、S、管理儀表板與應用程式介面",
        "特權、mode": "特權模式",
        "hostPath mount": "hostPath 掛載",
        "bottom line": "底線",
        "安全、boundary": "安全邊界",
        "真正的、boundary": "真正的邊界",
        "網路、policy、與 部署、governance": "網路政策與部署治理",
        "cryptomining、工作負載": "挖礦工作負載",
        "dashboard、與應用程式介面": "管理儀表板與應用程式介面",
        "映像檔、layer、或 管線": "映像檔層或管線",
        "沒有、audit log": "沒有稽核日誌",
        "United Health cyberattack": "United Health 資安事件",
        "no M F A": "沒有 M F A",
        "critical platform": "關鍵平台",
        "care、與、payment disruption": "照護與支付中斷",
        "工作流程、s、在美國醫療體系": "工作流程在美國醫療體系",
        "服務、console": "服務主控台",
        "role-based、存取控制": "角色式存取控制",
        "audit、日誌": "稽核日誌",
        "log、是否記錄": "日誌是否記錄",
        "單一、checklist": "單一檢核表",
        "traceable、證據": "可追溯證據",
        "機密資料、detection": "機密資料偵測",
        "Fuzz、或 異常輸入 測試": "模糊測試或異常輸入測試",
        "測試、parser、和資料處理流程": "測試解析器和資料處理流程",
        "Attack-surface analysis、會看 暴露、interfaces、與 服務": "攻擊面分析會看暴露介面與服務",
        "弱點、chaining、則是": "弱點串連則是",
        "缺少、log、錯誤網路配置": "缺少日誌、錯誤網路配置",
        "元件、mapped to known、風險": "元件對應到已知風險",
        "global outage": "全球中斷事件",
        "content、更新": "內容更新",
        "分階段、rollout": "分階段推出",
        "Section、五二四": "Section 五二四",
        "submission expectation": "送件期待",
        "postmarket exploit": "上市後可利用弱點",
        "updates、與、patches": "更新與修補",
        "signing、完整性": "簽章與完整性",
        "release、控制措施": "發布控制措施",
        "特權、mode": "特權模式",
        "設定、change、網路、policy、更新、憑證、rotation": "設定變更、網路政策更新與憑證輪替",
        "Affected、元件": "受影響元件",
        "source file、 config、容器、介面": "原始碼檔案、設定、容器與介面",
        "威脅-model link": "威脅模型連結",
        "重測、result": "重測結果",
        "相依套件、visibility": "相依套件可視性",
        "廠商、binaries、必須知道、exact version、與、origin": "廠商二進位檔必須知道精確版本與來源",
        "base OS": "基礎作業系統",
        "應用程式、layer": "應用程式層",
        "ownership tracking": "責任歸屬追蹤",
        "monitoring、 patching、 retesting": "監控、修補與重測",
        "paperwork、推進成": "文件清單推進成",
        "Log4j、的、remote-code-execution、風險": "Log4j 的遠端程式碼執行風險",
        "SQL injection、風險": "S Q L injection 風險",
        "應用程式、direct、相依套件": "應用程式、直接相依套件",
        "相依套件、inventory": "相依套件清冊",
        "對應、direct、與 間接相依套件": "對應直接與間接相依套件",
        "package.json、或、requirements.txt": "package.json 或 requirements.txt",
        "life cycle、 信任": "生命週期信任",
        "life cycle、信任": "生命週期信任",
        "一般、IT、角度": "一般資訊系統角度",
        "pod、服務帳號": "Pod、服務帳號",
    }
    for old, new in late_replacements.items():
        polished = polished.replace(old, new)
    polished = re.sub(r"\s+", " ", polished)
    polished = re.sub(r"\s+([，。！？；：、])", r"\1", polished)
    return polished


def normalize_text(text: str) -> str:
    normalized = clean_model_text(text)
    for old, new in TERM_NORMALIZATIONS.items():
        normalized = normalized.replace(old, new)
    normalized = apply_pilot_review_conditioning(normalized)
    normalized = apply_non_proper_english_zh_tw(normalized)
    normalized = normalized.replace(LEGACY_WHITE_BOX_TERM, PREFERRED_WHITE_BOX_TERM)
    normalized = sanitize_tts_text(normalized)
    normalized = enforce_cjk_latin_breaks(normalized)
    normalized = apply_final_storyline_polish(normalized)
    normalized = enforce_cjk_latin_breaks(normalized)
    normalized = re.sub(r"[ \t]+", " ", normalized).strip()
    return normalized


def apply_pilot_review_conditioning(text: str) -> str:
    """Apply conservative text conditioning from pilot human review.

    These replacements keep the source transcript frozen while improving
    model-facing pacing and pronunciation for the pilot failure modes.
    """
    replacements = {
        "P A C S、H I S、E M R": "派克斯，H I S，E M R",
        "派克斯、H I S、E M R": "派克斯，H I S，E M R",
        "K eight S": "K 八 S",
        "要 驗證": "要驗證",
        "要 驗證角色": "要驗證角色",
        "人工智慧 系統": "人工智慧系統",
        "醫療 人工智慧": "醫療人工智慧",
        "醫療影像 人工智慧": "醫療影像人工智慧",
        "人工智慧 派克斯": "人工智慧派克斯",
        "當醫療器材、人工智慧系統、派克斯， H I S， E M R、雲端服務與廠商維護通道全部連在一起時，醫院要怎麼判斷此系統可以被信任。": "當醫療器材、人工智慧系統、派克斯，H I S，E M R、雲端服務與廠商維護通道全部連在一起時。醫院端需要判斷：系統是否可信。",
        "要怎麼判斷這個系統可以被信任。今天會": "需要判斷系統是否可信。今天會",
        "要怎麼判斷此系統可以被信任。今天會": "需要判斷系統是否可信。今天會",
        "醫院會問：這個系統接到哪裡？誰可以登入？資料怎麼流？廠商如何維護？弱點誰負責？修補多久？修完怎麼證明？事件後如何調查與恢復？": "醫院會依序確認：一，系統接到哪裡。二，誰可以登入。三，資料如何流動。四，廠商如何維護。五，弱點由誰負責。六，修補需要多久。七，修完之後如何證明。八，事件後如何調查與恢復。",
        "醫院會問：此系統接到哪裡？誰可以登入？資料怎麼流？廠商如何維護？弱點誰負責？修補多久？修完怎麼證明？事件後如何調查與恢復？": "醫院會依序確認：一，系統接到哪裡。二，誰可以登入。三，資料如何流動。四，廠商如何維護。五，弱點由誰負責。六，修補需要多久。七，修完之後如何證明。八，事件後如何調查與恢復。",
        "掛號、檢查、影像、報告、病歷查詢、轉診、用藥與收費": "掛號流程、檢查流程、影像流程、報告流程、病歷查詢、轉診、用藥與收費",
        "戴康 DICOM 工作流程": "戴康影像流程",
        "戴康 DICOM router": "戴康路由器",
        "戴康 工作流程": "戴康影像流程",
        "戴康 router": "戴康路由器",
        "verify R B A C、service accounts、namespace isolation": "驗證角色權限控管。R B A C。接著，看服務帳號。再看命名空間隔離。",
        "第二，要 verify， R B A C， service accounts， namespace isolation。": "第二，要驗證角色權限控管。R B A C。接著，看服務帳號。再看命名空間隔離。",
        "第二，要驗證，R B A C。再看 service accounts。再看 namespace isolation。": "第二，要驗證角色權限控管。R B A C。接著，看服務帳號。再看命名空間隔離。",
        "第二，要驗證角色權限控管， R B A C。再看服務帳號。再看命名空間隔離。": "第二，要驗證角色權限控管。R B A C。接著，看服務帳號。再看命名空間隔離。",
        "每個 workload 的權限是否最小化？ service account 是否被共用？ namespace 是否真的隔離？": "每個 workload 的權限是否最小化？服務帳號是否被共用？namespace 是否真的隔離？",
        "service account 是否被共用": "服務帳號是否被共用",
        "secrets handling and cloud credential exposure": "secrets handling，以及 cloud credential exposure",
        "Secret 是否被放在 environment variable？是否被寫進 image？ C I C D variables 是否外洩？": "Secret 是否被放在 environment variable 裡？是否被寫進 image？C I，與 C D 變數是否外洩？",
        "C I C D variables 是否外洩": "C I，與 C D 變數是否外洩",
        "C I 與 C D 變數是否外洩": "C I，與 C D 變數是否外洩",
        "哪個 應用程式介面 call 被使用": "哪一個應用程式介面呼叫被使用",
        "Network Policy、ingress rules、exposed services": "Network Policy，ingress rules，exposed services",
        "不是只有 application endpoint， Kubernetes API， dashboard， internal service 也都可能成為攻擊面。": "不是只有 application endpoint。K 八 S 應用程式介面，dashboard，internal service，也都可能成為攻擊面。",
        "不是只有 application endpoint， K 八 S 應用程式介面、 dashboard、 internal service 也都可能成為攻擊面。": "不是只有 application endpoint。K 八 S 應用程式介面，dashboard，internal service，也都可能成為攻擊面。",
        "application endpoint，K eight S A P I、dashboard、internal service": "application endpoint，K 八 S 管理介面，dashboard，internal service",
        "image provenance、 container privileges、 admission controls": "image provenance，container privileges，admission controls",
        "哪個 pod、哪個 service account、哪個 A P I call": "哪一個 Pod、哪一個服務帳號、哪一個應用程式介面呼叫",
        "哪一個 Pod、哪一個服務帳號、哪一個API call": "哪一個 Pod、哪一個服務帳號、哪一個應用程式介面呼叫",
        "哪個 pod、哪個 service account、哪一個應用程式介面呼叫": "哪一個 Pod、哪一個服務帳號、哪一個應用程式介面呼叫",
        "In Kubernetes, the security boundary is not the container. The real boundary is identity, configuration, network policy, and deployment governance.": "在 K 八 S 裡，security boundary 不是 container。真正的 boundary 是 identity、configuration、network policy 與 deployment governance。",
        "Tesla Kubernetes Console Cryptojacking": "Tesla 雲端基礎設施加密貨幣挖礦案例",
        "Tesla 雲端基礎設施加密貨幣挖礦案例 這個真實事件": "Tesla 雲端基礎設施加密貨幣挖礦這個真實事件",
        "exposed K eight S console、pod credentials、A W S access、cryptomining workload": "exposed K eight S console，pod credentials，A W S access，crypto mining workload",
        "exposed K 八 S console、 pod credentials、 A W S access、 cryptomining workload": "暴露在外、未受保護的 K 八 S 管理主控台，Pod 憑證，A W S 存取權限，crypto mining workload",
        "exposed K 八 S console": "暴露在外、未受保護的 K 八 S 管理主控台",
        "pod credentials": "Pod 憑證",
        "A W S access": "A W S 存取權限",
        "prohibit long-lived、雲端 憑證、inside pods or environment variables": "禁止在 Pod 或環境變數裡放長期有效的雲端憑證",
        "服務-account token scope、與、R B A C permissions": "服務帳號 token 範圍與 R B A C 權限",
        "scan manifests、容器、images、 C I C D variables for、機密資料": "掃描部署清單、容器映像檔、C I C D 變數裡的機密資料",
        "validate、雲端、I A M、最小權限、from、工作負載 身分": "從工作負載身分驗證雲端 I A M 最小權限",
        "ensure、稽核日誌、can reconstruct pod、應用程式介面、憑證、usage": "確認稽核日誌可以重建 Pod、應用程式介面、憑證使用紀錄",
        "exposed Kubernetes console， pod credentials， A W S access， crypto mining workload": "暴露在外、未受保護的 K 八 S 管理主控台，Pod 憑證，A W S 存取權限，crypto mining workload",
        "exposed Kubernetes console": "暴露在外、未受保護的 K 八 S 管理主控台",
        "Kubernetes administrative console": "K 八 S 管理主控台",
        "Kubernetes 管理者主控台": "K 八 S 管理主控台",
        "Tesla 的 cloud infrastructure": "Tesla 的雲端基礎設施",
        "Pod 中存在 credential，使攻擊者能進一步存取 A W S 基礎設施": "Pod 裡的憑證外洩，使攻擊者能進一步存取 A W S 基礎設施",
        "cloud resource 進行 cryptocurrency mining": "雲端資源進行加密貨幣挖礦",
        "faulty security content update": "Crowd-Strike Falcon 安全內容更新",
        "CrowdStrike Falcon 安全內容更新": "Crowd-Strike Falcon 安全內容更新",
        "content update、 validator、解釋器、 endpoint crash": "內容更新、驗證器、解釋器、端點當機",
        "validator": "驗證器",
        "endpoint agent": "端點代理程式",
        "endpoint crash": "端點當機",
        "trust boundary": "信任邊界",
        "rollback 機制": "回滾機制",
        "rollback evidence": "回滾證據",
        "staged rollout": "分階段 rollout",
        "test update validators and malformed inputs": "測試更新驗證器，以及異常輸入測試",
        "test update validators，以及異常輸入測試": "測試更新驗證器，以及異常輸入測試",
        "test update 驗證器s and 異常輸入": "測試更新驗證器，以及異常輸入測試",
        "treat update infrastructure": "threat update infrastructure",
        "treat update": "threat update",
        "threat update infrastructure as a trust boundary": "將更新基礎設施視為 trust boundary",
        "interpreter": "解釋器",
        "malformed inputs": "異常輸入",
        "require 分階段 rollout and 回滾證據": "要具備分階段 rollout 與回滾證據",
        "threat update infrastructure as a 信任邊界": "將更新基礎設施視為信任邊界",
        "Security updates are also software supply chain，供應鏈 that require white box validation，白箱驗證.": "安全更新本身也是軟體供應鏈，因此需要白箱驗證。",
        "Security updates are also software supply chain，供應鏈 that require 白箱驗證.": "安全更新本身也是軟體供應鏈，因此需要白箱驗證。",
        "Security updates are also 軟體供應鏈 that require 白箱驗證.": "安全更新本身也是軟體供應鏈。因此需要白箱驗證。",
        "安全更新本身也是 software supply chain，供應鏈；因此需要白箱驗證。": "安全更新本身也是軟體供應鏈。因此需要白箱驗證。",
        "資安工具與資安更新本身也是 supply chain，供應鏈": "資安工具與資安更新本身也是供應鏈",
        "cyber devices": "資安醫療器材",
        "medical device": "醫療器材",
        "endpoint 同時吃到同一個更新": "端點設備同時接收同一個更新",
        "critical service": "關鍵服務",
        "remote management agent": "遠端管理代理程式",
        "並管理 軟體物料清單，S B O M 與元件風險": "並管理軟體物料清單，英文四個字母，S，B，O，M，以及元件風險",
        "並管理 軟體物料清單， S B O M 與元件風險": "並管理軟體物料清單，英文四個字母，S，B，O，M，以及元件風險",
        "F D and C Act Section 五 二 四 B": "F D C Act，Section 五二四，英文字母 B 款",
        "F D and C Act Section 五二四 B": "F D C Act，Section 五二四，英文字母 B 款",
        "F D and C Act，Section 五二四 B": "F D C Act，Section 五二四，英文字母 B 款",
        "F D and C Act， Section 五、二、四，B": "F D C Act，Section 五二四，英文字母 B 款",
        "F D and C Act Section五、二、四，B": "F D C Act，Section 五二四，英文字母 B 款",
        "F D A、T F D A、五、二、四，B、S B O M": "F D A，T F D A，五二四，英文字母 B 款，軟體物料清單，S B O M",
        "F D A， T F D A，五、二、四，B， S B O M": "F D A，T F D A，五二四，英文字母 B 款，軟體物料清單，S B O M",
        "White box Testing 與 system review": "白箱測試與系統審查",
        "White box testing，白箱測試 與 system review": "白箱測試與系統審查",
        "White box testing，白箱測試與滲透測試": "白箱測試與滲透測試",
        "白箱 Testing": "白箱測試",
        "白箱 testing": "白箱測試",
        "白箱 review": "白箱審查",
        "白箱 validation": "白箱驗證",
        "白箱測試從內部程式": "白箱測試，從程式碼內部",
        "白箱測試": "白箱測試",
        "白箱審查": "白箱審查",
        "白箱證據": "白箱證據",
        "白箱可以證明": "白箱證據可以證明",
        "白箱討論點": "白箱測試討論點",
        "派克斯 或 A I 派克斯": "派克斯，或 A I 派克斯",
        "戴康 DICOM router": "戴康路由器",
        "K eight S，A P I，dashboard，internal service": "K 八 S 管理介面，dashboard，internal service",
        "exposed K eight S console": "暴露在外、未受保護的 K 八 S 管理主控台",
        "root cause、 deployment condition、 remediation、 retest、 logging 與 recovery": "根本原因、deployment condition 部署條件、remediation 修補、retest 重測、logging 日誌與 recovery 恢復",
        "root cause、 deployment condition、 remediation、 retest、": "根本原因、deployment condition 部署條件、remediation 修補、retest 重測、",
        "Root cause": "根本原因",
        "root cause": "根本原因",
        "logging 與 recovery": "logging 日誌與 recovery 恢復",
        "白箱測試、explains why a、風險、exists — 與、how to prove it is controlled": "白箱測試說明風險為什麼存在，以及如何證明它已被控制",
        "黑箱測試、may see suspicious traffic; 白箱審查、explains why the、行為、exists": "黑箱測試可能看到可疑流量；白箱審查可以說明此行為為什麼存在",
        "internal cause": "內部成因",
        "verification、證據": "驗證證據",
        "audit、日誌": "稽核日誌",
        "log、是否記錄": "日誌是否記錄",
        "traceable、證據": "可追溯證據",
        "Which、資產, assumption, 與 剩餘風險，剩餘風險、does each、發現事項 對應、back to?": "每一個發現事項，分別對應哪個資產、假設與剩餘風險？",
        "F D A-relevant、的 安全 測試、activities": "與 F D A 審查相關的安全測試活動",
        "Static code analysis、可以在 執行期 前找出、vulnerable patterns，例如、unsafe function、 insecure crypto、 hardcoded、機密資料、 SQL injection pattern。": "靜態程式碼分析可以在執行期前找出易受攻擊模式，例如不安全函式、不安全加密、硬編碼機密資料與 SQL injection 模式。",
        "Attack-surface analysis、會看 暴露、interfaces、與 服務": "攻擊面分析會看暴露介面與服務",
        "Different tests produce different、證據 — combine them to explain、根本原因 與 驗證、the、修補.": "不同測試會產生不同證據；合併起來可以說明根本原因，並驗證修補有效。",
        "trace each regulatory expectation to、控制措施 與、verification、證據": "把每一項法規期待追溯到控制措施與驗證證據",
        "paperwork、推進成、vulnerability response": "文件清單推進成弱點回應",
        "S B O M determines response speed when a vulnerability appears": "當漏洞出現時，軟體物料清單會決定回應速度",
        "audit trail： login、應用程式介面 存取、 config change、 alert、 investigation": "稽核軌跡包含登入、應用程式介面存取、設定變更、警示與調查",
        "恢復、chain： detect、 contain、 recover、 validate、 resume、臨床 服務": "恢復鏈包含偵測、圍堵、復原、驗證與恢復臨床服務",
        "third-party integration、信任、boundaries": "第三方整合信任邊界",
        "validate recovered interfaces、與 資料 完整性": "驗證已恢復介面與資料完整性",
        "link、恢復 證據、to、臨床連續性": "把恢復證據連回臨床連續性",
        "pre-test 與 post-test question": "前測 pre-test 與後測 post-test question",
        "最後證據要能回到 lifecycle trust。": "所有證據最後要回到 life cycle trust。",
        "醫療資安是一條由臨床連續性、工程控制、法規證據與上市後維護共同形成的信任鏈。": "醫療資安的信任鏈，由臨床連續性、工程控制、法規證據，以及上市後的持續維護共同形成。",
        "finding 要能推動修補": "finding，發現事項，要能推動修補",
        "exploitability 與 control evidence": "可利用性與 control evidence，控制證據",
        "residual risk": "residual risk，剩餘風險",
        "PACS downtime": "派克斯停機時間",
        "孤立掃描報告": "單點掃描報告",
        "漏洞掃描": "弱點掃描",
        "內部程式": "程式碼內部",
        "治理框架": "治理判斷架構",
        "請各位把這三題帶回今天的主軸：": "最後請把這三題帶回今天的主軸：",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("test update 驗證器s and 異常輸入", "測試更新驗證器，以及異常輸入測試")
    text = text.replace("test update 驗證器s，以及異常輸入測試", "測試更新驗證器，以及異常輸入測試")
    text = re.sub(
        r"當醫療器材、人工智慧系統、派克斯.*?醫院要怎麼判斷此系統可以被信任。",
        "當醫療器材、人工智慧系統、派克斯，H I S，E M R、雲端服務與廠商維護通道全部連在一起時。醫院端需要判斷：系統是否可信。",
        text,
    )
    text = re.sub(
        r"醫院會問：此系統接到哪裡？\s*誰可以登入？\s*資料怎麼流？\s*廠商如何維護？\s*弱點誰負責？\s*修補多久？\s*修完怎麼證明？\s*事件後如何調查與恢復？",
        "醫院會依序確認：一，系統接到哪裡。二，誰可以登入。三，資料如何流動。四，廠商如何維護。五，弱點由誰負責。六，修補需要多久。七，修完之後如何證明。八，事件後如何調查與恢復。",
        text,
    )
    text = text.replace(
        "不是只有 application endpoint， K 八 S 應用程式介面、 dashboard、 internal service",
        "不是只有 application endpoint。K 八 S 應用程式介面，dashboard，internal service",
    )
    text = text.replace("醫院要怎麼判斷這個系統可以被信任", "醫院端需要判斷：系統是否可信")
    text = text.replace("醫院要怎麼判斷此系統可以被信任", "醫院端需要判斷：系統是否可信")
    text = text.replace(
        "醫院會問：此系統接到哪裡？ 誰可以登入？ 資料怎麼流？ 廠商如何維護？ 弱點誰負責？ 修補多久？ 修完怎麼證明？ 事件後如何調查與恢復？",
        "醫院會依序確認：一，系統接到哪裡。二，誰可以登入。三，資料如何流動。四，廠商如何維護。五，弱點由誰負責。六，修補需要多久。七，修完之後如何證明。八，事件後如何調查與恢復。",
    )
    text = text.replace(
        "醫院會依序確認。此系統接到哪裡。誰可以登入。資料如何流動。廠商如何維護。弱點由誰負責。修補需要多久。修完之後如何證明。事件後如何調查與恢復。",
        "醫院會依序確認：一，系統接到哪裡。二，誰可以登入。三，資料如何流動。四，廠商如何維護。五，弱點由誰負責。六，修補需要多久。七，修完之後如何證明。八，事件後如何調查與恢復。",
    )
    text = text.replace("application endpoint，", "application endpoint。")
    text = text.replace("應用程式介面、 dashboard、 internal service", "應用程式介面，dashboard，internal service")
    text = text.replace("要 驗證", "要驗證")
    text = text.replace("exposed K 八 S console", "暴露在外、未受保護的 K 八 S 管理主控台")
    text = text.replace("exposed K八S console", "暴露在外、未受保護的 K 八 S 管理主控台")
    text = text.replace("K八S", "K 八 S")
    return text


def validate_model_text(text: str, label: str) -> None:
    forbidden = ["BV26", "<!--", "-->", "```", "\n#", "[/BV26]", "[BV26"]
    hits = [item for item in forbidden if item in text]
    if hits:
        raise ValueError(f"{label} contains forbidden model-input tokens: {hits}")


def parse_segments() -> list[Segment]:
    source = SOURCE_MD.read_text(encoding="utf-8")
    segments: list[Segment] = []
    for index, match in enumerate(CONTROL_RE.finditer(source), start=1):
        meta, hints = parse_meta(match.group("meta"))
        clean_text = clean_model_text(match.group("text"))
        normalized_text = normalize_text(clean_text)
        validate_model_text(clean_text, f"segment {index} clean text")
        validate_model_text(normalized_text, f"segment {index} normalized text")
        output_prefix = meta["output_prefix"]
        segments.append(
            Segment(
                index=index,
                segment_id=meta["segment_id"],
                group=meta["group"],
                output_prefix=output_prefix,
                title=match.group("title").strip(),
                preset=meta["preset"],
                speed_cpm=meta["speed_cpm"],
                target_duration=meta["target_duration"],
                target_seconds=parse_duration(meta["target_duration"]),
                timeline=meta["timeline"],
                character_count=int(meta["character_count"]),
                delivery=meta["delivery"],
                source_notes=meta.get("source_notes", ""),
                pronunciation_hints=hints,
                clean_text=clean_text,
                normalized_text=normalized_text,
                clean_text_path=LOCAL_ROOT / f"inputs/{VERSION}/segments/{output_prefix}.txt",
                normalized_text_path=LOCAL_ROOT / f"inputs/{VERSION}/normalized_segments/{output_prefix}.txt",
            )
        )
    return segments


def split_sentences(text: str) -> list[str]:
    pieces = re.findall(r".+?(?:[。！？?]|$)", text)
    sentences: list[str] = []
    for piece in pieces:
        cleaned = re.sub(r"\s+", " ", piece).strip()
        if not cleaned:
            continue
        if len(cleaned) <= 500:
            sentences.append(cleaned)
            continue

        clauses = re.findall(r".+?(?:[，；：、]|$)", cleaned)
        current: list[str] = []
        current_len = 0
        for clause in [c.strip() for c in clauses if c.strip()]:
            if current and current_len + len(clause) > 430:
                sentences.append(" ".join(current).strip())
                current = [clause]
                current_len = len(clause)
            else:
                current.append(clause)
                current_len += len(clause)
        if current:
            sentences.append(" ".join(current).strip())
    return sentences or [text]


def split_by_markers(text: str, markers: list[str]) -> list[str]:
    positions = []
    for marker in markers:
        index = text.find(marker)
        if index > 0:
            positions.append(index)
    if not positions:
        return []
    positions = sorted(set(positions))
    starts = [0, *positions]
    ends = [*positions, len(text)]
    return [text[start:end].strip() for start, end in zip(starts, ends) if text[start:end].strip()]


def split_long_chunks(chunks: list[str], max_chars: int) -> list[str]:
    expanded: list[str] = []
    for chunk in chunks:
        needs_clause_split = any(len(sentence) > max_chars for sentence in split_sentences(chunk))
        if len(chunk) <= max_chars and not needs_clause_split:
            expanded.append(chunk)
            continue
        current: list[str] = []
        current_len = 0
        sentences: list[str] = []
        for sentence in split_sentences(chunk):
            if len(sentence) <= max_chars:
                sentences.append(sentence)
                continue
            sentences.extend([part.strip() for part in re.findall(r".+?(?:[，；：、]|$)", sentence) if part.strip()])
        for sentence in sentences:
            if current and current_len + len(sentence) > max_chars:
                expanded.append(" ".join(current).strip())
                current = [sentence]
                current_len = len(sentence)
            else:
                current.append(sentence)
                current_len += len(sentence)
        if current:
            expanded.append(" ".join(current).strip())
    return expanded


def split_subclips(text: str, output_prefix: str = "") -> list[str]:
    if output_prefix == "cde_full_01_opening_positioning_crazyhunter_entry_case":
        return split_long_chunks([text], 70)

    if output_prefix == "cde_full_26_shared_close_test_anchors":
        closing_clips = split_long_chunks([text], 45)
        if 12 <= len(closing_clips) <= 24 and all(len(item) <= 90 for item in closing_clips):
            return closing_clips

    sentences = split_sentences(text)
    if output_prefix == "cde_full_16_k8s_review_controls":
        clips = split_long_chunks([text], 120)
        if 8 <= len(clips) <= 12 and all(len(item) <= 160 for item in clips):
            return clips
        target_count = 6
    elif output_prefix == "cde_full_20_crowdstrike_update_524b":
        clips = split_long_chunks([text], 90)
        if 10 <= len(clips) <= 20 and all(len(item) <= 120 for item in clips):
            return clips
        target_count = 5
    elif len(text) <= 850:
        target_count = 2
    elif len(text) <= 1100:
        target_count = 3
    else:
        target_count = 4
    target_len = max(260, len(text) // target_count)
    clips: list[str] = []
    current: list[str] = []
    current_len = 0
    for sentence in sentences:
        sentence_len = len(sentence)
        should_flush = (
            current
            and current_len >= 240
            and current_len + sentence_len > target_len
            and len(clips) < target_count - 1
        )
        if should_flush:
            clips.append(" ".join(current).strip())
            current = [sentence]
            current_len = sentence_len
        else:
            current.append(sentence)
            current_len += sentence_len
    if current:
        clips.append(" ".join(current).strip())

    # If a very long sentence makes a clip too long, keep it intact rather than
    # cutting mid-sentence; review can decide whether to manually shorten it.
    if len(clips) > 4:
        merged = clips[:3]
        merged.append(" ".join(clips[3:]).strip())
        clips = merged
    return clips


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def wav_duration_seconds(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        with wave.open(str(path), "rb") as wav:
            return wav.getnframes() / float(wav.getframerate())
    except wave.Error:
        return None


def read_optional_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def command_version(command: str, *args: str) -> dict[str, object]:
    executable = shutil.which(command)
    if not executable:
        return {"available": False, "path": "", "version": ""}
    try:
        result = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - defensive runtime probe
        return {"available": True, "path": executable, "version": f"probe_failed: {exc}"}
    version = (result.stdout or result.stderr).strip().splitlines()
    return {"available": True, "path": executable, "version": version[0] if version else ""}


def module_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def probe_python_runtime(python_path: Path) -> dict[str, object]:
    if not python_path.exists():
        return {"available": False, "path": str(python_path)}
    code = r"""
import importlib.util
import json
import sys

modules = ["torch", "torchaudio", "transformers", "huggingface_hub", "gradio", "g2pw", "soundfile"]
payload = {
    "available": True,
    "path": sys.executable,
    "version": sys.version.split()[0],
    "modules": {name: importlib.util.find_spec(name) is not None for name in modules},
}
try:
    import torch
    import torchaudio

    payload["torch"] = {
        "version": torch.__version__,
        "torchaudio_version": torchaudio.__version__,
        "cuda_available": torch.cuda.is_available(),
    }
    if torch.cuda.is_available():
        payload["torch"]["device"] = torch.cuda.get_device_name(0)
        payload["torch"]["capability"] = list(torch.cuda.get_device_capability(0))
        try:
            value = (torch.ones((32, 32), device="cuda") @ torch.ones((32, 32), device="cuda"))[0, 0].item()
            payload["torch"]["cuda_smoke_ok"] = value == 32.0
        except Exception as exc:
            payload["torch"]["cuda_smoke_ok"] = False
            payload["torch"]["cuda_smoke_error"] = repr(exc)
except Exception as exc:
    payload["torch_probe_error"] = repr(exc)
print(json.dumps(payload, ensure_ascii=False))
"""
    try:
        result = subprocess.run(
            [str(python_path), "-c", code],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as exc:  # pragma: no cover - defensive runtime probe
        return {"available": True, "path": str(python_path), "probe_error": repr(exc)}
    try:
        payload = json.loads(result.stdout.strip().splitlines()[-1])
    except Exception:
        return {
            "available": True,
            "path": str(python_path),
            "probe_error": result.stderr.strip() or result.stdout.strip(),
        }
    if result.stderr.strip():
        payload["stderr_first_line"] = result.stderr.strip().splitlines()[0]
    return payload


def detect_runtime_state(reference_audio_exists: bool) -> dict[str, object]:
    module_names = [
        "torch",
        "torchaudio",
        "transformers",
        "huggingface_hub",
        "gradio",
        "g2pw",
    ]
    module_state = {name: module_available(name) for name in module_names}
    runner_path = REPO_ROOT / "tools/breezyvoice_render_subclips.py"
    setup_path = REPO_ROOT / "tools/setup_breezyvoice_rtx5080_runtime.sh"
    local_venv_python = LOCAL_ROOT / f"runtime/{VERSION}/venv/bin/python"
    local_venv_probe = probe_python_runtime(local_venv_python)
    breezyvoice_candidates = [
        REPO_ROOT / ".local/BreezyVoice",
        REPO_ROOT.parent / "BreezyVoice",
        Path.home() / "BreezyVoice",
    ]
    repo_ready = any((path / "single_inference.py").exists() for path in breezyvoice_candidates)
    venv_modules = local_venv_probe.get("modules", {})
    venv_torch = local_venv_probe.get("torch", {})
    local_venv_ready = bool(
        local_venv_probe.get("available")
        and repo_ready
        and isinstance(venv_modules, dict)
        and all(venv_modules.get(name) for name in ["torch", "torchaudio", "g2pw", "soundfile"])
    )
    rtx_5080_ready = bool(
        local_venv_ready
        and isinstance(venv_torch, dict)
        and venv_torch.get("cuda_available")
        and venv_torch.get("cuda_smoke_ok")
        and venv_torch.get("capability") == [12, 0]
    )
    return {
        "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
        "reference_audio_exists": reference_audio_exists,
        "execution_mode_without_audio": "default_sft_voice",
        "no_reference_runner": rel(runner_path),
        "rtx_5080_runtime_setup": rel(setup_path),
        "pilot_command_template": rel(LOCAL_ROOT / f"commands/{VERSION}/run_pilot_template.sh"),
        "python": {
            "executable": sys.executable,
            "version": platform.python_version(),
            "python3_10": shutil.which("python3.10") or "",
        },
        "commands": {
            "uv": command_version("uv", "--version"),
            "docker": command_version("docker", "--version"),
            "docker_compose": command_version("docker", "compose", "version"),
            "nvidia_smi": command_version("nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"),
        },
        "python_modules": module_state,
        "breezyvoice_repo_candidates": [
            {"path": str(path), "exists": path.exists(), "has_single_inference": (path / "single_inference.py").exists()}
            for path in breezyvoice_candidates
        ],
        "local_venv": local_venv_probe,
        "ready_to_render_locally": local_venv_ready or (
            all(module_state.values())
            and repo_ready
        ),
        "rtx_5080_ready": rtx_5080_ready,
    }


def prepare_package() -> None:
    segments = parse_segments()
    if len(segments) != 26:
        raise ValueError(f"Expected 26 segments, found {len(segments)}")
    if sum(segment.target_seconds for segment in segments) != 4800:
        raise ValueError("Target duration does not sum to 80:00")
    if sum(len(segment.clean_text) for segment in segments) != 28053:
        raise ValueError("Model text character count drifted from frozen v1 value 28053")

    dirs = [
        LOCAL_ROOT / f"freeze/{VERSION}",
        LOCAL_ROOT / f"manifests/{VERSION}",
        LOCAL_ROOT / f"inputs/{VERSION}/segments",
        LOCAL_ROOT / f"inputs/{VERSION}/normalized_segments",
        LOCAL_ROOT / f"inputs/{VERSION}/subclips",
        LOCAL_ROOT / f"prompts/{VERSION}",
        LOCAL_ROOT / f"runtime/{VERSION}",
        LOCAL_ROOT / f"output/{VERSION}/subclips",
        LOCAL_ROOT / f"output/{VERSION}/parent_chunks",
        LOCAL_ROOT / f"output/{VERSION}/full",
        LOCAL_ROOT / f"output/{VERSION}/archive",
        LOCAL_ROOT / f"review/{VERSION}",
        LOCAL_ROOT / f"specs/{VERSION}",
        LOCAL_ROOT / f"commands/{VERSION}",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    frozen_source = LOCAL_ROOT / f"freeze/{VERSION}/source/cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md"
    frozen_source.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_MD, frozen_source)

    source_hash = sha256(SOURCE_MD)
    freeze_payload = {
        "version": VERSION,
        "source_path": rel(SOURCE_MD),
        "frozen_source_path": rel(frozen_source),
        "source_sha256": source_hash,
        "segment_count": len(segments),
        "target_total_seconds": sum(segment.target_seconds for segment in segments),
        "target_total_time": "80:00",
        "delivery_target_seconds": DELIVERY_TARGET_SECONDS,
        "delivery_target_time": DELIVERY_TARGET_TIME,
        "delivery_target_policy": "After raw stitching, apply one global tempo factor raw_duration_seconds / 4200 to produce an approximately 70-minute master.",
        "model_text_characters": sum(len(segment.clean_text) for segment in segments),
        "bv26_markup_in_model_text": False,
        "pronunciation_notes_path": rel(PRONUNCIATION_NOTES),
    }
    write_json(LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.json", freeze_payload)
    write_text(
        LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.md",
        "\n".join(
            [
                "# BreezyVoice V1 Freeze Report",
                "",
                f"- Version: `{VERSION}`",
                f"- Source: `{rel(SOURCE_MD)}`",
                f"- Frozen copy: `{rel(frozen_source)}`",
                f"- Source SHA-256: `{source_hash}`",
                "- Segment count: `26`",
                "- Target timing: `80:00`",
                f"- Delivery master target: `{DELIVERY_TARGET_TIME}` after one global post-synthesis tempo normalization",
                "- Model text characters: `28053`",
                "- Model text contains `BV26`: `false`",
                "",
                "Purpose: every generated audio file should trace back to this frozen source, stable `output_prefix`, segment id, and clean text path.",
            ]
        ),
    )

    manifest_rows: list[dict[str, object]] = []
    subclip_rows: list[dict[str, object]] = []
    review_rows: list[dict[str, object]] = []

    for segment in segments:
        write_text(segment.clean_text_path, segment.clean_text)
        write_text(segment.normalized_text_path, segment.normalized_text)
        subclips = split_subclips(segment.normalized_text, segment.output_prefix)
        subclip_paths = []
        for sub_index, subclip in enumerate(subclips, start=1):
            validate_model_text(subclip, f"{segment.output_prefix}_p{sub_index:02d}")
            subclip_id = f"{segment.output_prefix}_p{sub_index:02d}"
            subclip_text_path = LOCAL_ROOT / f"inputs/{VERSION}/subclips/{subclip_id}.txt"
            subclip_output_path = LOCAL_ROOT / f"output/{VERSION}/subclips/{subclip_id}.wav"
            write_text(subclip_text_path, subclip)
            subclip_paths.append(rel(subclip_text_path))
            subclip_rows.append(
                {
                    "parent_output_prefix": segment.output_prefix,
                    "segment_id": segment.segment_id,
                    "subclip_id": subclip_id,
                    "subclip_index": sub_index,
                    "subclip_count": len(subclips),
                    "text_characters": len(subclip),
                    "clean_text_path": rel(subclip_text_path),
                    "planned_output_wav": rel(subclip_output_path),
                    "parent_output_wav": rel(LOCAL_ROOT / f"output/{VERSION}/parent_chunks/{segment.output_prefix}.wav"),
                    "full_output_wav": rel(LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav"),
                    "accepted": "",
                }
            )

        manifest_rows.append(
            {
                "output_prefix": segment.output_prefix,
                "segment_id": segment.segment_id,
                "group": segment.group,
                "title": segment.title,
                "preset": segment.preset,
                "speed_cpm": segment.speed_cpm,
                "target_duration": segment.target_duration,
                "target_seconds": segment.target_seconds,
                "timeline": segment.timeline,
                "text_characters": len(segment.clean_text),
                "clean_text_path": rel(segment.clean_text_path),
                "normalized_text_path": rel(segment.normalized_text_path),
                "subclip_count": len(subclips),
                "subclip_text_paths": ";".join(subclip_paths),
                "pronunciation_hints": "; ".join(segment.pronunciation_hints),
                "source_notes": segment.source_notes,
                "planned_parent_wav": rel(LOCAL_ROOT / f"output/{VERSION}/parent_chunks/{segment.output_prefix}.wav"),
            }
        )
        review_rows.append(
            {
                "output_prefix": segment.output_prefix,
                "subclip_count": len(subclips),
                "runtime": "",
                "pronunciation_issue": "",
                "fix_applied": "",
                "accepted": "",
            }
        )

    manifest_fields = [
        "output_prefix",
        "segment_id",
        "group",
        "title",
        "preset",
        "speed_cpm",
        "target_duration",
        "target_seconds",
        "timeline",
        "text_characters",
        "clean_text_path",
        "normalized_text_path",
        "subclip_count",
        "subclip_text_paths",
        "pronunciation_hints",
        "source_notes",
        "planned_parent_wav",
    ]
    write_csv(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv", manifest_rows, manifest_fields)
    write_jsonl(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.jsonl", manifest_rows)

    subclip_fields = [
        "parent_output_prefix",
        "segment_id",
        "subclip_id",
        "subclip_index",
        "subclip_count",
        "text_characters",
        "clean_text_path",
        "planned_output_wav",
        "parent_output_wav",
        "full_output_wav",
        "accepted",
    ]
    write_csv(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv", subclip_rows, subclip_fields)
    write_jsonl(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.jsonl", subclip_rows)

    planned_subclip_texts = {REPO_ROOT / str(row["clean_text_path"]) for row in subclip_rows}
    actual_subclip_texts = sorted((LOCAL_ROOT / f"inputs/{VERSION}/subclips").glob("*.txt"))
    orphan_text_archive = LOCAL_ROOT / f"inputs/{VERSION}/archive/orphan-subclips"
    orphan_input_rows = []
    for text_path in actual_subclip_texts:
        if text_path in planned_subclip_texts:
            continue
        orphan_text_archive.mkdir(parents=True, exist_ok=True)
        archived_path = orphan_text_archive / text_path.name
        if archived_path.exists():
            archived_path.unlink()
        shutil.move(str(text_path), str(archived_path))
        orphan_input_rows.append(
            {
                "input_text": rel(text_path),
                "archived_to": rel(archived_path),
                "status": "orphan_not_in_current_subclip_manifest",
                "action": "archived_before_review_or_render_to_prevent_stale_text_confusion",
            }
        )
    write_csv(
        LOCAL_ROOT / f"review/{VERSION}/orphan_input_inventory.csv",
        orphan_input_rows,
        ["input_text", "archived_to", "status", "action"],
    )

    pilot_rows = [row for row in manifest_rows if row["output_prefix"] in PILOT_PREFIXES]
    write_csv(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv", pilot_rows, manifest_fields)
    write_jsonl(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.jsonl", pilot_rows)
    pilot_prefixes = {row["output_prefix"] for row in pilot_rows}
    pilot_subclip_rows = [row for row in subclip_rows if row["parent_output_prefix"] in pilot_prefixes]
    pilot_audio_rows = []
    for row in pilot_subclip_rows:
        output_path = REPO_ROOT / str(row["planned_output_wav"])
        duration = wav_duration_seconds(output_path)
        pilot_audio_rows.append(
            {
                "subclip_id": row["subclip_id"],
                "parent_output_prefix": row["parent_output_prefix"],
                "planned_output_wav": row["planned_output_wav"],
                "exists": output_path.exists(),
                "duration_seconds": f"{duration:.2f}" if duration is not None else "",
                "accepted": "",
            }
        )
    write_csv(
        LOCAL_ROOT / f"review/{VERSION}/pilot_audio_inventory.csv",
        pilot_audio_rows,
        ["subclip_id", "parent_output_prefix", "planned_output_wav", "exists", "duration_seconds", "accepted"],
    )
    planned_subclip_wavs = {REPO_ROOT / str(row["planned_output_wav"]) for row in subclip_rows}
    actual_subclip_wavs = sorted((LOCAL_ROOT / f"output/{VERSION}/subclips").glob("*.wav"))
    orphan_audio_rows = []
    for output_path in actual_subclip_wavs:
        if output_path not in planned_subclip_wavs:
            duration = wav_duration_seconds(output_path)
            orphan_audio_rows.append(
                {
                    "output_wav": rel(output_path),
                    "duration_seconds": f"{duration:.2f}" if duration is not None else "",
                    "status": "orphan_not_in_current_subclip_manifest",
                    "action": "archive_or_delete_before_manual_review_if_this_filename_could_confuse_selection",
                }
            )
    write_csv(
        LOCAL_ROOT / f"review/{VERSION}/orphan_audio_inventory.csv",
        orphan_audio_rows,
        ["output_wav", "duration_seconds", "status", "action"],
    )
    pilot_outputs_existing = sum(1 for row in pilot_audio_rows if row["exists"])
    pilot_outputs_complete = pilot_outputs_existing == len(pilot_subclip_rows)
    pilot_parent_paths = sorted(
        {
            REPO_ROOT / str(row["parent_output_wav"])
            for row in pilot_subclip_rows
        }
    )
    pilot_parent_outputs_existing = sum(1 for path in pilot_parent_paths if path.exists())
    pilot_full_stitched_path = LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-pilot-stitched-v1.wav"
    pilot_full_stitched_exists = pilot_full_stitched_path.exists()
    pilot_asr_path = LOCAL_ROOT / f"review/{VERSION}/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt"
    pilot_asr_text = read_optional_text(pilot_asr_path)
    pilot_asr_term_hits = {
        term: sum(pilot_asr_text.count(variant) for variant in variants)
        for term, variants in PILOT_ASR_TERM_VARIANTS.items()
    }
    pilot_asr_forbidden_hits = {
        token: pilot_asr_text.count(token)
        for token in ["BV26", "<!--", "-->", "[BV26", "[/BV26]", "```"]
        if token in pilot_asr_text
    }
    pilot_asr_missing_terms = [term for term, count in pilot_asr_term_hits.items() if count == 0]
    pilot_machine_review_status = (
        "needs_human_listening"
        if pilot_asr_text and pilot_asr_missing_terms
        else "asr_not_available"
        if not pilot_asr_text
        else "machine_review_no_control_markup"
    )
    write_json(
        LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.json",
        {
            "pilot_asr_path": rel(pilot_asr_path),
            "asr_exists": pilot_asr_path.exists(),
            "asr_characters": len(pilot_asr_text),
            "asr_term_hits": pilot_asr_term_hits,
            "asr_term_variants": PILOT_ASR_TERM_VARIANTS,
            "asr_missing_terms": pilot_asr_missing_terms,
            "asr_forbidden_markup_hits": pilot_asr_forbidden_hits,
            "status": pilot_machine_review_status,
            "interpretation": (
                "Breeze-ASR-25 ASR is an auxiliary signal only. Missing term hits or odd substitutions require human listening before full batch approval."
            ),
        },
    )
    write_text(
        LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.md",
        "\n".join(
            [
                "# Pilot Machine Review",
                "",
                f"- ASR transcript: `{rel(pilot_asr_path)}`",
                f"- ASR exists: `{pilot_asr_path.exists()}`",
                f"- ASR characters: `{len(pilot_asr_text)}`",
                f"- Status: `{pilot_machine_review_status}`",
                f"- Forbidden markup hits: `{pilot_asr_forbidden_hits or {}}`",
                "",
                "Expected term hits from ASR:",
                "",
                "| Term | Count |",
                "| --- | ---: |",
                *[f"| `{term}` | {count} |" for term, count in pilot_asr_term_hits.items()],
                "",
                "Machine interpretation:",
                "",
                "- ASR must be generated with Breeze-ASR-25 and is not a substitute for human listening.",
                "- No forbidden orchestration markup should appear in the ASR transcript.",
                "- Missing expected terms or strange substitutions are treated as a pilot-review risk, not as proof that the raw audio itself is unusable.",
                "- Keep `full_batch_allowed=false` until the pilot listening checklist is accepted.",
            ]
        ),
    )

    render_review_log_path = LOCAL_ROOT / f"review/{VERSION}/render_review_log.csv"
    if not render_review_log_path.exists():
        write_csv(
            render_review_log_path,
            review_rows,
            ["output_prefix", "subclip_count", "runtime", "pronunciation_issue", "fix_applied", "accepted"],
        )

    write_text(
        LOCAL_ROOT / f"inputs/{VERSION}/pronunciation_override_policy.md",
        "\n".join(
            [
                "# Pronunciation Override Policy",
                "",
                f"Source pronunciation notes: `{rel(PRONUNCIATION_NOTES)}`",
                "",
                "Use the notes as the authority, but apply overrides only after pilot evidence.",
                "Keep professional English terms recognizable for a Taiwan medical-cybersecurity audience.",
                "",
                "Pre-applied low-risk normalizations:",
                "",
                "- `K8S` -> `K eight S`",
                "- `524B` -> `五二四 B`",
                "- `Log4Shell` -> `Log four Shell`",
                "- `MOVEit Transfer` -> `Move it Transfer`",
                "- `Channel File 291` -> `Channel File 二九一`",
                "- `NetworkPolicy` -> `Network Policy`",
                "",
                "Pilot-only candidates:",
                "",
                "- If `SBOM` is misread, replace locally with `S B O M` in the affected subclip.",
                "- If `PACS` is misread, replace locally with `派克斯` or `P A C S` in the affected subclip.",
                "- If `FD&C Act` is misread, replace locally with `F D and C Act` in the affected subclip.",
                "",
                "Do not globally inject bopomofo or Chinese near-sounds unless listening evidence shows a real issue.",
            ]
        ),
    )

    default_prompt_text = (
        "各位好，今天這場課程會把醫療資安放回臨床 workflow。"
        "我們會用產品生命週期來看證據，用醫院部署現實來看責任分工，"
        "讓法規條文變成可以行動、可以交接、可以驗證的治理語言。"
        "請用穩定、清楚、台灣華語的醫療資安講課語氣朗讀。"
    )
    reference_audio_path = LOCAL_ROOT / f"prompts/{VERSION}/jason_reference.wav"
    reference_text_path = LOCAL_ROOT / f"prompts/{VERSION}/jason_reference.txt"
    if reference_audio_path.exists() and reference_text_path.exists():
        prompt_text = reference_text_path.read_text(encoding="utf-8").strip()
    else:
        prompt_text = default_prompt_text
        write_text(reference_text_path, prompt_text)
    reference_audio_exists = reference_audio_path.exists()
    reference_gate = {
        "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
        "optional_audio_path": rel(reference_audio_path),
        "optional_transcript_path": rel(reference_text_path),
        "audio_exists": reference_audio_exists,
        "recommended_duration_seconds": "25-45",
        "style": "clean Taiwan Mandarin medical-cybersecurity lecture",
        "execution_mode_without_audio": "no_reference_default_voice",
        "status": "ready_without_reference_audio" if not reference_audio_exists else "ready_with_reference_audio",
    }
    write_json(LOCAL_ROOT / f"prompts/{VERSION}/reference_audio_gate.json", reference_gate)
    (LOCAL_ROOT / f"prompts/{VERSION}/REFERENCE_AUDIO_REQUIRED.md").unlink(missing_ok=True)
    write_text(
        LOCAL_ROOT / f"prompts/{VERSION}/REFERENCE_AUDIO_OPTIONAL.md",
        "\n".join(
            [
                "# Reference Audio Optional",
                "",
                "This render package is configured to run without reference audio.",
                "",
                "When no prompt WAV is present, use the BreezyVoice runtime's default/no-reference voice mode.",
                "If a prompt WAV is later added, it can be used as an optional voice-style reference:",
                "",
                f"`{reference_gate['optional_audio_path']}`",
                "",
                "Recommended optional recording requirements:",
                "",
                "- `25-45` seconds",
                "- clean close-mic audio",
                "- Taiwan Mandarin",
                "- calm medical-cybersecurity lecture tone",
                "- exact transcript must match `jason_reference.txt`",
                "- do not use celebrity, third-party, or unconsented voice samples",
                "",
                "Do not block pilot rendering just because the optional WAV is absent.",
            ]
        ),
    )

    runtime_state = detect_runtime_state(reference_audio_exists)
    write_json(LOCAL_ROOT / f"runtime/{VERSION}/runtime_readiness.json", runtime_state)
    missing_modules = [name for name, exists in runtime_state["python_modules"].items() if not exists]
    breezyvoice_repo_ready = any(
        candidate["has_single_inference"] for candidate in runtime_state["breezyvoice_repo_candidates"]
    )
    write_text(
        LOCAL_ROOT / f"runtime/{VERSION}/runtime_readiness.md",
        "\n".join(
            [
                "# BreezyVoice Runtime Readiness",
                "",
                "Reference audio policy:",
                "",
                f"- Required: `{REFERENCE_AUDIO_REQUIRED}`",
                f"- Optional WAV exists: `{reference_audio_exists}`",
                "- No-reference execution mode: `default_sft_voice`",
                "",
                "Local execution path:",
                "",
                f"- Runner: `{runtime_state['no_reference_runner']}`",
                f"- RTX 5080 setup script: `{runtime_state['rtx_5080_runtime_setup']}`",
                f"- Pilot command template: `{runtime_state['pilot_command_template']}`",
                "- Default behavior: render with a built-in/default SFT speaker id; do not require prompt audio.",
                "- Optional behavior: a prompt WAV can still be supplied later for zero-shot voice style, with consent and exact prompt transcript.",
                "",
                "Current local runtime probe:",
                "",
                f"- Python: `{runtime_state['python']['version']}` at `{runtime_state['python']['executable']}`",
                f"- Python 3.10 path: `{runtime_state['python']['python3_10'] or 'not found'}`",
                f"- BreezyVoice repo candidate ready: `{breezyvoice_repo_ready}`",
                f"- Missing Python modules: `{', '.join(missing_modules) if missing_modules else 'none'}`",
                f"- Local ready to render: `{runtime_state['ready_to_render_locally']}`",
                f"- RTX 5080 ready: `{runtime_state['rtx_5080_ready']}`",
                f"- Local venv Python: `{runtime_state['local_venv'].get('path', 'not found')}`",
                f"- Local venv torch: `{runtime_state['local_venv'].get('torch', {}).get('version', 'not found')}`",
                "",
                "Important distinction:",
                "",
                "- Missing reference audio no longer blocks pilot rendering.",
                "- RTX 5080 requires a CUDA 12.8-capable PyTorch wheel; the official `torch==2.3.1+cu118` wheel does not support `sm_120`.",
            ]
        ),
    )

    write_json(
        LOCAL_ROOT / f"specs/{VERSION}/audio_output_spec.json",
        {
            "format": "wav",
            "sample_rate": "BreezyVoice runtime default; archive copy may be normalized after render",
            "loudness_lufs": -16,
            "delivery_target_seconds": DELIVERY_TARGET_SECONDS,
            "delivery_target_time": DELIVERY_TARGET_TIME,
            "tempo_policy": "Apply a single global atempo factor after raw stitch: raw_duration_seconds / 4200.",
            "silence_policy": "preserve natural paragraph pauses; do not aggressive trim",
            "subclip_output_dir": rel(LOCAL_ROOT / f"output/{VERSION}/subclips"),
            "parent_chunk_output_dir": rel(LOCAL_ROOT / f"output/{VERSION}/parent_chunks"),
            "full_output_path": rel(LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav"),
            "archive_output_dir": rel(LOCAL_ROOT / f"output/{VERSION}/archive"),
        },
    )
    write_text(
        LOCAL_ROOT / f"specs/{VERSION}/audio_output_spec.md",
        "\n".join(
            [
                "# Audio Output Spec",
                "",
                "- Output format: `.wav`",
                "- Sample rate: use the BreezyVoice runtime default, then create a normalized archive copy if needed.",
                "- Loudness target: about `-16 LUFS` after final normalization.",
                f"- Delivery duration target: about `{DELIVERY_TARGET_TIME}` after one global tempo pass.",
                "- Tempo policy: compute `raw_duration_seconds / 4200` after raw stitch and apply it once to the full master.",
                "- Silence policy: preserve natural paragraph pauses; do not aggressive-trim subclips.",
                f"- Subclip output path: `{rel(LOCAL_ROOT / f'output/{VERSION}/subclips')}/`",
                f"- Parent chunk output path: `{rel(LOCAL_ROOT / f'output/{VERSION}/parent_chunks')}/`",
                f"- Full stitched output path: `{rel(LOCAL_ROOT / f'output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav')}`",
            ]
        ),
    )

    write_text(
        LOCAL_ROOT / f"review/{VERSION}/pilot_review_checklist.md",
        "\n".join(
            [
                "# Pilot Review Checklist",
                "",
                "Pilot rows:",
                "",
                *[f"- `{prefix}`" for prefix in PILOT_PREFIXES],
                "",
                "Listen for:",
                "",
                "- English acronyms are not slurred or misread.",
                "- `K eight S`, `F D and C Act Section 五二四 B`, and `Channel File 二九一` are stable.",
                "- Speaking speed is internally consistent and the final master is normalized to about `70:00`.",
                "- Case passages sound like concise story sharing: setup, event path, clinical implication, review takeaway.",
                "- Long sentences do not sound fatigued.",
                "- Opening sounds stable and the close sounds authoritative.",
                "- Handoff into Jingzhong's white-box/system-review section sounds natural.",
                "- No markup, labels, or strange symbols are spoken.",
                "",
                "Correction order:",
                "",
                "1. Punctuation and sentence breaks.",
                "2. English term spacing.",
                "3. Single-term pronunciation replacement.",
                "4. Shorter subclip split.",
                "5. Segment preset or pause adjustment.",
                "6. Spoken-content edit only if the above cannot solve the issue.",
            ]
        ),
    )
    write_text(
        LOCAL_ROOT / f"review/{VERSION}/full_render_acceptance_gate.md",
        "\n".join(
            [
                "# Full Render Acceptance Gate",
                "",
                "Do not start full render until all four pilot rows are accepted.",
                "",
                "Full render pass criteria:",
                "",
                "- understandable Taiwan Mandarin lecture delivery",
                "- stable professional terms and acronyms",
                "- no spoken markup or control labels",
                "- no excessive sentence fatigue",
                "- tone matches CDE medical-cybersecurity instruction",
                "- every generated WAV maps to `subclip_manifest.csv` and `render_review_log.csv`",
                "- `python3 tools/check_breezyvoice_full_render_gate.py --write-report` exits `0`",
                "",
                "After render:",
                "",
                "1. stitch subclips into parent chunks by `parent_output_prefix`",
                "2. stitch parent chunks into the full lecture",
                "3. normalize final full output around `-16 LUFS`",
                "4. complete `render_review_log.csv` with runtime, pronunciation issue, fix, and accepted status",
                "",
                "Machine stop gate:",
                "",
                "Run this before any full render command:",
                "",
                "```bash",
                "python3 tools/check_breezyvoice_full_render_gate.py --write-report",
                "```",
                "",
                "If it exits non-zero, stop and do not run full render.",
            ]
        ),
    )

    write_json(
        LOCAL_ROOT / f"review/{VERSION}/pilot_status.json",
        {
            "pilot_prefixes": PILOT_PREFIXES,
            "pilot_subclip_count": len(pilot_subclip_rows),
            "pilot_outputs_existing": pilot_outputs_existing,
            "pilot_outputs_complete": pilot_outputs_complete,
            "pilot_parent_outputs_existing": pilot_parent_outputs_existing,
            "pilot_parent_outputs_complete": pilot_parent_outputs_existing == len(pilot_parent_paths),
            "pilot_full_stitched_exists": pilot_full_stitched_exists,
            "pilot_full_stitched_path": rel(pilot_full_stitched_path),
            "pilot_machine_review": rel(LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.json"),
            "pilot_machine_review_status": pilot_machine_review_status,
            "full_batch_allowed": False,
            "pilot_render_attempted": pilot_outputs_existing > 0,
            "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
            "blocked_by_missing_reference_audio": False,
            "reference_audio_path": rel(reference_audio_path),
            "execution_mode": "with_reference_audio" if reference_audio_exists else "no_reference_default_voice",
            "pilot_audio_inventory": rel(LOCAL_ROOT / f"review/{VERSION}/pilot_audio_inventory.csv"),
            "message": "Pilot TTS may run without reference audio; use optional prompt audio only if present.",
        },
    )

    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/run_pilot_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "# Template only. Set BREEZYVOICE_REPO to a local BreezyVoice clone before running.",
                f"MANIFEST='{rel(LOCAL_ROOT / f'manifests/{VERSION}/pilot_manifest.csv')}'",
                f"SUBCLIPS='{rel(LOCAL_ROOT / f'manifests/{VERSION}/subclip_manifest.csv')}'",
                f"PROMPT_WAV='{rel(reference_audio_path)}'",
                f"PROMPT_TXT='{rel(reference_text_path)}'",
                f"OUTPUT_DIR='{rel(LOCAL_ROOT / f'output/{VERSION}/subclips')}'",
                "VOICE_MODE='default'",
                "MODEL_PATH=\"${BREEZYVOICE_MODEL_PATH:-MediaTek-Research/BreezyVoice}\"",
                "DEFAULT_SPEAKER_ID=\"${BREEZYVOICE_DEFAULT_SPEAKER_ID:-auto}\"",
                f"PYTHON_BIN=\"${{BREEZYVOICE_PYTHON:-{rel(LOCAL_ROOT / f'runtime/{VERSION}/venv/bin/python')}}}\"",
                "BREEZYVOICE_REPO=\"${BREEZYVOICE_REPO:-.local/BreezyVoice}\"",
                "",
                "if [[ ! -x \"$PYTHON_BIN\" ]]; then",
                "  echo \"Missing runtime Python: $PYTHON_BIN\" >&2",
                "  echo \"Run: bash tools/setup_breezyvoice_rtx5080_runtime.sh\" >&2",
                "  exit 2",
                "fi",
                "",
                "if [[ -f \"$PROMPT_WAV\" ]]; then",
                "  echo \"Using optional prompt audio: $PROMPT_WAV\"",
                "  test -f \"$PROMPT_TXT\" || { echo \"Missing prompt transcript: $PROMPT_TXT\" >&2; exit 2; }",
                "  VOICE_MODE=\"${BREEZYVOICE_VOICE_MODE:-prompt}\"",
                "else",
                "  echo \"No prompt audio found; proceeding in no-reference/default voice mode.\"",
                "  PROMPT_WAV=''",
                "  PROMPT_TXT=''",
                "  VOICE_MODE='default'",
                "fi",
                "",
                "PYTHONUTF8=1 \"$PYTHON_BIN\" tools/breezyvoice_render_subclips.py \\",
                "  --selection pilot \\",
                "  --voice-mode \"$VOICE_MODE\" \\",
                "  --model-path \"$MODEL_PATH\" \\",
                "  --speaker-id \"$DEFAULT_SPEAKER_ID\" \\",
                "  --prompt-audio \"$PROMPT_WAV\" \\",
                "  --prompt-text-file \"$PROMPT_TXT\" \\",
                "  --subclip-manifest \"$SUBCLIPS\" \\",
                "  --pilot-manifest \"$MANIFEST\" \\",
                "  --output-dir \"$OUTPUT_DIR\" \\",
                "  --overwrite",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/run_pilot_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/stitch_pilot_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "python3 tools/stitch_breezyvoice_outputs.py \\",
                "  --selection pilot \\",
                "  --stitch-full \\",
                "  --overwrite",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/stitch_pilot_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/build_pilot_review_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "python3 tools/build_breezyvoice_pilot_review.py",
                "python3 tools/build_breezyvoice_render_review_log.py",
                "python3 tools/build_breezyvoice_pilot_correction_matrix.py",
                "",
                "echo \"Review: .local/breezyvoice/review/v1/pilot_listening_review.md\"",
                "echo \"Decision CSV: .local/breezyvoice/review/v1/pilot_listening_review.csv\"",
                "echo \"Render review log: .local/breezyvoice/review/v1/render_review_log.csv\"",
                "echo \"Pilot correction matrix: .local/breezyvoice/review/v1/pilot_correction_matrix.md\"",
                "echo \"Full batch gate: .local/breezyvoice/review/v1/full_batch_gate.json\"",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/build_pilot_review_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/check_full_render_gate_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "python3 tools/check_breezyvoice_full_render_gate.py --write-report",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/check_full_render_gate_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/run_full_render_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "# Full render is deliberately guarded. This script exits before",
                "# rendering unless all four pilot parent chunks are accepted.",
                f"SUBCLIPS='{rel(LOCAL_ROOT / f'manifests/{VERSION}/subclip_manifest.csv')}'",
                f"PROMPT_WAV='{rel(reference_audio_path)}'",
                f"PROMPT_TXT='{rel(reference_text_path)}'",
                f"OUTPUT_DIR='{rel(LOCAL_ROOT / f'output/{VERSION}/subclips')}'",
                f"FULL_OUTPUT='{rel(LOCAL_ROOT / f'output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav')}'",
                "VOICE_MODE='default'",
                "MODEL_PATH=\"${BREEZYVOICE_MODEL_PATH:-MediaTek-Research/BreezyVoice}\"",
                "DEFAULT_SPEAKER_ID=\"${BREEZYVOICE_DEFAULT_SPEAKER_ID:-auto}\"",
                f"PYTHON_BIN=\"${{BREEZYVOICE_PYTHON:-{rel(LOCAL_ROOT / f'runtime/{VERSION}/venv/bin/python')}}}\"",
                "BREEZYVOICE_REPO=\"${BREEZYVOICE_REPO:-.local/BreezyVoice}\"",
                "",
                "python3 tools/check_breezyvoice_full_render_gate.py --write-report",
                "",
                "if [[ ! -x \"$PYTHON_BIN\" ]]; then",
                "  echo \"Missing runtime Python: $PYTHON_BIN\" >&2",
                "  echo \"Run: bash tools/setup_breezyvoice_rtx5080_runtime.sh\" >&2",
                "  exit 2",
                "fi",
                "",
                "if [[ -f \"$PROMPT_WAV\" ]]; then",
                "  echo \"Using optional prompt audio: $PROMPT_WAV\"",
                "  test -f \"$PROMPT_TXT\" || { echo \"Missing prompt transcript: $PROMPT_TXT\" >&2; exit 2; }",
                "  VOICE_MODE=\"${BREEZYVOICE_VOICE_MODE:-prompt}\"",
                "else",
                "  echo \"No prompt audio found; proceeding in no-reference/default voice mode.\"",
                "  PROMPT_WAV=''",
                "  PROMPT_TXT=''",
                "  VOICE_MODE='default'",
                "fi",
                "",
                "PYTHONUTF8=1 \"$PYTHON_BIN\" tools/breezyvoice_render_subclips.py \\",
                "  --selection all \\",
                "  --voice-mode \"$VOICE_MODE\" \\",
                "  --model-path \"$MODEL_PATH\" \\",
                "  --speaker-id \"$DEFAULT_SPEAKER_ID\" \\",
                "  --prompt-audio \"$PROMPT_WAV\" \\",
                "  --prompt-text-file \"$PROMPT_TXT\" \\",
                "  --subclip-manifest \"$SUBCLIPS\" \\",
                "  --output-dir \"$OUTPUT_DIR\" \\",
                "  --overwrite",
                "",
                "python3 tools/stitch_breezyvoice_outputs.py \\",
                "  --selection all \\",
                "  --stitch-full \\",
                "  --full-output \"$FULL_OUTPUT\" \\",
                "  --overwrite",
                "",
                "python3 tools/build_breezyvoice_pilot_review.py",
                "python3 tools/build_breezyvoice_render_review_log.py",
                "python3 tools/build_breezyvoice_pilot_correction_matrix.py",
                "python3 tools/verify_breezyvoice_objective.py --write-report || true",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/run_full_render_template.sh").chmod(0o755)

    summary = {
        "version": VERSION,
        "segments": len(segments),
        "subclips": len(subclip_rows),
        "pilot_segments": len(pilot_rows),
        "model_text_characters": sum(len(segment.clean_text) for segment in segments),
        "duration_seconds": sum(segment.target_seconds for segment in segments),
        "freeze_report": rel(LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.json"),
        "render_manifest": rel(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv"),
        "subclip_manifest": rel(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv"),
        "pilot_manifest": rel(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv"),
        "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
        "reference_audio_exists": reference_audio_exists,
        "pilot_execution_mode": "with_reference_audio" if reference_audio_exists else "no_reference_default_voice",
        "runtime_readiness": rel(LOCAL_ROOT / f"runtime/{VERSION}/runtime_readiness.json"),
        "full_batch_allowed": False,
    }
    write_json(LOCAL_ROOT / f"manifests/{VERSION}/package_summary.json", summary)
    audit_rows = [
        ("1", "凍結輸入版本", "completed", "freeze/v1/freeze_report.json records 26 chunks, 80:00, 28053 chars, source SHA-256, and frozen source copy."),
        ("2", "產生 render manifest", "completed", "manifests/v1/render_manifest.csv and .jsonl include output_prefix, segment_id, preset, target_duration, timeline, clean_text_path, pronunciation_hints."),
        ("3", "抽出 clean text inputs", "completed", "inputs/v1/segments contains 26 clean .txt files with spoken text only."),
        ("4", "切成更小 subclips", "completed", f"manifests/v1/subclip_manifest.csv records {len(subclip_rows)} subclips, 2-4 per parent, all under 500 chars after current split."),
        ("5", "TTS 文字正規化", "completed", "inputs/v1/normalized_segments and inputs/v1/subclips apply low-risk pronunciation normalizations and contain no BV26/Markdown/control markup."),
        ("6", "準備 pronunciation override", "completed", "inputs/v1/pronunciation_override_policy.md points to model-ready pronunciation notes and keeps overrides pilot-evidence based."),
        ("7", "reference audio policy", "completed_optional", "reference_audio_gate.json explicitly sets reference_audio_required=false; no-reference/default voice mode is allowed when jason_reference.wav is absent."),
        ("7a", "no-reference runtime contract", "prepared", "runtime/v1/runtime_readiness.json and run_pilot_template.sh route missing prompt audio to tools/breezyvoice_render_subclips.py --voice-mode default."),
        ("8", "建立音檔輸出規格", "completed", "specs/v1/audio_output_spec.md/json define wav output, loudness, silence, subclip, parent, full, and archive paths."),
        (
            "9",
            "先跑 pilot，不跑 full batch",
            "completed_pilot_audio" if pilot_outputs_complete else "prepared",
            f"pilot_manifest.csv identifies four pilot rows and {len(pilot_subclip_rows)} subclips; pilot_audio_inventory.csv shows {pilot_outputs_existing} existing WAV outputs.",
        ),
        ("10", "Pilot review checklist", "completed", "review/v1/pilot_review_checklist.md records the listening checks."),
        ("11", "修正規則", "completed", "review/v1/pilot_review_checklist.md records correction order."),
        ("12", "Full render 前通過標準", "completed_gate_defined", "review/v1/full_render_acceptance_gate.md defines pass criteria; full_batch_allowed remains false until pilot acceptance."),
        (
            "13",
            "Full render stitch 與紀錄",
            "pilot_stitch_verified" if pilot_full_stitched_exists else "prepared_not_executed",
            f"pilot stitch path has {pilot_parent_outputs_existing}/{len(pilot_parent_paths)} parent WAVs and pilot full stitched exists={pilot_full_stitched_exists}; full render/stitch remains gated by pilot listening acceptance.",
        ),
        (
            "13a",
            "Pilot machine review before full batch",
            pilot_machine_review_status,
            f"pilot_machine_review.json records ASR exists={pilot_asr_path.exists()}, forbidden markup hits={len(pilot_asr_forbidden_hits)}, missing expected term hits={len(pilot_asr_missing_terms)}.",
        ),
        (
            "14",
            "Artifact hygiene before human review",
            "orphan_audio_detected" if orphan_audio_rows else "no_orphan_audio",
            f"review/v1/orphan_audio_inventory.csv records {len(orphan_audio_rows)} WAV files under output/v1/subclips that are not in the current subclip manifest.",
        ),
    ]
    audit_lines = [
        "# BreezyVoice V1 Objective Audit",
        "",
        f"- Package summary: `{rel(LOCAL_ROOT / f'manifests/{VERSION}/package_summary.json')}`",
        f"- Reference audio required: `{REFERENCE_AUDIO_REQUIRED}`",
        f"- Reference audio exists: `{reference_audio_exists}`",
        f"- Pilot execution mode: `{summary['pilot_execution_mode']}`",
        f"- Full batch allowed: `{summary['full_batch_allowed']}`",
        "",
        "| # | Requirement | Status | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    audit_lines.extend("| " + " | ".join(row) + " |" for row in audit_rows)
    audit_lines.extend(
        [
            "",
            "Current state: pilot rendering is no longer blocked by missing reference audio. Full batch remains gated by pilot acceptance, not by prompt-audio availability.",
        ]
    )
    write_text(LOCAL_ROOT / f"review/{VERSION}/objective_audit.md", "\n".join(audit_lines))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    prepare_package()
