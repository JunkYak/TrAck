import { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import * as Dialog from '@radix-ui/react-dialog';
import { AnimatePresence, motion } from 'framer-motion';

const NAV_LINKS = [
  { name: 'Kitchen', path: '/nutrition/kitchen' },
  { name: 'Foods', path: '/nutrition/foods' },
  { name: 'Recipes', path: '/nutrition/recipes' },
  { name: 'Templates', path: '/nutrition/templates' },
];

export const NutritionWorkspaceLayout = () => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  return (
    <div className="flex h-screen bg-[#0A0A0A] text-white overflow-hidden">
      
      {/* DESKTOP SIDEBAR (Notion-style, hidden on mobile) */}
      <aside className="hidden lg:flex w-60 flex-col bg-[#0A0A0A] border-r border-[#1A1A1A]">
        <div className="p-6">
          <h2 className="text-lg font-bold text-amber-500 tracking-tight">trAck Nutrition</h2>
        </div>
        <nav className="flex-1 px-4 space-y-1">
          {NAV_LINKS.map((link) => (
            <NavLink
              key={link.name}
              to={link.path}
              className={({ isActive }) =>
                `block px-3 py-2 rounded-md transition-colors ${
                  isActive ? 'bg-[#1A1A1A] text-white' : 'text-gray-400 hover:text-white hover:bg-[#121212]'
                }`
              }
            >
              {link.name}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col relative bg-[#121212]">
        
        {/* MOBILE HEADER (Hidden on desktop) */}
        <header className="lg:hidden flex items-center h-16 px-4 border-b border-[#1A1A1A] bg-[#0A0A0A]">
          <button 
            onClick={() => setIsDrawerOpen(true)}
            className="p-2 text-gray-400 hover:text-white focus:outline-none"
            aria-label="Open menu"
          >
            {/* Hamburger Icon */}
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <span className="ml-4 font-bold text-amber-500">trAck Nutrition</span>
        </header>

        {/* WORKSPACE CONTENT (Kitchen, Foods, etc. render here) */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto p-4 lg:p-8">
            <Outlet />
          </div>
        </div>
      </main>

      {/* MOBILE DRAWER (Radix UI + Framer Motion) */}
      <Dialog.Root open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
        <AnimatePresence>
          {isDrawerOpen && (
            <Dialog.Portal forceMount>
              <Dialog.Overlay asChild>
                <motion.div 
                  className="fixed inset-0 bg-black/60 z-40 lg:hidden"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                />
              </Dialog.Overlay>
              <Dialog.Content asChild>
                <motion.div 
                  className="fixed inset-y-0 left-0 w-3/4 max-w-sm bg-[#0A0A0A] border-r border-[#1A1A1A] z-50 shadow-2xl lg:hidden flex flex-col"
                  initial={{ x: '-100%' }}
                  animate={{ x: 0 }}
                  exit={{ x: '-100%' }}
                  transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                >
                  <div className="p-6 flex justify-between items-center border-b border-[#1A1A1A]">
                    <Dialog.Title className="text-lg font-bold text-amber-500">Menu</Dialog.Title>
                    <Dialog.Close asChild>
                      <button className="text-gray-400 hover:text-white p-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </Dialog.Close>
                  </div>
                  <nav className="flex-1 p-4 space-y-2">
                    {NAV_LINKS.map((link) => (
                      <NavLink
                        key={link.name}
                        to={link.path}
                        onClick={() => setIsDrawerOpen(false)}
                        className={({ isActive }) =>
                          `block px-4 py-3 rounded-md transition-colors ${
                            isActive ? 'bg-[#1A1A1A] text-white font-medium' : 'text-gray-400 hover:text-white'
                          }`
                        }
                      >
                        {link.name}
                      </NavLink>
                    ))}
                  </nav>
                </motion.div>
              </Dialog.Content>
            </Dialog.Portal>
          )}
        </AnimatePresence>
      </Dialog.Root>

    </div>
  );
};
