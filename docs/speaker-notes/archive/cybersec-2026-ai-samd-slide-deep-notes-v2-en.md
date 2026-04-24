# CYBERSEC 2026 AI SaMD Slide Deep Notes - English Companion

Status: archived English deep-note companion retained for rehearsal depth. Use `../cybersec-2026-ai-samd-slide-deep-notes-v1-positive-progressive-zh-tw.md` for the current compact/fallback rehearsal script and `../reference/` for canonical `v1.3` slide-by-slide prep.

This English note follows the generated compact `14`-slide fallback storyline. Do not treat it as the canonical `v1.3` deck map. The point of this version is not to cram every detail into slides; it is to prepare the knowledge, cases, trends, and workflows behind the talk so the stage delivery can have depth while the slides remain one-point-per-page, low-text, and spacious. The current owner-approved delivery surface is `outputs/deck/cybersec-2026-ai-samd-cybersecurity-in-practice-v1.3.pdf`.

First, update the most important current trend: every place that mentions FDA cybersecurity guidance should use **FDA 2026 Guidance**. On February 3, 2026, FDA issued the new *Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions*, replacing the June 27, 2025 version. FDA says the guidance provides recommendations for medical-device cybersecurity design, labeling, and premarket submission content, and it addresses FD&C Act section 524B. Industry commentary generally reads the 2026 version as mainly aligning with QMSR / ISO 13485 language rather than overturning the technical expectations. So the talk can frame it this way: **cybersecurity is no longer an add-on document; it is part of the quality management system.** ([U.S. Food and Drug Administration][1])

---

# Slide 1 | AI SaMD Cybersecurity In Practice

This slide is not here to introduce how impressive you are. Its job is to tell everyone immediately that this is not an AI hype talk, not a regulatory reading session, and not a tool list. You need to converge FDA 524B, Threat Modeling, and Patch SLA into one product-trust path: **the product boundary must be defined before risk can be located; risk must become visible before the evidence chain can connect; findings must be governed before repairability can be proven.** The slide blueprint already defines Slide 1 as a "product-trust and decision-support talk" and asks for the opening path Boundary -> Evidence -> Decision -> Repair proof. That direction is correct.

For a general audience, explain it plainly: "An AI medical product does not only need to calculate the answer. It has to be used safely inside a hospital." Imagine an AI that can contour a brain tumor. In a demo, it looks beautiful. But a hospital will ask: where does the data come from? Who can use it? Who checks the result if it is wrong? How does the system recover if it breaks? Who fixes vulnerabilities? How do you prove the fix worked? Once these questions appear, AI has moved from a model into product responsibility.

For engineers, this slide should signal that the talk is not only about model robustness. Using the DeepBT Detector-Plus documentation as an example, the product is not just the Brain Tumor AI Module. It includes Web UI, Integration Module, Brain Tumor AI Module, Docker, WSL2, DCMTK, Node.js, Python, and PACS/DICOM workflow. The SBOM also brings component source, version pinning, provenance, integrity, and support status into the management scope. That means engineers must think beyond model weights and include the software supply chain and runtime environment.

For managers, the real management language of Slide 1 is: "We are not adding documents for submission; we are building product-trust capability." FDA 524B requires a cyber device premarket submission to include plans to monitor, identify, and address postmarket vulnerabilities and exploits, plus CVD, postmarket updates and patches, and SBOM. These are not paper exercises. They are postmarket operating capabilities. ([U.S. Food and Drug Administration][2])

The workflow behind this slide can stay in speaker notes rather than on the slide: from day one, the product team should maintain four folders. First: Boundary, containing intended use, system boundary, and data flow. Second: Evidence, containing architecture, threat model, risk assessment, controls, and testing. Third: Decision, containing finding triage, risk acceptance, and compensating controls. Fourth: Repair proof, containing patch records, retest evidence, customer advisories, and release history. These four folders are the operational backbone of the whole talk.

On stage, this slide should take only 10 seconds. Do not add biography and do not over-explain the background. You can say: "Hello everyone, I am Jiasheng Lin. Today is not about reciting regulations, and it is not about showing a tool list. I want to connect everything through one question: what evidence and decisions does an AI model need before it can become a trusted medical product?"

---

# Slide 2 | Required CYBERSEC Disclaimer

This slide is a compliance beat, not a narrative slide. The blueprint clearly states that Slide 2 is the required CYBERSEC disclaimer and must be separated from the main story. The organizer email also explicitly requires speakers to place the disclaimer page immediately after the cover.

The knowledge point is simple: in medicine, cybersecurity, and regulation, a clear boundary is itself a sign of professionalism. In a public talk, you cannot make the content sound like legal advice, guarantee that any company will be compliant by copying the talk, or show private customer details, hospital topology, internal product details, student data, or patent-sensitive mechanisms on the big screen. The Talk Design also states that the public talk must exclude private hospital/client details, proprietary code, student records, exploit recipes, and patent-sensitive implementation mechanics.

For a general audience, this slide simply says: "The speaker is clear about responsibility boundaries." For engineers, it is a reminder not to turn real exploit steps or internal architecture details into public attack instructions. For managers, it reduces communication risk: when you later discuss FDA, Patch SLA, and incident response, you are explaining governance principles and implementable methods, not issuing a public guarantee for any specific product.

One current trend is also worth noting: CYBERSEC 2026 adds AI real-time translation. That means your sentences should be shorter, clearer, and less abbreviation-heavy; otherwise, real-time translation can break the meaning. The organizer notice says participants can use a QR Code to select the language for AI real-time translation. Therefore, the later anchor lines should be translation-friendly and memorable: "You are not selling a model," "Regulation wants evidence, not slogans," and "Cyber Safety is Patient Safety."

