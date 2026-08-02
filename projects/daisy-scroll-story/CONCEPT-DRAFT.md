# Daisy Maison Scroll Story — Concept Draft

Status: working homepage shop-window prototype in an unpublished draft theme.

## Draft theme

- Store: `daisymaisonuk.myshopify.com`
- Theme: `Codex - Scroll Story Concept - 20 Jul 2026`
- Theme ID: `203638636883`
- Role: unpublished
- Local source: `projects/daisy-scroll-story/theme`
- Preview: `https://daisymaisonuk.myshopify.com?preview_theme_id=203638636883`
- Editor: `https://daisymaisonuk.myshopify.com/admin/themes/203638636883/editor`
- Safety rule: never publish or modify the live theme as part of this concept.

## Working agreement

- This file is the single source of truth.
- Claude leads narrative, emotional arc, and copy critique through the Claude CLI.
- Codex orchestrates the work, generates visual explorations, and implements the Shopify prototype.
- No dedicated Scroll World skill will be installed yet. Reconsider only after the first successful prototype reveals a repeatable workflow.
- Stay concise during concept alignment; increase reasoning and generation effort only after Max approves the direction.

## Current hypothesis

Pilot a short, skippable, name-first scroll story for the Mr & Mrs street sign. Capture the customer's names before the cinematic sequence, carry those names through the visuals, and finish with an invisible handoff into the pre-filled live personaliser.

The product-page experiment is now secondary. The approved primary direction is a desktop homepage shop window that keeps commerce immediate while giving exploratory visitors a short, tactile brand experience.

## Homepage shop-window prototype

- Preview route: `https://daisymaison.co.uk/?view=shop-window`
- Template: alternate homepage template `index.shop-window`; the normal homepage template is unchanged.
- Existing header, search, navigation, announcement strip, footer, and mobile toolbar remain available.
- The first viewport presents three real leading products: On Your Wedding Day pebble picture, Mr & Mrs street sign, and Family pebble hanging heart.
- Each object is a native one-click link to its relevant collection, with a separate Shop all gifts route.
- Desktop uses one short native-scroll recomposition. It does not lock, scrub, or delay navigation.
- Mobile is a compact static shop window with all three collection routes visible together.
- Reduced-motion, coarse-pointer, save-data, and unsupported environments receive a static layout without the extra storytelling scroll distance.
- Shopify Liquid validation passes for the section and alternate homepage template.
- Visual checks completed at 1440 x 900 and 390 x 844; native links, responsive layout, scroll progress, and reduced-motion fallback were verified.
- Existing theme header scripts still emit compatibility errors because they assume optional header elements are present. No errors originate from the shop-window component.

## Approved direction

- Product: Mr & Mrs personalised street sign.
- Mood: romantic, tactile, quietly magical, and realistic.
- Quality bar: restrained pre-AI agency craft; no cartoonish AI spectacle.
- Traffic assumption: mobile-first and high-volume, with friction treated as the primary constraint.
- Core asset: reuse the approved exact SVG sign generator rather than approximating the product in generated imagery.
- Personalisation: the name inputs are visible above the fold and the exact SVG updates immediately.
- Responsive approach: one implementation and one narrative, with separately art-directed mobile and desktop compositions.
- Mobile: vertical, full-bleed, thumb-reachable inputs, and a sticky bottom CTA.
- Desktop: wider sign-and-input composition, generous whitespace, and restrained pointer-aware depth effects.
- Scene count: four. Additional scenes must earn their place through measurable product comprehension or conversion value.

## Four-scene spine

1. Hook: sign in a realistic romantic setting, with name inputs already visible.
2. Personalise: the approved exact SVG updates live; this is the primary magic moment.
3. Believe: craftsmanship, materials, scale, and compact real-world proof.
4. Buy: price, delivery confidence, and a direct handoff into purchase.

## Implementation snapshot

- Product route: `https://daisymaison.co.uk/products/mr-mrs-personalised-street-sign-gift?view=scroll-story`
- Template: alternate product template `product.scroll-story`; the normal product template is unchanged.
- The exact approved Mr & Mrs sign SVG is rendered inline and updates live from the surname and date inputs.
- One accessible, native-scroll implementation serves both breakpoints, with separately art-directed mobile and desktop layouts.
- Mobile keeps the surname input in the first viewport and provides a sticky purchase handoff.
- Desktop uses a cinematic split composition with a persistent product visual and a quieter editorial reading column.
- Four scenes are implemented: Hook, Personalise, Believe, and Buy.
- Reduced-motion preferences are respected and the experience does not hijack scrolling.
- Shopify Liquid validation passes for the new section, snippet, template, and font asset.
- Visual checks completed at 390 x 844 and 1440 x 900, including live name/date updates and sticky CTA behaviour.
- The draft currently reuses the existing product wedding photograph. Final art direction and any additional photography remain a later creative pass.
- Existing theme header scripts emit compatibility errors on the alternate view because they assume optional header elements are present. The story component remains functional; resolve this in the theme integration pass rather than coupling the prototype to hidden header markup.

## Draft structure for the creative pass

1. Product, audience, and one intended feeling.
2. Four concise scroll beats: input, reveal, craft, emotional setting/handoff.
3. Headline and supporting copy for each beat.
4. Visual and motion brief for each beat.
5. Mobile performance and accessibility limits.
6. Success criteria against the existing product page.

## Next approval

Review the working prototype for emotional tone, first-viewport clarity, and the desktop/mobile compositions before investing in final imagery or deeper motion.
