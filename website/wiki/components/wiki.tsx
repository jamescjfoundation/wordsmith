import type { ReactNode } from 'react';

/** A key or shortcut: <Kbd>Ctrl</Kbd>+<Kbd>S</Kbd> */
export function Kbd({ children }: { children: ReactNode }) {
  return <kbd className="ws-kbd">{children}</kbd>;
}

const STATUS = {
  available: 'Available',
  'in-progress': 'In progress',
  planned: 'Planned',
} as const;

/** Marks how far along a feature is: <Status value="planned" /> */
export function Status({ value, children }: { value: keyof typeof STATUS; children?: ReactNode }) {
  return <span className={`ws-status ws-status-${value}`}>{children ?? STATUS[value]}</span>;
}
