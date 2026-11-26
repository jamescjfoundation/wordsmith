import defaultMdxComponents from 'fumadocs-ui/mdx';
import { Accordion, Accordions } from 'fumadocs-ui/components/accordion';
import { File, Files, Folder } from 'fumadocs-ui/components/files';
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';
import { Step, Steps } from 'fumadocs-ui/components/steps';
import { Tab, Tabs } from 'fumadocs-ui/components/tabs';
import type { MDXComponents } from 'mdx/types';
import { Kbd, Status } from './wiki';
import { AppRelease, Downloads } from './apps';
import { AppIcon, Wordmark } from '@/lib/brand';

/* Everything here can be used in any .mdx page without an import. */
export function getMDXComponents(components?: MDXComponents) {
  return {
    ...defaultMdxComponents,
    img: (props) => <ImageZoom {...(props as React.ComponentProps<typeof ImageZoom>)} />,
    Accordion,
    Accordions,
    File,
    Files,
    Folder,
    Step,
    Steps,
    Tab,
    Tabs,
    Kbd,
    Status,
    // an app's latest release and its downloads, from website/data/: <AppRelease app="script" />, <Downloads app="book" />
    AppRelease,
    Downloads,
    // the brand kit's app icons and wordmarks: <Card icon={<AppIcon app="wordsmith-script" />}>
    AppIcon,
    Wordmark,
    ...components,
  } satisfies MDXComponents;
}

export const useMDXComponents = getMDXComponents;

declare global {
  type MDXProvidedComponents = ReturnType<typeof getMDXComponents>;
}
