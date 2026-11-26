// Types for releases.mjs, which is plain JavaScript so the tests can run it with Node alone.

export type ReleaseFile = { name: string; url: string; size: number; sha256?: string };

export type Release = {
  version: string;
  tag: string;
  date: string;
  url: string;
  prerelease: boolean;
  files: ReleaseFile[];
};

export type State = 'none' | 'preview' | 'released';

/** One app's data file, website/data/apps/<slug>.json */
export type AppData = {
  slug: string;
  order: number;
  name: string;
  repository: string;
  for: string;
  description: string;
  state: Record<State, Record<string, string>>;
  platforms: string[];
};

/** One entry of website/data/platforms.json: `files` is the pattern its release files' names match */
export type Platform = { id: string; name: string; detail: string; files: string };

export type AppState = {
  app: AppData;
  release: Release | null;
  state: State;
  /** the app's words for its state: chip, line, download */
  words: Record<string, string>;
  releasesUrl: string;
  platforms: { id: string; name: string; detail: string; files: ReleaseFile[] }[];
};

export function versionKey(version: string): [number, number, number];
export function stateOf(release: Pick<Release, 'version' | 'prerelease'> | null): State;
export function longDate(day: string): string;
export function sizeWords(size: number): string;
export function stateWords(app: Pick<AppData, 'state'>, release: Pick<Release, 'version' | 'date' | 'prerelease'> | null): Record<string, string>;
export function filesFor(release: Pick<Release, 'files'> | null, platform: Pick<Platform, 'files'>): ReleaseFile[];
export function appState(slug: string): AppState;
