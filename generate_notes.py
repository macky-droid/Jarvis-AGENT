#!/usr/bin/env python3
"""
Generates 25 realistic sample markdown notes for 'Solstice Craft Roastery & Artisan Lab'
into ./notes across 6 business categories with rich cross-references and [[wikilinks]].
"""
import os

NOTES = [
    # Operations
    (
        "operations/Espresso Calibration & Extraction.md",
        """# Espresso Calibration & Extraction

Daily morning dialing-in is the heartbeat of Solstice Roastery. Every barista on opening shift must pull three benchmark shots of our [[House Blend - Solar Flare]] before the front doors open at 6:30 AM.

### Parameter Baselines
- **Dose in**: 19.5g ± 0.1g into an 18g VST precision basket.
- **Yield out**: 40g liquid beverage weight (1:2.05 brew ratio).
- **Contact time**: 27 to 30 seconds under 8.5 bars of pressure.
- **Water temperature**: Calibrated to exactly 201.5°F via the [[La Marzocco Linea PB Maintenance]] PID settings.

Water mineral balance is critical to flavor separation; verify morning conductivity with the [[Reverse Osmosis Water Filtration]] meter. If total dissolved solids drift below 110 ppm, the espresso presents harsh citric acidity. Grinder burr clearance must be checked against [[Mahlkonig EK43 Grinder Alignment]] protocols whenever baristas notice channeling or flow variations exceeding three seconds. All calibration readings are logged into the shift ledger to support our [[Barista Apprenticeship Curriculum]] and ongoing [[Quality Control & Cupping Protocol]].
"""
    ),
    (
        "operations/Green Bean Sourcing & Direct Trade.md",
        """# Green Bean Sourcing & Direct Trade

Our procurement model prioritizes relationship-first sourcing with producer cooperatives across Huila (Colombia), Yirgacheffe (Ethiopia), and Santa Ana (El Salvador). We commit to minimum prices 45% above Fair Trade minimums to ensure regenerative farming practices and living wages.

### Current Green Portfolio
- **Colombia Finca El Paraiso**: Double anaerobic washed pink bourbon.
- **Ethiopia Worka Sakaro**: Natural process heirloom varieties with intense blueberry and jasmine notes. Used prominently in our [[Seasonal Maple Cardamom Latte]] and single-origin offerings.
- **Guatemala Antigua Finca Medina**: Washed Bourbon/Caturra, delivering the chocolate praline core of [[House Blend - Solar Flare]].

All shipments arrive in 69kg jute bags lined with GrainPro barrier film and are routed to [[Inventory Logistics & Storage]] under climate-controlled conditions. Samples from every lot undergo pre-shipment and arrival analysis following the [[Quality Control & Cupping Protocol]] before batch commitments are scheduled into [[Batch Roasting Profiles & Curves]].
"""
    ),
    (
        "operations/Batch Roasting Profiles & Curves.md",
        """# Batch Roasting Profiles & Curves

Roasting at Solstice balances thermodynamic precision with sensory intuition. We utilize the convection-dominant [[Loring S35 Kestrel Roaster]] to achieve clean, vibrant cup profiles with minimal environmental emissions.

### Roast Architecture Principles
1. **Charge Temperature**: 385°F at 70% burner output to establish early convective momentum.
2. **Turning Point (TP)**: Target 1:15 at 195°F.
3. **Dry End (Yellowing)**: 4:30 to 5:00 at 305°F. Maintain steady rate of rise (RoR) decline without flatlining.
4. **First Crack (FC)**: Typically initiated at 382°F (around 8:15). Reduce gas to 35% to prevent runaway temperatures.
5. **Development Time Ratio (DTR)**: 12.5% for filter roasts; 15.8% for the [[House Blend - Solar Flare]].

Post-roast degas duration dictates packaging workflows in [[Packaging & Compostable Pouch Costs]]. Every production roast curve is recorded via Cropster and reviewed against target benchmarks during the Friday session of our [[Quality Control & Cupping Protocol]].
"""
    ),
    (
        "operations/Quality Control & Cupping Protocol.md",
        """# Quality Control & Cupping Protocol

Sensory evaluation guarantees consistency across wholesale orders and our retail bar. Solstice adheres strictly to the Specialty Coffee Association (SCA) cupping protocol every Tuesday and Friday at 2:00 PM.

### Cupping Station Setup
- Ratio: 8.25g ground coffee to 150ml water at 200°F (93°C).
- Water source: Directly pulled from our [[Reverse Osmosis Water Filtration]] mineralized bypass loop (125 ppm TDS, 3 grain hardness).
- Grind size: Coarse grind calibrated on our designated [[Mahlkonig EK43 Grinder Alignment]] bench.

Tasting notes are recorded across fragrance, aroma, flavor, aftertaste, acidity, body, and balance. Any production batch scoring below 84 points is withheld from packaging and redirected to cold brew extraction via [[Cold Brew Steep Ratios]]. This data also guides farm feedback loops in [[Green Bean Sourcing & Direct Trade]] and training adjustments in the [[Barista Apprenticeship Curriculum]].
"""
    ),
    (
        "operations/Inventory Logistics & Storage.md",
        """# Inventory Logistics & Storage

Proper stewardship of raw green coffee and finished roasted stock prevents loss from humidity fluctuations and oxidation. Our 2,400 sq ft back-of-house storage warehouse is kept strictly at 65°F (18°C) and 55% relative humidity using dual industrial dehumidifiers.

### Inventory Thresholds & FIFO
- **Green Stock**: Minimum four-week buffer (approx. 24 bags) to absorb shipping port delays from [[Green Bean Sourcing & Direct Trade]].
- **Roasted Retail Goods**: No retail coffee bag sits past day 14 post-roast; older bags are transferred to bulk cold brew production in [[Cold Brew Steep Ratios]].
- **Packaging Materials**: Cardboard mailers and pouches tracked under [[Packaging & Compostable Pouch Costs]]. Re-order threshold is 2,000 units.

Weekly stock reconciliation connects directly to our [[POS System & Revenue Breakdown]] to spot shrinkage, waste margins, and track wholesale fulfillment velocity for [[Wholesale Partner Acquisition]].
"""
    ),

    # Recipes
    (
        "recipes/House Blend - Solar Flare.md",
        """# House Blend - Solar Flare

Solar Flare is Solstice's flagship medium-roast blend, engineered to deliver comforting chocolate sweetness with an uplifting citrus zest. It forms the foundation of all milk drinks pulled on the [[La Marzocco Linea PB Maintenance]] and accounts for 62% of all whole-bean retail transactions.

### Blend Composition
- **50% Colombia Huila Pink Bourbon** (Sweet stonefruit and cane sugar finish).
- **30% Guatemala Antigua Finca Medina** (Dark cacao, toasted almond, velvety body).
- **20% Ethiopia Worka Sakaro Washed** (Meyer lemon brightness, white florals).

Components are roasted individually using distinct roast recipes in [[Batch Roasting Profiles & Curves]] before being post-blended. Baristas dial this in daily under the [[Espresso Calibration & Extraction]] routine. It pairs harmoniously with steamed oat milk prepared under [[Oat Milk Microfoam Standards]] and is the primary subscription item in our [[Coffee Subscription Club Strategy]].
"""
    ),
    (
        "recipes/Cold Brew Steep Ratios.md",
        """# Cold Brew Steep Ratios

During warm weather months from May to September, cold brew comprises up to 35% of total beverage revenue. We brew in 50-gallon stainless steel infusion tanks fitted with 50-micron dual filtration screens.

### Formula & Immersion Process
- **Batch Size**: 25 lbs coarse ground coffee to 35 gallons filtered water from [[Reverse Osmosis Water Filtration]].
- **Grind Setting**: Setting 14 on the dedicated [[Mahlkonig EK43 Grinder Alignment]].
- **Steep Environment**: Walk-in cold room maintained at 38°F for 18 hours continuous slow extraction.

The resulting concentrate yields a rich, smooth body with low astringency, exhibiting notes of bakers chocolate and dried fig. Concentrate is cut 1:1 with chilled water for standard cold brew, or used as a key ingredient in signature drinks like our [[Seasonal Maple Cardamom Latte]]. Stock turns and keg volumes are tracked weekly in [[Inventory Logistics & Storage]].
"""
    ),
    (
        "recipes/Oat Milk Microfoam Standards.md",
        """# Oat Milk Microfoam Standards

Alternative milk drinks represent over 58% of our daily drink order volume. We partner exclusively with Minor Figures Barista Oat for its neutral acidity and stable foaming capabilities.

### Texturing Guidelines
1. Fill pitcher to bottom of spout indentation (approx 6.5 oz for 10 oz cup).
2. Purge steam wand on the [[La Marzocco Linea PB Maintenance]] before inserting nozzle tip 0.5 cm below milk surface.
3. Aerate for the first 2-3 seconds until pitcher feels lukewarm (approx 95°F), then submerge tip to initiate rapid vortex rolling.
4. Shut steam off at 138°F; thermal inertia will carry milk to target 142°F. Never exceed 148°F or oat starches break down into chalky paste.

Microfoam must present wet paint gloss with zero visible air bubbles. Mastering this silky microfoam is Module 3 of our [[Barista Apprenticeship Curriculum]], essential for pouring intricate latte art that reinforces our [[Instagram & Visual Brand Identity]].
"""
    ),
    (
        "recipes/Seasonal Maple Cardamom Latte.md",
        """# Seasonal Maple Cardamom Latte

Our autumn and winter signature beverage features house-crafted spiced syrup crafted from organic Grade-A Vermont amber maple syrup, green cardamom pods, and Ceylon cinnamon quills.

### Syrup Preparation (Weekly 4-Liter Batch)
- 2000ml pure maple syrup heated to 185°F.
- 120g cracked cardamom pods toasted for 3 minutes.
- Simmer 45 minutes; strain through fine chinoise.

### Drink Assembly (12 oz Serving)
- Double shot (40g espresso) of [[House Blend - Solar Flare]] pulled per [[Espresso Calibration & Extraction]].
- 25g house cardamom maple syrup stirred directly into hot espresso.
- 8 oz oat milk textured to [[Oat Milk Microfoam Standards]].
- Garnished with freshly grated nutmeg and cardamom dust.

This beverage boasts an exceptional 78% gross margin, contributing heavily to our fall profitability reported in [[Q3 Operating Margin & Unit Economics]] and driving social engagement highlighted in [[Instagram & Visual Brand Identity]].
"""
    ),

    # Equipment
    (
        "equipment/Loring S35 Kestrel Roaster.md",
        """# Loring S35 Kestrel Roaster

The Loring S35 Kestrel is the mechanical nucleus of our roasting operations. Unlike conventional direct-fired drum roasters, the Loring utilizes a closed-loop single-burner cyclone system that recirculates heated process air.

### Key Operational Specs
- **Capacity**: 7kg to 35kg green coffee batch sizes.
- **Energy Efficiency**: Reduces greenhouse gas emissions and fuel consumption by approximately 80% compared to traditional afterburners.
- **Data Telemetry**: Modbus Ethernet integration streaming air temp, burner feedback, drum pressure, and RoR straight into our roast profiling software.

Routine preventative maintenance occurs every 100 roast hours: clean cyclone collection fins, vacuum chaff drum, and inspect pneumatic green loading hopper. Roaster reliability is paramount for hitting targets outlined in [[Batch Roasting Profiles & Curves]] and keeping pace with fulfillment demands from [[Wholesale Partner Acquisition]].
"""
    ),
    (
        "equipment/La Marzocco Linea PB Maintenance.md",
        """# La Marzocco Linea PB Maintenance

The 3-group Linea PB on our front bar is equipped with dual boiler architecture and integrated scales (ABR technology) that automate gravimetric espresso extraction.

### Preventative Maintenance Schedule
- **Daily Close**: Backflush each group with Cafiza detergent followed by clean water cycle; soak steam tips in milk cleanser.
- **Weekly**: Disassemble shower screens and dispersion screws; ultrasonic bath cleaning. Replace portafilter silicone gaskets every 90 days.
- **Quarterly**: Test boiler vacuum relief valves, inspect proportional solenoid valves, and recalibrate internal load cells using certified 100g calibration weights.

Scale accuracy is imperative for baristas executing [[Espresso Calibration & Extraction]]. Machine health also hinges on water feed purity maintained by our [[Reverse Osmosis Water Filtration]] system. Service costs are categorized under capital equipment upkeep in [[Q3 Operating Margin & Unit Economics]].
"""
    ),
    (
        "equipment/Mahlkonig EK43 Grinder Alignment.md",
        """# Mahlkonig EK43 Grinder Alignment

The Mahlkonig EK43 grinder is celebrated for its 98mm cast steel flat burrs, delivering exceptionally uniform particle size distribution with minimal fines generation.

### Burr Alignment Calibration
Burr parallel alignment must be checked monthly or whenever the dial indicates drift:
1. Thoroughly clean burr carrier with brass wire brush and isopropyl alcohol.
2. Apply whiteboard marker ink around the perimeter bevel of the fixed burr.
3. Reassemble, power on, and gently bring burrs to the chirp point.
4. Disassemble and examine marker rub pattern. If coverage is under 90%, shim low spots with food-grade aluminum foil tape (0.015mm).

Proper alignment reduces micro-channeling in espresso and improves extraction yields during [[Espresso Calibration & Extraction]] and batch cuppings in [[Quality Control & Cupping Protocol]]. Burr life is tracked in [[Inventory Logistics & Storage]] with replacement scheduled every 14,000 lbs.
"""
    ),
    (
        "equipment/Reverse Osmosis Water Filtration.md",
        """# Reverse Osmosis Water Filtration

Brewed coffee is 98.5% water, while espresso is nearly 90% water. City tap water varies heavily in seasonal chlorine and mineral hardness, making on-site water treatment indispensable.

### System Architecture
We run an OptiPure BWS350 reverse osmosis system paired with a blending precision bypass valve and calcite remineralization cartridge.
- **Target Total Dissolved Solids (TDS)**: 125 ppm.
- **Total Hardness**: 50 to 70 ppm CaCO3.
- **Total Alkalinity**: 40 to 45 ppm.
- **pH Target**: 7.2 to 7.4.

This custom water feeds the [[La Marzocco Linea PB Maintenance]], the cupping sink for [[Quality Control & Cupping Protocol]], and brewing tanks for [[Cold Brew Steep Ratios]]. Neglecting filter replacements leads to mineral scale buildup in boilers, risking expensive emergency downtime highlighted in [[Capital Expenditure - Roastery Expansion]].
"""
    ),

    # Marketing
    (
        "marketing/Coffee Subscription Club Strategy.md",
        """# Coffee Subscription Club Strategy

Our direct-to-consumer (DTC) subscription program creates predictable monthly recurring revenue (MRR) that cushions cash flow against seasonal cafe foot traffic dips.

### Subscription Tiers
1. **The Roaster's Flight ($36/mo)**: Two 250g bags of curated micro-lots, highlighting seasonal releases from [[Green Bean Sourcing & Direct Trade]].
2. **The Daily Ritual ($19/mo)**: Single 12oz bag of [[House Blend - Solar Flare]] shipped on the 1st or 15th.
3. **The Espresso Lab ($48/mo)**: 2lb whole bean bag optimized for home espresso enthusiasts.

Subscribers receive exclusive access to early harvest drops and discounts on merch promoted via [[Instagram & Visual Brand Identity]]. Fulfillment is batched every Monday morning from [[Inventory Logistics & Storage]], utilizing custom mailers from [[Packaging & Compostable Pouch Costs]]. Subscription MRR metrics are analyzed monthly in [[POS System & Revenue Breakdown]].
"""
    ),
    (
        "marketing/Instagram & Visual Brand Identity.md",
        """# Instagram & Visual Brand Identity

Solstice's brand identity balances Nordic minimalist design with warm artisanal textures: charcoal black (#1A1A1E), raw kraft paper, and energetic golden amber (#F59E0B).

### Content Pillars
- **Behind the Flame**: High-speed macro video clips of first crack and roasting on the [[Loring S35 Kestrel Roaster]].
- **Barista Craftsmanship**: Pour-over slow pours and latte art created with [[Oat Milk Microfoam Standards]].
- **Origin Chronicles**: Farmer spotlight carousels highlighting harvest stories from [[Green Bean Sourcing & Direct Trade]].
- **Seasonal Releases**: Aesthetic lifestyle photography promoting specialty drinks like the [[Seasonal Maple Cardamom Latte]].

Instagram serves as our primary top-of-funnel discovery engine for new patrons visiting our cafe and tourists discovering our [[Local Farmers Market Popups]]. Visual identity consistency is reinforced across our packaging designed under [[Packaging & Compostable Pouch Costs]].
"""
    ),
    (
        "marketing/Local Farmers Market Popups.md",
        """# Local Farmers Market Popups

Every Saturday and Sunday from April through November, Solstice operates a 10x10 mobile coffee popup at the Downtown Greenmarket.

### Booth Configuration
- 2x 5-gallon nitro draft kegs dispensing chilled drinks from [[Cold Brew Steep Ratios]].
- Pour-over station featuring single-origin coffees from [[Green Bean Sourcing & Direct Trade]].
- Retail display showcasing bagged beans in [[Packaging & Compostable Pouch Costs]].

The popup generates $1,800 to $2,400 in weekend gross revenue, but more importantly, converts local market shoppers into permanent cafe regulars and newsletter subscribers for our [[Coffee Subscription Club Strategy]]. Staffing is handled by apprentices completing their rotation in the [[Barista Apprenticeship Curriculum]], with cashless square POS sync routing into [[POS System & Revenue Breakdown]].
"""
    ),
    (
        "marketing/Wholesale Partner Acquisition.md",
        """# Wholesale Partner Acquisition

Wholesale accounts represent 40% of roasted output by volume, supplying specialty cafes, boutique hotels, tech offices, and high-end bakeries across the metropolitan area.

### Value Proposition to Partners
- Discounted tiered pricing on [[House Blend - Solar Flare]] and seasonal filter roasts.
- Comprehensive staff training certified under our [[Barista Apprenticeship Curriculum]].
- Emergency loaner grinders and preventive tech support modeled after [[La Marzocco Linea PB Maintenance]].
- Roasting schedules synchronized with commercial deliveries through [[Batch Roasting Profiles & Curves]].

The sales pipeline is managed with an 8-week sales cadence: blind sample kits, followed by on-site cuppings using [[Quality Control & Cupping Protocol]], and concluding with cafe flow audits. Wholesale margins and credit lines are closely reviewed in [[Q3 Operating Margin & Unit Economics]].
"""
    ),

    # People
    (
        "people/Barista Apprenticeship Curriculum.md",
        """# Barista Apprenticeship Curriculum

Investing in our frontline staff lowers turnover and elevates guest hospitality. Every new hire completes a paid 6-week Barista Apprenticeship program before working unassisted peak shifts.

### Curriculum Modules
- **Week 1 - Seed to Cup**: Agronomy, washing processes, and origins covered in [[Green Bean Sourcing & Direct Trade]].
- **Week 2 - Espresso Foundation**: Dialing recipes, distribution tools, and [[Espresso Calibration & Extraction]].
- **Week 3 - Milk Chemistry**: Steam techniques and microfoam texture according to [[Oat Milk Microfoam Standards]].
- **Week 4 - Equipment Maintenance**: Daily cleaning routines for the [[La Marzocco Linea PB Maintenance]] and [[Mahlkonig EK43 Grinder Alignment]].
- **Week 5 - Sensory Calibration**: Palate development and participating in the [[Quality Control & Cupping Protocol]].
- **Week 6 - Hospitality & Speed**: Embodying our [[Customer Experience Philosophy]] during morning rushes.

Graduates receive a 10% wage bump and an embroidered apron, contributing to healthy labor retention noted in [[Weekly Shift Scheduling & Fair Wage]].
"""
    ),
    (
        "people/Weekly Shift Scheduling & Fair Wage.md",
        """# Weekly Shift Scheduling & Fair Wage

Solstice operates on a transparent certified living-wage model. Rather than relying on volatile tipping culture, we pay all retail baristas a base wage of $22.50/hour with an equalized tip pool distributed biweekly.

### Scheduling Tenets
- Shifts are published 3 weeks in advance via 7shifts to allow work-life predictability.
- Minimum 11 hours rest between closing and opening shifts (strict "no clopening" rule).
- Four-day work week (36 hours full-time) available upon completion of the [[Barista Apprenticeship Curriculum]].
- Daily floor rotation every two hours between bar, register, prep, and breaks to uphold standards in [[Health, Safety & Ergonomics]].

Labor costs represent 34% of gross revenue, a deliberate investment reflected in our [[Q3 Operating Margin & Unit Economics]]. Low turnover preserves our high-touch [[Customer Experience Philosophy]].
"""
    ),
    (
        "people/Customer Experience Philosophy.md",
        """# Customer Experience Philosophy

Specialty coffee has historically suffered from pretension. At Solstice, our core motto is: "Elevated Coffee, Unpretentious Hospitality."

### The Three Touchpoints of Service
1. **The Welcome (First 5 Seconds)**: Genuine eye contact and greeting as guests walk past the door, regardless of how long the line is.
2. **The Recommendation**: Guiding customers without condescension. When a guest asks for caramel syrup, warmly suggest our house-crafted [[Seasonal Maple Cardamom Latte]] or explain the natural sweetness in our [[House Blend - Solar Flare]].
3. **The Hand-off**: Calling names with warmth, serving drinks on wooden oak trays with custom tasting cards printed through our marketing budget in [[Instagram & Visual Brand Identity]].

Team members are empowered with a $15/day complimentary beverage buffer to replace any drink a customer doesn't love or surprise a stressed guest. This dedication builds the loyalty that powers our retail traffic in [[POS System & Revenue Breakdown]].
"""
    ),
    (
        "people/Health, Safety & Ergonomics.md",
        """# Health, Safety & Ergonomics

Barista repetitive strain injuries (RSI) from tamping, lifting heavy milk cases, and prolonged standing pose real operational risks if left unaddressed.

### Ergonomic Protocols
- **Automated Tamping**: Puqpress automated tamping units installed beside the [[La Marzocco Linea PB Maintenance]] eliminate wrist strain from manual tamping pressure.
- **Anti-Fatigue Flooring**: Gel-cushioned shock-absorbing floor mats installed behind all bar and roasting stations.
- **Lifting Guidelines**: Two-person lift mandatory for any green coffee jute bag over 50 lbs in [[Inventory Logistics & Storage]].
- **Hearing Protection**: Custom-molded earplugs provided for roastery personnel operating the [[Loring S35 Kestrel Roaster]].

Incident-free hours are monitored monthly by leadership and reviewed alongside staffing schedules in [[Weekly Shift Scheduling & Fair Wage]].
"""
    ),

    # Finance
    (
        "finance/Q3 Operating Margin & Unit Economics.md",
        """# Q3 Operating Margin & Unit Economics

Our Q3 financial performance showcased robust top-line growth driven by cafe retail volume, expansion of our [[Coffee Subscription Club Strategy]], and wholesale account additions via [[Wholesale Partner Acquisition]].

### Revenue & Cost Structure
- **Gross Revenue**: $218,400 (Retail Cafe 56%, Wholesale 28%, DTC Subscription 16%).
- **Cost of Goods Sold (COGS)**: 27.5% ($60,060), including green coffee sourced via [[Green Bean Sourcing & Direct Trade]] and milk/syrups.
- **Labor & Benefits**: 34.2% ($74,690), adhering to our [[Weekly Shift Scheduling & Fair Wage]].
- **Occupancy & Utilities**: 12.8% ($27,955), incorporating energy costs from running the [[Loring S35 Kestrel Roaster]].
- **Net Operating Margin (EBITDA)**: 16.4% ($35,815).

Healthy margins have provided the surplus cash reserves necessary to fund the upcoming [[Capital Expenditure - Roastery Expansion]] and absorb raw pouch price hikes detailed in [[Packaging & Compostable Pouch Costs]].
"""
    ),
    (
        "finance/Packaging & Compostable Pouch Costs.md",
        """# Packaging & Compostable Pouch Costs

As part of our commitment to environmental sustainability, 100% of Solstice retail coffee bags are certified home-compostable, made from multi-layer kraft paper and plant-derived PLA inner barriers.

### Cost Breakdown per Unit (12oz / 340g Retail Bag)
- Compostable printed gusseted pouch with degassing valve: $0.84.
- Custom adhesive label (matte stock, printed locally): $0.14.
- Total packaging cost per finished unit: $0.98.
- Shipping mailer (100% recycled unbleached corrugated box): $1.15.

While compostable bags cost $0.32 more per unit than standard plastic foil laminates, consumer response documented in [[Instagram & Visual Brand Identity]] and direct feedback from the [[Coffee Subscription Club Strategy]] demonstrate that customers gladly support the premium. Inventory order volumes are managed through [[Inventory Logistics & Storage]].
"""
    ),
    (
        "finance/POS System & Revenue Breakdown.md",
        """# POS System & Revenue Breakdown

We utilize Toast POS integrated with Shopify e-commerce to unify in-store cafe sales, mobile order-ahead, and wholesale invoicing into a centralized accounting stream.

### Monthly Sales Channel Distribution
- **In-Store Espresso & Filter Drinks**: 48% (Led by [[Espresso Calibration & Extraction]] and [[House Blend - Solar Flare]]).
- **Cold Beverages**: 22% (Driven heavily by [[Cold Brew Steep Ratios]] and iced signature specials).
- **Whole Bean Bags**: 18% (Retail store shelves & farmers market booths from [[Local Farmers Market Popups]]).
- **Pastries & Food Collaborations**: 12% (Locally sourced from partner artisan bakeries).

Average order value (AOV) in-store sits at $8.65, bolstered by upsells of the [[Seasonal Maple Cardamom Latte]]. Daily close reports reconcile against inventory usage recorded in [[Inventory Logistics & Storage]] and guide financial modeling in [[Q3 Operating Margin & Unit Economics]].
"""
    ),
    (
        "finance/Capital Expenditure - Roastery Expansion.md",
        """# Capital Expenditure - Roastery Expansion

To accommodate growing demand from [[Wholesale Partner Acquisition]] and the rapid growth of our [[Coffee Subscription Club Strategy]], Solstice is preparing for a major Phase 2 facility expansion in Q1 of next year.

### Projected CapEx Budget ($145,000 Total)
1. **Secondary Roaster Installation**: $85,000 deposit towards an additional high-capacity roaster to supplement the existing [[Loring S35 Kestrel Roaster]].
2. **Commercial Water Treatment Overhaul**: $18,000 for upgraded dual-membrane [[Reverse Osmosis Water Filtration]] infrastructure.
3. **Cupping Lab & Training Academy**: $22,000 for an amphitheater-style cupping room to host public workshops and scale the [[Barista Apprenticeship Curriculum]].
4. **Permits & Mechanical Engineering**: $20,000 for roaster ductwork venting and gas supply line upgrades.

Financing is structured with 50% retained cash reserves from our [[Q3 Operating Margin & Unit Economics]] and 50% low-interest SBA equipment loan financing.
"""
    )
]

def main():
    base_dir = "./notes"
    os.makedirs(base_dir, exist_ok=True)
    count = 0
    for rel_path, content in NOTES:
        full_path = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        count += 1
    print(f"Successfully generated {count} realistic notes into {base_dir}")

if __name__ == "__main__":
    main()
