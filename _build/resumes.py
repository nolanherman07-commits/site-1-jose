# Builds Jose's Listing and Buyer résumé PDFs plus their cover images for the home page.
# Run: python3 _build/resumes.py   (needs: pip install playwright && playwright install chromium)
# Numbers and reviews match the top of _build/build.py. Update both when Jose's stats change.
import os, html
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
os.chdir(ROOT)
E = html.escape

NAME, FIRST = "Jose Lugo", "Jose"
TEAM, BROKERAGE = "Aspyre Collective", "eXp Realty"
PHONE, EMAIL = "910-679-9255", "jose@aspyrecollective.com"
ADDRESS = "1213 Culbreth Dr, Suite 109, Wilmington, NC 28405"
SITE = "nolanherman07-commits.github.io/site-1-jose"  # change once Jose's domain is live

STATS = [("115+", "transactions"), ("30", "sales in the last 12 months"), ("5.0★", "on Zillow · 20 reviews"),
         ("$2.7M", "top sale"), ("$35K–2.7M", "price range sold"), ("4", "coastal counties served")]
SOLD = [("419 Caswell Beach Rd", "Oak Island", "$1,700,000"), ("4929 E Pelican Dr", "Oak Island", "$1,285,000"),
        ("3609 Mason Port Dr", "Wilmington", "$870,000"), ("57 Pinewood Dr", "Carolina Shores", "$465,000"),
        ("584 Asphodel Dr SW", "Supply · Land", "$75,000")]
SERVICES = [("Residential", "Buying or selling a home, from first-time buyers to seven-figure beach houses."),
            ("Commercial", "Sales and lease negotiations for business owners and investors."),
            ("Investment", "Flips, rentals and the BRRRR method: Buy, Rehab, Rent, Refinance, Repeat."),
            ("Custom builds", "Build your dream home on your own lot or through an all-inclusive package.")]
COUNTIES = [("New Hanover", "Wilmington · Wrightsville Beach · Carolina Beach · Castle Hayne"),
            ("Brunswick", "Leland · Oak Island · Supply · Carolina Shores"),
            ("Pender", "Hampstead"), ("Onslow", "Sneads Ferry")]
# Exact lines from Jose's Zillow reviews
REVIEWS = [
  ("He is a hard core advocate for his clients and will fight for you to get exactly what you want.", "Annalee H.", "Bought in Carolina Beach"),
  ("Jose and his team went above and beyond throughout the entire process.", "Thomas Z.", "Bought in Carolina Shores"),
  ("From day one, Jose listened to our specific needs, and made things happen for us.", "Brandi & Kevin", "Bought in Castle Hayne"),
  ("He was super responsive and helped us remotely find the right place for us.", "Michael F.", "Out-of-state buyer · Oak Island"),
  ("Jose’s knowledge of our target area was invaluable.", "Charles K.", "Bought a beach house"),
  ("No detail slipped through the cracks.", "Santina M.", "First home · Sneads Ferry"),
  ("Not only did he find it but he helped create it! Not only did we find an amazing agent, but an amazing friend along the way.", "Thomas D.", "First-time buyer · Winnabow"),
  ("Thank you Jose for making my housing dreams come true.", "Berna S.", "Home buyer"),
]
LISTING_STEPS = ["Sign the listing agreement & go over your goals", "Price your home from recent sales near you",
  "Prep your home to show at its best", "Schedule the professional photographer", "Build your Zillow Showcase virtual tour & floor plan",
  "Create the MLS listing and review it with you", "Go live", "Coordinate & pre-qualify all showings",
  "Weekly updates with buyer feedback", "Pre-qualify every offer before presenting it", "Offer consultation & negotiate all offers",
  "Coordinate inspections, appraisal & repairs", "Coordinate attorney, lender & title", "Review the final numbers before closing", "Closing day: SOLD!"]
