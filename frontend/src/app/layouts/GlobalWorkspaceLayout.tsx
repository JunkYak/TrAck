import { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import * as Dialog from '@radix-ui/react-dialog';
import { AnimatePresence, motion } from 'framer-motion';

const NAV_GROUPS = [
  {
    title: 'Overview',
    links: [
      { name: 'Dashboard', path: '/dashboard' },
    ]
  },
  {
    title: 'Nutrition',
    links: [
      { name: 'Kitchen', path: '/nutrition/kitchen' },
      { name: 'Foods', path: '/nutrition/foods' },
      { name: 'Recipes', path: '/nutrition/recipes' },
      { name: 'Templates', path: '/nutrition/templates' },
    ]
  },
  {
    title: 'Health',
    links: [
      { name: 'Weight', path: '/health/weight' },
      { name: 'Measurements', path: '/health/measurements' },
    ]
  },
  {
    title: 'Training',
    links: [
      { name: 'Exercises', path: '/training/exercises' },
      { name: 'Cardio', path: '/training/cardio' },
    ]
  }
];

export const GlobalWorkspaceLayout = () => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  return (
    <div className="flex h-screen bg-[#0A0A0A] text-white overflow-hidden">
      
      {/* DESKTOP SIDEBAR */}
      <aside className="hidden lg:flex w-64 flex-col bg-[#0A0A0A] border-r border-[#1A1A1A] overflow-y-auto custom-scrollbar">
        <div className="p-6 sticky top-0 bg-[#0A0A0A] z-10 border-b border-[#1A1A1A] mb-4">
          <h2 className="text-xl font-black text-amber-500 tracking-tight flex items-center gap-2">
            <span className="text-2xl">⚡</span> trAck
          </h2>
        </div>
        <nav className="flex-1 px-4 space-y-6 pb-6">
          {NAV_GROUPS.map((group) => (
            <div key={group.title}>
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 px-3">{group.title}</h3>
              <div className="space-y-1">
                {group.links.map((link) => (
                  <NavLink
                    key={link.name}
                    to={link.path}
                    className={({ isActive }) =>
                      `block px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
                        isActive ? 'bg-[#1A1A1A] text-amber-500 shadow-sm' : 'text-gray-400 hover:text-white hover:bg-[#121212]'
                      }`
                    }
                  >
                    {link.name}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col relative bg-[#121212]">
        
        {/* MOBILE HEADER */}
        <header className="lg:hidden flex items-center h-16 px-4 border-b border-[#1A1A1A] bg-[#0A0A0A] shrink-0">
          <button 
            onClick={() => setIsDrawerOpen(true)}
            className="p-2 text-gray-400 hover:text-white focus:outline-none"
            aria-label="Open menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <span className="ml-4 font-black text-amber-500 flex items-center gap-2">
            <span>⚡</span> trAck
          </span>
        </header>

        {/* WORKSPACE CONTENT */}
        <div className="flex-1 overflow-y-auto custom-scrollbar relative">
          <div className="max-w-5xl mx-auto p-4 lg:p-8 min-h-full">
            <Outlet />
          </div>
        </div>
      </main>

      {/* MOBILE DRAWER */}
      <Dialog.Root open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
        <AnimatePresence>
          {isDrawerOpen && (
            <Dialog.Portal forceMount>
              <Dialog.Overlay asChild>
                <motion.div 
                  className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                />
              </Dialog.Overlay>
              <Dialog.Content asChild>
                <motion.div 
                  className="fixed inset-y-0 left-0 w-[80%] max-w-sm bg-[#0A0A0A] border-r border-[#1A1A1A] z-50 shadow-2xl lg:hidden flex flex-col overflow-hidden"
                  initial={{ x: '-100%' }}
                  animate={{ x: 0 }}
                  exit={{ x: '-100%' }}
                  transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                >
                  <div className="p-6 flex justify-between items-center border-b border-[#1A1A1A] shrink-0 bg-[#0A0A0A]">
                    <Dialog.Title className="text-xl font-black text-amber-500 flex items-center gap-2">
                      <span>⚡</span> trAck
                    </Dialog.Title>
                    <Dialog.Close asChild>
                      <button className="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-[#1A1A1A] transition-colors">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </Dialog.Close>
                  </div>
                  <nav className="flex-1 overflow-y-auto p-4 space-y-6 custom-scrollbar pb-10">
                    {NAV_GROUPS.map((group) => (
                      <div key={group.title}>
                        <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 px-4">{group.title}</h3>
                        <div className="space-y-1">
                          {group.links.map((link) => (
                            <NavLink
                              key={link.name}
                              to={link.path}
                              onClick={() => setIsDrawerOpen(false)}
                              className={({ isActive }) =>
                                `block px-4 py-3 rounded-lg transition-colors text-base font-medium ${
                                  isActive ? 'bg-[#1A1A1A] text-amber-500 shadow-sm' : 'text-gray-400 hover:text-white hover:bg-[#121212]'
                                }`
                              }
                            >
                              {link.name}
                            </NavLink>
                          ))}
                        </div>
                      </div>
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
