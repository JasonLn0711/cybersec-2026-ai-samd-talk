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
    "White box Testing": "白箱測試",
    "white-box validation": "白箱驗證",
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


def normalize_text(text: str) -> str:
    normalized = clean_model_text(text)
    for old, new in TERM_NORMALIZATIONS.items():
        normalized = normalized.replace(old, new)
    normalized = apply_pilot_review_conditioning(normalized)
    normalized = normalized.replace(LEGACY_WHITE_BOX_TERM, PREFERRED_WHITE_BOX_TERM)
    normalized = sanitize_tts_text(normalized)
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
                "- Speaking speed stays close to the `80:00` pacing plan.",
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