MARKETING = ["Pricing analysis from recent sales near you", "Professional photo shoot", "Zillow Showcase virtual tour",
  "Interactive floor plan", "Full MLS listing you review before it goes live", "Placement on Zillow, Realtor.com & Redfin",
  "Syndication to thousands of real estate sites", "“For sale” yard sign", "Social media posts & targeted ads",
  "“Just listed” campaign to my database", "Outreach to top local buyer agents", "Property flyers",
  "Pre-qualified buyers only for private showings", "Open house on request", "Showing feedback from every buyer agent", "Weekly updates on your listing"]
BUYER_STEPS = ["Consultation: what you want, where, and your budget", "Get pre-approved with a trusted lender",
  "Search, including homes before they hit the internet", "Tour homes together, in person or by video",
  "Pull recent sales so you never overpay", "Write a strong offer & negotiate", "Due diligence: inspections, appraisal & repairs",
  "Coordinate lender, attorney & title", "Final walk-through", "Closing day: welcome home!"]
PROMISE_COMMON = ["I will always provide expert advice so you can make the best decision for yourself and your family.",
  "I will always give you the truth, regardless of the situation.", "I will always do what is right for your best interest."]
PROMISE = {
 "listing": [PROMISE_COMMON[0], "I will always be 100% forthcoming about your home’s price, condition and what it will take to sell.",
   PROMISE_COMMON[1], PROMISE_COMMON[2], "I will fight to get you the most for your home in the right amount of time.",
   "I will always use the most effective strategies to market your home.", "I will always communicate with you proactively.",
   "I will return your calls, emails and texts with urgency.", "I will spend every day working to find a qualified buyer for your home.",
   "I will make sure you understand every document before you sign it."],
 "buyer": [PROMISE_COMMON[0], "I will always be 100% forthcoming about price and terms, so your offer is the strongest it can be.",
   PROMISE_COMMON[1], PROMISE_COMMON[2], "I will fight to get you the most home for your dollar, and make sure you do not overpay.",
   "I will use every tool I have to find the right home, even before it hits the internet.", "I will always communicate with you proactively.",
   "I will return your calls, emails and texts with urgency.", "I will spend every day searching for your next home.",
   "I will make sure you understand every document before you sign it."],
}

def fp(p):  # file URL for local assets
    return "file://" + os.path.abspath(p)