Workflow checks before this slide: first, confirm that the disclaimer image has the correct resolution and aspect ratio. Second, do not add your own legal interpretation. Third, move immediately into Slide 3 after this slide; do not let the audience get stuck in the formal page. On stage, say only: "This is the required conference disclaimer. I will pause here for a moment so everyone can see it. Now let us move directly into the real question for today."

---

# Slide 3 | You Are Not Selling A Model

This is the first major reframing moment of the talk. Many AI teams initially say, "We only provide a model." But clinical settings do not see it that way. Physicians see the result, patients bear the consequences, and the company is responsible for the whole use context. This slide must move the audience from "Is the model accurate?" to "Can product responsibility be proven?" The Talk Design identifies this as a core memory anchor, and it is the most important entry point of the talk.

For a general audience, say it this way: you are not selling a powerful engine; you are selling a vehicle that must actually go on the road. No matter how strong the engine is, if the brakes are unstable, the dashboard displays nonsense, maintenance is unclear, and recall processes do not exist, the vehicle is not trustworthy. AI medical products are the same. Model accuracy is only the engine; what a hospital buys is whether the whole vehicle can be safely driven.

Using the product scenario in the attachment, DeepBT Detector-Plus is AI software that assists radiation-therapy planning by generating an initial brain-tumor contour. It takes T1W+C / T2W MRI as input, outputs DICOM PR / RTSS, and explicitly requires medical professionals to confirm or modify the AI contour before treatment. That setting is important because it tells the audience this is not fully automated physician replacement. It is a decision-support product placed inside a clinical workflow.

For engineers, this slide is really about product boundary. The model is only one asset. Around it are Web UI, Temporary DICOM Storage, Brain Tumor AI Model, PACS, DICOM Viewer, C-FIND, C-MOVE, C-STORE, logs, and configuration files. The Threat Model already uses STRIDE to analyze Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege, and maps those threats to system assets and cybersecurity requirements. That is evidence of product responsibility, not only model performance.

For managers, say it this way: responsibility does not begin on the day an incident happens; it begins the day the product enters the clinical workflow. If intended use is unclear, model limits are not stated, user roles are not defined, security update processes are missing, and there is no customer incident-reporting contact, the responsibility eventually returns to the company. This is not fearmongering. It is the reality of postmarket medical-device responsibility.

In the real world, AI medical devices are rapidly increasing. FDA maintains the AI-enabled medical device list to give the market, healthcare professionals, and patients more transparency about authorized medical devices that use AI technology, and FDA says the list will continue to be updated. That helps your talk: AI medical devices are not future tense. They are present tense. Product responsibility is therefore not a future problem. It is a current problem. ([U.S. Food and Drug Administration][3])

A fictional example: a team builds a brain MRI segmentation model that performs well on a validation set. After entering a hospital, they find that some users choose the wrong image sequence, some DICOM metadata is incomplete, some results are displayed by the viewer in the wrong context, and some temporary data is not cleared. None of these problems are the model score itself, but all of them affect clinical trust. That is what "You are not selling a model" means.

Workflow: this slide should introduce a "responsibility map." In the first product version, the team should write clearly: who uses it, where it is used, what the input is, what the output is, whether the output can be directly used, who confirms it, how long data is cached, how exceptions are handled, how the product is updated, and how customers report incidents. This responsibility map becomes the common starting point for architecture view, threat model, risk assessment, testing, labeling, and Patch SLA.

---

# Slide 4 | AI Is Becoming Infrastructure

This slide answers "Why is this urgent now?" The answer is not that AI is fashionable. The answer is that AI is becoming care infrastructure. In 2026, AI is no longer just a model file. It connects to runtime, data, identity, update chain, support paths, and finally clinical workflow. The blueprint positions this slide as "AI deployment stack -> clinical continuity failure path," which is a strong design because it connects technology trends to clinical reality.

The trend is clear: AI is being built as large-scale infrastructure. In March 2026, Roche announced an expansion of its NVIDIA AI factory, adding 2,176 Blackwell GPUs and bringing the total on-premise plus cloud GPU infrastructure to more than 3,500 GPUs for diagnostics, therapeutics, clinical trials, and large-scale data insights. You do not need to put the Roche logo on the slide. You can simply say: "The medical and life-sciences industry is treating AI as infrastructure, not as a single model." ([Roche][4])

Taiwan context should also be included, but it must not become a second national-strategy presentation. Taiwan's 2025 seventh-phase National Cybersecurity Development Program mentions whole-of-society cyber defense, critical-infrastructure resilience, domestic cybersecurity industry, and emerging AI cybersecurity technology. The National Cybersecurity Strategy 2025 also frames its four pillars as whole-of-society defense resilience, homeland defense and critical infrastructure, key industries and supply chain, and AI application and security. The Talk Design already reminds us that national strategy should raise the altitude, not pull the topic away. ([Executive Yuan][5])

For a general audience, use a utilities metaphor. AI used to be like a standalone appliance; if it broke, the impact was limited. Now AI starts to connect to hospital data flows, account permissions, update chains, customer support, and PACS/HIS workflow. It becomes part of the building's utilities. If it fails, the issue is no longer a demo that cannot run; clinical workflow may be delayed.

For engineers, view this slide through three layers: model, runtime, and infrastructure. The model layer covers provenance, evaluation, model version, and model tampering. The runtime layer covers container, API, secrets, logs, resource limits, and policy enforcement. The infrastructure layer covers identity, network segmentation, host-based firewall, SBOM, update channel, and support boundary. Your Controls document already includes JWT, DICOM-TLS, AES-256, Default-Deny, Nginx single entry point, SIEM forwarding, golden-image recovery, and signed container images. Those are concrete ways to govern AI as infrastructure.

