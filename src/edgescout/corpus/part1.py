"""edgescout skills 1-15: scope and fingerprint phases."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "authorization-boundary-documentation",
        "title": "Authorization Boundary Documentation",
        "summary": "Write down exactly which hosts, paths, header manipulations and request rates the edge-testing engagement permits before any request leaves the workstation",
        "use_when": "an edge or cache assessment is about to start and the written rules of engagement name no host list, rate ceiling or permitted header set",
        "avoid_when": "the program already publishes a machine-readable scope file and the signed rules of engagement list permitted verbs and header classes",
        "tags": ["scope", "rules-of-engagement", "authorization"],
        "steps": [
            "Collect the signed rules of engagement, the public program page and any scope file into one place and note the document versions you used.",
            "List every in-scope hostname, CDN front door, alternative port and staging alias exactly as written, without normalizing or guessing wildcards.",
            "Record the permitted HTTP verbs, header manipulation classes, request-rate ceiling and the explicit ban list in one table you can quote back.",
            "Confirm whether direct-to-origin requests, cache-busting query strings and authenticated sessions are allowed, since each changes the test plan.",
            "Write the boundary as a short pre-flight checklist you re-read before the first request of every session, not as a note you recall from memory.",
            "Save the boundary text beside the evidence you will collect so a reviewer can prove every recorded request fell inside the permitted set.",
        ],
        "signals": [
            "Rules of engagement mention hosts but are silent on header manipulation or cache-busting",
            "Program page says 'CDN in scope' while the origin IP is marked out of scope",
            "Rate limits are described in prose rather than a number you can enforce",
            "A previous session already recorded requests against a hostname you cannot find in writing",
        ],
        "patterns": [
            (
                "Boundary record",
                "scope:\n  hosts: [app.example.test, api.example.test]\n  verbs: [GET, HEAD]\n  header_classes: [cache-key-probe, forward-rename]\n  direct_origin: forbidden\n  rate_rps: 2\n  cache_bust: allowed",
            ),
            (
                "Pre-flight echo",
                "Before session start, restate: hosts, verbs, header classes, rate ceiling, and the two explicit bans. Any element you cannot quote from the document is a gap to resolve, not a permission to assume.",
            ),
            (
                "Evidence binding",
                "Store boundary.md next to evidence/*.log so each recorded request line has a document version it can be checked against during review.",
            ),
        ],
        "pitfalls": [
            "Reading a wildcard as permission for every subdomain when the program lists specific hosts only",
            "Assuming staging and production share scope because they share a hostname pattern",
            "Treating an old email thread as current authorization after the program changed its rules",
        ],
        "done_when": [
            "A written boundary table names hosts, verbs, header classes, rate ceiling and explicit bans",
            "Every later evidence file carries the document version used to justify it",
        ],
        "refs": [
            "[PortSwigger - Web cache deception](https://portswigger.net/web-security/web-cache-deception)",
            "[OWASP - Testing for improper access control](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "cdn-contract-inventory",
        "title": "CDN Contract Inventory",
        "summary": "Establish which caching layer is contracted to do what, so an unexpected behaviour is measured against the documented configuration rather than a guess",
        "use_when": "the engagement begins with several candidate edge vendors or an undocumented middle proxy sitting between client and application",
        "avoid_when": "a single vendor is already identified and its published caching defaults are known to the team that owns the property",
        "tags": ["cdn", "inventory", "architecture"],
        "steps": [
            "Ask the owner for the current edge vendor list, zone file or DNS records showing which hostnames route through which provider.",
            "Record which layer owns cache policy: origin headers, vendor dashboard rules, infrastructure-as-code, or a mix of all three.",
            "Note any second tier such as an internal reverse proxy, a service mesh sidecar cache or a browser-facing service worker.",
            "List the purge capabilities available to the team: per-URL, prefix, tag, or full flush, and who is allowed to trigger them.",
            "Capture the documented intent per content class: static assets public, personalized responses uncached, API responses short-lived.",
            "Write the inventory as a table of host, layer, policy owner and purge scope, and mark every cell you could not confirm as unknown.",
        ],
        "signals": [
            "DNS answer differs from the hostname the owner believes is being served",
            "Two vendors appear in the response header chain for the same asset class",
            "The owner describes purge behaviour that contradicts the vendor default",
            "A middleware cache exists that no one on the team can configure",
        ],
        "patterns": [
            (
                "Layer table",
                "host | layer | policy owner | purge scope\napp.example.test | vendor-cdn | origin headers | per-url\napi.example.test | vendor-cdn + internal proxy | dashboard rules | tag\nassets.example.test | vendor-cdn | infrastructure-as-code | prefix",
            ),
            (
                "Ownership question",
                "For each host ask: where does a cache directive get written, who can change it, and what happens to a response that carries no directive at all. Silence on the third answer marks an implicit policy.",
            ),
            (
                "Unknown cell rule",
                "Mark any table cell you could not confirm from a document or a live response as unknown and carry it into the fingerprint phase as a question to answer.",
            ),
        ],
        "pitfalls": [
            "Assuming the vendor named in a marketing page is the layer actually answering the request",
            "Ignoring a middleware cache that never appears in vendor documentation or dashboards",
            "Recording purge scope from a remembered incident instead of the current configured behaviour",
        ],
        "done_when": [
            "A layer table covers every in-scope host with policy owner and purge scope",
            "Unknown cells are listed explicitly and assigned to a fingerprint question",
        ],
        "refs": [
            "[MDN - HTTP caching overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)",
            "[OWASP - Reverse proxy and caching misconfiguration](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "personal-data-cache-scope",
        "title": "Personal Data Cache Scope",
        "summary": "Identify the endpoints whose responses contain personal, session-bound or tenant-specific data before testing, so shared-cache behaviour is never exercised against real user records",
        "use_when": "any path can return account, billing, message or tenant data and the cache policy for those paths has not been verified",
        "avoid_when": "the engagement target is exclusively static, public, non-tenant content with a documented shared cache policy",
        "tags": ["personal-data", "privacy", "scope"],
        "steps": [
            "Walk the application's own navigation and API list to enumerate paths that return identifying, financial or tenant-specific fields.",
            "Tag each path by data class: public, internal, personal, secret, since each class implies a different cache requirement.",
            "Check the documented response headers for the personal and secret classes and record whether private or no-store is present.",
            "Create synthetic test accounts and seed data you own, then use only those records for any shared-cache observation.",
            "Note any path that mixes public and personal content in one response, because a single cache rule will apply to the whole body.",
            "Mark the personal-class paths in the plan as observation-only: record headers, never serve one session's body to another.",
        ],
        "signals": [
            "A profile or billing route carries cache-control directives that allow shared storage",
            "Two tenants appear to share a route template differing only in an unkeyed segment",
            "Server-side rendering returns per-user markup on a path with a long freshness lifetime",
            "A response holding personal data omits the private directive entirely",
        ],
        "patterns": [
            (
                "Class ladder",
                "public -> may be stored in a shared cache when policy allows\ninternal -> team-readable, never shared\npersonal -> private, single user or session only\nsecret -> no-store, never written to any shared store",
            ),
            (
            "Header expectation",
            "Cache-Control: private, no-store for personal and secret classes; any value lacking those tokens is a finding, not a starting assumption of safety.",
            ),
            (
                "Synthetic-only rule",
                "Seed only accounts you control, and if a test would require reading another record to compare, stop and record the header evidence instead of the body.",
            ),
        ],
        "pitfalls": [
            "Comparing real user records to prove a shared-cache leak and turning a finding into a privacy incident",
            "Classifying a route by its URL pattern when the response is personalized by a cookie instead",
            "Assuming the absence of a caching header means shared storage is impossible",
        ],
        "done_when": [
            "Every in-scope path carries a data class tag and an expected cache policy",
            "Only synthetic records owned by the tester appear in any recorded evidence",
        ],
        "refs": [
            "[OWASP - Sensitive data exposure](https://owasp.org/www-project-top-ten/)",
            "[MDN - Cache-Control private directive](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "origin-direct-access-scope",
        "title": "Origin Direct Access Scope",
        "summary": "Determine whether contacting the origin outside the edge is permitted, because this single decision changes both the test plan and the class of finding you may produce",
        "use_when": "an origin address may be discoverable from DNS history, certificates or headers and the rules of engagement are silent on direct contact",
        "avoid_when": "the program states plainly that origin addresses are out of scope or that all traffic must pass through the edge",
        "tags": ["origin", "scope", "architecture"],
        "steps": [
            "Search the rules of engagement for the exact terms origin, direct, bypass and IP, and quote the surrounding sentences verbatim in your notes.",
            "When the document is silent, ask the program a direct yes-or-no question about origin contact and wait for the answer before proceeding.",
            "If origin contact is out of scope, restrict discovery to passive observations already visible in responses that traverse the edge.",
            "When permitted, plan a low-rate request set against the origin that mirrors only the synthetic content used elsewhere in the engagement.",
            "Record which findings depend on origin access so a reader can distinguish an edge defect from an origin exposure.",
            "Re-confirm the decision at any change of engagement, since scope updates often reverse this one item without changing host lists.",
        ],
        "signals": [
            "Rules of engagement list a hostname but never mention the address behind it",
            "Certificate transparency or DNS history already reveals candidate origin addresses",
            "Responses differ depending on whether the request arrived through the edge",
            "The program has no written answer to a direct origin-contact question",
        ],
        "patterns": [
            (
                "Decision record",
                "origin_direct: unknown | permitted | forbidden\nsource: <document section or program reply>\ndate: <ISO date>\nconsequence: passive only | low-rate direct tests allowed",
            ),
            (
                "Passive fallback",
                "If origin contact is forbidden, derive evidence only from edge-traversing responses: header chains, error page fingerprints, and routing differences observed from the permitted path.",
            ),
            (
                "Finding label",
                "Tag every finding as edge-observed or origin-observed so a reader never infers a bypass result from a test the boundary forbade.",
            ),
        ],
        "pitfalls": [
            "Probing an origin address that a program considers private infrastructure and turning a finding into a scope breach",
            "Concluding that an origin is unreachable because a firewall rejected the request you were not cleared to send",
            "Reporting an origin exposure as an edge defect when the two layers were never separated in evidence",
        ],
        "done_when": [
            "Origin contact is recorded as permitted or forbidden with a quoted source",
            "Every finding produced later carries an edge-observed or origin-observed label",
        ],
        "refs": [
            "[PortSwigger - Server-side request forgery](https://portswigger.net/web-security/ssrf)",
            "[OWASP - Edge and origin security](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "shared-cache-consent-check",
        "title": "Shared Cache Consent Check",
        "summary": "Confirm that shared caching of the tested content is contractually allowed, since caching a response you were not permitted to share changes the incident class entirely",
        "use_when": "the property sits behind a third-party cache and terms of service, an enterprise agreement or a data-processing addendum may restrict storage",
        "avoid_when": "the owner confirms in writing that all in-scope content is public and may be stored and replayed by any intermediary",
        "tags": ["consent", "cdn", "privacy"],
        "steps": [
            "Read the program terms for words such as cache, store, replicate, archive and intermediary, and quote each sentence that touches storage.",
            "Ask whether third-party edge storage of test content is expected behaviour for the property under the current agreement.",
            "Check whether the agreement restricts the geographic regions where responses may be stored during the assessment.",
            "Note any content class the owner marks as non-cacheable by policy even where no header enforces it yet.",
            "Carry the answer into the plan: shared-cache observations are permitted only for classes the owner explicitly cleared.",
            "Record the consent answer next to your boundary document so a later reader can see why certain tests were skipped.",
        ],
        "signals": [
            "Terms mention data residency while the edge provider operates in other regions",
            "The owner states a no-cache policy that no response header currently enforces",
            "A data-processing addendum lists caching as a sub-processor activity to review",
            "Test content is being replicated to regions the agreement does not cover",
        ],
        "patterns": [
            (
                "Consent matrix",
                "content class | storage permitted | region limit | source\npublic docs | yes | none | terms section 4\naccount pages | no | none | owner reply 2026-05-11\ntenant reports | no | region-limited | dpa annex b",
            ),
            (
                "Silence handling",
                "Absence of a restriction is not consent. Record consent as unknown and limit yourself to header observation until an owner reply resolves it.",
            ),
            (
                "Skip note",
                "When a test is skipped for consent reasons, write one line naming the test, the class and the consent source so the gap is visible in the report.",
            ),
        ],
        "pitfalls": [
            "Treating public availability as permission to have content stored and replayed by a third party",
            "Running a shared-cache observation against a class the owner listed as non-cacheable",
            "Reaching a consent conclusion from a general privacy policy rather than the engagement terms",
        ],
        "done_when": [
            "A consent matrix records storage permission and region limits per content class",
            "Skipped tests appear in the report with the consent reason attached",
        ],
        "refs": [
            "[OWASP - Privacy and data protection considerations](https://owasp.org/www-project-application-security-verification-standard/)",
            "[IETF RFC 9111 - HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "non-destructive-probe-selection",
        "title": "Non-Destructive Probe Selection",
        "summary": "Choose request shapes that reveal caching behaviour without mutating state, so an edge assessment never leaves the property different from how it was found",
        "use_when": "designing the request set for a cache or edge assessment where verbs, headers and query parameters can be varied",
        "avoid_when": "the engagement explicitly commissions state-changing tests and the owner has provided a disposable environment for them",
        "tags": ["methodology", "safety", "probes"],
        "steps": [
            "Prefer GET and HEAD observations and treat any other verb as out of the default plan until a specific question requires it.",
            "Vary one header or query dimension per request so an observed difference can be attributed to exactly one change.",
            "Use cache-busting parameters only where the boundary permits them, and remove them from any request you intend to observe for storage.",
            "Cap request rate at the ceiling from the boundary document and add a pause between probe families to keep logs readable.",
            "Stop a probe family as soon as the behaviour is characterized rather than repeating it across every path.",
            "Write down the exact request shape you used beside each response so a reviewer can reproduce without guessing.",
        ],
        "signals": [
            "A test set includes verbs that create, update or delete server state",
            "Two dimensions change in a single request, making the observed difference ambiguous",
            "Probe volume already exceeds the ceiling written in the boundary document",
            "Repeated identical requests are still running after the behaviour was clear",
        ],
        "patterns": [
            (
                "One-dimension rule",
                "Request N and request N+1 differ in exactly one field: one header, one query parameter, one path segment. Anything else invalidates the comparison.",
            ),
            (
                "Verb whitelist",
                "Default verbs: GET for body comparison, HEAD for header comparison. Every other verb needs a named question and an owner-approved environment.",
            ),
            (
                "Rate note",
                "log line: time, verb, path, changed_dimension, cache_status. If two lines share a timestamp with different dimensions, split them.",
            ),
        ],
        "pitfalls": [
            "Sending a state-changing verb to production while probing whether a response gets stored",
            "Bursting requests fast enough that rate limiting or a purge races your observation",
            "Reusing a session cookie across probes and losing the ability to separate identity from cache effects",
        ],
        "done_when": [
            "The probe set uses only the approved verbs and varies one dimension per request",
            "Each recorded response has the request shape and the changed dimension written beside it",
        ],
        "refs": [
            "[PortSwigger - Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)",
            "[MDN - HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "evidence-hygiene-for-cached-responses",
        "title": "Evidence Hygiene for Cached Responses",
        "summary": "Record edge behaviour without archiving response bodies that may contain personal or session-bound data, keeping the evidence package safe to share with the vendor",
        "use_when": "collecting responses during an edge assessment where any recorded body might contain account data, tokens or tenant content",
        "avoid_when": "the entire test surface is public static content that the owner has cleared for full archiving",
        "tags": ["evidence", "privacy", "reporting"],
        "steps": [
            "Record request line, status, timing and the full caching header set for every observation before considering body capture.",
            "Capture bodies only for synthetic content you own, and redact any value that resembles a token, cookie or account identifier first.",
            "For personal-class responses, store a SHA-256 of the body plus its length instead of the body itself, so sameness can still be proven.",
            "Keep a numbered index linking each evidence line to the boundary document version and the probe that produced it.",
            "Store raw header dumps separately from the narrative report so a reviewer can re-check claims without reading prose.",
            "Delete transient captures once the report is filed, keeping only what the disclosure record requires.",
        ],
        "signals": [
            "An evidence folder contains responses from accounts the tester does not own",
            "Recorded headers include a session cookie or bearer token in clear text",
            "The same account data appears in several unrelated evidence files",
            "A report draft embeds a full response body where a hash would prove the point",
        ],
        "patterns": [
            (
                "Body substitute",
                "sha256: 3f2a... length: 4821 content-class: personal -> proves sameness across two responses without storing either body",
            ),
            (
                "Header record",
                "status=200 age=118 cache-control=private, max-age=0 cf-cache-status=HIT vary=Cookie via=1.1 vendor-edge -> enough to prove shared storage",
            ),
            (
                "Index line",
                "E-014 | 2026-05-11T09:22Z | GET /account | dimension=cookie | boundary v3 | body=hash-only",
            ),
        ],
        "pitfalls": [
            "Pasting a response with a live session token into an issue that a vendor portal will retain forever",
            "Keeping raw captures in a public repository together with the disclosure report",
            "Losing the link between an evidence line and the probe that produced it, which makes the claim unverifiable",
        ],
        "done_when": [
            "No archived evidence contains a session token, cookie or third-party personal record",
            "Every evidence line carries an index, a timestamp and a boundary document version",
        ],
        "refs": [
            "[OWASP - Content security policy and data handling](https://cheatsheetseries.owasp.org/)",
            "[NIST SP 800-53 - audit and accountability](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
        ],
        "meta": {"phase": "scope"},
    },
    {
        "slug": "edge-layer-identification",
        "title": "Edge Layer Identification",
        "summary": "Determine which caching layer actually answers a request by reading the header chain, so every later observation is attributed to the right component",
        "use_when": "a hostname is in scope and the responsible vendor, proxy or internal cache has not been confirmed from a live response",
        "avoid_when": "the owner has already supplied a documented layer diagram that matches observed response headers",
        "tags": ["fingerprint", "cdn", "headers"],
        "steps": [
            "Send a GET for a stable public asset and capture the complete response header set verbatim, including the order headers appear in.",
            "Look for vendor signatures such as a ray identifier, an edge request id, a served-by token or a generic cache status header.",
            "Record every layer named in the via and forwarded chains, since more than one cache may be answering the same request.",
            "Compare a cacheable asset with a dynamic route to see which headers persist across content classes.",
            "Repeat once with a cache-busting parameter to see which headers change between a miss and a hit.",
            "Write the identified layers into the inventory table with the header evidence that justified each entry.",
        ],
        "signals": [
            "A ray or request id header appears only on responses that crossed a vendor edge",
            "The via chain names an intermediary the owner did not list in the architecture note",
            "Header names differ between a static asset and a dynamic route on the same host",
            "A cache status header changes value when only the query string changes",
        ],
        "patterns": [
            (
                "Signature table",
                "header | example value | layer implied\nserver | vendor-edge/2.3 | edge vendor\nvia | 1.1 vendor-edge | edge hop present\nx-cache | hit from edge | edge stored the response\nx-request-id | 8f2c... | origin correlation id",
            ),
            (
                "Miss-hit pair",
                "Same path requested twice with different cache-busting values: the header present only on the second answer marks the storing layer.",
            ),
            (
                "Chain notation",
                "client -> vendor-edge -> internal-proxy -> origin, each layer written only when a header in the response proves that hop exists",
            ),
        ],
        "pitfalls": [
            "Attributing storage to the vendor whose logo appears in a server header while an internal proxy holds the copy",
            "Reading a generic cache header as vendor proof when the origin emits the same header itself",
            "Fingerprinting once and assuming every content class traverses an identical chain",
        ],
        "done_when": [
            "Every in-scope host has a recorded layer chain with the header evidence for each hop",
            "Cache status behaviour is confirmed on at least two content classes",
        ],
        "refs": [
            "[MDN - Via header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Via)",
            "[IETF RFC 9111 - HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "cache-status-header-reading",
        "title": "Cache Status Header Reading",
        "summary": "Read each vendor's cache status vocabulary correctly and map it onto the shared hit and miss states, so a test result is never misread because of naming differences",
        "use_when": "responses carry a cache status header from an unfamiliar vendor or the same word means different things across two layers",
        "avoid_when": "no status header is present and behaviour must be derived from timing and repeat-request comparison instead",
        "tags": ["fingerprint", "headers", "cache-status"],
        "steps": [
            "Capture the vendor's status header verbatim on a first request, a second identical request and a request after a purge, if a purge is permitted.",
            "Map each observed value onto the shared vocabulary of hit, miss, refresh, expired and bypass before drawing any conclusion.",
            "Note compound values where a layer reports upstream and local states in one token, since only one of them describes storage.",
            "Check whether the header is present on error responses as well, because cached errors change availability behaviour.",
            "Record which content classes produce which status values, since policy often differs between static and dynamic routes.",
            "Keep the mapping table with your evidence so a reader who knows another vendor can follow the result.",
        ],
        "signals": [
            "The same vendor token appears with a qualifier that names a second layer",
            "A status value flips between two tokens without any change to the request",
            "Error responses carry a status token identical to successful cached responses",
            "One content class never reports a status header at all",
        ],
        "patterns": [
            (
                "State map",
                "vendor token -> shared state\nhit, fresh, served-from-edge -> hit\nmiss, not-in-cache, refresh -> miss\nexpired, stale, revalidated -> expired\nbypass, no-store, uncacheable -> bypass",
            ),
            (
                "Compound value",
                "tcp_hit/200 or HIT, HIT means the outer layer stored it; write the layer next to the token instead of collapsing both into 'cached'.",
            ),
            (
                "Flip test",
                "two identical requests, no intervening change: if the token flips, an independent event such as a purge or expiry happened and must be noted",
            ),
        ],
        "pitfalls": [
            "Reading a miss token as evidence the response was never stored by an upstream layer",
            "Comparing tokens from two vendors as if their vocabularies were defined by the same specification",
            "Ignoring a missing status header, which usually means the layer in front does not expose its state",
        ],
        "done_when": [
            "A token mapping table exists for every status header observed in scope",
            "Hit, miss and bypass states are confirmed by repeat requests rather than assumed from naming",
        ],
        "refs": [
            "[IETF RFC 9111 - Section 4 cache validation](https://www.rfc-editor.org/rfc/rfc9111)",
            "[MDN - Age header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Age)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "freshness-and-age-derivation",
        "title": "Freshness and Age Derivation",
        "summary": "Derive how long a stored response stays fresh from cache-control and age, so probe timing matches the property's real storage window instead of a guess",
        "use_when": "planning repeat observations where the remaining freshness lifetime determines whether a second request reaches the origin",
        "avoid_when": "the response carries no-store or no-cache and therefore never becomes fresh in any shared cache",
        "tags": ["fingerprint", "ttl", "headers"],
        "steps": [
            "Read cache-control from the response and record each directive that affects storage: max-age, s-maxage, no-store, no-cache, private, must-revalidate.",
            "Read the age header to learn how long the stored copy has already been in the cache before your request reached it.",
            "Compute remaining freshness as max-age minus age, using s-maxage where a shared cache honours it over max-age.",
            "Check whether a later response from the same path reports a smaller age, which indicates revalidation or a fresh store rather than expiry.",
            "Record the derived window beside the path so probe spacing can sit comfortably inside it.",
            "Note any path where the origin sets one lifetime and the observed window is longer, since a second policy layer is overriding the header.",
        ],
        "signals": [
            "Observed storage outlives the longest directive the origin ever sent",
            "The age value grows across requests and then resets without a purge",
            "s-maxage and max-age differ, and the shared cache appears to honour the larger one",
            "A no-store response still returns an age header from an upstream layer",
        ],
        "patterns": [
            (
                "Window arithmetic",
                "remaining = max_age - age_seconds; probe twice inside remaining, then once after it to observe revalidation behaviour",
            ),
            (
                "Directive table",
                "max-age=60 s-maxage=300 -> shared cache may hold 300s, browser holds 60s\nno-store -> no store anywhere, age header should stay 0\nprivate -> shared cache must not store, single client may",
            ),
            (
                "Override check",
                "header says max-age=60 but observed window is 300s: write 'policy layer present' and continue fingerprinting the layer that added it",
            ),
        ],
        "pitfalls": [
            "Spacing probes by a remembered default instead of the lifetime this response actually declares",
            "Treating an age header on a no-store response as proof that storage occurred",
            "Computing the window from max-age while the shared cache honours a different directive",
        ],
        "done_when": [
            "A freshness window is recorded per tested path with the directives that produced it",
            "Probe spacing sits inside the derived window and is repeated once outside it",
        ],
        "refs": [
            "[IETF RFC 9111 - Calculating freshness lifetime](https://www.rfc-editor.org/rfc/rfc9111)",
            "[MDN - Cache-Control max-age](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "cache-key-composition-probing",
        "title": "Cache Key Composition Probing",
        "summary": "Infer which request dimensions make up the cache key by varying one dimension at a time and observing whether the served copy changes",
        "use_when": "the key composition of an in-scope path is undocumented and later tests depend on knowing what separates two stored copies",
        "avoid_when": "the owner supplies a key configuration from their vendor console or infrastructure-as-code repository",
        "tags": ["fingerprint", "cache-key", "methodology"],
        "steps": [
            "Establish a baseline: fetch the path with no added parameters twice and confirm both answers carry the same cache status and body.",
            "Vary one dimension at a time and record whether the status token changes, which reveals whether that dimension separated the lookup.",
            "Test candidate dimensions in this order: path, query parameters as a set, individual query parameters, host, then selected headers.",
            "Include headers commonly used for content negotiation, such as accept and accept-language, because they frequently sit outside the key.",
            "For each dimension, note whether a different body, a different status or neither result indicates keyed or unkeyed behaviour.",
            "Write a key composition statement naming every dimension you proved keyed and every dimension you proved unkeyed.",
        ],
        "signals": [
            "Changing a query parameter returns the identical stored body and status token",
            "Two paths differing only in a trailing separator share one stored copy",
            "An accept-language change alters the body while the status token stays a hit",
            "A dimension you expected to be keyed produces no observable difference at all",
        ],
        "patterns": [
            (
                "Key statement",
                "keyed: scheme, host, path, query-set\nunkeyed: accept-language, x-forwarded-host, utm params\nunknown: cookie, authorization",
            ),
            (
                "Pairing log",
                "dimension | request A status/body | request B status/body | verdict\nquery ?a=1 vs ?a=2 | hit/identical | hit/identical | unkeyed\naccept-language en vs fr | hit/body-x | hit/body-y | keyed",
            ),
            (
                "Unknown reserve",
                "Dimensions whose behaviour cannot be observed safely stay marked unknown and get a conservative assumption in the audit phase.",
            ),
        ],
        "pitfalls": [
            "Changing two dimensions in one request and attributing the difference to whichever one you were thinking about",
            "Assuming a dimension is keyed because it is named in vendor documentation rather than in observed behaviour",
            "Forgetting that an unkeyed dimension which changes the response is the precondition for a poisoning finding",
        ],
        "done_when": [
            "A key statement lists every dimension proved keyed, unkeyed or unknown",
            "Each verdict is backed by a paired request log line with both status tokens",
        ],
        "refs": [
            "[PortSwigger - Web cache poisoning fundamentals](https://portswigger.net/web-security/web-cache-poisoning)",
            "[IETF RFC 9111 - Vary and cache keys](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "origin-versus-edge-error-signature",
        "title": "Origin Versus Edge Error Signature",
        "summary": "Separate errors generated at the edge from errors returned by the origin, so an availability finding is attributed to the layer that actually produced it",
        "use_when": "an error response appears during testing and the report must say which layer generated it",
        "avoid_when": "the response carries a correlation id that the owner already maps to a single known layer",
        "tags": ["fingerprint", "errors", "attribution"],
        "steps": [
            "Capture the complete error response including status, headers and any body fingerprint, without attempting to influence the error further.",
            "Compare its header set with a known-good response from the same host to see which vendor headers are missing or added.",
            "Check whether the error carries an age or cache status token, which tells you whether the error itself was stored.",
            "Repeat the same request once with a cache-busting parameter to see whether the origin reproduces the same error.",
            "Note the correlation id or request id and ask the owner which layer logs it, since only one layer will have that record.",
            "Record the attribution as edge-generated, origin-generated or stored-error, each with the evidence line that proves it.",
        ],
        "signals": [
            "The error body lacks the vendor header chain present on successful responses",
            "An error response carries an age value greater than zero",
            "The same error appears with and without a cache-busting parameter",
            "A vendor-branded error page shows no origin correlation id at all",
        ],
        "patterns": [
            (
                "Attribution table",
                "status | vendor headers | age | correlation id | attribution\n503 | present | 0 | vendor-token | edge-generated\n500 | present | 118 | origin-token | stored-error\n502 | absent | 0 | none | origin-generated",
            ),
            (
                "Bust compare",
                "same path with and without a bust parameter: identical error body plus identical origin id means the origin produced it, not the edge",
            ),
            (
                "Stored-error note",
                "if age is above zero on an error, write that the error was replayed from storage and treat availability impact accordingly",
            ),
        ],
        "pitfalls": [
            "Reporting a vendor-generated maintenance page as an origin outage",
            "Treating a cached error as a live one and exaggerating the availability impact",
            "Concluding the origin is healthy because the edge served a stored success while origin fails",
        ],
        "done_when": [
            "Every observed error is labelled edge-generated, origin-generated or stored-error with evidence",
            "At least one error class is confirmed by a cache-busted repeat request",
        ],
        "refs": [
            "[MDN - 502 Bad Gateway](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/502)",
            "[OWASP - Error handling and information leakage](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "secondary-layer-detection",
        "title": "Secondary Layer Detection",
        "summary": "Detect caching layers below the vendor edge, such as an internal proxy or service worker, because a defect in the lower layer will never show up in vendor status headers",
        "use_when": "a behaviour difference exists between two clients that both traverse the same vendor edge",
        "avoid_when": "the architecture note confirms there is exactly one caching layer between client and origin",
        "tags": ["fingerprint", "architecture", "layers"],
        "steps": [
            "Compare responses from two different client contexts that share the same edge, noting differences the vendor status token cannot explain.",
            "Inspect the response for directives that only a downstream layer would honour, such as proxy-revalidate or a stale directive.",
            "Check whether conditional requests are answered by the edge or passed through, since revalidation at a lower layer leaves a distinct header pattern.",
            "Look for storage hints in service-worker or application-cache behaviour on the client side of the property.",
            "Ask the owner about middleware caches, read-through caches and API gateways that store responses in front of the application.",
            "Record each discovered layer in the inventory with the observation that revealed it.",
        ],
        "signals": [
            "Two clients behind the same edge receive different bodies for the same key",
            "A response changes only after a browser reload or a service-worker update",
            "The origin logs a request that the edge status header says was served from cache",
            "An internal proxy appears in a forwarded chain on error responses only",
        ],
        "patterns": [
            (
                "Layer question list",
                "Is there a reverse proxy with caching? a gateway cache? a read-through cache? a browser service worker? an application-level memoization of responses? Record each answer with a source.",
            ),
            (
                "Evidence pair",
                "client A hit/body-1 and client B hit/body-2 on the same key: the differentiator must be a layer below the edge or an unkeyed dimension",
            ),
            (
                "Revalidation trace",
                "conditional request answered with 304 at the edge versus forwarded to origin: the header set differs and identifies which layer validated",
            ),
        ],
        "pitfalls": [
            "Stopping the fingerprint once the vendor edge is identified while an internal cache holds the interesting copy",
            "Blaming the edge for a difference produced by a service worker running on the client",
            "Assuming an internal cache was disabled because it does not appear in vendor documentation",
        ],
        "done_when": [
            "Every identified caching layer appears in the inventory with a revealing observation",
            "Behaviour that vendor status headers cannot explain is attributed to a named layer",
        ],
        "refs": [
            "[MDN - Service worker overview](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)",
            "[OWASP - Reverse proxy testing](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "vary-variant-mapping",
        "title": "Vary Variant Mapping",
        "summary": "Map how the vary header splits one key into variant sub-entries, since a leak or a miss behaves differently per variant rather than per path",
        "use_when": "a response carries vary and later tests need to know whether two requests share a stored variant or occupy separate ones",
        "avoid_when": "the response carries no vary directive and no other header hints at content negotiation",
        "tags": ["fingerprint", "vary", "cache-key"],
        "steps": [
            "Record the exact vary token list from the response and note which request headers it names.",
            "For each named request header, issue two requests differing only in that header and observe whether the status token separates them.",
            "Include cookie and authorization in the map when the origin names them, since those variants carry identity-bound content.",
            "Check whether vary is present on the first response but missing on a later one for the same path, which marks an inconsistent policy.",
            "Record the variant count actually observed rather than the theoretical count implied by the header list.",
            "Carry the map into the audit phase as the model of which requests can collide and which are guaranteed to be isolated.",
        ],
        "signals": [
            "Vary names a header the edge does not include in its lookup at all",
            "One variant is served fresh while another for the same path is served from storage",
            "The vary list differs between a first response and a repeat response on the same path",
            "Vary lists an entire header class such as cookie, implying many stored variants",
        ],
        "patterns": [
            (
                "Variant map",
                "path: /search\nvary: accept-encoding, accept-language\nobserved variants: en, fr, default -> 3 entries, keyed by accept-language only",
            ),
            (
                "Split check",
                "two requests, same path, one header differing: same status token means one entry serves both variants, different token means the header splits the key",
            ),
            (
                "Inconsistent policy",
                "vary present on first answer and absent later: record the transition, because the missing list is where two variants can start to collide",
            ),
        ],
        "pitfalls": [
            "Assuming vary always appears in the stored entry when it is only sent on the first response",
            "Counting theoretical variants from the header list instead of the ones actually observed",
            "Forgetting accept-encoding, which splits variants on every path and hides the dimension you meant to study",
        ],
        "done_when": [
            "A variant map records the vary list and the observed variant count per path",
            "Every named header has a separate observation proving keyed, unkeyed or inconsistent behaviour",
        ],
        "refs": [
            "[IETF RFC 9111 - Vary validation](https://www.rfc-editor.org/rfc/rfc9111)",
            "[MDN - Vary header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Vary)",
        ],
        "meta": {"phase": "fingerprint"},
    },
    {
        "slug": "config-propagation-model-detection",
        "title": "Config Propagation Model Detection",
        "summary": "Work out whether edge configuration is pushed from a control plane or pulled from origin headers, because it decides who owns a fix and how fast a change takes effect",
        "use_when": "the owner describes cache rules but the effective behaviour on a path contradicts what the origin sends",
        "avoid_when": "one configuration source is documented and its effect matches observed behaviour on every tested path",
        "tags": ["fingerprint", "configuration", "architecture"],
        "steps": [
            "Pick a path where origin cache headers and observed storage disagree, and record both sides of the contradiction verbatim.",
            "Check whether the disagreement follows a vendor rule pattern such as an override or a bypass list that only a control plane could apply.",
            "Ask where the rule lives: dashboard, configuration repository, deployment pipeline or origin code, and note the answer's source.",
            "Test propagation timing only if the owner permits a configuration change, otherwise record it as an open question for the owner.",
            "Check whether different edge locations disagree, which would indicate a rollout that has not finished propagating.",
            "Write a one-paragraph ownership statement saying which layer would have to change to alter the observed behaviour.",
        ],
        "signals": [
            "A path stores responses the origin explicitly marks as not storable",
            "The owner names a dashboard rule that contradicts a header seen in responses",
            "Two edge locations return different cache behaviour for an identical request",
            "A recent configuration change explains a behaviour shift seen between test sessions",
        ],
        "patterns": [
            (
                "Contradiction record",
                "path: /api/report\norigin says: Cache-Control: no-store\nobserved: stored, age=118, status hit\nconclusion: control-plane rule overrides origin directive",
            ),
            (
                "Ownership statement",
                "To change this behaviour, edit <layer> via <channel>; origin header changes alone would not take effect because the control-plane rule wins.",
            ),
            (
                "Propagation note",
                "If two locations disagree, record the timestamp of both observations and treat the configuration as mid-rollout rather than inconsistent by design",
            ),
        ],
        "pitfalls": [
            "Reporting an origin header fix when a control-plane rule would continue to override it",
            "Assuming configuration is pushed when a pull-based default silently applies vendor caching rules",
            "Calling a mid-rollout difference a bug and filing it before propagation had finished",
        ],
        "done_when": [
            "Each tested path has a recorded contradiction or a confirmed alignment with its configuration source",
            "An ownership statement names the layer and channel that would change the behaviour",
        ],
        "refs": [
            "[OWASP - Cache control directives](https://cheatsheetseries.owasp.org/)",
            "[IETF RFC 9111 - Caching in HTTP](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "fingerprint"},
    },
]