CSS = f"""
@font-face{{font-family:IS;src:url('{fp('_build/fonts/instrument-serif-latin-400-normal.woff2')}');}}
@font-face{{font-family:IS;font-style:italic;src:url('{fp('_build/fonts/instrument-serif-latin-400-italic.woff2')}');}}
@font-face{{font-family:IN;font-weight:300;src:url('{fp('_build/fonts/Inter-Light.otf')}');}}
@font-face{{font-family:IN;font-weight:400;src:url('{fp('_build/fonts/Inter-Regular.otf')}');}}
@font-face{{font-family:IN;font-weight:500;src:url('{fp('_build/fonts/Inter-Medium.otf')}');}}
@font-face{{font-family:IN;font-weight:600;src:url('{fp('_build/fonts/Inter-SemiBold.otf')}');}}
@page{{size:8.5in 11in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--ink:#1c2a37;--deep:#15202b;--accent:#3a5165;--sand:#d8c39a;--cream:#f6efdd;--muted:#6b7682}}
body{{font-family:IN,sans-serif;font-size:10pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:8.5in;height:11in;position:relative;overflow:hidden;padding:.75in .7in .9in;page-break-after:always}}
.dark{{background:var(--ink);color:#e8edf1}} .light{{background:var(--cream);color:var(--ink)}}
h1,h2,h3{{font-family:IS,serif;font-weight:400;line-height:1.02;letter-spacing:-.01em}}
h2{{font-size:48pt;margin-bottom:14pt}} h3{{font-size:21pt;margin-bottom:4pt}}
em{{font-style:italic;color:var(--accent)}} .dark em,.cover em,.back em,.mission em{{color:var(--sand)}}
.eye{{font-size:7.5pt;letter-spacing:.26em;text-transform:uppercase;font-weight:600;color:var(--accent);margin-bottom:12pt}}
.dark .eye,.mission .eye{{color:var(--sand)}}
.lede{{font-size:12pt;max-width:6.4in;color:inherit;opacity:.85;margin-bottom:30pt}}
.foot{{position:absolute;left:.7in;right:.7in;bottom:.4in;display:flex;justify-content:space-between;font-size:6.5pt;letter-spacing:.22em;text-transform:uppercase;opacity:.55}}
/* cover */
.cover{{padding:0;color:#fff;background:var(--deep)}}
.cover .bg{{position:absolute;inset:0;background:url('{fp('images/stills/beach.jpg')}') center/cover;filter:saturate(.75)}}
.cover .sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(21,32,43,.55) 0%,rgba(21,32,43,.25) 35%,rgba(21,32,43,.9) 72%,rgba(21,32,43,1) 100%)}}
.cover .in{{position:absolute;inset:.55in .7in .6in;display:flex;flex-direction:column}}
.disc{{font-size:6pt;opacity:.6;text-align:center}}
.cover .logo{{width:2.1in;margin:.35in auto 0;filter:brightness(0) invert(1)}}
.cover h1{{font-size:56pt;margin-top:auto}}
.tag{{display:inline-block;margin-top:16pt;background:var(--sand);color:var(--ink);font-size:7pt;letter-spacing:.24em;text-transform:uppercase;font-weight:600;padding:6pt 11pt}}
.agent{{display:flex;align-items:center;gap:14pt;border-top:1px solid rgba(255,255,255,.25);margin-top:30pt;padding-top:20pt}}
.agent img{{width:.85in;height:.85in;border-radius:50%;object-fit:cover;object-position:top;border:2px solid var(--sand)}}
.agent b{{font-family:IS;font-weight:400;font-size:17pt;display:block}} .agent span{{font-size:8pt;opacity:.8}}
/* meet */
.meet{{display:grid;grid-template-columns:2.4in 1fr;gap:.4in}}
.meet .photo{{width:100%;height:3.7in;object-fit:cover;object-position:top;border-radius:10pt;border-bottom:4px solid var(--accent)}}
.side{{margin-top:14pt;display:grid;gap:9pt}}
.side div{{background:#fff;border-radius:8pt;padding:13pt 14pt;font-size:9.3pt;line-height:1.45}} .side b{{display:block;font-weight:600;font-size:10pt;margin-bottom:2pt}}
.meet h2{{font-size:48pt}} .meet p{{margin-bottom:14pt;font-size:11pt;line-height:1.65}}
.pull{{font-family:IS;font-style:italic;font-size:19pt;line-height:1.3;color:var(--accent);border-left:2px solid var(--accent);padding-left:14pt;margin:6pt 0 14pt}}
/* stats */
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:12pt;margin-bottom:28pt}}
.stat{{border:1px solid rgba(255,255,255,.14);border-radius:8pt;padding:16pt 16pt 14pt}}
.stat b{{font-family:IS;font-weight:400;font-size:32pt;white-space:nowrap;color:var(--sand);display:block;line-height:1;margin-bottom:6pt}} .stat span{{font-size:9pt;opacity:.75}}
.sold{{border-top:1px solid rgba(255,255,255,.18)}}
.sold div{{display:flex;justify-content:space-between;padding:11pt 0;border-bottom:1px solid rgba(255,255,255,.12);font-size:11pt;align-items:baseline}}
.sold span{{opacity:.6}} .sold b{{font-family:IS;font-weight:400;font-size:20pt;color:var(--sand)}}
/* services */
.svc{{display:grid;grid-template-columns:1fr 1fr;gap:14pt;margin-bottom:40pt}}
.svc div{{background:#fff;border-radius:10pt;padding:24pt 20pt 22pt;border-top:3px solid var(--accent)}} .svc p{{font-size:10.5pt;color:#3b4652}}
.cty div{{display:grid;grid-template-columns:1.4in 1fr;padding:15pt 0;border-bottom:1px solid rgba(28,42,55,.15);font-size:10.5pt;align-items:baseline}}
.cty b{{font-family:IS;font-weight:400;font-size:20pt}}
/* steps */
.steps{{display:grid;grid-template-columns:1fr 1fr;column-gap:.35in}}
.steps div{{display:flex;gap:10pt;align-items:baseline;padding:15pt 0;border-bottom:1px solid rgba(128,140,150,.28);font-size:10.5pt}}
.steps i{{font-family:IS;font-style:normal;font-size:20pt;color:var(--accent);min-width:26pt}} .dark .steps i{{color:var(--sand)}}
.steps div.last{{background:var(--sand);color:var(--ink);border-radius:5pt;padding:12pt 14pt;font-weight:600;border:0;margin-top:10pt}}
.steps div.last i{{color:var(--ink)}}
.steps.loose div{{padding:26pt 0}} .steps.tight div{{padding:10.5pt 0}}
/* promise */
.prom div{{display:flex;gap:14pt;padding:8pt 0;border-bottom:1px solid rgba(28,42,55,.1);font-size:10.5pt}}
.prom i{{font-family:IS;font-size:20pt;color:var(--accent);min-width:24pt;line-height:1}}
.mission{{margin-top:20pt;background:var(--ink);color:#e8edf1;border-radius:10pt;padding:24pt 26pt}}
.mission p{{font-size:10pt;opacity:.85}} .mission h3{{font-size:26pt;margin-bottom:6pt}}
/* reviews */
.rv{{columns:2;column-gap:12pt}}
.rv figure{{break-inside:avoid;background:#fff;border-radius:9pt;padding:18pt 18pt 16pt;margin-bottom:14pt;border-top:3px solid var(--accent)}}
.rv .st{{color:#c79a3a;font-size:8pt;letter-spacing:2pt}} .rv blockquote{{font-family:IS;font-style:italic;font-size:16.5pt;line-height:1.25;margin:7pt 0 10pt}}
.rv figcaption{{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}} .rv figcaption b{{color:var(--ink)}}
/* back */
.back{{padding:0;text-align:center;color:#fff;background:var(--deep)}}
.back .bg{{position:absolute;inset:0;background:url('{fp('images/stills/beach.jpg')}') center/cover;opacity:.28;filter:grayscale(.4)}}
.back .in{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 .8in}}
.back img.hs{{width:1.25in;height:1.25in;border-radius:50%;object-fit:cover;object-position:top;border:3px solid var(--sand);margin-bottom:22pt}}
.back h2{{font-size:60pt}} .back p{{font-size:10.5pt;line-height:1.8}} .back p b{{color:var(--sand);font-weight:500}}
.back .logo{{width:1.7in;margin-top:30pt;filter:brightness(0) invert(1);opacity:.9}}
.back .fine{{position:absolute;bottom:.45in;left:.8in;right:.8in;font-size:6.2pt;opacity:.55}}
"""

