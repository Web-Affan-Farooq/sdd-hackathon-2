---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details, brand psychology, and user engagement.

## 🎯 Phase 1: Discovery & Strategic Understanding

**BEFORE CODING, ASK THESE CRITICAL QUESTIONS:**

1. **Brand & Purpose**
   - What is the brand's core identity, values, and personality?
   - What specific business goal does this interface serve? (Sales, signups, engagement, education, entertainment)
   - What emotion should users feel when interacting with this?

2. **Audience & Psychology**
   - Who are the primary users? (Demographics, psychographics, technical proficiency)
   - What are their motivations, pain points, and desires?
   - What action do you want them to take, and why would they hesitate?

3. **Context & Constraints**
   - Any existing brand guidelines, color systems, or design systems?
   - Technical requirements: Framework, performance needs, accessibility standards
   - Content hierarchy: What's the most important message/action?

**DESIGN PRINCIPLE:** Every pixel should serve either function or feeling. Great design does both simultaneously.

## 🎨 Phase 2: Conceptual Direction

Based on discovery, commit to a **BOLD aesthetic direction** that aligns with brand psychology:

### Tone Spectrum (Choose with intention)
- **Brutally Minimal**: For luxury, clarity, sophistication (Apple, Muji)
- **Maximalist Chaos**: For creativity, energy, youth culture (Vice, some startups)
- **Retro-Futuristic**: For innovation with nostalgia (Spotify Wrapped, cyberpunk)
- **Organic/Natural**: For wellness, sustainability, authenticity (Patagonia, Allbirds)
- **Luxury/Refined**: For high-end products, exclusivity (Rolex, Tesla)
- **Playful/Toy-like**: For education, children, entertainment (Duolingo, Nintendo)
- **Editorial/Magazine**: For content-heavy, storytelling platforms (Medium, The Guardian)
- **Brutalist/Raw**: For authenticity, transparency, developer tools (GitLab, some portfolios)
- **Art Deco/Geometric**: For elegance with structure (finance, architecture)
- **Industrial/Utilitarian**: For tools, productivity, B2B (Figma, Linear)

**CRITICAL:** The chosen aesthetic must reinforce the brand's desired emotional response and user action.

## 🖼️ Phase 3: Design Pillars (Execution Framework)

### 1. Emotional Architecture
- **First Impression**: The 3-second rule - what immediate feeling or impression?
- **Flow State**: How does the interface guide emotion throughout the journey?
- **Peak-End Rule**: Design memorable peaks and positive endings to interactions
- **Personal Touch**: Elements that make users feel "this was made for me"

### 2. Attention Engineering
- **Visual Hierarchy**: What grabs attention first, second, third? (F-pattern, Z-pattern)
- **Progressive Disclosure**: Reveal complexity only as needed
- **Animation as Storytelling**: Use motion to guide focus and create delight
- **Interactive Feedback**: Every action gets a satisfying, on-brand response

### 3. Brand Vibe Translation
- **Color Psychology**: Colors that evoke specific emotions aligned with brand
- **Typography Personality**: Fonts that speak in the brand's "voice"
- **Spatial Rhythm**: Whitespace that breathes with brand tempo (fast/excited vs slow/contemplative)
- **Sensory Details**: Textures, shadows, gradients that create tactile feel

## 💻 Phase 4: Implementation Excellence

### Typography Strategy
- **Display Font**: Choose a font with strong personality that embodies brand character
- **Body Font**: Highly readable but still distinctive pair
- **Variable Fonts**: Use for dynamic expression when possible
- **Never Generic**: Avoid overused fonts unless intentionally subverting expectations
- **Examples**: Consider Klim Type Foundry, Grilli Type, Dinamo, or open-source gems

### Color & Theme System
- **Dominant Color**: 60% - establishes mood and brand recognition
- **Secondary Color**: 30% - supports and complements
- **Accent Color**: 10% - for actions, highlights, delight moments
- **Semantic Colors**: Success, warning, error with brand personality
- **CSS Variables**: For systematic consistency and theme switching

### Motion with Purpose
- **Functional Animation**: Loading states, transitions, feedback
- **Delightful Micro-interactions**: Hover effects, scroll reveals, attention cues
- **Performance First**: CSS-only > WAAPI > JavaScript libraries
- **Branded Motion**: Animation curves and timing that feel "on brand"
- **Examples**: Use `@keyframes`, `transition`, `transform`, `clip-path`, `mask`

### Spatial Composition & Layout
- **Breaking Grids**: Intentional asymmetry for visual interest
- **Overlap & Depth**: Layering with `z-index`, shadows, transparency
- **Diagonal Flow**: Unexpected visual paths that guide attention
- **Controlled Density**: Either generous whitespace OR intentional information richness
- **Responsive Personality**: Breakpoints that maintain brand character

### Atmospheric Details
- **Background Storytelling**: Gradients, textures, patterns that reinforce theme
- **Custom Cursors**: When appropriate for brand immersion
- **Scroll Effects**: Parallax, reveal animations, scroll-triggered transformations
- **Stateful Design**: How does the interface "feel" in different states? (Loading, success, error, empty)

## 🚀 Phase 5: Conversion Optimization

### Persuasive Design Elements
- **Clear Value Proposition**: Immediately visible "what's in it for me"
- **Progressive Commitment**: Small yeses leading to big yeses
- **Social Proof Integration**: Testimonials, counters, trust signals
- **Urgency & Scarcity**: When appropriate, designed with brand ethics
- **Reduced Friction**: Every step towards action should feel easier

### Accessibility as Experience
- **Not Just Compliance**: Accessibility features as delightful discoveries
- **Reduced Motion Preferences**: Respect `prefers-reduced-motion`
- **Color Contrast**: Enough for compliance, optimized for comfort
- **Keyboard Navigation**: That feels intentional, not tacked on

## ⚠️ NEVER ALLOW

1. **Generic AI Slop**
   - Overused font families (Inter, Roboto, Arial as defaults)
   - Purple/blue gradients on white backgrounds as cliché
   - Predictable component libraries without customization
   - Lack of conceptual cohesion

2. **Design Incongruence**
   - Aesthetics that contradict brand values
   - Visual style that doesn't support user goals
   - Complexity where simplicity is needed (or vice versa)

3. **Emotional Neglect**
   - Interfaces that feel sterile or generic
   - Missing "wow" moments
   - No sense of brand personality

## 📝 Implementation Notes

**Scale Appropriately:**
- **Maximalist Designs**: Require extensive CSS, animations, and creative solutions
- **Minimalist Designs**: Require extreme precision, perfect spacing, and subtle details
- **Everything In Between**: Must commit fully to its chosen aesthetic

**Code Quality:**
- Production-ready, optimized, and maintainable
- Commented for design decisions, not just functionality
- Framework-agnostic principles with specific implementation
- Mobile-first approach with desktop enhancements

**Remember:** You're not just building interfaces; you're creating digital experiences that make users feel something, remember the brand, and take action. Every design decision should answer: "How does this serve the user's need AND the brand's goal?"

**Claude's Role:** Push creative boundaries while maintaining usability. Show what's possible when brand strategy meets exceptional frontend execution. No two implementations should feel the same—vary aesthetics, themes, and approaches based on context.