A real case is Change Healthcare. The 2024 Change Healthcare cyberattack caused major disruption across the U.S. healthcare system. An AHA survey reported that among roughly 1,000 responding hospitals, 94% reported financial impact and 74% reported direct patient-care impact. This shows that medical cybersecurity incidents do not have to directly attack a single medical device. They can attack third-party healthcare infrastructure and still affect clinical and financial workflows. ([American Hospital Association][6])

Taiwan also has local cases. iThome reported that in February 2025, MacKay Memorial Hospital was attacked by CrazyHunter ransomware. The known attack path involved malicious program deployment through AD hosts and BYOVD techniques. The Ministry of Health and Welfare H-ISAC issued an alert, and MOHW plus the cybersecurity authority formed a rapid response team to assist. This lets a Taiwan audience know that medical cybersecurity is not foreign news. It has already happened in local healthcare environments. ([iThome][7])

Workflow: introduce an "AI infrastructure readiness check." Before deployment, ask: where does the model run? Where does the data come from? Who can call the API? Who monitors logs? Who can update it? How does rollback work if update fails? How does the hospital fall back? If these answers are not written into the architecture view and labeling, "AI infrastructure" is only a slogan.

---

# Slide 5 | Risk Grows With Architecture

This slide is the map for the whole talk. The four product scales are: Model, Viewer, Platform / Database, and Connected Medical System. Both the blueprint and the Talk Design require this slide to remain, because the later regulation, testing, and Patch SLA sections all return to this map.

The core knowledge is: **the same AI model creates completely different cybersecurity responsibility depending on the product boundary.** If it is only a model artifact, you protect model source, data lineage, dependencies, SBOM, version pinning, and update boundary. If it adds a viewer, you must handle file parsing, upload, cache, and output interpretation. If it becomes a platform/database, you must handle identity, API, database, audit log, and backup. If it enters a connected medical system, you must handle PACS/HIS, hospital network, update server, remote service, and downtime fallback.

For a general audience, say: "Risk does not suddenly become larger. Responsibility grows every time the product connects to one more thing." A standalone home computer has one risk profile. If it connects to a school system, accounts matter. If it connects to a schoolwide grade database, data permissions matter. If it connects to an admissions platform, service continuity matters. Medical AI is the same. Every layer crossed creates a new evidence burden.

FDA 2026 Guidance also supports this view. FDA says the guidance aims to help marketed medical devices have enough resiliency against cybersecurity threats and addresses premarket documentation for devices with cybersecurity risk. That means FDA is looking at risk in the real device system, not at an isolated algorithm's attractive claim. ([U.S. Food and Drug Administration][1])

For engineers, the hidden content of this slide is the architecture view. Your Cybersecurity Architecture Views document decomposes system workflow into DICOM query C-FIND, transfer C-MOVE, AI model processing, and output C-STORE, and it separates the Internal Protected Boundary from the External Boundary. This kind of architecture view is not for decoration; it reveals trust boundaries, data flows, attack surface, and shared responsibility.

For managers, this slide is a resource-prioritization tool. A small team cannot do everything on day one, but it must at least know which layer it is in. If still at model stage, start with model release card, SBOM, and data lineage. If it already has a viewer, add parser/input/cache/output risk. If it is already a platform, add IAM, API, audit log, and backup. If it connects to a hospital network, add deployment guide, HDO responsibility, incident reporting, and downtime fallback.

Workflow: call it "Product Boundary Review." Whenever a product adds a feature, PM, RD, QA, regulatory, and security ask together: "Did we cross a layer?" Adding a viewer crosses into user-facing workflow. Adding a database crosses into operational responsibility. Adding PACS/HIS crosses into clinical continuity. Every layer-crossing should update architecture, threat model, risk assessment, testing scope, labeling, and Patch SLA.

---

# Slide 6 | Evidence, Not Slogans

This is the densest knowledge slide and the easiest one to overrun. The core sentence must come first: **Regulation wants evidence, not slogans.** The Evaluation System specifically says that if FDA/TFDA/NIST are only named but not operationally translated, Content Depth can reach at most 13/20. So this slide must not become a regulatory reading. It must translate regulation into engineering and governance evidence.

FDA 524B can be compressed into several obligations: monitor, identify, and address postmarket cybersecurity vulnerabilities and exploits, including coordinated vulnerability disclosure; establish processes to reasonably assure the device and related systems are cybersecure; provide postmarket updates and patches; and provide an SBOM including commercial, open-source, and off-the-shelf components. FDA's FAQ explicitly lists these requirements. ([U.S. Food and Drug Administration][2])

The latest meaning of FDA 2026 Guidance is that these obligations must connect to the quality management system. The FDA 2026 page says the guidance provides recommendations for cybersecurity design, labeling, and premarket submission content, and replaces the June 2025 version. Industry commentary also notes that the 2026 update mainly aligns with QMSR / ISO 13485 and keeps core cybersecurity expectations such as SPDF, Threat Modeling, Security Architecture, Security Testing, and SBOM. Your framing can be: "The version update does not ask everyone to redo everything. It reminds us that cybersecurity has entered quality-system language." ([U.S. Food and Drug Administration][1])

For a general audience, use a health-check metaphor. Saying "I am healthy" is not enough. You need test results, physician interpretation, and follow-up records. Medical-device cybersecurity is the same. Saying "We are secure" is not enough. You need architecture, threat model, risk assessment, controls, testing, finding disposition, and patch/retest records.

For engineers, this slide is about traceability. Your attachment already has a full evidence chain: Risk Management Report summarizes risk method, mitigations, testing, residual risks, traceability matrix, and postmarketing plan; Threat Model uses STRIDE; Controls map requirements to design IDs; Testing maps test IDs to pass/fail; Metrics define patch completion rate, time-to-remediate, and time-to-deploy. That is risk -> control -> test -> fix -> evidence.

