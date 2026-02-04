'use client';

import { ThemeToggle } from './ThemeToggle';

export function Header() {
  return (
    <header className="h-16 border-b bg-card flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold">Welcome back!</h1>
      </div>
      <ThemeToggle />
    </header>
  );
}
