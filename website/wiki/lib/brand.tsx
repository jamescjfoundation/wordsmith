/* The brand kit's logos and icons, copied unchanged from brand/ into public/brand/ by
   scripts/brand.mjs. Plain <img>: next/image would need a loader for a static export. */
/* eslint-disable @next/next/no-img-element */

// public/ files are served under the base path; brand files keep the kit's folder names
const base = '/wiki/brand';

export const apps = {
  'wordsmith-script': { name: 'Wordsmith Script', section: 'script' },
  'wordsmith-manuscript': { name: 'Wordsmith Manuscript', section: 'manuscript' },
  'wordsmith-book': { name: 'Wordsmith Book', section: 'book' },
} as const;

export type Brand = 'wordsmith-and-ink' | keyof typeof apps;

/** The app for a wiki section ("script" → "wordsmith-script"), if the section is an app's */
export function appForSection(section: string | undefined): keyof typeof apps | undefined {
  return (Object.keys(apps) as (keyof typeof apps)[]).find((key) => apps[key].section === section);
}

export const brandUrl = {
  favicon: (brand: Brand) => `${base}/${brand}/app-icon/favicon.svg`,
  icon: (brand: Brand) => `${base}/${brand}/app-icon/${brand}-icon.svg`,
  iconSmall: (brand: Brand) => `${base}/${brand}/app-icon/${brand}-icon-small.svg`,
  wordmark: (brand: Brand, ground: 'ink' | 'paper') => `${base}/${brand}/logo/${brand}-wordmark-${ground}.svg`,
};

/** The app icon. Below 48 px the kit's small version is used, as the brand guide asks. */
export function AppIcon({ app, size = 36 }: { app: Brand; size?: number }) {
  const src = size < 48 ? brandUrl.iconSmall(app) : brandUrl.icon(app);
  return <img className="ws-app-icon" src={src} alt="" width={size} height={size} />;
}

/** The wordmark: the ink version on light grounds, the paper version on dark ones. */
export function Wordmark({ brand, label, className }: { brand: Brand; label: string; className?: string }) {
  return (
    <span className={`ws-wordmark ${className ?? ''}`}>
      <img className="ws-on-light" src={brandUrl.wordmark(brand, 'ink')} alt={label} />
      <img className="ws-on-dark" src={brandUrl.wordmark(brand, 'paper')} alt="" aria-hidden="true" />
    </span>
  );
}