def foot(kind, n):
    return f'<div class="foot"><span>{NAME} · REALTOR® · {TEAM} · {BROKERAGE}</span><span>{kind} résumé · {n:02d}</span></div>'

def cover(kind):
    head = "Your home sold<br/>for <em>top dollar.</em>" if kind == "listing" else "Your next home,<br/>bought <em>right.</em>"
    return f'''<section class="pg cover"><div class="bg"></div><div class="sh"></div><div class="in">
<p class="disc">*If you are already working with a REALTOR®, please disregard this advertisement.</p>
<img class="logo" src="{fp('images/logo.png')}" alt=""/>
<p class="eye" style="margin-top:auto;margin-bottom:10pt">{"Listing" if kind=="listing" else "Buyer"} résumé</p>
<h1 style="margin-top:0">{head}</h1>
<div><span class="tag">Wilmington · The beaches · The Brunswick coast</span></div>
<div class="agent"><img src="{fp('images/headshot.jpg')}" alt=""/><div><b>{NAME}, REALTOR®</b><span>{PHONE} · {EMAIL}<br/>{TEAM} · {BROKERAGE}</span></div></div>
</div></section>'''

def meet(kind, n):
    return f'''<section class="pg light"><div class="meet">
<div><img class="photo" src="{fp('images/headshot.jpg')}" alt=""/>
<div class="side"><div><b>115+ transactions</b>Completed in just over three years across residential and commercial real estate.</div>
<div><b>Commercial expertise</b>Sales and lease negotiations for business owners and investors.</div>
<div><b>Investor &amp; builder</b>Flips and rentals through the BRRRR method, plus custom home builds.</div></div></div>
<div><p class="eye">Meet your agent</p><h2>{FIRST} <em>Lugo</em></h2>
<p>{NAME} is a real estate professional with a reputation for delivering exceptional results across both residential and commercial real estate. In just over three years, he has completed more than 115 successful transactions, from securing dream homes for buyers to achieving top-dollar sales for sellers.</p>
<p class="pull">Known on Zillow as “a hard core advocate for his clients.”</p>
<p>{FIRST}’s comprehensive knowledge of market trends, property valuation and investment strategy means every client gets tailored advice, whether it’s your first home or your fifth.</p>
<p>He works with {TEAM} at {BROKERAGE}, serving New Hanover, Pender, Brunswick and Onslow counties, from Sneads Ferry to Carolina Shores. His goal is simple: {"sell your home for the most money, in the right amount of time." if kind=="listing" else "find you the right home, at the right price, with confidence."}</p>
</div></div>{foot(kind, n)}</section>'''

