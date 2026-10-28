"""edgescout skills 31-50: detect, harden and document phases."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "origin-address-exposure-detection",
        "title": "Origin Address Exposure Detection",
        "summary": "Notice when responses or published records reveal the address behind the edge, since an exposed origin bypasses every edge control the property relies on",
        "use_when": "the assessment includes observing whether infrastructure behind the edge is discoverable from permitted sources",
        "avoid_when": "origin discovery is out of scope and only edge-traversing observations are permitted",
        "tags": ["detect", "origin", "recon"],
        "steps": [
            "Confirm from the boundary document which sources are permitted for this observation: responses, published records, or nothing beyond the edge.",
            "Read error pages, debug output, mail records and certificate records that already traverse or sit beside the permitted path.",
            "Look for direct addresses in response headers, comment fields, redirects and any alternate-name entry the property publishes.",
            "Record each candidate with the exact source that revealed it, and mark the source as passive or active accordingly.",
            "Check whether the candidate would be reachable outside the edge only if the boundary permits such a check; otherwise leave it unverified.",
            "Report exposure with the discovery source and a note on which edge controls a direct path would sidestep.",
        ],
        "signals": [
            "A response header names an internal address or a private hostname",
            "An error page displays an internal service address or a stack trace with one",
            "Published mail or certificate records point at an address the team did not intend to publish",
            "A debug endpoint reachable through the edge echoes upstream connection details",
        ],
        "patterns": [
            (
                "Source record",
                "candidate: 203.0.113.10\nsource: response header via upstream address\npassive/active: passive\nverified reachable: not tested (out of scope)",
            ),
            (
                "Edge-control note",
                "a direct path would skip: edge firewall rules, rate limits, geo controls and edge authentication, all listed so impact is concrete",
            ),
            (
                "Allowed-source list",
                "permitted: response headers, published records. forbidden: direct connection tests. write both before collecting anything",
            ),
        ],
        "pitfalls": [
            "Actively connecting to a candidate address when the boundary allows passive observation only",
            "Reporting a public load-balancer address as an exposed origin when it is a documented front door",
            "Omitting which edge controls a direct path would bypass, which leaves the impact vague",
        ],
        "done_when": [
            "Each candidate has a recorded source labelled passive or active with a verification status",
            "The report names the specific edge controls a direct path would sidestep",
        ],
        "refs": [
            "[PortSwigger - SSRF as an origin discovery side effect](https://portswigger.net/web-security/ssrf)",
            "[OWASP - Infrastructure disclosure](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "clean-state-reproduction-recipe",
        "title": "Clean-State Reproduction Recipe",
        "summary": "Produce a reproduction that starts from an empty cache state every time, so a reviewer or the vendor can replay the observation without inheriting your stored entries",
        "use_when": "an edge observation must be handed to a vendor or a reviewer who will replay it in a different environment",
        "avoid_when": "the behaviour is deterministic and cannot depend on stored state, which a repeat request already proved",
        "tags": ["detect", "reproduction", "evidence"],
        "steps": [
            "Identify every cache layer that could hold state between your requests: edge, internal proxy and browser-side storage.",
            "Use a cache-busting parameter or a fresh request shape where the boundary permits it, so the lookup starts cold.",
            "Open a clean client context with no cookies and no storage, so identity does not influence which entry is selected.",
            "Write the exact request sequence in order, including waits, so the sequence can be replayed without interpretation.",
            "Record the status token for each step so a reader can tell a cold lookup from a warm one.",
            "Package the recipe with the observation it produced and note any step that a vendor might not be able to reproduce.",
        ],
        "signals": [
            "A reproduction succeeds on your machine but fails for a reviewer using a warm browser session",
            "The first request of a session behaves differently from every later request",
            "A step in the sequence has no recorded status token, leaving the state ambiguous",
            "The recipe relies on a stored entry from an earlier test that a purge has since removed",
        ],
        "patterns": [
            (
                "Recipe block",
                "1. open clean context, no cookies\n2. GET /path?bust=1 -> expect miss\n3. GET /path?bust=1 -> record status\n4. GET /path -> record status and body hash\nrecord every status token",
            ),
            (
                "State declaration",
                "declare the layers cleared before step 1: edge entry unknown, internal proxy cleared or not, browser storage cleared",
            ),
            (
                "Repro note",
                "if a step cannot be replayed outside your session, write it as an environment assumption rather than presenting it as deterministic",
            ),
        ],
        "pitfalls": [
            "Writing a reproduction that silently depends on entries your earlier probes created",
            "Omitting the clean-context step, so the reviewer's identity selects a different entry",
            "Presenting an environment-dependent sequence as though it were deterministic",
        ],
        "done_when": [
            "A numbered recipe records every request with its status token and the cleared layers",
            "The recipe reproduces in a fresh context without relying on entries from earlier tests",
        ],
        "refs": [
            "[PortSwigger - Reproducing cache issues](https://portswigger.net/web-security/web-cache-poisoning)",
            "[NIST - Evidence handling guidance](https://csrc.nist.gov/publications/detail/sp/800-86/final)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "cross-client-leak-confirmation",
        "title": "Cross-Client Leak Confirmation",
        "summary": "Confirm whether one client can receive content stored for another by alternating two sessions you own, and stop at the header evidence if bodies would diverge",
        "use_when": "a path appears to serve a stored response across identities and the finding needs confirmation rather than suspicion",
        "avoid_when": "the response marks itself private and alternating sessions already confirm isolation",
        "tags": ["detect", "isolation", "shared-cache"],
        "steps": [
            "Create two synthetic sessions with distinct content you own, so any mismatch is between your own records.",
            "Request the same path alternately with session A, session B and then A again, recording the status token each time.",
            "Compare a stable fingerprint of the response, such as a hash of a non-sensitive region, rather than archiving whole bodies.",
            "Check whether the mismatch follows the session or the storage, by repeating the alternation after a purge.",
            "If bodies would contain personal content beyond your own records, stop and report the header-level evidence instead.",
            "Record the alternation log with the verdict: isolated, shared, or indeterminate with the reason it could not be settled.",
        ],
        "signals": [
            "Session B receives content whose fingerprint matches what session A received earlier",
            "The mismatch persists across several alternations rather than appearing once",
            "A purge changes which session receives which entry, tying the behaviour to storage rather than identity",
            "The origin's own logs show a single fetch while two clients received the same content",
        ],
        "patterns": [
            (
                "Alternation log",
                "A -> hash-1 hit\nB -> hash-1 hit   <- mismatch, expected hash-2\nA -> hash-1 hit\npurge\nA -> hash-2 miss\nB -> hash-2 miss  <- behaviour changed after purge",
            ),
            (
                "Fingerprint rule",
                "hash a non-sensitive region such as a length or a marker string; if no such region exists, fall back to header comparison alone",
            ),
            (
                "Stop condition",
                "if confirming would require reading a third party's record, record the header evidence and mark the verdict indeterminate",
            ),
        ],
        "pitfalls": [
            "Continuing an alternation once bodies from another tenant would be read to settle it",
            "Concluding a leak from a single mismatch that a purge or expiry could explain",
            "Archiving full bodies as proof when a fingerprint would establish sameness",
        ],
        "done_when": [
            "An alternation log records hash and status per turn for at least two full cycles",
            "The verdict names isolation, sharing, or indeterminate with the stop condition that applied",
        ],
        "refs": [
            "[OWASP - Cache-based isolation testing](https://owasp.org/www-project-web-security-testing-guide/)",
            "[IETF RFC 9111 - Shared cache requirements](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "conditional-request-behavior-audit",
        "title": "Conditional Request Behavior Audit",
        "summary": "Check how validators behave at the edge, since a mismatched etag or not-modified handling can serve stale state or mask an update that already happened at the origin",
        "use_when": "responses carry validators such as etag or last-modified and the edge participates in revalidation",
        "avoid_when": "the path uses no validators and revalidation never occurs for any tested request",
        "tags": ["detect", "validators", "revalidation"],
        "steps": [
            "Capture the etag and last-modified values from an initial response and record whether the edge reported it as stored.",
            "Send a conditional request with the captured validator and record status, headers and cache status token.",
            "Modify content through the application's own supported path if permitted, then repeat the conditional request.",
            "Check whether the edge revalidated against the origin or answered from its stored copy without contacting it.",
            "Verify that a changed etag at the origin produces a fresh answer at the edge rather than a not-modified built from stale state.",
            "Record each conditional exchange with the validator used, the status and which layer answered it.",
        ],
        "signals": [
            "A conditional request returns not-modified while the origin's current content hash differs",
            "The etag reported by the edge never changes after an update made through the application",
            "A conditional request is answered from storage without a corresponding origin fetch in logs",
            "Weak and strong validators are mixed in a way that lets a changed body keep an old validator",
        ],
        "patterns": [
            (
                "Exchange line",
                "if-none-match: W/\"abc\" -> 304, status hit, origin fetch: none -> edge answered alone\nafter update: if-none-match: W/\"abc\" -> 200, status miss, new etag -> revalidated",
            ),
            (
                "Validator compare",
                "record origin etag and edge-reported etag per observation; a persistent mismatch marks stale revalidation state",
            ),
            (
                "Layer attribution",
                "304 with no origin fetch means the edge held the validator; a 304 accompanied by an origin fetch means the origin confirmed it",
            ),
        ],
        "pitfalls": [
            "Reading a 304 as proof the content is current when only the edge's stored copy was consulted",
            "Comparing validators across representations that were never meant to be the same resource",
            "Skipping the update step, which is the only way to see whether revalidation actually reaches the origin",
        ],
        "done_when": [
            "Each conditional exchange records validator, status, cache token and origin involvement",
            "At least one exchange is repeated after a content update to confirm revalidation behaviour",
        ],
        "refs": [
            "[IETF RFC 9110 - Conditional requests](https://www.rfc-editor.org/rfc/rfc9110)",
            "[MDN - ETag header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/ETag)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "range-request-key-collision",
        "title": "Range Request Key Collision",
        "summary": "Check whether partial-content requests share a key with full requests, because a range answer stored under one key can be replayed as another client's whole resource",
        "use_when": "the property serves resources that clients request with range headers, such as downloads or media",
        "avoid_when": "the origin returns the complete resource for every request regardless of the range header",
        "tags": ["detect", "range", "cache-key"],
        "steps": [
            "Request the resource normally and record the full answer's status, cache token and content length.",
            "Request the same path with a range header covering a small span and record status, content range and cache token.",
            "Repeat the full request after the ranged one to see whether a partial answer is returned where the whole resource is expected.",
            "Check whether the range header participates in the key, using the pairing evidence from the two requests.",
            "Test a second range span to see whether different spans share one entry or create separate entries.",
            "Record the collision as observed, not observed, or indeterminate, with the request pair that justifies the label.",
        ],
        "signals": [
            "A request with no range header returns a partial answer after a ranged request was made",
            "The cache status token is identical for a full request and a ranged request on the same path",
            "Different spans appear to share one stored entry",
            "A content range header is present on an answer to a request that sent no range",
        ],
        "patterns": [
            (
                "Pair log",
                "GET /file            -> 200, length 100000, hit\nGET /file Range 0-99  -> 206, content-range 0-99, hit\nGET /file            -> 206, content-range 0-99 -> collision observed",
            ),
            (
                "Span compare",
                "range 0-99 and range 100-199: same status token means one entry for both spans, different token means spans are keyed separately",
            ),
            (
                "Verdict labels",
                "collision observed | no collision | indeterminate, each written with the pair line rather than a narrative claim",
            ),
        ],
        "pitfalls": [
            "Reporting a collision from a single pair without the follow-up full request that reveals replay",
            "Testing one span only, which cannot distinguish sharing from per-span storage",
            "Forgetting that some servers ignore range requests entirely, making the whole check meaningless for that path",
        ],
        "done_when": [
            "A pair log records full, ranged and post-ranged requests with status, length and cache token",
            "A span comparison shows whether spans share or split the stored entry",
        ],
        "refs": [
            "[IETF RFC 9110 - Range requests](https://www.rfc-editor.org/rfc/rfc9110)",
            "[MDN - Range header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Range)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "redirect-chain-storage-behavior",
        "title": "Redirect Chain Storage Behavior",
        "summary": "Trace how each hop of a redirect chain is stored, because a cached intermediate hop can trap clients in a loop or send them to a target that has since changed",
        "use_when": "an in-scope path answers with redirects and any hop may be subject to shared storage",
        "avoid_when": "the path returns a single permanent redirect that the owner confirms is immutable",
        "tags": ["detect", "redirects", "cache-key"],
        "steps": [
            "Follow the chain hop by hop and record status, location header and cache status token for each hop separately.",
            "Check which hops are stored and for how long, using the freshness directives each hop carries.",
            "Look for a hop whose stored location differs from what the origin currently returns for that same path.",
            "Test whether a purge of the first hop clears the later hops or leaves intermediate entries in place.",
            "Check for a loop that only appears when a stored hop is combined with a client-side redirect rule.",
            "Record the chain as a table of hop, status, location, stored, lifetime, with the anomaly in its own row.",
        ],
        "signals": [
            "An intermediate hop is stored while the final target is not",
            "A stored location points at a target the origin has since changed",
            "Purging the first hop leaves a later hop still reported as stored",
            "The chain behaves differently when replayed from a clean context than from a warm one",
        ],
        "patterns": [
            (
                "Hop table",
                "hop 1: 301 location /a hit lifetime 86400\nhop 2: 302 location /b miss lifetime 0\nhop 3: 200 hit lifetime 3600",
            ),
            (
                "Target drift",
                "stored location on hop 1 vs current origin location: if they differ, record the old target and the moment it stopped being correct",
            ),
            (
                "Purge sweep",
                "purge hop 1, then re-request each later hop: entries that survive are the ones the purge scope did not reach",
            ),
        ],
        "pitfalls": [
            "Reporting the chain as a whole when only one specific hop is stored or wrong",
            "Following redirects with a tool that caches locally and confusing that with edge storage",
            "Missing a loop that requires a clean context to appear, because a warm session follows different hops",
        ],
        "done_when": [
            "A hop table records status, location, stored state and lifetime for every hop",
            "Target drift and purge sweep results are recorded as separate rows with evidence",
        ],
        "refs": [
            "[IETF RFC 9110 - Redirect status codes](https://www.rfc-editor.org/rfc/rfc9110)",
            "[MDN - Location header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Location)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "decode-order-mismatch-detection",
        "title": "Decode Order Mismatch Detection",
        "summary": "Detect when the edge and the origin decode a request differently, since a decoding gap lets one interpretation reach the cache and a different one reach the application",
        "use_when": "the key statement shows encoding affects lookup and the origin may decode input on a different schedule than the edge",
        "avoid_when": "both layers are proven to produce identical normalized paths and parameters for every variant tested",
        "tags": ["detect", "encoding", "cache-key"],
        "steps": [
            "Build a small variant set covering single encoding, double encoding, mixed case escapes and an overlong separator.",
            "Request each variant and record status, location and cache status token without adding any other variation.",
            "Compare the edge's view of the normalized path with the origin's view, using the application's own routing response as the origin side.",
            "Look for a case where two variants land on one stored entry while the origin treats them as different routes.",
            "Check whether a rejected variant's error response is stored and later served for an accepted variant.",
            "Record each mismatch with the variant pair, the stored entry they shared and how the origin treated each.",
        ],
        "signals": [
            "Two encodings of one path share a stored entry while the origin routes them differently",
            "An error for one variant is stored and later returned for a different variant",
            "A decoded path reaches the application with a form the edge never evaluated",
            "Trailing-separator or dot-segment variants normalize differently at each layer",
        ],
        "patterns": [
            (
                "Variant pair",
                "variant A: /path%2fsub -> stored entry E1, origin route: /path/sub\nvariant B: /path/sub    -> stored entry E1, origin route: /path/sub  <- same entry, confirm intentionally",
            ),
            (
                "Decode ladder",
                "note decode count at each layer: edge once, application twice, or the reverse; an unequal ladder is where interpretations diverge",
            ),
            (
                "Error reuse line",
                "stored 404 for variant A later returned for variant B: record both spellings and the status token on each response",
            ),
        ],
        "pitfalls": [
            "Testing only fully encoded variants and missing the mixed or double-encoded case where layers disagree",
            "Concluding a mismatch without asking the origin how it routed each variant",
            "Reporting a decode difference that has no effect because no entry is stored for either variant",
        ],
        "done_when": [
            "A variant table records status, location and cache token for every encoding tested",
            "Any shared entry names both spellings and states how the origin routed each",
        ],
        "refs": [
            "[IETF RFC 3986 - Percent-encoding normalization](https://www.rfc-editor.org/rfc/rfc3986)",
            "[PortSwigger - Path confusion](https://portswigger.net/web-security/request-smuggling)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "cross-location-content-drift",
        "title": "Cross-Location Content Drift",
        "summary": "Check whether the same key returns different content at different edge locations, since drift means purges and deploys have not converged everywhere",
        "use_when": "the property operates in multiple regions or the owner reports that changes appear unevenly across users",
        "avoid_when": "a single edge location serves all traffic and the owner confirms one deployment domain",
        "tags": ["detect", "consistency", "operations"],
        "steps": [
            "Request the same key through each permitted entry point or region and record status, cache token and content fingerprint.",
            "Compare the fingerprints across locations and record which locations agree and which diverge.",
            "After an application-side change, repeat the comparison to see whether the change propagated everywhere.",
            "Check whether a purge reached all locations or only the one where it was issued.",
            "Note the time elapsed between issuing a change and every location reporting the new fingerprint.",
            "Report drift with the diverging locations, the fingerprints and the convergence time actually observed.",
        ],
        "signals": [
            "Two locations return different fingerprints for the same key at the same time",
            "A purge issued in one location leaves others serving the previous content",
            "A deploy is visible on one region while another still returns the prior version",
            "Convergence takes longer than the team's stated rollout expectation",
        ],
        "patterns": [
            (
                "Drift table",
                "location | fingerprint | status | observed at\neu | a1f2 | hit | 09:12Z\nus | 77bc | hit | 09:12Z  <- divergence",
            ),
            (
                "Convergence note",
                "change issued 09:10Z, all locations agree 09:14Z -> 4 minutes observed, recorded as the actual rollout window",
            ),
            (
                "Purge reach",
                "purge issued at one location: re-request the same key at every location and record which returned a miss",
            ),
        ],
        "pitfalls": [
            "Measuring drift once and treating a mid-rollout snapshot as a permanent inconsistency",
            "Comparing locations at different times and blaming propagation for a difference caused by timing",
            "Reporting drift without the convergence measurement that would tell the owner how large it really is",
        ],
        "done_when": [
            "A drift table records fingerprint, status and timestamp for every location tested",
            "A convergence time is measured after a change or purge rather than estimated",
        ],
        "refs": [
            "[Cloudflare - Cache propagation across locations](https://developers.cloudflare.com/cache/)",
            "[IETF RFC 9111 - Cache coherence expectations](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "identity-header-key-separation",
        "title": "Identity Header Key Separation",
        "summary": "Verify that identity-bearing headers separate stored entries, since a key that ignores identity is the shortest path from one account's content to another's",
        "use_when": "content selection depends on identity headers such as cookie or authorization and storage is permitted on the path",
        "avoid_when": "the response is marked no-store, in which case no shared entry can exist for any identity",
        "tags": ["detect", "authentication", "cache-key"],
        "steps": [
            "Identify which header the origin actually uses to select content, by inspecting its own responses rather than guessing.",
            "Build two synthetic sessions you own that produce visibly different content on the same path.",
            "Request the path with each session and record status token, cache token and a fingerprint of a non-sensitive region.",
            "Request the path with no identity header at all to see whether an unauthenticated answer occupies the same entry.",
            "Check whether the identity header appears in the key statement, and record the verdict if it does not.",
            "Report separation as proven, broken or indeterminate with the alternation evidence for each case.",
        ],
        "signals": [
            "The key statement lists no identity header while the origin selects content by one",
            "An unauthenticated request receives content that belongs to a session",
            "Two sessions receive the same fingerprint on a path meant to be per-account",
            "Removing the identity header changes nothing about which stored entry answers",
        ],
        "patterns": [
            (
                "Separation line",
                "session A -> hash-1, hit\nsession B -> hash-2, hit\nno identity -> hash-1, hit  <- unauthenticated share with A",
            ),
            (
                "Identity discovery",
                "ask the origin: send two requests differing only in the identity header and see whether content changes; that header is the one the key must include",
            ),
            (
                "Verdict labels",
                "proven (all three requests separate correctly) | broken (any sharing observed) | indeterminate (bodies could not be compared)",
            ),
        ],
        "pitfalls": [
            "Assuming the key includes a header that the origin uses without ever proving it",
            "Concluding separation from a single pair when a cold store can produce the same appearance",
            "Continuing an alternation that would require reading another tenant's content to settle",
        ],
        "done_when": [
            "Three-way evidence covers two sessions plus an unauthenticated request with fingerprints recorded",
            "The verdict is labelled proven, broken or indeterminate with the evidence attached",
        ],
        "refs": [
            "[OWASP - Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)",
            "[IETF RFC 9111 - Shared cache key requirements](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "detect"},
    },
    {
        "slug": "explicit-key-dimension-policy",
        "title": "Explicit Key Dimension Policy",
        "summary": "Write down which request dimensions belong in the cache key and which must be excluded, so key composition becomes a reviewed decision rather than an inherited default",
        "use_when": "key composition was discovered by probing and no reviewed document says what the key should contain",
        "avoid_when": "the owner already maintains a reviewed key policy that matches observed behaviour",
        "tags": ["harden", "cache-key", "policy"],
        "steps": [
            "List every dimension observed during fingerprinting and audit, marking each proven keyed, unkeyed or unknown.",
            "For each dimension decide whether it must be in the key because it changes content, or excluded because it never does.",
            "Write the resulting policy as a short table with one row per dimension and the reason for its placement.",
            "Require that identity-bearing dimensions be present in the key wherever storage is permitted on that path.",
            "Route unknown dimensions to a conservative default, either excluded from key and not stored, or keyed and documented.",
            "Have the owner review and store the table beside the configuration, so a later change can be checked against it.",
        ],
        "signals": [
            "Key composition is known only to whoever last edited the vendor console",
            "Dimensions proven non-contributing are still splitting entries",
            "An unknown dimension sits in the key with no recorded reason",
            "Identity dimensions are absent from the key on a path that stores responses",
        ],
        "patterns": [
            (
                "Policy table",
                "dimension | placement | reason\npath | in key | changes content\nauthorization | in key | selects identity\nutm params | excluded | never changes output\nx-forwarded-host | excluded and rejected | untrusted input",
            ),
            (
                "Unknown default",
                "unknown dimension -> treat as content-changing and key it, unless the owner explicitly accepts the storage cost of the alternative",
            ),
            (
                "Review line",
                "policy reviewed by <role> on <date>; every later configuration diff must explain a row it changes",
            ),
        ],
        "pitfalls": [
            "Writing a policy that describes current behaviour rather than what the behaviour should be",
            "Allowing an unknown dimension to stay in the key silently, which hides its capacity cost",
            "Leaving identity dimensions out of the key on a path whose responses are personalized",
        ],
        "done_when": [
            "A policy table covers every dimension observed with placement and reason per row",
            "The owner has reviewed the table and it sits beside the configuration source",
        ],
        "refs": [
            "[IETF RFC 9111 - Vary and cache keys](https://www.rfc-editor.org/rfc/rfc9111)",
            "[OWASP - Configuration management](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "unkeyed-input-rejection",
        "title": "Unkeyed Input Rejection",
        "summary": "Make the edge and the origin ignore untrusted input that never participates in the key, closing the path between a reflected header and a stored shared response",
        "use_when": "an unkeyed header was proven to influence the response during the audit phase",
        "avoid_when": "every header that influences output is already part of the key and the response is marked private",
        "tags": ["harden", "headers", "defense"],
        "steps": [
            "List the specific headers proven unkeyed and influential, and write each one down by its exact name.",
            "Configure the edge to drop or override those headers before the request reaches the application.",
            "Configure the origin to reject or normalize the same headers independently, since one layer alone is not a durable fix.",
            "Re-run the original pairing test that first revealed the influence and confirm the response no longer changes.",
            "Add the rejection to configuration-as-code so the fix survives a dashboard reset or a rebuild.",
            "Record the retest result with the original pairing log so the closure is provable rather than asserted.",
        ],
        "signals": [
            "A header known to be unkeyed still reaches the application after the first fix attempt",
            "Only the edge drops the header while the origin continues to honour it",
            "The fix lives only in a console and disappears on the next configuration deploy",
            "The original pairing test still produces a differing response after the change",
        ],
        "patterns": [
            (
                "Rejection record",
                "header | layer | action | retest result\nx-original-url | edge | drop | response unchanged\nx-original-url | origin | reject | response unchanged",
            ),
            (
                "Retest rule",
                "reuse the exact pairing log from the finding; a retest that changes any other dimension does not close the item",
            ),
            (
                "Code placement",
                "the rejection belongs in the configuration repository or the origin middleware, not only in a console, so a rebuild keeps it",
            ),
        ],
        "pitfalls": [
            "Fixing only one layer and assuming the other will never be reached directly",
            "Retesting with a different request shape and declaring closure from a different experiment",
            "Leaving the fix in a console configuration that a routine deploy overwrites",
        ],
        "done_when": [
            "Every header from the finding has a rejection recorded at each layer that receives it",
            "The original pairing retest shows an unchanged response and the retest log is attached",
        ],
        "refs": [
            "[OWASP - Input validation cheat sheet](https://cheatsheetseries.owasp.org/)",
            "[PortSwigger - Cache poisoning remediation](https://portswigger.net/web-security/web-cache-poisoning)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "personalized-response-private-default",
        "title": "Personalized Response Private Default",
        "summary": "Make privacy the default for responses that carry identity-bound content, so a missing header cannot quietly turn into shared storage",
        "use_when": "any content class varies by session, account or tenant and the current default permits shared storage",
        "avoid_when": "the class is already marked private or no-store by a rule that applies to the whole class",
        "tags": ["harden", "privacy", "policy"],
        "steps": [
            "Identify every content class whose body depends on identity, using the class ladder recorded during scope.",
            "Set the default for those classes to private and no-store at the layer that attaches directives.",
            "Confirm the edge honours the default rather than overriding it with a broader rule.",
            "Test a new path added after the change, since a default is only proven by a path nobody hand-configured.",
            "Add a regression check to the deployment pipeline that fails when a personalized route omits the directives.",
            "Record the classes covered and the path used to prove the default, so coverage can be audited later.",
        ],
        "signals": [
            "A newly added personalized route ships without private or no-store",
            "The edge overrides the origin default for a class the team believes is protected",
            "A pipeline check does not exist, so a header omission ships unnoticed",
            "Coverage lists paths individually instead of covering a content class",
        ],
        "patterns": [
            (
                "Default line",
                "class: personal -> default: private, no-store; override: none permitted without an owner review",
            ),
            (
                "New-path probe",
                "request a route created after the change, with no hand-edited rule: if it lacks the directives, the default did not reach it",
            ),
            (
                "Regression check",
                "pipeline assertion: any route in the personal class must emit both tokens or the deploy fails",
            ),
        ],
        "pitfalls": [
            "Setting the default at the origin while an edge rule continues to override it",
            "Testing only routes that existed before the change, which cannot prove a default applies to new work",
            "Writing per-path rules when a class-level default would cover the whole surface",
        ],
        "done_when": [
            "The class list is covered by a default and each class has a confirming response header",
            "A route added after the change emits the expected directives without hand configuration",
        ],
        "refs": [
            "[MDN - Cache-Control private and no-store](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)",
            "[OWASP - Sensitive data protection](https://owasp.org/www-project-top-ten/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "purge-runbook-authoring",
        "title": "Purge Runbook Authoring",
        "summary": "Write the purge procedure for each content class, including who may trigger it and how fast it must take effect, so content removal is a rehearsed step rather than an improvisation",
        "use_when": "content removal depends on purge and no written procedure exists for when and how to clear entries",
        "avoid_when": "short lifetimes make purge unnecessary and the owner confirms removal never relies on it",
        "tags": ["harden", "purge", "operations"],
        "steps": [
            "List each content class and the purge type that reaches all of its entries, including keyed variants.",
            "Record the role authorized to trigger each purge type and the escalation path when that role is unavailable.",
            "State the expected propagation time per purge type, measured from an earlier test rather than assumed.",
            "Describe the verification step: which request to send afterwards and what status token proves the purge landed.",
            "Cover the failure path: what to do when verification still shows a stored copy after the expected delay.",
            "Store the runbook with the operations documentation and rehearse it once against a synthetic path.",
        ],
        "signals": [
            "No written procedure exists for removing a specific class of content",
            "Only one person knows how to trigger the purge type a class requires",
            "Propagation time is stated as a guess rather than a measurement",
            "There is no verification step to prove a purge actually cleared the entry",
        ],
        "patterns": [
            (
                "Runbook entry",
                "class: article | purge: tag | role: release-engineer | expected: 60s | verify: GET with bust -> expect miss",
            ),
            (
                "Verification line",
                "after purge, request the canonical path, one keyed variant and one expired entry; all three must report a miss",
            ),
            (
                "Escalation",
                "if any of the three still reports a hit after the expected delay, escalate to <role> and fall back to <fallback purge type>",
            ),
        ],
        "pitfalls": [
            "Writing a runbook that covers only the canonical URL while variants survive it",
            "Naming a role that no current team member actually holds",
            "Skipping rehearsal, so the first real use of the runbook is during an incident",
        ],
        "done_when": [
            "Every content class has a runbook entry with purge type, role, expected delay and verification",
            "The procedure has been rehearsed once against a synthetic path with the result recorded",
        ],
        "refs": [
            "[IETF RFC 9111 - Invalidating stored responses](https://www.rfc-editor.org/rfc/rfc9111)",
            "[OWASP - Incident response guidance](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "origin-exposure-lockdown",
        "title": "Origin Exposure Lockdown",
        "summary": "Restrict direct access to origin infrastructure so the edge remains the only way in, restoring the value of every control the edge is expected to enforce",
        "use_when": "an origin address was discovered or confirmed during detection and the owner can apply an access restriction",
        "avoid_when": "the address is a documented public front door rather than an origin that should sit behind the edge",
        "tags": ["harden", "origin", "network"],
        "steps": [
            "Confirm which addresses are genuinely origin endpoints rather than documented public endpoints.",
            "Enumerate the legitimate callers of each origin address, including scheduled jobs, partner integrations and internal tools.",
            "Apply a network restriction that admits only the edge provider's published address ranges and the enumerated callers.",
            "Verify from a permitted vantage point that direct requests are refused while edge-traversing requests still succeed.",
            "Record the source of the address ranges used and schedule a review, since provider ranges change over time.",
            "Document the residual exposure for any caller that cannot be allow-listed, with an owner and a remediation date.",
        ],
        "signals": [
            "A direct request outside the edge reaches the application successfully",
            "Address ranges were copied from memory rather than a published, dated source",
            "A scheduled job or partner integration broke after the restriction was applied",
            "No review date exists for the allow-list, so drift accumulates silently",
        ],
        "patterns": [
            (
                "Lockdown record",
                "address | source of ranges | callers allow-listed | direct test | edge test\n203.0.113.10 | provider published ranges 2026-05 | 4 | refused | 200",
            ),
            (
                "Verification pair",
                "one direct request from a permitted vantage point expecting refusal, one edge-traversing request expecting success, both recorded",
            ),
            (
                "Residual list",
                "caller | why it cannot be allow-listed | owner | target date -> written so nothing is quietly left open",
            ),
        ],
        "pitfalls": [
            "Applying a restriction that blocks a scheduled job and causes an outage the team did not ask for",
            "Hard-coding provider address ranges with no review date and letting them drift",
            "Locking down an address that was actually a public endpoint and breaking legitimate traffic",
        ],
        "done_when": [
            "A lockdown record shows direct refusal and edge success for each address changed",
            "Residual callers that could not be allow-listed are listed with owners and dates",
        ],
        "refs": [
            "[OWASP - Network segmentation and access control](https://owasp.org/www-project-web-security-testing-guide/)",
            "[Cloudflare - Origin server protection](https://developers.cloudflare.com/fundamentals/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "stale-window-bounding",
        "title": "Stale Window Bounding",
        "summary": "Cap how long a stored response may be served after its revocation point, so a deleted document or a closed account cannot be replayed for hours",
        "use_when": "the audit measured a worst-case serving window that exceeds the property's revocation expectation",
        "avoid_when": "the measured window already sits inside the stated revocation expectation on every tested path",
        "tags": ["harden", "ttl", "policy"],
        "steps": [
            "Record the measured worst-case window and the revocation expectation it violates, both with their sources.",
            "Reduce the stale allowances on the affected class to a value that fits inside the expectation with margin.",
            "Apply must-revalidate where a stored entry may not be reused once stale without a successful revalidation.",
            "Re-measure the window after the change by repeating the directive and freshness calculation on a live response.",
            "Check that reducing the window did not break the availability behaviour the allowance originally protected.",
            "Record the before and after windows with the configuration change that produced the difference.",
        ],
        "signals": [
            "A stale allowance outlives the property's stated revocation expectation",
            "Reducing the allowance caused availability problems that were not anticipated",
            "The change was applied at one layer while a second layer still permits the longer window",
            "The after window was never re-measured, so the fix rests on a calculation only",
        ],
        "patterns": [
            (
                "Before and after",
                "before: max-age=3600 + swr=86400 -> 90000s\nafter: max-age=300 + swr=60 + must-revalidate -> 360s\nexpectation: 900s -> now inside the bound",
            ),
            (
                "Layer sweep",
                "re-read directives at every layer that attaches them; one layer accepting the bound while another does not leaves the defect in place",
            ),
            (
                "Availability check",
                "repeat the request during a simulated origin error if permitted, to confirm the reduced allowance did not remove the protection it existed for",
            ),
        ],
        "pitfalls": [
            "Changing only one layer's directives and leaving the other able to extend the window",
            "Cutting an allowance without checking what availability behaviour depended on it",
            "Trusting the arithmetic without re-reading a live response after the change",
        ],
        "done_when": [
            "Before and after windows are recorded with the configuration change that produced them",
            "The after window fits inside the stated expectation on a live response, not only on paper",
        ],
        "refs": [
            "[IETF RFC 5861 - Stale response directives](https://www.rfc-editor.org/rfc/rfc5861)",
            "[MDN - Cache-Control directives reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "edge-config-drift-monitoring",
        "title": "Edge Config Drift Monitoring",
        "summary": "Keep observed edge behaviour continuously compared with the declared key policy and storage policy, so a configuration drift is noticed before an incident reports it",
        "use_when": "key and storage policies exist in writing but nothing currently checks that live behaviour still matches them",
        "avoid_when": "an automated check already runs on every deploy and alerts on a mismatch",
        "tags": ["harden", "monitoring", "configuration"],
        "steps": [
            "Choose a small sentinel set of paths covering each content class, including one personalized route and one asset route.",
            "Capture the expected behaviour per sentinel: storage permitted, key dimensions present and directive set emitted.",
            "Run the comparison on a schedule from a clean context and record any deviation from the expected behaviour.",
            "Route each deviation to the owner of the layer responsible, since only that owner can correct it.",
            "Add new content classes to the sentinel set as they appear, so coverage grows with the property.",
            "Track deviations over time so a recurring drift is visible as a trend rather than a series of isolated alerts.",
        ],
        "signals": [
            "A sentinel path starts storing responses it was expected never to store",
            "An expected key dimension disappears from observed behaviour after a configuration deploy",
            "No scheduled check exists, so drift is only discovered when someone investigates an incident",
            "The sentinel set has not been updated since a new content class shipped",
        ],
        "patterns": [
            (
                "Sentinel row",
                "path: /account | class: personal | expect: no-store | expect key: cookie | last check: ok 2026-05-11",
            ),
            (
                "Deviation line",
                "sentinel: /account | expected no-store | observed public, max-age=60 | detected 2026-05-12 | owner: edge platform",
            ),
            (
                "Coverage growth",
                "every new content class must add a sentinel in the same change that introduces the class, otherwise the check silently loses ground",
            ),
        ],
        "pitfalls": [
            "Building a sentinel set that covers only public assets and never a personalized route",
            "Alerting on every deviation without routing it to the layer that owns the fix",
            "Never adding sentinels for new classes, so coverage shrinks relative to the application",
        ],
        "done_when": [
            "A sentinel set covers every content class with expected storage, key and directive values",
            "A scheduled comparison runs and each deviation is routed to a named layer owner",
        ],
        "refs": [
            "[NIST SP 800-53 - Configuration management controls](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)",
            "[OWASP - Security configuration review](https://owasp.org/www-project-application-security-verification-standard/)",
        ],
        "meta": {"phase": "harden"},
    },
    {
        "slug": "edge-finding-evidence-pack",
        "title": "Edge Finding Evidence Pack",
        "summary": "Assemble a report where every edge claim carries the request pair, the cache status tokens and the timestamps that prove it",
        "use_when": "an edge or cache observation is ready to be written up for the owner or a vendor",
        "avoid_when": "the finding has already been reported and only a closing note remains",
        "tags": ["document", "evidence", "reporting"],
        "steps": [
            "State the defect in one sentence that names the layer, the dimension and the outcome, without adjectives.",
            "Attach the pairing log: the two or three requests whose only difference was the dimension at issue.",
            "Include cache status tokens, age values and the relevant directives for each request in the pair.",
            "Record the timestamps so a reader can tell which observation came before another.",
            "Give the reproduction recipe from clean state and the boundary document version that permitted each request.",
            "State the realistic impact in terms of what a normal client would observe, and keep speculation out of it.",
        ],
        "signals": [
            "A report claims a cache defect without showing the request pair that revealed it",
            "Status tokens are missing from the evidence, leaving stored versus live ambiguous",
            "Observations have no timestamps, so the order of events cannot be established",
            "Impact is described in hypothetical terms no tested request supports",
        ],
        "patterns": [
            (
                "Claim skeleton",
                "claim: <layer> stores <content> keyed without <dimension>\npair: request A / request B, differing only in <dimension>\ntokens: <status on each>\nimpact: <what a normal client sees>",
            ),
            (
                "Evidence block",
                "2026-05-11T09:12Z GET /path (no header) -> 200 hit age=118\n2026-05-11T09:12Z GET /path (header X)  -> 200 hit age=0\n2026-05-11T09:13Z GET /path (no header) -> 200 hit age=0 body changed",
            ),
            (
                "Boundary note",
                "attach the boundary document version and mark each request as permitted by it, so a reviewer can audit the test itself",
            ),
        ],
        "pitfalls": [
            "Presenting a narrative claim when the reader needs the raw request pair to judge it",
            "Leaving out the layer attribution, so the owner cannot route the report to the right team",
            "Inflating impact beyond what the recorded requests demonstrate",
        ],
        "done_when": [
            "Every claim in the report is followed by a request pair with status tokens and timestamps",
            "The reproduction recipe and boundary version are attached to the pack",
        ],
        "refs": [
            "[OWASP - Reporting security findings](https://owasp.org/www-project-web-security-testing-guide/)",
            "[NIST SP 800-61 - Incident handling guidance](https://csrc.nist.gov/pubs/sp/800/61/r2/final)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "clean-cache-reproduction-recipe-publication",
        "title": "Clean Cache Reproduction Recipe Publication",
        "summary": "Publish a reproduction the vendor can run without your session state, so the report does not depend on entries only your workstation created",
        "use_when": "a vendor or owner must independently reproduce an edge observation before acting on it",
        "avoid_when": "the owner already reproduced the observation themselves and only needs the evidence pack",
        "tags": ["document", "reproduction", "vendor"],
        "steps": [
            "Rewrite the internal recipe so it uses only publicly reachable requests that the boundary permits for the vendor.",
            "Name the cleared state before step one: which layers must be cold and how the reader achieves that.",
            "Give expected output per step, including status tokens, so the reader can tell a match from a divergence.",
            "Note the environmental assumptions the recipe depends on, such as region or account state.",
            "Run the published recipe once from a fresh context yourself and confirm the expected output still appears.",
            "Attach the recipe to the report and mark which findings depend on it for reproduction.",
        ],
        "signals": [
            "The vendor replies that the observation does not reproduce on their side",
            "The recipe contains steps that only work with entries your session created",
            "Expected output is described in prose rather than as status values to match",
            "Environmental assumptions such as region are unstated",
        ],
        "patterns": [
            (
                "Published recipe",
                "precondition: empty cookie jar, edge region X\n1. GET /path -> expect 200, status miss\n2. GET /path -> expect 200, status hit\n3. GET with <dimension> -> expect status hit, body differs from step 2",
            ),
            (
                "Assumption list",
                "assumes: account in region X, content class public, no purge in the last 60s -> listed so divergence has an explanation",
            ),
            (
                "Dependency note",
                "findings F-02 and F-05 require this recipe; findings F-01 and F-03 reproduce from the evidence block alone",
            ),
        ],
        "pitfalls": [
            "Publishing a recipe that silently depends on an entry created by an earlier probe",
            "Omitting region or account state, then reading a regional difference as a failed reproduction",
            "Never re-running the published version, so a later change to the property invalidates it unnoticed",
        ],
        "done_when": [
            "The published recipe runs from a fresh context and produces the stated expected output",
            "Environmental assumptions and dependent findings are listed beside it",
        ],
        "refs": [
            "[PortSwigger - Writing reproducible reports](https://portswigger.net/web-security/web-cache-poisoning)",
            "[HackerOne - Report quality guidance](https://www.hackerone.com/)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "layer-aware-remediation-wording",
        "title": "Layer-Aware Remediation Wording",
        "summary": "Write remediation steps against the layer that actually owns each change, so the receiving team can act without first untangling which component caused the defect",
        "use_when": "an edge finding is ready to include remediation and more than one layer was involved in the behaviour",
        "avoid_when": "one single layer owns the whole behaviour and the fix is a one-line configuration change",
        "tags": ["document", "remediation", "communication"],
        "steps": [
            "Name the layer for each step: edge configuration, origin code, origin headers or network restriction.",
            "State the expected effect of each step so a reader can verify the change worked rather than assume it did.",
            "Order steps so that any prerequisite layer is corrected before dependent layers are touched.",
            "Include a retest instruction for each step using the same pairing log that revealed the defect.",
            "Mark steps that require a role or a maintenance window, since those need scheduling rather than a merge request.",
            "List what was deliberately not changed, with the reason, so the reader knows the scope of the fix.",
        ],
        "signals": [
            "A remediation step names a header fix when a control-plane rule would continue to override it",
            "Steps carry no retest instruction, so closure cannot be verified",
            "A step requiring production access appears with no role or window requirement",
            "The report does not say which parts of the behaviour were left unchanged",
        ],
        "patterns": [
            (
                "Step line",
                "layer: edge config | change: drop x-original-url | effect: header no longer reaches origin | retest: reuse pairing log, expect unchanged body",
            ),
            (
                "Order rule",
                "fix the layer that wins the conflict first; correcting a subordinate layer while the winning rule remains changes nothing observable",
            ),
            (
                "Not-changed list",
                "unchanged: origin header parsing, because the edge drop covers it; recorded so the reader does not report it as an outstanding item",
            ),
        ],
        "pitfalls": [
            "Assigning every fix to the origin team when a control-plane rule is the deciding layer",
            "Omitting retest instructions, which makes an owner's closure claim unverifiable",
            "Hiding steps that need a maintenance window, so they are quietly dropped from the plan",
        ],
        "done_when": [
            "Every remediation step names its layer, expected effect and retest instruction",
            "Unchanged items are listed with reasons so nothing is silently omitted",
        ],
        "refs": [
            "[OWASP - Defect remediation guidance](https://owasp.org/www-project-web-security-testing-guide/)",
            "[NIST SP 800-40 - Enterprise patch management](https://csrc.nist.gov/pubs/sp/800/40/r4/final)",
        ],
        "meta": {"phase": "document"},
    },
    {
        "slug": "vendor-coordinated-disclosure",
        "title": "Vendor Coordinated Disclosure",
        "summary": "Route an edge defect to the party that can actually fix it, whether that is the property owner or the edge vendor, and set a disclosure timeline that both can meet",
        "use_when": "a finding involves a third-party edge vendor's own configuration or product behaviour",
        "avoid_when": "the defect is entirely in the owner's configuration and needs no vendor involvement",
        "tags": ["document", "disclosure", "coordination"],
        "steps": [
            "Decide the fixing party from the layer attribution: owner configuration, owner code, or vendor product behaviour.",
            "Prepare the report with the evidence pack and the reproduction recipe, redacted to remove tenant content entirely.",
            "Send it first to the property owner, since they hold the relationship and the contractual path to the vendor.",
            "Agree a timeline: acknowledgement, target fix date and a disclosure date, recorded in writing.",
            "Re-test after the fix lands using the same recipe, and record whether the behaviour actually changed.",
            "Close with a note on what remains open, including any item that depends on a vendor release you do not control.",
        ],
        "signals": [
            "The defect requires a change only the edge vendor can make to their product",
            "The report reaches the vendor before the owner has seen it, breaking the agreed channel",
            "No re-test was performed after the fix was announced",
            "Items remain open with no owner and no date attached",
        ],
        "patterns": [
            (
                "Routing line",
                "defect: control-plane rule applied by vendor default | fixing party: owner config first, vendor product second | channel: owner to vendor",
            ),
            (
                "Timeline block",
                "ack by <date> | fix target <date> | re-test <date> | disclosure <date> -> written and confirmed by both sides",
            ),
            (
                "Closure note",
                "re-tested with published recipe at <timestamp>: behaviour changed from <before token> to <after token> -> item closed",
            ),
        ],
        "pitfalls": [
            "Contacting a vendor directly about a defect that is really the owner's configuration choice",
            "Publishing tenant content in a report that will be retained by a vendor portal indefinitely",
            "Announcing closure without a re-test that shows the behaviour actually changed",
        ],
        "done_when": [
            "The fixing party and channel are named, with a timeline confirmed in writing",
            "A re-test after the fix records the before and after status tokens for each closed item",
        ],
        "refs": [
            "[ISO 29147 - Vulnerability disclosure guidance](https://www.iso.org/standard/72311.html)",
            "[OWASP - Coordinated disclosure](https://owasp.org/www-project-vulnerability-disclosure/)",
        ],
        "meta": {"phase": "document"},
    },
]