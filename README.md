# La Grifería — lagriferiapr.com

Static website for **La Grifería**, a craft beer bar located at Paseo Real Marina, Aguadilla, Puerto Rico. Served via GitHub Pages at [lagriferiapr.com](https://lagriferiapr.com).

---

## Architecture

Single-file static site — everything lives in `index.html` (HTML + CSS + JS inline). No build step, no dependencies, no framework. Deploy by pushing to `main`; GitHub Pages serves it automatically.

```
lagriferiapr.com/
├── index.html        # Entire site — markup, styles, scripts
├── CNAME             # GitHub Pages custom domain config
├── README.md
└── Fotos/            # All photography assets (~260 MB)
    ├── IMG_0145.jpg  # Hero flatlay — all dishes on wooden table
    ├── IMG_9683.jpg  # Hero BG — ocean terrace, blue sky (MAIN HERO)
    ├── IMG_9685.jpg  # Terraza exterior — used in "La Vista" pillar
    ├── IMG_9686.jpg  # Exterior angle — used in gallery
    ├── IMG_9748.jpg  # Dark stout being poured — tap closeup
    ├── IMG_9752.jpg  # Golden lager pour — used in "La Cerveza" pillar
    ├── IMG_9753.jpg  # (available, unused)
    ├── IMG_0146.jpg  # Wide gallery shot
    ├── IMG_0152-2.jpg # (available, unused)
    ├── IMG_9698.jpg  # (available, unused)
    ├── Cerveza/      # 11 beer photos — Camacho cans + pours
    ├── Fish Tacos/   # 5 photos
    ├── Chicken Wings/ # 5 photos
    ├── Dumplings/    # 5 photos
    ├── Tuna Tartar/  # 4 photos
    ├── calamares/    # 4 photos
    ├── Edamames/     # 4 photos
    ├── Papaya Salad/ # 5 photos
    └── Pad thai/     # 3 photos
```

---

## Design System

### Color Palette

| Token      | Value     | Usage                                      |
|------------|-----------|--------------------------------------------|
| `--navy`   | `#0B2545` | Primary dark, pillar overlays              |
| `--yellow` | `#F4C542` | Brand accent — matches physical signage    |
| `--ocean`  | `#1A5F8A` | Mid-tone blue (available, not yet used)    |
| `--dark`   | `#080E1A` | Page background, deepest dark              |
| `--cream`  | `#FAF7F2` | Primary text color                         |
| `--mist`   | `#8B9CAB` | Secondary/muted text                       |
| `--coral`  | `#E07B54` | Accent warm (available for future use)     |

The yellow (`#F4C542`) is the single most important brand color — it matches the physical yellow tile accent on the building exterior. All CTAs, labels, and highlights use it.

### Typography

| Role           | Font               | Weight      | Usage                         |
|----------------|--------------------|-------------|-------------------------------|
| Display/Impact | `Bebas Neue`       | 400         | Hero title, nav logo, ticker  |
| Elegant heads  | `Playfair Display` | 400, 700    | Section titles, card names    |
| Body           | `Inter`            | 300–600     | Paragraphs, labels, UI        |

Loaded from Google Fonts. The combination creates contrast: Bebas Neue gives raw energy (street/beach vibe), Playfair Display adds sophistication, Inter keeps body text readable.

### Spacing & Layout

- Desktop container: `padding: 0 4rem` on sections
- Mobile container: `padding: 0 1.5rem` on sections
- Section vertical padding: `6rem` desktop, `4rem` mobile
- Grid gap: `1.5px` (near-seamless) for the pillars and gallery grids
- Border radius: `4px` — subtle, not pill-shaped

---

## Sections

### 1. Nav
- Fixed, transparent on hero — transitions to `rgba(8,14,26,0.92)` with `backdrop-filter: blur(12px)` on scroll
- Logo: "La **Grifería**" in Bebas Neue, yellow accent on "Grifería"
- Mobile: hamburger → full-screen overlay menu
- CTA button: "Visítanos" → `#visita`

### 2. Hero
- Full-viewport (`100vh`) with `Fotos/IMG_9683.jpg` as background
- Gradient overlay: transparent top → `rgba(8,14,26,0.95)` bottom
- Text animates in with staggered `fadeUp` keyframes (0.3s, 0.5s, 0.7s, 0.9s delays)
- Background has a subtle zoom-out on load (`scale(1.05)` → `scale(1)` over 8s)
- Vertical scroll indicator bottom-right (hidden on mobile)

### 3. Ticker
- Full-width yellow band, black text, infinite horizontal scroll via CSS `animation: ticker`
- Content: Cerveza Artesanal · Frente al Mar · Aguadilla, PR · Cervezas Camacho · Buenas Vibras · Gastronomía Creativa
- To change speed: edit `animation: ticker 20s linear infinite` (lower = faster)

### 4. Nosotros (Pillars)
- 3-column grid with `aspect-ratio: 3/4` portrait cards
- Each pillar: photo with brightness/saturation filter, gradient overlay, numbered label (01/02/03), yellow line that animates width on hover
- Photos: IMG_9685 (Vista), IMG_9752 (Cerveza), IMG_0145 (Comida)
- Collapses to single column on mobile

### 5. Cervezas
- Dark section with amber radial glow effect
- 2-column layout: text left, image right
- Stacked image effect: main photo + accent photo (hidden on mobile)
- Beer style tags in pill-shaped outlined buttons
- To add/remove beer styles: edit `.cerveza-tags` span elements

### 6. Menú
- **El menú es vivo**: la sección `#menu` se pinta sola leyendo `cervezas-camacho.html` (la pantalla del televisor) y `menu-config.js` en cada visita. No hay carta escrita a mano en `index.html`.
- **Para cambiar la carta: edita `cervezas-camacho.html`, nunca `index.html`.** Nombre, descripción y precio de cada `.item`; secciones nuevas con un `.sec-title`.
- Qué cocina aparece la decide `HAY_COMIDA` en `menu-config.js` (`'chilea'` | `'chona'` | `'burger662'` | `false`), igual que en el televisor. Con `false` el website muestra solo bebidas.
- Un popup nuevo necesita dos cosas, o el nombre no enciende nada: su lámina en `cervezas-camacho.html` con el id `lamina-<nombre>`, y ese nombre en la lista de conocidos dentro de `cualPopup()` —está en `index.html` y en `cervezas-camacho.html`—. Si el nombre lleva dígitos, como `'burger662'`, la expresión que lee el config tiene que aceptarlos: `[A-Za-z0-9]+` y no `[A-Za-z]+`.
- Los precios **sí** se muestran — son los mismos del televisor.
- Si el fetch falla, el visitante ve una nota y nada más. No hay carta de respaldo: una copia escondida envejece mintiendo, que era el problema original.
- Contrato: no renombrar `.sec-title`, `.item`, `.item-name`, `.item-desc`, `.item-price`, `.col-inner` ni los ids `lamina-*` en `cervezas-camacho.html` sin actualizar el script del website (hay un aviso igual al inicio de ese archivo).
- Frescura: igual que el deploy de Pages (suele ser ~1 minuto) más el caché de Pages (hasta 10 minutos).

### 7. Galería
- CSS Grid, 4 columns desktop / 2 columns mobile
- Some items span 2 rows (`g-tall`) or 2 columns (`g-wide`) for visual rhythm
- Hover: `brightness(1)` + `scale(1.05)` on the image
- To swap photos: change the `src` attribute on any `<img>` inside `.galeria-grid`

### 8. Visítanos
- Side-by-side: info panel left, Google Maps embed right
- Map is styled with `filter: grayscale(1) invert(1)` to match the dark theme
- **The map embed URL is a placeholder** — replace with real embed from Google Maps → Share → Embed a map

### 9. Footer
- Three-column: brand name / copyright / nav links
- Collapses to stacked column on mobile

---

## Scroll Animations

All `.reveal` elements animate from `opacity: 0; transform: translateY(40px)` to visible when they enter the viewport. Powered by `IntersectionObserver` with `threshold: 0.12`.

Delay variants: `.reveal-delay-1` (0.1s), `.reveal-delay-2` (0.2s), `.reveal-delay-3` (0.3s), `.reveal-delay-4` (0.4s).

---

## GitHub Pages Setup

The site is served from the `main` branch root. GitHub Pages is configured with the custom domain in `CNAME`. DNS should point:

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
CNAME www lagriferiapr.com
```

---

## What Needs Updating

- [ ] **Hours** — verify exact current hours in the `#visita` section
- [ ] **Google Maps embed** — replace the placeholder iframe `src` with the real embed URL from Google Maps
- [ ] **Instagram/Facebook URLs** — verify handles are `lagriferiapr` on both platforms
- [ ] **Image optimization** — photos are 3–7 MB each; consider running through `squoosh` or `imagemagick` to compress for faster load. Target: <400 KB per image.
- [ ] **Unused photos** — `IMG_0152-2.jpg`, `IMG_9698.jpg`, `IMG_9753.jpg` are available but not used yet

---

## Common Edits

**Change a section background photo:**
Find the relevant `<img>` tag or `background-image` CSS and update the path.

**Change the menu:**
You don't edit it here. Edit `cervezas-camacho.html` (the TV screen file) — the website reads it on every visit. See section 6 for the contract.

**Change brand yellow:**
Update `--yellow: #F4C542;` in `:root`.

**Change hero photo:**
Update `background-image: url('Fotos/IMG_9683.jpg');` in `.hero-bg`.
