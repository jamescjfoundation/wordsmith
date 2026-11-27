/* An app's state on a wiki page: its latest release and its downloads. Nothing here is typed
   into a page: it comes from website/data/ (see lib/releases.mjs), so a page changes when an app
   publishes a release, without an edit. */
import { appState, sizeWords } from '@/lib/releases.mjs';

type Slug = 'script' | 'manuscript' | 'book' | 'launcher';

/** The app's latest release as a small mark: "Version 1.0.0", or a link to its releases page before it has one. */
export function AppRelease({ app }: { app: Slug }) {
  const { release, state, words, releasesUrl } = appState(app);
  if (!release) return <a href={releasesUrl}>Releases page</a>;
  return (
    <a className={`ws-status ws-status-${state === 'released' ? 'available' : 'in-progress'}`} href={release.url}>
      {words.chip}
    </a>
  );
}

/** The app's downloads: one line per system, with the release's files once there is a release. */
export function Downloads({ app }: { app: Slug }) {
  const { app: about, release, words, releasesUrl, platforms } = appState(app);
  return (
    <div className="ws-downloads">
      <p>{words.download}</p>
      <ul>
        {platforms.map((platform) => (
          <li key={platform.id}>
            <strong>{platform.name}</strong> ({platform.detail}):{' '}
            {platform.files.length > 0 ? (
              platform.files.map((file, at) => (
                <span key={file.name}>
                  {at > 0 && ', '}
                  <a href={file.url}>{file.name}</a> ({sizeWords(file.size)})
                </span>
              ))
            ) : release ? (
              <>
                version {release.version} has no file for this system; see <a href={release.url}>the release</a>
              </>
            ) : (
              <a href={releasesUrl}>{about.name} releases</a>
            )}
          </li>
        ))}
      </ul>
      {release && (
        <p>
          <a href={release.url}>Every file of version {release.version}</a>, on GitHub.
        </p>
      )}
    </div>
  );
}
