# Tamimah Prospecting & Daily Reporting Agent --- Specification

**Version:** 1.0\
**Prepared from:** Tamimah Telecom & Computer Technology (TTCT) Company
Profile 2026 and the 2 November 2026 requirements meeting\
**Primary operating market:** Sultanate of Oman\
**Primary user:** Ismail\
**Primary output:** Daily business-development report, delivered
preferably through WhatsApp\
**Operating cadence:** Five days per week

------------------------------------------------------------------------

## 1. Purpose

Build an AI-assisted business prospecting and reporting agent for
Tamimah Telecom & Computer Technology (TTCT).

The agent must identify **real businesses in Oman** that plausibly match
Tamimah's target customer profile, explain which Tamimah product or
service may be relevant to each business, and prepare a daily report
that Ismail can review and share with his manager.

The initial operational requirement is to produce **five researched
walk-in prospects per reporting day**.

This is not a generic company-list generator. It is an ICP-led B2B
prospecting system that connects a prospect's observable business
characteristics to a relevant Tamimah offering.

## 2. Business context

The supplied 2026 company profile describes Tamimah Telecom & Computer
Technology as an Omani technology company, headquartered in Muscat,
established in 1984, and part of the Tamimah Group. It designs, builds,
hosts and supports platforms and services for government, enterprise and
telecom customers.

The profile states, among other credentials:

-   30+ platforms across seven business pillars.
-   400+ projects delivered across the GCC.
-   35+ contact centres delivered in Oman and Qatar.
-   80+ mobile and web applications in production.
-   Omani ownership and Riyada SME certification.
-   Solutions can be hosted in Oman, on-premise or in hybrid
    environments, depending on the offering.

The profile presents the following seven business pillars. The agent
must use these as the initial product taxonomy, while prioritising only
the offerings that Ismail confirms are in scope for his sales activity.

### 2.1 Tamimah's seven business pillars

1.  **AI & Intelligent Automation**
    -   Raddak: AI voice contact centre in Omani Arabic or English.
    -   AI Speech Analytics: call quality and compliance analysis.
    -   Mabel: live voice translation.
    -   Vision: camera-based intelligent vision solutions.
    -   AI Twin: lifelike digital humans.
    -   ASISTA: agentic AI for multi-step processes with human control.
    -   Alloo: no-code chatbot with live-agent handoff.
    -   AIoT: AI on sensors and edge devices, including predictive
        maintenance and alerts.
    -   AI Factory workspace and AI services: AI chat, knowledge/RAG,
        OCR, integrations, hosting and operations.
2.  **Messaging & Communication**
    -   Bulk SMS, OTPs, alerts and two-way SMS through REST/SMPP APIs.
    -   Mass SMS marketing.
    -   ERSAL: SMS, WhatsApp, voice, email and push communication.
    -   ALERTA: multi-channel crisis alerts and escalation.
    -   EKO: encrypted team chat and video on customer-owned servers.
3.  **Customer Experience & Engagement**
    -   TawasulCX: omnichannel contact-centre platform for voice,
        WhatsApp, social and email.
    -   Rafed: CRM and social inbox, SLAs, case management and customer
        view.
    -   Operon: field-service booking, dispatch, job cards and
        invoicing.
    -   Level: loyalty, rewards and campaigns across app, web and store.
    -   Contact-centre services and related implementation/support.
4.  **Smart Cities & Connected Infrastructure**
    -   Smart Parking and ANPR-enabled parking solutions.
    -   NEXT IoT: sensors, cameras, dashboards and alerts.
    -   MeshTrac: asset and people tracking using BLE, LoRaWAN and RFID.
    -   AynX 360: GPS command centre, geofencing and audit.
5.  **Enterprise Platforms**
    -   Odoo implementation and support for CRM, inventory, accounting,
        HR, payroll and projects.
    -   ERPNext services for sovereign deployments.
    -   B2C, B2B and marketplace e-commerce.
    -   Tamimah Pay: payment gateway/API integrations.
    -   Amlak: asset and inventory management.
6.  **Industry Solutions**
    -   Shiply: logistics, suppliers, warehouses and fleets.
    -   SmartCare: telehealth and e-prescriptions.
    -   Wasel: gas-cylinder delivery with GPS and cashless payment.
    -   We Meet: sports court booking and team formation.
    -   Yumzy: white-label delivery platform.
    -   CERCLE: club management and member app.
