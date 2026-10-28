"""edgescout skills 16-30: audit phase."""

from __future__ import annotations

SKILLS: list[dict] = [
    {
        "slug": "unkeyed-header-reflection-audit",
        "title": "Unkeyed Header Reflection Audit",
        "summary": "Look for request headers that influence the response while sitting outside the cache key, since a reflected unkeyed input is the precondition for poisoning a stored copy",
        "use_when": "the key statement from fingerprinting marks a header unkeyed and the response is storable by a shared cache",
        "avoid_when": "the header is proven keyed, or the path carries no-store so no shared copy can exist",
        "tags": ["audit", "cache-key", "headers"],
        "steps": [
            "List every header the key statement marked unkeyed and rank them by how likely they are to reach application logic.",
            "For each candidate, send two requests differing only in that header and compare status, body and header set between them.",
            "Prefer headers used for routing or rewrites and forwarding renames, because those are the ones applications most often trust.",
            "When the body differs, capture only the differing region and record the header name that caused it, not the full body.",
            "Check whether the differing response was stored, by repeating the baseline request without the injected header.",
            "Record the finding as reflected-input with the pairing log, or close the header as inert with the same evidence.",
        ],
        "signals": [
            "Changing an unkeyed header changes the response body or status on an otherwise identical request",
            "A rewrite or routing header reaches the application even though the edge does not key on it",
            "The baseline request after a header-varied request returns the changed body from storage",
            "A reflected header value appears in a link, redirect or generated asset reference",
        ],
        "patterns": [
            (
                "Pairing log",
                "GET /path  header: none            -> 200 body-A status hit\nGET /path  header: x-original-url: X -> 200 body-B status hit\nbaseline   header: none            -> 200 body-B status hit  <- stored copy changed",
            ),
            (
                "Candidate order",
                "start with routing and rewrite headers, then forwarded host, then forwarded proto, then any custom vendor header the origin documents as trusted",
            ),
            (
                "Result label",
                "reflected-and-stored | reflected-not-stored | inert; each label needs the pairing log line that produced it",
            ),
        ],
        "pitfalls": [
            "Changing two headers in one request and losing the attribution needed to describe the defect",
            "Concluding storage happened without running the baseline request that proves it",
            "Testing a header on a no-store path and reporting a poisoning risk that the policy already prevents",
        ],
        "done_when": [
            "Every unkeyed header from the key statement has a pairing log entry and a result label",
            "Any reflected case includes a baseline request proving whether the changed body was stored",
        ],
        "refs": [
            "[PortSwigger - Web cache poisoning](https://portswigger.net/web-security/web-cache-poisoning)",
            "[MDN - Forwarded header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Forwarded)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "query-parameter-key-composition-audit",
        "title": "Query Parameter Key Composition Audit",
        "summary": "Determine which query parameters separate stored copies and which are ignored, including the tracking and decoration parameters that frequently sit outside the key",
        "use_when": "a path accepts query parameters and the key statement has not yet classified them as keyed or unkeyed",
        "avoid_when": "the path is documented to ignore all query input and observed behaviour confirms one stored entry per path",
        "tags": ["audit", "cache-key", "query"],
        "steps": [
            "Enumerate the parameters the application itself exposes through forms, links or documentation rather than guessing names.",
            "For each parameter, issue two requests with different values and record whether the status token separates them.",
            "Include a null value, an empty value and a reordered parameter list, because each shape can be normalized differently.",
            "Check whether parameters that do not affect the rendered output are nevertheless keyed, which inflates storage rather than changing content.",
            "Test whether a parameter is decoded once or twice at each layer, since a decode mismatch splits or merges entries unexpectedly.",
            "Record a parameter table listing keyed, unkeyed, normalizing and unknown behaviour with one log line per verdict.",
        ],
        "signals": [
            "A parameter changes the rendered response while the status token stays identical across both values",
            "Two different values for one parameter share a single stored copy",
            "Parameter order or encoding changes the stored entry without changing the output",
            "A tracking parameter is ignored by the application but still splits the cache key",
        ],
        "patterns": [
            (
                "Parameter table",
                "param | values tested | status separates | body differs | verdict\nid | 1,2 | no | yes | unkeyed and reflected\nsort | asc,desc | yes | yes | keyed\nutm_source | a,b | no | no | ignored and unkeyed",
            ),
            (
                "Encoding triple",
                "test the raw value, the percent-encoded value and the double-encoded value once each; a difference between them marks a decode mismatch between layers",
            ),
            (
                "Storage inflation note",
                "when a parameter is keyed but never changes output, record it as an entry-multiplier and flag it to the owner as a capacity concern",
            ),
        ],
        "pitfalls": [
            "Testing only well-formed values and missing the empty or repeated parameter case that behaves differently",
            "Assuming a tracking parameter is unkeyed because vendor defaults say so rather than because it was observed",
            "Overlooking that an unkeyed reflected parameter is exactly the shape a poisoning test needs",
        ],
        "done_when": [
            "A parameter table covers every parameter the application exposes with a verdict per value shape",
            "Decode behaviour is recorded for at least the raw, encoded and double-encoded cases",
        ],
        "refs": [
            "[PortSwigger - Cache key confusion](https://portswigger.net/web-security/web-cache-poisoning)",
            "[IETF RFC 3986 - URI syntax](https://www.rfc-editor.org/rfc/rfc3986)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "path-normalization-key-collision",
        "title": "Path Normalization Key Collision",
        "summary": "Find path spellings that normalize to one stored entry, so two logically different resources are shown to share a cache key they were never meant to share",
        "use_when": "the edge and the origin may disagree about path decoding, case or default documents on an in-scope host",
        "avoid_when": "the origin is proven to normalize identically to the edge and both layers return the same status for every variant tested",
        "tags": ["audit", "cache-key", "paths"],
        "steps": [
            "Build a variant list for one representative path: default document, trailing separator, encoded separator, dot segment and upper case.",
            "Request each variant without any cache-busting parameter and record status, location header and cache status token.",
            "Compare the edge answer with the origin's own view by checking whether the application treats two variants as one route.",
            "Look for a case where a 404 or a redirect for one variant is served in place of the correct resource for another.",
            "Repeat the collision check after the storage window expires, since an expired entry may behave differently from a fresh one.",
            "Record each collision with the exact spelling pair and the shared status both spellings received.",
        ],
        "signals": [
            "Two spellings of one path return an identical stored response with an identical status token",
            "An encoded separator variant returns the default document or a redirect meant for another route",
            "Case variants share one stored entry on a path where the origin is case sensitive",
            "A trailing separator triggers a redirect that is then stored and replayed for the canonical path",
        ],
        "patterns": [
            (
                "Variant set",
                "/path, /path/, /path/index.html, /path%2f, /./path, /PATH  -> record status, location and cache token for each",
            ),
            (
                "Collision line",
                "spelling A: /account/  -> 200, hit\nspelling B: /account   -> 200, hit, same body hash -> one entry serves both spellings",
            ),
            (
                "Redirect capture",
                "if a redirect for a variant is stored, note the target: replaying it for the canonical path turns a cosmetic issue into a routing defect",
            ),
        ],
        "pitfalls": [
            "Testing only the canonical spelling and never the separator, encoding and case variants",
            "Treating a redirect difference as cosmetic when the redirect itself is what gets stored",
            "Ignoring that a collision is only reportable when both spellings are in scope for the assessment",
        ],
        "done_when": [
            "Each tested path has a variant table with status, location and cache token per spelling",
            "Any collision records both spellings and the shared response they received",
        ],
        "refs": [
            "[IETF RFC 3986 - Path component syntax](https://www.rfc-editor.org/rfc/rfc3986)",
            "[PortSwigger - Web cache deception](https://portswigger.net/web-security/web-cache-deception)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "content-negotiation-key-dimensions",
        "title": "Content Negotiation Key Dimensions",
        "summary": "Audit how accept, accept-encoding and accept-language participate in the key, since negotiation mismatches serve one client's representation to another",
        "use_when": "the response varies on a negotiation header or the application renders different bodies per client preference",
        "avoid_when": "the path returns one fixed representation and the vary list is empty on every observed response",
        "tags": ["audit", "content-negotiation", "vary"],
        "steps": [
            "Record the vary list the response carries and identify which negotiation headers it names.",
            "For each named header, request two clearly different preferences and confirm the status token separates the two variants.",
            "Test a preference the vary list omits, because an omission there is where one variant can be served to another client.",
            "Check whether the edge honours the preference itself, such as serving a compressed variant without asking the origin.",
            "Verify that a stored variant carries its own vary list forward so later readers of that copy see the same constraint.",
            "Document the negotiation matrix: header, values tested, keyed or not, body actually returned.",
        ],
        "signals": [
            "The vary list omits a negotiation header that clearly changes the rendered body",
            "A compressed variant is served to a client that did not request it",
            "The stored copy's vary list differs from the vary list on the first response",
            "One variant receives a long freshness lifetime while another is never stored",
        ],
        "patterns": [
            (
                "Negotiation matrix",
                "header | values | keyed | body returned\naccept-encoding | gzip, identity | yes | matches request\naccept-language | en, fr | no | always en  <- omission\naccept | json, html | yes | matches request",
            ),
            (
                "Stored-vary check",
                "first response: vary: accept-encoding\nstored response: vary absent -> the stored entry lost its constraint, record the transition",
            ),
            (
                "Honor test",
                "request an encoding the origin does not support and note whether the edge answers from storage anyway instead of passing the request through",
            ),
        ],
        "pitfalls": [
            "Assuming the vary list the origin sends is the list the edge actually applies",
            "Testing negotiation only with well-formed values and missing the absent-header case",
            "Forgetting that accept-encoding changes every variant count and distorts the rest of the matrix",
        ],
        "done_when": [
            "A negotiation matrix records each header, the values tested and the keyed verdict",
            "The stored copy's vary list is compared with the first response's list for every tested path",
        ],
        "refs": [
            "[IETF RFC 9110 - Content negotiation](https://www.rfc-editor.org/rfc/rfc9110)",
            "[MDN - Accept-Encoding header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept-Encoding)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "authenticated-response-shared-storage",
        "title": "Authenticated Response Shared Storage",
        "summary": "Check whether identity-bound responses can be stored in a cache that serves other users, which is the highest-impact outcome a shared cache can produce",
        "use_when": "a path returns different content per session or account and the response does not clearly mark itself as private",
        "avoid_when": "the response carries private or no-store and a repeat request from a second session confirms isolation",
        "tags": ["audit", "authentication", "shared-cache"],
        "steps": [
            "Create two synthetic sessions you own and request the same authenticated path with each, recording the full header set both times.",
            "Check both responses for private, no-store and no-cache, and note any of them missing from a response that carries per-session content.",
            "Confirm the key statement includes whichever identity dimension the origin uses, such as cookie or authorization.",
            "Ask for the path once without any credentials to see whether an unauthenticated answer is stored and then replayed to a signed-in client.",
            "Verify isolation by alternating the two sessions several times rather than trusting a single successful pair.",
            "Record the verdict with the header evidence and the alternation log, using only your own synthetic accounts.",
        ],
        "signals": [
            "An authenticated response omits private and no-store while containing account-specific content",
            "The key statement does not include the identity header the origin uses to select content",
            "A signed-in client receives content that matches a different session's earlier request",
            "An unauthenticated request is answered from storage with content that belongs to a session",
        ],
        "patterns": [
            (
                "Isolation log",
                "session A -> 200 body-A, status hit, cache-control: public, max-age=60\nsession B -> 200 body-A  <- body-B expected, mismatch recorded",
            ),
            (
                "Header expectation",
                "authenticated + personalized -> Cache-Control: private, no-store; anything else on this class is a finding",
            ),
            (
                "No-credential probe",
                "request with no identity header at all: if the answer comes from storage, the stored entry was not partitioned by identity",
            ),
        ],
        "pitfalls": [
            "Using two real user accounts and turning an isolation test into a privacy incident",
            "Testing once and concluding isolation when the store may simply have been cold the first time",
            "Forgetting an unauthenticated request, which is often the case where the mismatch first appears",
        ],
        "done_when": [
            "Two synthetic sessions alternate several times with the header sets recorded for both",
            "A verdict of isolated or shared is backed by the alternation log and the observed directives",
        ],
        "refs": [
            "[OWASP - Session management testing](https://owasp.org/www-project-web-security-testing-guide/)",
            "[IETF RFC 9111 - Storing responses in shared caches](https://www.rfc-editor.org/rfc/rfc9111)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "set-cookie-on-cacheable-response",
        "title": "Set-Cookie on Cacheable Response",
        "summary": "Find responses that both set a cookie and allow shared storage, since a replayed Set-Cookie header can hand one client another client's session state",
        "use_when": "any in-scope response carries a Set-Cookie header together with storage-permitting cache directives",
        "avoid_when": "the response marks itself private or no-store, so a shared cache must never store it",
        "tags": ["audit", "cookies", "shared-cache"],
        "steps": [
            "Capture the full response for each path that sets a cookie and record the cache directives alongside it.",
            "Flag any response where Set-Cookie coexists with a directive that permits shared storage.",
            "Repeat the request without a cookie jar to see whether the stored copy replays the Set-Cookie header to a fresh client.",
            "Inspect the cookie attributes on the flagged responses: scope, path, secure, same-site and any session lifetime.",
            "Check whether a purge or expiry removes the replayed cookie promptly, or whether it persists for the whole freshness lifetime.",
            "Record each case with the directive set, the cookie attributes and the replay observation from a clean client.",
        ],
        "signals": [
            "Set-Cookie appears on a response the edge reports as stored",
            "A request with no prior cookie receives a Set-Cookie header served from storage",
            "The cookie carries a broad scope while the response caching allows any client to receive it",
            "The replayed cookie survives longer than the application intended the session to live",
        ],
        "patterns": [
            (
                "Flag rule",
                "set-cookie present AND cache-control lacks private and lacks no-store -> flag for replay test",
            ),
            (
                "Clean-client probe",
                "empty cookie jar, same URL, note whether set-cookie returns with an age above zero; age above zero means a stored copy delivered it",
            ),
            (
                "Attribute record",
                "name scope path secure same-site lifetime -> written beside the flag so impact is judged from the cookie, not the header alone",
            ),
        ],
        "pitfalls": [
            "Reporting a cookie replay without checking whether the response was actually stored rather than regenerated",
            "Judging impact from the header alone without reading the cookie scope and lifetime",
            "Missing a path that sets a session cookie on a public asset such as a tracking pixel",
        ],
        "done_when": [
            "Every response with Set-Cookie and storage-permitting directives has a clean-client replay observation",
            "Cookie attributes are recorded beside each flag so impact can be judged",
        ],
        "refs": [
            "[MDN - Set-Cookie header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)",
            "[OWASP - Session fixation and cookie security](https://cheatsheetseries.owasp.org/)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "cache-control-override-conflict",
        "title": "Cache-Control Override Conflict",
        "summary": "Find places where the effective storage policy differs from what the origin sent, because a silently overridden directive is where unintended storage begins",
        "use_when": "observed storage behaviour contradicts the cache directives the origin attaches to a response",
        "avoid_when": "the origin's directives and the observed storage window agree on every tested path",
        "tags": ["audit", "headers", "policy"],
        "steps": [
            "Record the origin's cache directives verbatim for each tested path together with the observed storage behaviour.",
            "Classify the relationship: honoured, tightened by the layer, or weakened by the layer, with one line per path.",
            "Where the layer weakened the directive, ask whether a control-plane rule exists and note where it lives.",
            "Check both directions of conflict: a no-store the edge ignores, and a public the edge refuses to store.",
            "Note conflicts that differ between content classes, since one rule may apply to assets and another to application routes.",
            "Summarize each conflict as an ownership item: which layer must change for the two sides to agree.",
        ],
        "signals": [
            "A response marked no-store still shows an age value on a later request",
            "A response marked public is never stored on a path where assets are normally cached",
            "s-maxage and max-age disagree and the layer honours neither",
            "One content class follows the origin while another is overridden by a rule",
        ],
        "patterns": [
            (
                "Conflict line",
                "path | origin says | observed | classification | owner\n/api | no-store | stored, age=118 | weakened | control-plane rule",
            ),
            (
                "Both-direction test",
                "always test a restrictive directive and a permissive one on the same host, because a single rule can cause either direction of conflict",
            ),
            (
                "Ownership handoff",
                "the fix belongs to whoever edits <layer>; note this explicitly so the report does not tell the origin team to change a header that is ignored",
            ),
        ],
        "pitfalls": [
            "Reporting the conflict to the wrong team when a control-plane rule is the actual source",
            "Testing only restrictive directives and missing a permissive directive the layer refuses",
            "Assuming a conflict is intentional when no one on the team can name the rule that produces it",
        ],
        "done_when": [
            "Every tested path has a conflict classification of honoured, tightened or weakened",
            "Each conflict names the layer that owns the fix rather than only the symptom",
        ],
        "refs": [
            "[IETF RFC 9111 - Cache-control directives](https://www.rfc-editor.org/rfc/rfc9111)",
            "[MDN - Cache-Control header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "verb-handling-in-shared-storage",
        "title": "Verb Handling in Shared Storage",
        "summary": "Audit which HTTP verbs the edge stores and replays, because a stored write or a replayed read for the wrong verb breaks application semantics for every later client",
        "use_when": "the boundary permits non-idempotent verb observation and the edge may be storing responses by more than the request line",
        "avoid_when": "the engagement restricts testing to GET and HEAD and the owner confirms other verbs bypass the cache entirely",
        "tags": ["audit", "verbs", "shared-cache"],
        "steps": [
            "Confirm from the rules of engagement which verbs may be sent and which must remain untouched.",
            "For each permitted verb, record the cache status token and whether a stored copy exists for the same path.",
            "Test whether a stored GET answer is returned for a request that used another verb on the same path.",
            "Check whether a state-changing verb's response carries storage-permitting directives at all.",
            "Verify that a purge of the path clears every verb's entry, not just the one you observed.",
            "Record the verb matrix: verb, stored, replayed, purge effect, with the status token for each cell.",
        ],
        "signals": [
            "A response to a state-changing verb carries directives that permit shared storage",
            "A second verb on the same path receives the answer stored for a GET request",
            "Purging one path leaves other verbs' answers still reported as stored",
            "A caching status token appears on a response that should never be stored",
        ],
        "patterns": [
            (
                "Verb matrix",
                "verb | stored | replayed | purge clears\nGET | yes | yes | yes\nHEAD | yes | yes | yes\nPOST | flagged | no | unknown",
            ),
            (
                "Permit rule",
                "state-changing verb + storage-permitting directive -> record as a policy defect even when no replay was observed",
            ),
            (
                "Purge scope note",
                "purge the path once with permission, then re-request every tested verb to see which entries survived",
            ),
        ],
        "pitfalls": [
            "Sending a state-changing verb purely to fill a matrix cell when the boundary forbids it",
            "Concluding an entry was purged without re-requesting every verb for that path",
            "Reporting a stored HEAD as a stored GET, since the two behave differently for body comparison",
        ],
        "done_when": [
            "A verb matrix records stored, replayed and purge behaviour for every permitted verb",
            "State-changing verbs are either tested under explicit permission or explicitly marked untested",
        ],
        "refs": [
            "[IETF RFC 9110 - HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110)",
            "[MDN - HTTP methods overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "unkeyed-host-url-generation",
        "title": "Unkeyed Host URL Generation",
        "summary": "Detect when an unkeyed host or forwarded-host header reaches link generation, because stored absolute URLs turn one request into a poisonable shared response",
        "use_when": "the key statement marks the host or a forwarded host header unkeyed and the application renders absolute URLs anywhere in the body",
        "avoid_when": "the application renders only relative references and a body comparison confirms the host never appears in output",
        "tags": ["audit", "host-header", "url-generation"],
        "steps": [
            "Enumerate the response regions that can contain an absolute URL: links, asset references, canonical tags, redirects and generated tokens.",
            "Send two requests differing only in a forwarded host header while keeping every other dimension identical.",
            "Compare those regions specifically rather than the whole body, since only the URL-bearing region matters for this check.",
            "Check whether any observed change was stored by repeating the clean baseline request afterwards.",
            "Verify whether the changed URL would be followed or rendered by a normal client, which sets the realistic impact.",
            "Record the finding with the exact regions that changed and whether a stored copy retained the changed value.",
        ],
        "signals": [
            "A forwarded host header changes a link, asset path or canonical URL in the rendered body",
            "A redirect location is built from a header the edge does not include in the key",
            "The clean baseline after a header-varied request returns the changed URL from storage",
            "A generated token or callback URL embeds the forwarded host value",
        ],
        "patterns": [
            (
                "Region diff",
                "regions to compare: <a href>, <link href>, <script src>, <meta content>, location header; record only the changed region",
            ),
            (
                "Baseline-after rule",
                "after any header-varied request, re-request without the header: an unchanged baseline means no storage, a changed baseline means the copy was stored",
            ),
            (
                "Impact sentence",
                "the stored copy would make a normal client request <host> for an asset; write this sentence with the observed host value redacted to the scheme and registrable domain",
            ),
        ],
        "pitfalls": [
            "Reporting a reflected value that was never stored, which downgrades the finding to a response-splitting style observation",
            "Comparing full bodies and missing a two-character difference inside a long asset URL",
            "Describing impact without stating whether a normal client would actually follow the changed URL",
        ],
        "done_when": [
            "URL-bearing regions are compared for every unkeyed host-style header tested",
            "A baseline-after request records whether any observed change was stored",
        ],
        "refs": [
            "[PortSwigger - Host header attacks](https://portswigger.net/web-security/host-header)",
            "[MDN - Forwarded header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Forwarded)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "cache-key-duplication-splitting",
        "title": "Cache Key Duplication Splitting",
        "summary": "Find dimensions that split one logical resource into many stored entries, which raises origin load and storage cost and can hide a purge behind an entry you never saw",
        "use_when": "the key statement lists dimensions that do not change output but still create separate stored entries",
        "avoid_when": "the owner confirms every keyed dimension changes the response body or headers",
        "tags": ["audit", "capacity", "cache-key"],
        "steps": [
            "List every keyed dimension from the key statement and mark whether it changes the response in your observations.",
            "Quantify the split for one representative path by varying each non-contributing dimension and counting distinct entries.",
            "Check whether tracking or decoration parameters are included in the key while the application ignores them.",
            "Note whether the split is bounded by a rule or unbounded, since an unbounded set grows with request volume.",
            "Estimate the practical effect: additional origin requests per visitor and the purge surface that now covers more entries.",
            "Report the split with the counted entries and the responsible configuration rule, recommending key exclusion for non-contributing dimensions.",
        ],
        "signals": [
            "Adding a tracking parameter creates a new stored entry without changing the response",
            "The same resource exists in many entries differing only by a parameter the application never reads",
            "Origin request logs show repeated fetches for one path with varying parameter values",
            "A purge by path leaves sibling entries still reported as stored",
        ],
        "patterns": [
            (
                "Split count",
                "path /article with 6 tracking values -> 6 stored entries, identical bodies, origin fetched 6 times",
            ),
            (
                "Bounded check",
                "is the varying set finite, such as language, or unbounded, such as client-supplied identifiers? write which one applies to this path",
            ),
            (
                "Recommendation line",
                "exclude <dimension> from the key under rule <rule-name>; it never changes the response and multiplying entries increases origin traffic",
            ),
        ],
        "pitfalls": [
            "Treating a capacity concern as a security finding and overstating its impact class",
            "Counting entries from an unbounded parameter set without saying the count is an estimate",
            "Recommending key exclusion without noting that the dimension must first be proven non-contributing",
        ],
        "done_when": [
            "A counted split example records entries for one path and the dimension responsible",
            "The recommendation names the configuration rule to change and the precondition proven first",
        ],
        "refs": [
            "[IETF RFC 9111 - Constructing cache keys](https://www.rfc-editor.org/rfc/rfc9111)",
            "[Cloudflare - Cache key configuration](https://developers.cloudflare.com/cache/)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "stale-window-overflow-audit",
        "title": "Stale Window Overflow Audit",
        "summary": "Measure how long content can be served past its revocation point through stale allowances, since a revoked document or a deleted account may still be replayed for hours",
        "use_when": "responses carry stale-while-revalidate, stale-if-error or must-revalidate in combination with a meaningful freshness lifetime",
        "avoid_when": "the response uses no stale allowances and must-revalidate is enforced on every tested path",
        "tags": ["audit", "ttl", "freshness"],
        "steps": [
            "Record every stale-related directive on the response with its numeric value where the directive takes one.",
            "Compute the worst-case serving window as freshness lifetime plus the largest stale allowance the policy permits.",
            "Compare that window with the property's own revocation expectations, such as how fast a document removal must take effect.",
            "Check whether an error at the origin extends serving further under a stale-if-error allowance.",
            "Verify what happens to a stored entry when the application explicitly purges it, since a purge should override any allowance.",
            "Report the worst-case window with the directives that produce it and the revocation expectation it violates.",
        ],
        "signals": [
            "A stale allowance is large enough to outlive a document revocation or an account deletion",
            "An error response at the origin triggers extended serving of an older copy",
            "A purge does not take effect immediately on a path with a stale allowance",
            "must-revalidate is absent while a long stale allowance is configured",
        ],
        "patterns": [
            (
                "Worst-case line",
                "max-age=3600 + stale-while-revalidate=86400 -> up to 90000s of continued serving after the stated lifetime",
            ),
            (
                "Revocation compare",
                "property expectation: revocation within 15 minutes; observed worst case: 25 hours -> gap written with both numbers",
            ),
            (
                "Purge override test",
                "purge the path with permission, then re-request: an immediate miss proves the purge wins, a stale hit proves the allowance wins",
            ),
        ],
        "pitfalls": [
            "Adding directives incorrectly and overstating or understating the serving window",
            "Reporting a theoretical window without checking whether a purge overrides it in practice",
            "Ignoring the error path, which is often the case where the longest serving window appears",
        ],
        "done_when": [
            "A worst-case window is computed per tested path with the directives shown",
            "The purge override behaviour is confirmed by an observed request after a purge",
        ],
        "refs": [
            "[IETF RFC 5861 - HTTP cache-control extensions for stale responses](https://www.rfc-editor.org/rfc/rfc5861)",
            "[MDN - Stale-while-revalidate](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "overbroad-match-rule-review",
        "title": "Overbroad Match Rule Review",
        "summary": "Identify cache rules whose match scope covers dynamic or personalized paths, since a single wildcard is often the whole cause of unintended storage",
        "use_when": "the owner describes rules in wildcard form or observed storage covers more paths than the team intended",
        "avoid_when": "rules are expressed per content class and each tested path is matched by an explicit rule rather than a wildcard",
        "tags": ["audit", "configuration", "policy"],
        "steps": [
            "Ask for the rule set in effect, or infer it from behaviour, and write each rule's match expression verbatim.",
            "Map every tested path to the rule that matched it, starting with the broadest wildcard that applies.",
            "Identify dynamic routes, such as account or API paths, that fall under a broad asset rule.",
            "Check whether a negation or bypass list exists for the dynamic routes and whether it is evaluated before the wildcard.",
            "Verify that a path intended to be excluded actually reports no storage on a repeat request.",
            "Report each overbroad match with the rule text, the paths it captures and the specific paths that should be excluded.",
        ],
        "signals": [
            "A single wildcard rule appears to govern asset and application routes alike",
            "An account or API path reports storage despite the team believing it excluded",
            "A bypass list exists but is evaluated after the wildcard that already matched",
            "Excluding a path requires editing a rule the team does not own",
        ],
        "patterns": [
            (
                "Rule map",
                "rule: /* -> captures: /assets/*, /account/*, /api/*\nrule: !/api/* -> evaluated after, never reached for these paths",
            ),
            (
                "Path-to-rule line",
                "/account/settings | matched by /* at priority 1 | expected: excluded | observed: stored -> finding",
            ),
            (
                "Order note",
                "record the evaluation order of rules, because a correct exclusion evaluated after a broader match has no effect at all",
            ),
        ],
        "pitfalls": [
            "Reporting the wildcard as the defect when the real defect is the order the rules are evaluated in",
            "Assuming a path is excluded because a negation exists rather than because a request proved it",
            "Testing only one dynamic route when the wildcard captures a whole class of them",
        ],
        "done_when": [
            "Every tested path maps to the rule that matched it with the rule text recorded",
            "Excluded paths are proven excluded by a repeat request, not by the existence of a negation",
        ],
        "refs": [
            "[OWASP - Access control and cache configuration](https://owasp.org/www-project-web-security-testing-guide/)",
            "[Cloudflare - Cache rule evaluation order](https://developers.cloudflare.com/cache/)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "signed-asset-key-bypass-audit",
        "title": "Signed Asset Key Bypass Audit",
        "summary": "Verify that time-limited signed asset access cannot be bypassed through a stored copy that outlives the signature it was fetched with",
        "use_when": "the property serves signed URLs or signed cookies for protected assets behind a shared cache",
        "avoid_when": "protected assets are served with no-store so no shared copy can exist regardless of signing",
        "tags": ["audit", "signed-urls", "access-control"],
        "steps": [
            "Confirm how the signature is presented: query parameter, cookie or header, and record which of these the key includes.",
            "Fetch a signed asset with a valid signature and record the storage directives and status token on the answer.",
            "Repeat the request without the signature to see whether a stored copy is served to an unsigned client.",
            "Check whether the signature parameter is excluded from the key while the response is still stored.",
            "Verify that an expired signature cannot retrieve a stored copy, and record what the edge returns instead.",
            "Report each case with the signature presentation, the key treatment and the observed unsigned or expired behaviour.",
        ],
        "signals": [
            "A stored asset answer returns for a request that presented no signature at all",
            "The signature parameter is excluded from the key while the protected response is stored",
            "An expired signature retrieves content that a valid signature originally fetched",
            "Two different signatures share one stored entry because neither is part of the key",
        ],
        "patterns": [
            (
                "Signature table",
                "presentation: query param\nkey includes: no\nstored: yes\nunsigned request: 200 from storage -> bypass observed",
            ),
            (
                "Expiry probe",
                "valid signature -> 200 stored; expired signature -> record status and body hash; identical hashes mean the copy was served regardless",
            ),
            (
                "Expected result",
                "unsigned or expired -> 403 or 404 from origin, never a stored 200 that a signature originally unlocked",
            ),
        ],
        "pitfalls": [
            "Testing expiry only with a still-valid signature and never waiting for or constructing an expired one",
            "Reporting a bypass when the asset was public all along and the signature was decorative",
            "Overlooking that a signature in a cookie may already be part of the key while one in a query parameter is not",
        ],
        "done_when": [
            "A signature table records presentation, key treatment and storage for each protected class tested",
            "Unsigned and expired requests each have an observed status and body comparison",
        ],
        "refs": [
            "[AWS - Signed URLs and signed cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-urls.html)",
            "[OWASP - Insecure direct object references](https://owasp.org/www-project-web-security-testing-guide/)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "purge-coverage-gap-analysis",
        "title": "Purge Coverage Gap Analysis",
        "summary": "Check that the purge mechanism reaches every entry class the property relies on, because a purge that misses one class leaves revoked content served indefinitely",
        "use_when": "the owner relies on purge for content removal and the purge scope or granularity has not been verified",
        "avoid_when": "policies use short lifetimes everywhere and content removal never depends on an explicit purge",
        "tags": ["audit", "purge", "operations"],
        "steps": [
            "Record the purge capabilities available: by URL, by prefix, by tag, by host and full flush, with who may trigger each.",
            "For each tested path class, determine which purge type would actually clear it, including every variant entry.",
            "Purge a synthetic test path where permission allows, then re-request every variant to confirm which entries cleared.",
            "Check whether variants created by keyed dimensions survive a purge that targeted only the canonical URL.",
            "Note propagation delay from purge request to observed miss, since a slow purge extends the revocation window.",
            "Write a coverage table: path class, required purge type, confirmed effect, propagation delay.",
        ],
        "signals": [
            "A purge by canonical URL leaves keyed variants still reported as stored",
            "The team can purge only by host while content removal expectations assume per-path effect",
            "Propagation delay is long enough to matter for a revocation that must happen quickly",
            "Some content class can be purged only by a full flush nobody is authorized to trigger",
        ],
        "patterns": [
            (
                "Coverage table",
                "class | entry count | purge type needed | confirmed | delay\narticle | 3 variants | tag purge | no | -\nasset | 1 entry | url purge | yes | 4s",
            ),
            (
                "Variant sweep",
                "after purge: re-request canonical, each keyed variant and one expired entry; report which three survived",
            ),
            (
                "Authorization note",
                "record who can trigger each purge type, because a capability nobody may use is not a capability the process has",
            ),
        ],
        "pitfalls": [
            "Purging the canonical URL and concluding coverage without checking the keyed variants",
            "Measuring propagation once and reporting it as a stable figure",
            "Recording a purge capability that exists in the vendor console but that no role is permitted to trigger",
        ],
        "done_when": [
            "A coverage table lists every tested class with the purge type needed and the confirmed effect",
            "A purge test records canonical, variant and expired entry outcomes with the propagation delay",
        ],
        "refs": [
            "[IETF RFC 9111 - Invalidating stored responses](https://www.rfc-editor.org/rfc/rfc9111)",
            "[Akamapi - Cache purge options](https://techdocs.akamai.com/property-manager/docs/welcome-to-property-manager)",
        ],
        "meta": {"phase": "audit"},
    },
    {
        "slug": "negative-response-storage-audit",
        "title": "Negative Response Storage Audit",
        "summary": "Audit whether error and empty responses are stored and replayed, since a cached failure turns one origin hiccup into an outage that outlives its cause",
        "use_when": "error statuses appear during testing or the property serves content that can legitimately disappear between requests",
        "avoid_when": "the owner confirms errors are excluded from storage by rule and a repeat request proves no error is stored",
        "tags": ["audit", "errors", "availability"],
        "steps": [
            "Record the cache status token and directives on each error class observed during the engagement.",
            "Trigger a controlled, non-destructive error such as a not-found path and check whether the answer is stored.",
            "Re-request the same path after the error was produced and note whether storage or a live origin answer is returned.",
            "Check whether an error response carries a long freshness lifetime while the successful responses on the host use short ones.",
            "Verify what a purge or a recovery at the origin does to a stored error: does it clear, or must it expire naturally?",
            "Report each stored-error case with its status, lifetime, and the recovery behaviour observed.",
        ],
        "signals": [
            "An error response carries an age value greater than zero on a later request",
            "A transient failure is still being served after the origin recovered",
            "The error's freshness lifetime exceeds the lifetime the origin sets for successful responses",
            "A purge does not clear a stored error while clearing the success entry on the same path",
        ],
        "patterns": [
            (
                "Error storage line",
                "status=503 age=42 cache-control=max-age=300 -> stored for 300s after the transient cause",
            ),
            (
                "Recovery check",
                "wait for origin recovery, then re-request: a stored error still returned means availability impact continues past the cause",
            ),
            (
                "Lifetime compare",
                "error lifetime vs success lifetime on the same host; a longer error lifetime is the reportable asymmetry",
            ),
        ],
        "pitfalls": [
            "Triggering an error in a way that stresses the origin rather than a controlled not-found path",
            "Reporting a stored error without checking whether a purge or expiry clears it",
            "Comparing lifetimes across different hosts instead of within the same host",
        ],
        "done_when": [
            "Each observed error class has a status, age and lifetime recorded",
            "Recovery behaviour is confirmed by a request after the transient cause ended",
        ],
        "refs": [
            "[IETF RFC 9111 - Freshness and error handling](https://www.rfc-editor.org/rfc/rfc9111)",
            "[MDN - 503 Service Unavailable](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/503)",
        ],
        "meta": {"phase": "audit"},
    },
]