def results(kind, n):
    stats = "".join(f'<div class="stat"><b>{b}</b><span>{s}</span></div>' for b, s in STATS)
    sold = "".join(f'<div><span style="opacity:1">{E(a)} <span>· {E(c)}, NC</span></span><b>{p}</b></div>' for a, c, p in SOLD)
    return f'''<section class="pg dark"><p class="eye">Résumé</p><h2>Results that <em>speak.</em></h2>
<p class="lede" style="margin-bottom:20pt">Real numbers from {FIRST}’s Zillow profile and closed sales.</p>
<div class="stats">{stats}</div>
<p class="eye">Recently sold</p><div class="sold">{sold}</div>{foot(kind, n)}</section>'''

def services(kind, n):
    svc = "".join(f'<div><h3>{t}</h3><p>{b}</p></div>' for t, b in SERVICES)
    cty = "".join(f'<div><b>{c}</b><span>{t}</span></div>' for c, t in COUNTIES)
    return f'''<section class="pg light"><p class="eye">What I do</p><h2>One agent for <em>every move.</em></h2>
<p class="lede">Whatever comes next, buying, selling, investing or building, you only need one number.</p>
<div class="svc">{svc}</div><p class="eye">Where I work</p><div class="cty">{cty}</div>{foot(kind, n)}</section>'''

def steps(items, loose=False):
    out = ""
    for i, s in enumerate(items, 1):
        out += f'<div{" class=\"last\"" if i == len(items) else ""}><i>{i:02d}</i><span>{E(s)}</span></div>'
    return f'<div class="steps{" loose" if loose else ""}">{out}</div>'

def process(kind, n):
    if kind == "listing":
        return f'''<section class="pg dark"><p class="eye">The listing process</p><h2>Fifteen steps to <em>sold.</em></h2>
<p class="lede">You always know what’s next, and I handle the details.</p>{steps(LISTING_STEPS)}{foot(kind, n)}</section>'''
    return f'''<section class="pg dark"><p class="eye">How buying works</p><h2>Your path to the <em>keys.</em></h2>
<p class="lede">I guide you through every step and handle the details, whether you’re local or moving from out of state.</p>{steps(BUYER_STEPS, True)}{foot(kind, n)}</section>'''