7.  **Workforce & Digital Workplace**
    -   Tareeqi: route planning and live field-team tracking.
    -   Digipazz: visitor invitations, QR passes and host alerts.
    -   xCard: NFC business cards with QR fallback.
    -   Voxo: surveys across multiple channels.
    -   Amilify: project management using Kanban and Gantt.
    -   MANZAR: digital-screen CMS and monitoring.

**Source boundary:** This product taxonomy is taken from the supplied
company profile. It does not establish that every offering is currently
assigned to Ismail, actively being sold, available in every market
segment, or appropriate for every prospect. Confirm sales priorities
with Ismail before treating any offering as an active campaign.

## 3. Objective and success criteria

### 3.1 Minimum viable objective

On each of five reporting days per week, the agent should:

1.  Discover businesses located in Oman.
2.  Evaluate them against the approved ICP.
3.  Select five qualified businesses as potential walk-in prospects.
4.  Provide evidence-backed business details and a reason each may fit.
5.  Prepare the daily report using activity data supplied by Ismail.
6.  Deliver the report to Ismail through the approved channel,
    preferably WhatsApp.

### 3.2 Success criteria

-   Exactly five **qualified** walk-in suggestions are included when
    five can be verified.
-   Every prospect is a real business with a traceable source.
-   No business is represented as visited, contacted, called, met or
    demonstrated to unless Ismail confirms that activity.
-   Each prospect is mapped to a specific Tamimah offering or relevant
    business pillar.
-   The report distinguishes researched recommendations from completed
    sales activity.
-   Duplicate prospects are suppressed across recent reports.
-   Missing data is marked as unknown or not supplied, not invented.
-   Ismail can review and share the report without substantial
    reformatting.

If fewer than five prospects meet the minimum quality threshold, the
agent must report the shortfall and provide only the qualified prospects
found. It must not pad the list with weak or fabricated entries.

## 4. Users and responsibilities

### Ismail

-   Supplies or approves the company profile and ICP refinements.
-   Confirms which Tamimah services/products he is responsible for
    selling.
-   Supplies actual daily counts/details for calls, meetings and demos,
    and follow-ups.
-   Reviews the report and shares it with his manager.
-   Confirms whether any suggested prospect was actually visited or
    contacted.

### Agent

-   Conducts research and prospect qualification.
-   Generates five potential walk-in prospects per reporting day,
    subject to quality rules.
-   Maps prospects to Tamimah offerings.
-   Drafts the report using supplied activity data.
-   Delivers the report after the configured review/approval process.
-   Maintains source, duplicate and report history.

### Manager

-   Receives the report from Ismail.
-   The agent is not required to communicate directly with the manager
    in the initial version.

## 5. ICP framework

The profile provides a broad portfolio and reference customer sectors,
but it does **not** provide a final, explicit ICP for Ismail's sales
assignment. The agent must therefore support a configurable ICP and must
not silently assume that every sector or product is equally important.

### 5.1 Initial sector taxonomy

The company profile identifies customer sectors including:

-   Government and public bodies.
-   Public bodies, justice and defence.
-   Banking and insurance.
-   Energy and industry.
-   Telecom, media and education.
-   Aviation, travel and mobility.
-   Business groups and finance.
-   Retail, health and culture.

These sectors may be used as initial discovery categories, subject to
Ismail's approval and any restrictions on government or regulated-sector
outreach.

### 5.2 Initial prospect hypotheses

The following are **hypotheses for testing**, not confirmed sales
priorities:

  -----------------------------------------------------------------------
  Prospect type           Potential need          Relevant Tamimah
                                                  capability
  ----------------------- ----------------------- -----------------------
  Banks and financial     OTPs, secure messaging, Messaging, EKO,
  institutions            customer support,       TawasulCX, AI
                          alerts                  

  Hospitals and           Patient communication,  Messaging, AI,
  healthcare groups       contact centre,         TawasulCX, SmartCare
                          appointment workflows   

  Logistics and fleet     Fleet visibility, route MeshTrac, AynX 360,
  operators               planning, asset         Tareeqi, Shiply
                          tracking                

  Retail chains and       Inventory, ERP, CRM,    Odoo, ERPNext, Amlak,
  multi-branch groups     loyalty, e-commerce     Level, eCommerce

  Industrial and energy   Asset monitoring,       AIoT, NEXT IoT,
  companies               predictive maintenance, MeshTrac, Tareeqi
                          workforce tracking      

  Telecom and large       Messaging, customer     ERSAL, SMS, TawasulCX,
  service providers       experience, AI          AI Factory
                          automation              

  Hotels and hospitality  Customer engagement,    Rafed, ERSAL, Odoo, AI
  groups                  CRM, messaging,         
                          operations              

  Educational             Notifications,          SMS, ERSAL, AI,
  institutions            applications,           mobile/web apps
                          communication and       
                          support                 

  Large business groups   ERP, integrations,      Odoo, ERPNext, ASISTA,
                          workflow automation,    Amilify
                          digital workplace       
  -----------------------------------------------------------------------

