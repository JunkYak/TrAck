import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useFoods, useRecipes, useTemplates, useCreateLogEntry } from '../../api/nutrition';
import { useDebounce } from '../../../../hooks/useDebounce';
import { SelectionList } from './SelectionList';
import { buildFoodEntry, buildRecipeEntry } from '../../utils/nutritionCalculations';
import { flattenTemplateForLog } from '../../utils/templateCalculations';
import { FoodItemRead, RecipeRead, MealTemplateRead } from '../../types';

interface AddLogInlinePanelProps {
  date: string;
}

export const AddLogInlinePanel = ({ date }: AddLogInlinePanelProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [foodSearch, setFoodSearch] = useState('');
  const searchInputRef = useRef<HTMLInputElement>(null);
  const debouncedSearch = useDebounce(foodSearch, 300);
  
  // Independent API queries
  const { data: foods, isLoading: foodsLoading, isError: foodsError } = useFoods(debouncedSearch);
  const { data: recipes, isLoading: recipesLoading, isError: recipesError } = useRecipes();
  const { data: templates, isLoading: templatesLoading, isError: templatesError } = useTemplates();
  
  const createMutation = useCreateLogEntry();

  const handleSelectFood = (food: FoodItemRead) => {
    createMutation.mutate({ date, entry: buildFoodEntry(food) });
    searchInputRef.current?.focus();
  };

  const handleSelectRecipe = (recipe: RecipeRead) => {
    createMutation.mutate({ date, entry: buildRecipeEntry(recipe) });
    searchInputRef.current?.focus();
  };

  const handleSelectTemplate = (template: MealTemplateRead) => {
    createMutation.mutate({ date, entry: flattenTemplateForLog(template) });
    searchInputRef.current?.focus();
  };

  return (
    <div className="w-full mb-12">
      <div 
        className="w-full bg-[#1A1A1A] hover:bg-[#2A2A2A] transition-colors border border-[#2A2A2A] rounded-xl p-4 text-center cursor-pointer group"
        onClick={() => setIsExpanded(!isExpanded)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setIsExpanded(!isExpanded);
          }
        }}
      >
        <span className="text-amber-500 font-bold group-hover:text-amber-400">
          {isExpanded ? "Close Selection" : "+ Add To Today's Log"}
        </span>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div 
            initial={{ height: 0, opacity: 0, marginTop: 0 }}
            animate={{ height: 'auto', opacity: 1, marginTop: 16 }}
            exit={{ height: 0, opacity: 0, marginTop: 0 }}
            className="overflow-hidden"
          >
            <div className="flex flex-col lg:flex-row gap-4">
              <SelectionList<MealTemplateRead>
                title="Templates"
                data={templates}
                isLoading={templatesLoading}
                isError={templatesError}
                onSelect={handleSelectTemplate}
                renderItem={(t) => (
                  <div className="flex flex-col">
                    <span className="font-bold text-purple-400">{t.name}</span>
                    <span className="text-xs text-gray-500 mt-1">{t.foods.length + t.recipes.length} items</span>
                  </div>
                )}
              />
              <SelectionList<RecipeRead>
                title="Recipes"
                data={recipes}
                isLoading={recipesLoading}
                isError={recipesError}
                onSelect={handleSelectRecipe}
                renderItem={(r) => (
                  <div className="flex flex-col">
                    <span className="font-bold text-blue-400">{r.name}</span>
                    <span className="text-xs text-gray-500 mt-1">{r.ingredients.length} ingredients</span>
                  </div>
                )}
              />
              <div className="flex-1 min-w-[250px]">
                <div className="mb-4">
                  <input
                    ref={searchInputRef}
                    type="text"
                    value={foodSearch}
                    onChange={(e) => setFoodSearch(e.target.value)}
                    placeholder="Search foods database..."
                    className="w-full bg-[#1A1A1A] border border-[#2A2A2A] text-white p-2 rounded-lg outline-none focus:border-amber-500 transition-colors text-sm"
                  />
                </div>
                {!debouncedSearch ? (
                  <div className="p-4 bg-[#0A0A0A] border border-[#1A1A1A] rounded-xl text-center text-sm text-gray-500">
                    Start typing to search foods.
                  </div>
                ) : (
                  <SelectionList<FoodItemRead>
                    title="Foods"
                    data={foods}
                    isLoading={foodsLoading}
                    isError={foodsError}
                    onSelect={handleSelectFood}
                    renderItem={(f) => (
                      <div className="flex flex-col">
                        <span className="font-bold text-emerald-400">{f.name}</span>
                        <span className="text-xs text-gray-500 mt-1">{f.calories_per_unit} kcal / {f.unit}</span>
                      </div>
                    )}
                  />
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