For managers, translate this into an auditable decision chain. Risk is what we fear. Control is what we do. Test is how we prove it works. Fix is how we respond when problems are found. Evidence is how all of this is preserved. If the chain does not connect, even a thick document set is only a folder. If the chain connects, the documents become product maturity.

A real case is FDA's safety communication on Contec/Epsimed patient monitors. FDA's 2025 update stated that Contec's patch would completely remove networking functionality from the affected devices, making them local-monitoring only. That is a powerful example: a fix is not always "adding functionality." Sometimes, to reduce unacceptable risk, a connectivity feature must be removed. ([U.S. Food and Drug Administration][8])

Workflow: use an "Evidence Chain Ticket." Each finding cannot only say "fixed." It needs Risk ID, Control ID, Test ID, Finding ID, Decision, Retest Evidence, and Archive Location. For example, a Web UI permission issue maps to Spoofing/Elevation of Privilege. Controls may be JWT/RBAC/default-deny. Tests may be unauthorized access or black-box pen test. The decision may be fix now or compensate. The final record must include retest result and release record. That is the engineering loop FDA wants to see.

---

# Slide 7 | Model, Governance, Stack

This slide translates the evidence chain from Slide 6 into three languages the company can actually use internally: model evidence, governance language, and AI stack security. The blueprint clearly says that NIST is shared language here, not a checklist; AI RMF's Govern, Map, Measure, Manage should be separated from CSF 2.0's Govern, Identify, Protect, Detect, Respond, Recover. Do not force everything into one control table.

Model evidence is for regulatory, clinical, and AI teams. It must explain intended use, data, V&V, and limits. In 2020, Taiwan FDA announced the "Technical Guidance for Registration of Medical Device Software Using Artificial Intelligence / Machine Learning Technology" to help prepare registration materials for AI/ML medical-device software. For Taiwan teams, this means AI cannot only claim that the model is accurate. It must explain use, data, verification, and limitations. ([Taiwan FDA][9])

FDA's AI-enabled device software draft guidance also emphasizes total product life cycle. FDA says the draft guidance gives documentation recommendations for marketing submissions for AI-enabled device software functions, supporting FDA's evaluation of safety and effectiveness, and reflecting risk management across the device TPLC. This supports your slide: AI SaMD is not one-time submission; it is lifecycle management. ([U.S. Food and Drug Administration][10])

Governance language is shared by managers, PM, QA, regulatory, and security. NIST CSF 2.0 explicitly expands to all organizations and sectors and strengthens governance and supply chain. NIST also issued a 2026 concept note for an AI RMF Trustworthy AI in Critical Infrastructure Profile, intended to help critical-infrastructure operators turn AI trustworthiness requirements into actionable practices. This means AI risk management has moved from an internal model-team problem into cross-supply-chain, cross-lifecycle, cross-role governance. ([NIST][11])

AI stack security is for engineers. Do not protect only the model; protect runtime and infrastructure too. OWASP LLM Top 10 2025 lists prompt injection, insecure output handling, training data poisoning, model DoS, and supply chain vulnerabilities as risks for LLM applications. iThome's guide also summarizes 2025 LLM risks as prompt injection, sensitive information disclosure, supply chain risk, data and model poisoning, improper output handling, and excessive agency. Even if your product is not an LLM, these trends remind the audience that AI security has expanded into input, output, data, model, supply chain, and runtime. ([OWASP Foundation][12])

For a general audience, say: a trustworthy AI team must answer three questions. First, what can and cannot the model do? Second, who in the company makes risk decisions? Third, is the software and environment that runs the model secure? Missing any one of these means product security is incomplete.

For engineers, this slide can connect to your Risk Assessment. The document uses NIST SP 800-30 likelihood, impact, and risk matrix, and sets acceptance criteria so High / Very High risks must be resolved before release, while all residual risks must be reduced to Moderate or Low and continuously monitored. That is how technical findings become governance decisions.

Workflow: call it "Three-Layer Governance Review." The Model behavior column contains intended use, data split, V&V, and model limits. The Software stack column contains SBOM, provenance, isolation, updates, signing, and runtime controls. The Clinical workflow column contains user roles, human-in-the-loop, continuity, fallback, and residual risk. Use these three columns in every design review so model, engineering, and regulatory teams do not talk past each other.

---

# Slide 8 | Scale 1-2: Model To Viewer

This slide explains the first two product scales. Scale 1 is Model. Scale 2 is Viewer. The blueprint says it well: the Model stage needs artifact, data lineage, SBOM, and update boundary; the Viewer stage adds parser, upload, cache, and output interpretation.

The core of Scale 1 is that **the model itself is an asset**. Non-specialists may think a model is only a file. But for medical AI, a model artifact includes source, version, training-data context, validation results, dependencies, hash/signature, and update boundary. If the model is replaced, tampered with, or used in the wrong version, the clinical output may become untrustworthy.

Your SBOM document is a good backup example. It records that DeepBT Detector-Plus uses Python 3.8+, Node.js 20+, Docker, WSL2, DCMTK, and JSON, and that Docker-based deployment pins dependency versions. It also says external dependencies come from official repositories such as PyPI and npm, while internal components trace source and change history through version control. These are not paperwork details; they are basic capabilities for tracing a model product.

The core of Scale 2 is that **the viewer turns the model into a use context**. Once there is a viewer, someone uploads files, reads DICOM, views screens, and interprets AI output. Attackers do not have to attack the model; they can attack the file parser, malformed DICOM handling, cache, UI error messages, or output interpretation.