The agent must state the specific reason for a match. An industry label
alone is not sufficient evidence of need.

### 5.3 Required ICP configuration

Before production use, maintain an editable configuration with:

-   Approved products/services for Ismail.
-   Priority sectors and excluded sectors.
-   Target organisation size or minimum scale, if applicable.
-   Target cities/regions in Oman.
-   Preferred prospect types and disqualifiers.
-   Whether public-sector organisations are in scope.
-   Whether existing customers, partners or competitors should be
    excluded.
-   Required contact-person seniority, if decision-maker research is
    included.
-   Any minimum evidence requirement.

If a value has not been provided, leave it configurable and label it
**TBD**. Do not invent an answer.

## 6. Prospect discovery and research

### 6.1 Primary source

Google Maps was identified in the meeting as the primary lead-generation
source.

Use it to discover and verify local business listings, including:

-   Business name.
-   Business category.
-   Location/address.
-   Public phone number, where listed.
-   Website, where listed.
-   Google Maps listing URL.
-   Reviews or other public listing signals only where useful and
    accurately represented.

### 6.2 Supporting sources

Where available and permitted, enrich the prospect using:

-   The business's official website.
-   Official company pages and public business directories.
-   Publicly accessible company profiles.
-   Official public announcements or service pages.

Google Maps is the primary discovery source; it should not be treated as
proof of company size, technology requirements, budget, decision-maker
identity or purchase intent.

### 6.3 Search strategy

The agent should search by a combination of:

-   Approved industry.
-   Business type.
-   City/region in Oman.
-   Relevant operational characteristics.
-   Relevant Tamimah product/use case.

Search coverage should be systematic rather than repeatedly searching
only broad terms such as "companies in Oman".

### 6.4 Verification

For each selected business:

-   Confirm that the listing appears to represent a real operating
    organisation.
-   Confirm that the location is in Oman.
-   Prefer an official website or a reliable public listing.
-   Cross-check material details when possible.
-   Record the source URL and the date checked.
-   Mark missing or uncertain details clearly.

Do not create contact details, website URLs, addresses or company facts.

## 7. Prospect qualification and scoring

Use a transparent 100-point score. Scores are prioritisation aids, not
proof of buying intent.

  ------------------------------------------------------------------------
  Criterion                                   Weight Evaluation
  --------------------- ---------------------------- ---------------------
  ICP/industry fit                                25 Does the organisation
                                                     belong to an approved
                                                     target segment?

  Offering fit                                    25 Is there a clear
                                                     connection to an
                                                     approved Tamimah
                                                     product/service?

  Business                                        15 Is there public
  scale/complexity                                   evidence of relevant
                                                     operational
                                                     complexity or scale?

  Evidence of potential                           15 Is there a visible
  use case                                           business process,
                                                     service or operating
                                                     model that maps to
                                                     the offering?

  Oman presence and                               10 Is the business
  verifiability                                      verifiably
                                                     located/operating in
                                                     Oman?

  Contactability                                  10 Is there a usable
                                                     public business
                                                     contact channel?
  ------------------------------------------------------------------------

Suggested bands:

-   **80--100:** High-priority prospect.
-   **65--79:** Qualified prospect.
-   **50--64:** Research further; do not include in the five unless
    Ismail approves.
-   **Below 50:** Do not include.

A prospect must meet the minimum verification requirements regardless of
score. A high numerical score must never override fabricated, missing or
contradictory evidence.

## 8. Daily reporting requirements

The meeting established four report categories:

1.  Calls made.
2.  Meetings and demos.
3.  Walk-ins.
4.  Follow-ups.

A separate "New Leads" section is **not required**.

### 8.1 Calls made

-   Data must be supplied or confirmed by Ismail.
-   The agent may format and summarise the supplied data.
-   The agent must not infer that calls occurred from a prospect list.