def marketing(kind, n):
    items = "".join(f'<div><i>{i:02d}</i><span>{s}</span></div>' for i, s in enumerate(MARKETING, 1))
    return f'''<section class="pg light"><p class="eye">Marketing plan of action</p><h2>Every buyer. <em>Every channel.</em></h2>
<p class="lede">Your home doesn’t just hit the MLS. Every listing gets professional photos and a Zillow Showcase virtual tour and floor plan, so buyers can walk through it from anywhere.</p>
<div class="steps tight">{items}</div>{foot(kind, n)}</section>'''

def promise(kind, n):
    items = "".join(f'<div><i>{i}</i><span>{E(s)}</span></div>' for i, s in enumerate(PROMISE[kind], 1))
    return f'''<section class="pg light"><p class="eye">My promise</p><h2>My commitments <em>to you.</em></h2>
<div class="prom">{items}</div>
<div class="mission"><p class="eye">Mission statement</p><h3>An agent <em>for life.</em></h3>
<p>It is my mission to provide an experience so positive that you’ll feel the trust, comfort and confidence of securing a real estate agent for life. Your best interest will always come first, because I’m dedicated to long-term relationships and earning the referrals of the people you care about most.</p></div>
{foot(kind, n)}</section>'''

def reviews(kind, n):
    cards = "".join(f'<figure><div class="st">★★★★★</div><blockquote>“{E(q)}”</blockquote><figcaption><b>{E(nm)}</b> · {E(d)}</figcaption></figure>' for q, nm, d in REVIEWS)
    return f'''<section class="pg light"><p class="eye">Past client testimonials · 5.0 on Zillow</p><h2>Don’t take my <em>word for it.</em></h2>
<div class="rv">{cards}</div>{foot(kind, n)}</section>'''

def back():
    return f'''<section class="pg back"><div class="bg"></div><div class="in">
<img class="hs" src="{fp('images/headshot.jpg')}" alt=""/><h2>Let’s go <em>home.</em></h2>
<p>Call or text <b>{PHONE}</b><br/>{EMAIL}<br/>{SITE}</p>
<img class="logo" src="{fp('images/logo.png')}" alt=""/>
<p style="font-size:7.5pt;opacity:.7;margin-top:10pt">{NAME}, REALTOR® · {TEAM} · {BROKERAGE}<br/>{ADDRESS}</p></div>
<p class="fine">*If you are already working with a REALTOR®, please disregard this advertisement. Equal Housing Opportunity.</p></section>'''

def doc(kind):
    if kind == "listing":
        parts = [cover(kind), meet(kind, 2), results(kind, 3), services(kind, 4), process(kind, 5), marketing(kind, 6), promise(kind, 7), reviews(kind, 8), back()]
    else:
        parts = [cover(kind), meet(kind, 2), results(kind, 3), process(kind, 4), services(kind, 5), promise(kind, 6), reviews(kind, 7), back()]
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'

OUT = {"listing": "Jose-Lugo-Listing-Resume.pdf", "buyer": "Jose-Lugo-Buyer-Resume.pdf"}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 816, "height": 1056}, device_scale_factor=2)
    for kind, out in OUT.items():
        tmp = f"/tmp/resume-{kind}.html"
        open(tmp, "w").write(doc(kind))
        pg.goto("file://" + tmp); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
        pg.pdf(path=out, width="8.5in", height="11in", print_background=True, prefer_css_page_size=True)
        pg.screenshot(path=f"images/resume-{kind}.png", clip={"x": 0, "y": 0, "width": 816, "height": 1056})
    b.close()
from PIL import Image
for kind in OUT:
    Image.open(f"images/resume-{kind}.png").convert("RGB").resize((816, 1056)).save(f"images/resume-{kind}.jpg", quality=86)
    os.remove(f"images/resume-{kind}.png")
print("built", ", ".join(OUT.values()))