A real case is MicroDicom DICOM Viewer. NVD describes CVE-2025-35975 as an out-of-bounds write vulnerability in MicroDicom DICOM Viewer, where an attacker can execute arbitrary code by convincing the user to open a malicious DCM file. CISA also issued a related medical advisory. This is a strong Slide 8 case because it proves that the viewer/parser is not merely a wrapper. It is real attack surface. ([NVD][13])

For a general audience, use an exam and grading-system metaphor. The model is like the teacher, and the viewer is the system that hands the exam paper to the teacher. If someone submits a strangely formatted exam paper and the grading system gets infected when opening it, the teacher's intelligence does not help. The viewer, parser, and upload flow of medical AI are that grading system.

For engineers, this slide can connect to your Architecture Views and Controls. Temporary DICOM Storage must be protected. AI model files need code signing. DICOM transmission needs application-level integrity checks. Error messages should show only brief error codes, avoiding stack traces, internal paths, and library versions. These controls directly map to viewer / parser / cache / output use context.

Workflow: Scale 1 should create a model release card: model version, training/validation dataset references, performance metrics, known limitations, SBOM, hash/signature, and approved intended use. Scale 2 should create a viewer input safety workflow: DICOM conformance validation, file size/type checks, malformed-file testing, fuzzing, temporary data encryption, automatic cache deletion, generic error message, and output limitation notice. That way you are not only saying "viewer has risk"; you are explaining the governance path for the viewer.

---

# Slide 9 | Scale 3-4: Platform To Connected Medical System

This slide moves risk from product interface into company operations and clinical continuity. Scale 3 is Platform / Database. Scale 4 is Connected Medical System. The blueprint asks this slide to show vendor-owned, shared, and hospital-owned risk zones. That is critical because medical AI cybersecurity cannot be completed by the vendor alone, and it cannot be completed by the hospital alone.

The core of Scale 3 is that once there is a platform/database, identity, permissions, APIs, databases, audit logs, and backups appear. At this point, risk is not only "the product has a vulnerability." It is company operational risk. Data leakage affects brand and compliance. API abuse affects service. Incomplete audit logs affect incident investigation. Unavailable backups affect recovery.

In your Risk Assessment, S2 is Web UI user accounts affected by valid-credential impersonation, I2 is sensitive data exposure through insecure storage, D1 is local server unavailability from excessive requests, and E1 is container breakout / privilege escalation. These are exactly the risks that must be addressed once the product becomes a platform.

The core of Scale 4 is that once the product connects to hospital network, PACS/HIS, update server, and remote service, the risk becomes clinical continuity. Your Architecture Views state that DeepBT Detector-Plus is standalone software installed on local workstations, directly interacting with PACS through C-FIND, C-MOVE, and C-STORE, without cloud storage, remote connections, or external internet access, thereby limiting external exposure. That design can be used as an example of reducing product-boundary risk, but you should also be honest: once it connects to a hospital LAN, internal lateral-movement risk still exists.

A real case is Synnovis. NHS says that after the Synnovis cyber incident, the company took a long time to restore services, with full restoration only in December 2024; attackers also published stolen data in June 2024. This case shows that when a healthcare supplier is attacked, the impact is not limited to one product. It affects service recovery, data risk, clinical workflow, and public trust. ([NHS England][14])

Another local example is the MacKay incident. iThome reported that on February 11, 2025, MacKay was attacked by CrazyHunter, hundreds of computers went down, registration systems were affected, and more than one hundred patients were impacted. Follow-up reporting confirmed that the affected scope was mainly emergency rooms in Taipei and Tamsui. This is useful for Slide 9 or Slide 10 as one reminder: "Medical cybersecurity incidents are not abstract; they touch emergency care, registration, medical records, and clinical workflow." ([iThome][15])

For managers, use the financial-sector analogy: finance talks about uninterrupted transactions; telecommunications talks about uninterrupted connectivity; energy talks about uninterrupted supply; healthcare talks about clinical continuity. This line is already in the Talk Design and should be kept. It lets managers understand in one second that cybersecurity is not a cost center. It is service-continuity capability.

Workflow: Scale 3 should establish a platform security baseline: MFA/RBAC, API authorization, rate limit, audit log, encryption-at-rest, and backup/restore drill. Scale 4 should establish a connected deployment checklist: isolated VLAN, Default-Deny host firewall, allowed PACS IP/AE Title, DICOM-TLS or VPN, log forwarding to SIEM/SOC, secure update channel, manual update window, downtime fallback, hospital IT contact, and incident reporting route. Your Labeling document already includes HDO responsibility, isolated VLAN, Default-Deny, port usage, incident reporting, and secure update practice in user guidance. That is strong implementation evidence.

---

# Slide 10 | Cyber Safety Is Patient Safety

This slide is the emotional peak of the whole talk. The screen only needs one sentence: **Cyber Safety Is Patient Safety.** The Evaluation System and Rehearsal Workflow both imply that this slide must not be diluted because it is the center of audience impact. Do not put a checklist, a framework, or dramatic hospital imagery here.

The sentence is not a slogan. The basic direction of FDA 2026 Guidance is to ensure medical devices have enough resiliency against cybersecurity threats, because if devices or healthcare systems are unavailable, untrustworthy, or unrepairable, safety and effectiveness are affected. For your delivery, translate the CIA triad into medical language: Availability is not only uptime; it is whether physicians can obtain results when needed. Integrity is not only unchanged data; it is whether physicians can trust the output. Repairability is not only engineering process; it is whether safe recovery is possible after an incident. ([U.S. Food and Drug Administration][1])

ECRI 2026 Top Health Technology Hazards also supports this point. ECRI lists misuse of healthcare AI chatbots as a major 2026 health technology hazard and also warns about "systems outages / digital darkness." ECRI says LLM tools can appear authoritative but are not designed or validated for medical purposes, and wrong advice may affect patient safety. This can be a Slide 10 supplement: "AI risk is not only cybersecurity. It also includes misplaced trust, misuse, and system outage." ([ECRI and ISMP][16])