### 8.2 Meetings and demos

-   Data must be supplied or confirmed by Ismail.
-   Distinguish meetings scheduled from meetings completed.
-   Distinguish demos offered from demos actually delivered, if the
    supplied data supports that distinction.

### 8.3 Walk-ins

-   The agent generates five researched businesses as **suggested
    walk-in prospects**.
-   Each entry should contain the business name, location, public
    contact information where available, relevant Tamimah offering,
    qualification rationale, source and score.
-   These are recommendations for possible visits, not evidence that
    visits occurred.
-   If Ismail later confirms an actual visit, the report may record it
    as completed activity.

### 8.4 Follow-ups

-   Data must be supplied or confirmed by Ismail.
-   The agent may organise follow-up details by business, status and
    next action.
-   It must not claim a follow-up was completed unless confirmed.

### 8.5 Missing activity data

If Ismail has not supplied activity data, use a clear label such as
**"Not supplied"** or **"Awaiting Ismail's update."** Do not fill
missing activity fields with plausible-looking numbers.

## 9. Daily workflow

1.  **Load configuration:** Read the current ICP, approved product
    focus, exclusions and reporting date.
2.  **Review recent history:** Load previous prospect lists to avoid
    unnecessary repeats.
3.  **Discover:** Search Google Maps for businesses in the approved Oman
    target areas and sectors.
4.  **Enrich:** Check official websites and other permitted public
    sources.
5.  **Qualify:** Apply hard verification rules, ICP fit and scoring.
6.  **Deduplicate:** Compare against the prospect history and remove
    duplicate businesses.
7.  **Select:** Choose up to five best-qualified walk-in prospects.
8.  **Collect activity data:** Use Ismail's supplied calls,
    meetings/demos and follow-up information.
9.  **Generate report:** Produce the agreed four-section report.
10. **Quality check:** Validate sources, dates, counts, wording and
    factual claims.
11. **Approval and delivery:** Send the report to Ismail through the
    approved WhatsApp workflow, or provide a shareable draft if
    automated delivery is not configured.
12. **Log outcome:** Save the report, sources, prospects, delivery
    status and any corrections.

## 10. Report format

**Daily Business Development Report --- Tamimah Telecom**

**Date:** \[Reporting date\]

### 1. Calls Made

\[Ismail-confirmed activity data or "Not supplied".\]

### 2. Meetings & Demos

\[Ismail-confirmed activity data or "Not supplied".\]

### 3. Walk-in Prospects

For each of up to five prospects:

-   **Business:** \[Verified name\]
-   **Industry:** \[Industry/category\]
-   **Location:** \[Oman location\]
-   **Public contact:** \[Phone, if verified\]
-   **Website:** \[Official URL, if verified\]
-   **Relevant Tamimah offering:** \[Specific product/service\]
-   **Why it may fit:** \[Evidence-based rationale\]
-   **Priority:** \[Score and band\]
-   **Source:** \[Google Maps and supporting sources\]
-   **Suggested next step:** \[Research-backed, non-deceptive
    recommendation\]

Add a clear note: **"These are researched prospect suggestions; they are
not recorded as completed visits."**

### 4. Follow-ups

\[Ismail-confirmed follow-up data or "Not supplied".\]

**Prepared for Ismail --- internal business-development reporting.**

The report should be concise enough to read and forward through
WhatsApp. A longer prospect appendix may be provided separately if
useful.

## 11. Delivery requirements

Preferred channel: WhatsApp.

The initial system should support:

-   Preparing a WhatsApp-ready text report.
-   Sending it to Ismail only after the destination number and delivery
    method are configured and authorised.
-   Reporting whether delivery succeeded or failed.
-   Retrying only under a defined, safe retry policy.
-   Providing a copyable report if WhatsApp automation is unavailable.

The meeting did not establish a WhatsApp API provider, destination
number, authentication method or approved sending account. These are
implementation dependencies and must be configured rather than assumed.

## 12. Data model

Recommended entities:

### Prospect

-   `prospect_id`
-   `business_name`
-   `normalised_business_name`
-   `industry`
-   `business_category`
-   `city`
-   `address`
-   `phone`
-   `website`
-   `google_maps_url`
-   `source_urls[]`
-   `source_checked_at`
-   `tamimah_pillar`
-   `relevant_offering`
-   `fit_rationale`
-   `qualification_score`
-   `qualification_band`
-   `verification_status`
-   `first_seen_at`
-   `last_seen_at`
-   `last_reported_at`
-   `status` (suggested, contacted, visited, disqualified, converted,
    etc.)