Real-world cases can be connected again. Change Healthcare shows that third-party healthcare infrastructure outages affect patient care and finances. Synnovis shows pathology service interruption can take months to recover. MacKay shows that Taiwanese hospital emergency systems can be disrupted by ransomware. Contec shows that medical-device vulnerability patching can directly change device functionality, such as removing networking functionality. Together, these cases support one sentence: medical cybersecurity is not an IT slogan; it is care continuity. ([American Hospital Association][6])

For a general audience, say: "If the system cannot be used, physicians must fall back to manual workflows. If the data cannot be trusted, physicians must reconfirm. If the vulnerability cannot be repaired, the hospital carries long-term risk." For engineers, this line means every security finding needs a clinical-impact field. For managers, it means security budget is not buying tools; it is buying clinical workflow resilience.

Workflow: call it "Cyber-to-Clinical Translation." Add a clinical impact column to every risk register. Does this vulnerability affect confidentiality, integrity, or availability? Could it make AI results untrustworthy? Could it delay clinical workflow? Could it expose multiple patients' data? Does it require downtime fallback? Does it require a hospital advisory? This column lets physicians, managers, QA, regulatory, and security speak one language.

On stage, slow down. Say "Cyber Safety is Patient Safety" and pause. Do not rush into cases. Let the sentence enter the audience's mind first, then add one sentence: "This is not because security people want to make themselves sound important. It is because healthcare settings already tell us that system interruption quickly becomes care interruption."

---

# Slide 11 | White-Box + Black-Box

This slide enters implementation, but it must not become a tool list. The newer blueprint is more precise: the title is "Testing Portfolio: What Question Does Each Test Answer?" In other words, each testing method must answer a decision question. That is more mature than simply saying white-box / black-box.

For a general audience, white-box is like a teacher reading your solution process, while black-box is like an examiner only seeing whether you can be fooled. White-box looks from the inside: code, config, dependency, container, secrets, SBOM. Black-box looks from the outside: login, API, viewer, upload, network exposure, and whether attack paths can be chained.

For engineers, the key is that each test answers a different question. SBOM / SCA answers: "What components do we use, and do they have known vulnerabilities?" White-box answers: "What cheap, fixable, traceable issues can we find before release?" Fuzz / abuse case answers: "Can abnormal input break the workflow?" Black-box answers: "What is visible from the outside?" Pen test answers: "Can vulnerabilities chain into a realistic attack?" Retest answers: "Did the fix really work?"

Your Cybersecurity Testing document is good backup material. CS.T001 tests unauthorized access. CS.T002 tests bcrypt password hashing. CS.T005 tests network isolation, host-based firewall, and secure DICOM transmission. CS.T006 tests encryption-at-rest and model protection. CS.T009 tests audit logging. CS.T010 tests Docker recovery. CS.T011 tests secure update / version locking. CS.T012 is external black-box penetration test. CS.T013 is internal vulnerability scan. That is a testing portfolio, not a tool pile.

MicroDicom is again a useful real case. DICOM viewer vulnerabilities remind us that malformed-file testing and parser robustness are not optional. If opening a malicious DCM file can trigger arbitrary code execution, that is a very concrete threat for any product processing medical images. ([NVD][13])

For managers, the point is: testing is not for making a report look good; testing produces decisions. If test results do not have owner, severity, due date, fix decision, and retest evidence, they are only an outsourced report. Your Unresolved Anomalies document states that after integrated Threat Modeling, Risk Assessment, and external Penetration Testing, no unresolved anomaly exceeded the acceptable risk threshold, and all identified vulnerabilities were remediated or mitigated to Low residual risk. That is a management-level conclusion: not "we tested," but "risk converged."

Workflow: use a "Testing-to-Finding Pipeline." First define scope: Web UI, API, DICOM port, temporary storage, AI model files, update path. Then run white-box: SAST, SCA, secret scan, container config, SBOM matching. Then run black-box: auth bypass, API abuse, DICOM handling, network scan, pen test. Then send findings into Patch SLA, retest after repair, and finally archive evidence. Testing becomes the station before governance, not a list of tool names in the talk.

---

# Slide 12 | Patch SLA

This slide is the operational climax of the talk. The Talk Design explicitly lists "No decision, no governance; no evidence, no trust" as a memory anchor. The Rehearsal Workflow also requires the Decision node on Slide 12 to be visually and verbally central.

First, clarify one thing: Patch SLA is not a fixed term in the original FDA text. It is your translation of FDA 524B's updates / patches, reasonable time, CVD, and postmarket vulnerability management into a company operating model. This translation matters because managers may not understand 524B, but they understand SLA, owner, severity, due date, decision, and evidence.

FDA 524B requires cyber device sponsors to provide plans to monitor, identify, and address postmarket vulnerabilities and exploits, including CVD; it also requires updates and patches plus SBOM. Inside a company, these requirements become: who receives vulnerabilities? Who determines applicability? Who assigns severity? Who decides fix now, compensate, defer, or not applicable? Who notifies customers? Who retests? Where is the evidence stored? ([U.S. Food and Drug Administration][2])

Your Management Plan already handles this with nuance. It uses a dual track: critical vulnerabilities go through expedited mitigation, targeting a Security Advisory and validated compensating controls within 15 calendar days after risk confirmation, and a Risk Mitigation Plan within 30 calendar days. Non-critical vulnerabilities, or vulnerabilities effectively mitigated by network isolation / default-deny firewall, enter the periodic security update cycle. It also states a Safety Override: if a patch may affect AI model accuracy, DICOM structure, or system stability, patient safety and clinical effectiveness take priority over the standard security SLA.

This is important because medical products are not ordinary SaaS. Ordinary SaaS may say "critical patches go live immediately." Medical AI must ask: will this patch change model output? Will it affect DICOM structure? Will it break clinical validation? Therefore, a medical AI Patch SLA is not simply faster-is-better. It is **control risk quickly while not breaking patient safety.**

Your Controls document also implements this in engineering terms: CS.D014 uses immutable infrastructure. It does not patch individual files inside a running container; it replaces the whole digitally signed container image. If a security patch may affect AI model integrity, the update pauses until clinical validation is complete and compensating controls are prioritized.

Your Metrics document makes this slide sound like management language. It defines Patch Completion Rate, Time-to-Remediate, and Time-to-Deploy, and says Time-to-Deploy can stop when an update package is provided to customers through a secure channel or when a Security Advisory / compensating control is delivered to the designated contact. Delays caused by customer-side change management should not count as manufacturer internal performance failure. This is practical because healthcare updates are often governed by HDO change management.

The best real case remains Contec/Epsimed patient monitor. FDA says the Contec patch removes networking functionality, limiting the device to local monitoring. FDA also reminds patients and caregivers not to install the patch themselves; healthcare facility IT/security staff should obtain the patch and installation instructions. This case precisely shows that Patch SLA includes security, clinical impact, installation responsibility, and customer communication. It is not merely "shipping an update package." ([U.S. Food and Drug Administration][8])

Workflow: make it very clear. Intake: vulnerabilities come from internal testing, customer reports, CISA KEV, NVD, and supplier advisories. Triage: determine whether the issue applies to the product, is exploitable, and affects clinical safety. Decision: choose fix now, compensate, defer with timeline, or not applicable with rationale. Action: issue Security Advisory, patch, add firewall rule, update configuration, or document risk acceptance. Retest: verify whether controls are effective. Archive: preserve advisory, risk rationale, test report, release note, and customer notification. This is your Patch SLA operating model.

---

# Slide 13 | Small Team 30 / 60 / 90

This slide should lower pressure without lowering standards. The blueprint defines 30 / 60 / 90 as an adoption scaffold, not a regulatory requirement and not a fixed SLA format. This sentence is important because the audience must not think FDA requires exactly 30/60/90. You are offering a practical way for small teams to start the first evidence loop.

For a general audience, understand 30 / 60 / 90 this way: in the first month, draw the floor plan of the house; in the second month, install locks and cameras; in the third month, ask outsiders to test whether the doors are actually locked. The point is not to become perfect in three months. The point is that after three months, the team stops relying on oral memory and starts producing repeatable evidence.

The 30-day goal is to make the product visible. A small team should create inventory, SBOM, data flow, intended use, and known vulnerabilities. Your SBOM and Architecture Views already show what should be inventoried: product components, external dependencies, hardware requirements, DICOM workflow, Internal Protected Boundary, External Boundary, PACS connection, Temporary DICOM Storage, AI model, and update path.

The 60-day goal is to make risk enter a workflow. Run one STRIDE threat modeling workshop, establish CI security gates, define the finding workflow, and write a customer security note template. Your Threat Model divides threats into S/T/R/I/D/E and maps each threat category to cybersecurity requirement IDs. That can become the simplest workshop template for a small team.

The 90-day goal is external validation and repair evidence. Arrange external black-box pen test, internal vulnerability scan, Patch SLA drill, CVD process, retest evidence, and release-history cleanup. Your Testing and Unresolved Anomalies documents already demonstrate this loop: tests need test ID, tool, method, pass/fail criteria, and result; residual anomalies must state whether they exceed the acceptable risk threshold.

As a current trend, CISA KEV should become a prioritization input for small teams at the 60/90-day stage. CISA says the KEV Catalog is an authoritative source of vulnerabilities exploited in the wild, and organizations should use KEV as an input to vulnerability management prioritization frameworks. Your Management Plan already says internal tools regularly cross-reference the device SBOM against CISA KEV, applicable KEVs are automatically categorized as critical vulnerabilities, applicability assessment is completed within 72 hours, and then the issue enters expedited patching SLA. That is a strong small-team maturity practice. ([CISA][17])

For managers, turn 30/60/90 into three management milestones. After 30 days, the company knows what it has. After 60 days, the company knows how risk enters workflow. After 90 days, the company has external validation and repair evidence. This is much more concrete than "we will keep improving," and easier for boards, investors, hospital procurement, QA, and regulatory teams to accept.

A fictional case: an eight-person AI medical team draws its data flow in 30 days and discovers that DICOM cache has no clear retention policy. In 60 days, STRIDE reveals that AI model tampering and unauthorized PACS access are high-priority risks. In 90 days, black-box pen testing finds TLS/limitation issues in the login interface, so the team first uses IP restriction / firewall compensating controls to reduce risk, then schedules formal repair and retest. This is not something only large enterprises can do. It is a small team's first evidence loop.

---

# Slide 14 | Build Trust Before The Audit

The last slide should close the loop and should not introduce a new framework. The blueprint and Rehearsal Workflow both remind us that Slide 14 must not add new content, another roadmap, or contact-heavy material. This slide only needs the audience to remember the final line: **Build security into the product first; regulatory documents will naturally grow from it.**

The knowledge core is secure-by-design. Do not finish the product and then ask security to patch holes. Do not add documents only before submission. Do not generate an SBOM only when a customer asks. Instead, make security part of product design, development, testing, deployment, and postmarket maintenance. FDA 2026 Guidance places cybersecurity inside Quality Management System Considerations, which supports this close: security is not the final sticker; it is part of the quality system. ([U.S. Food and Drug Administration][1])