-   `status_evidence`
-   `notes`

### Daily activity

-   `report_date`
-   `calls_data`
-   `meetings_data`
-   `demos_data`
-   `followups_data`
-   `provided_by`
-   `provided_at`
-   `confirmation_status`

### Daily report

-   `report_id`
-   `report_date`
-   `prospect_ids[]`
-   `activity_record_id`
-   `report_text`
-   `quality_check_status`
-   `approval_status`
-   `delivery_channel`
-   `delivery_status`
-   `delivered_at`
-   `correction_history`

### ICP configuration

-   `approved_offerings[]`
-   `priority_sectors[]`
-   `excluded_sectors[]`
-   `target_regions[]`
-   `minimum_score`
-   `minimum_verification_requirements`
-   `duplicate_lookback_days`
-   `reporting_days`
-   `report_delivery_preferences`

## 13. Integrations and implementation considerations

Potential integration categories:

-   Google Maps / Places data source for local business discovery,
    subject to API access, licensing and usage terms.
-   Web search or website retrieval for public-source enrichment.
-   Persistent database or CRM for prospects, history, deduplication and
    reports.
-   WhatsApp Business Platform or an approved provider for report
    delivery.
-   A secure input mechanism for Ismail to submit daily activity data.
-   Scheduler/orchestrator for five reporting days per week.

No specific vendor, API, database or automation platform was mandated in
the meeting. Choose based on existing Tamimah infrastructure, access,
cost and maintainability.

## 14. MVP scope

### Include in MVP

-   Configurable ICP.
-   Tamimah product/service taxonomy.
-   Oman business discovery with Google Maps as primary source.
-   Public-source enrichment.
-   Prospect qualification and scoring.
-   Five qualified walk-in suggestions per reporting day where
    available.
-   Duplicate prevention.
-   Four-section daily report.
-   Ismail-provided activity data.
-   WhatsApp-ready report and delivery integration once authorised.
-   Report and source history.

### Exclude from MVP unless separately approved

-   Automated calling.
-   Automated WhatsApp outreach to prospects.
-   Sending sales pitches to businesses.
-   Booking meetings or walk-ins.
-   Claiming that a prospect has been contacted or visited.
-   Predicting budgets or purchase intent without evidence.
-   Scraping restricted or access-controlled data.
-   Generating fictional activity metrics.
-   Direct submission to the manager without Ismail's review.

## 15. Open questions / implementation blockers

These questions must be resolved with Ismail:

1.  Which exact Tamimah products/services is Ismail responsible for
    selling?
2.  Which sectors are highest priority, and which should be excluded?
3.  Are government and public-sector organisations in scope for this
    prospecting workflow?
4.  Is the target market all of Oman or specific cities/regions?
5.  Is there a minimum company size or business profile?
6.  Should the agent identify named decision-makers, or are public
    business contact details sufficient?
7.  What are the reporting days and preferred delivery time?
8.  What exact format/sample report should be reproduced?
9.  How will Ismail submit calls, meetings/demos and follow-up data?
10. Which WhatsApp number and approved API/provider should receive the
    report?
11. Should Ismail approve each report before it is sent?
12. What is the required duplicate exclusion window?

Until answered, keep these as configuration fields or clearly labelled
assumptions.

## 16. Acceptance tests

The MVP is ready for pilot when it can demonstrate that:

-   A run searches only the configured Oman geography.
-   Each selected business has a traceable source.
-   Each selected business has an explicit ICP and offering match.
-   The agent does not invent phone numbers, websites or business
    details.
-   Duplicate businesses are detected against prior reports.
-   Five prospects are selected only when five pass the quality
    threshold.
-   Fewer than five qualified prospects results in a transparent
    shortfall.
-   The report contains exactly the four requested categories and no
    separate New Leads section.
-   Activity figures are populated only from Ismail-confirmed input.
-   Suggested walk-ins are labelled as suggestions, not completed
    visits.
-   The report is readable in WhatsApp format.
-   Delivery status and report history are logged.

------------------------------------------------------------------------

**Core product principle:** The agent should optimise for useful,
verifiable business opportunities---not the appearance of activity or
the number of rows in a report.