For a general audience, use a building fire-safety metaphor. Stairs, alarms, sprinklers, and emergency lighting are not added only after the building is finished. They must exist in the design from the start. Medical AI is the same. Cybersecurity is not a final add-on. It begins with product boundary, data flow, user roles, repair process, and incident reporting.

For engineers, this slide is a reminder that security evidence is not a report format. It is the trace left by normal engineering work. Threat model is not rushed out before review; it is done during architecture design. SBOM is not organized only when customers ask; it is a build artifact. Testing is not only an external report; it is a release gate. Patch SLA is not customer-service language; it is finding governance. Retest evidence is not a screenshot after fixing; it is repair proof.

For managers, the sentence should land on responsibility: mature teams are not the teams with the most documents; they are the teams where every risk can be proven, repaired, and tracked. Your attachment already has a complete evidence package: Risk Management Report, Threat Model, Risk Assessment, SBOM, Safety/Security Vulnerability Assessment, Unresolved Anomalies, Controls, Architecture Views, Testing, Management Plan, Metrics, Labeling, and Software Level of Support. These documents should not be seen as "a pile of documents for FDA." They should be seen as different views of a product-trust system.

You can close like this: "Today we started from a model and walked toward a connected medical system. With every step, the product becomes more valuable, and it also needs to be more trusted, more repairable, and more auditable. So I want to end with one sentence: build security into the product first; regulatory documents will naturally grow from it. A truly mature team is not the one with the most documents, but the one where every risk can be proven, repaired, and tracked. Thank you."

---

# Three Stronger Angles For The Whole Talk

The first upgrade is to frame **FDA 2026 Guidance** as "cybersecurity entering the quality system," not merely "FDA updated a document." Industry commentary also says the 2026 version is mainly QMSR alignment and does not overturn the core technical expectations. This lets the talk sound more mature: "The real point is not chasing versions. The real point is putting cybersecurity evidence into the QMS." ([Hattrick][18])

The second upgrade is to include the **AI lifecycle**. FDA AI-enabled device draft guidance emphasizes TPLC. FDA PCCP guidance also supports AI-enabled devices continuing to iterate within a reviewed change plan while maintaining safety and effectiveness. This connects well with Patch SLA: AI medical devices are not unable to change; they need to know which changes can be preplanned, which changes require safety/clinical validation, and which changes trigger regulatory review. ([U.S. Food and Drug Administration][10])

The third upgrade is to speak in **resilience language**. Taiwan's national cybersecurity strategy, NIST CSF 2.0, NIST AI RMF critical-infrastructure profile, CISA KEV, Change Healthcare, Synnovis, MacKay, and Contec all say the same thing: cybersecurity is not point defense. It is integrated governance across product boundary, supply chain, clinical continuity, repairability, and evidence. ([NIST][11])

One-sentence summary of this stronger version:

**AI SaMD cybersecurity is not about protecting one model. It is about building a product system that can be trusted, repaired, and proven in the real medical world.**

[1]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket "Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions | FDA"
[2]: https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs "Cybersecurity in Medical Devices Frequently Asked Questions (FAQs) | FDA"
[3]: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices "Artificial Intelligence-Enabled Medical Devices | FDA"
[4]: https://www.roche.com/media/releases/med-cor-2026-03-16 "Roche launches NVIDIA AI factory to accelerate the development of new therapeutics and diagnostics solutions"
[5]: https://english.ey.gov.tw/Page/61BF20C3E89B856/3cee52d1-96e4-48e0-b0a3-a7a9ba000ee3 "National Cybersecurity Development Program enters seventh phase (Executive Yuan, R.O.C. (Taiwan)-Executive Yuan Press Releases Detail)"
[6]: https://www.aha.org/news/news/2024-03-15-aha-survey-change-healthcare-cyberattack-having-significant-disruptions-patient-care-hospitals-finances "AHA survey: Change Healthcare cyberattack having significant disruptions on patient care, hospitals' finances | AHA News"
[7]: https://www.ithome.com.tw/news/167327 "MacKay Memorial Hospital 2025 ransomware incident timeline | iThome"
[8]: https://www.fda.gov/medical-devices/safety-communications/cybersecurity-vulnerabilities-certain-patient-monitors-contec-and-epsimed-fda-safety-communication "Cybersecurity Vulnerabilities with Certain Patient Monitors from Contec and Epsimed: FDA Safety Communication | FDA"
[9]: https://www.fda.gov.tw/tc/siteListContent.aspx?id=34961&sid=3787&utm_source=chatgpt.com "Technical guidance for registration of AI/ML medical-device software"
[10]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing "Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations | FDA"
[11]: https://www.nist.gov/news-events/news/2024/02/nist-releases-version-20-landmark-cybersecurity-framework "NIST Releases Version 2.0 of Landmark Cybersecurity Framework | NIST"
[12]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for Large Language Model Applications | OWASP Foundation"
[13]: https://nvd.nist.gov/vuln/detail/cve-2025-35975?utm_source=chatgpt.com "CVE-2025-35975 Detail - NVD"
[14]: https://www.england.nhs.uk/synnovis-cyber-incident/ "NHS England - Synnovis cyber incident"
[15]: https://www.ithome.com.tw/news/167318 "MacKay Hospital attacked by CrazyHunter ransomware; MOHW and cybersecurity authority formed rapid response support | iThome"
[16]: https://home.ecri.org/blogs/ecri-news/misuse-of-ai-chatbots-tops-annual-list-of-health-technology-hazards "Misuse of AI chatbots tops annual list of health technology hazards"
[17]: https://www.cisa.gov/known-exploited-vulnerabilities-catalog?utm_source=chatgpt.com "Known Exploited Vulnerabilities Catalog"
[18]: https://www.hattrick-it.com/blog/cybersecurityguidanceupdate/ "FDA Cybersecurity Guidance 2026: What Changed?"
