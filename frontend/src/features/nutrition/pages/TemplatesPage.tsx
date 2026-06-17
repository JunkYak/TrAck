import { useState } from 'react';
import { useTemplates, useDeleteTemplate } from '../api/nutrition';
import { TemplateCard } from '../components/Templates/TemplateCard';
import { TemplateFormDialog } from '../components/Templates/TemplateFormDialog';
import { MealTemplateRead } from '../types';

export const TemplatesPage = () => {
  const { data: templates, isLoading, isError } = useTemplates();
  const deleteMutation = useDeleteTemplate();
  
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [templateToEdit, setTemplateToEdit] = useState<MealTemplateRead | null>(null);

  const handleCreateNew = () => {
    setTemplateToEdit(null);
    setIsDialogOpen(true);
  };

  const handleEdit = (template: MealTemplateRead) => {
    setTemplateToEdit(template);
    setIsDialogOpen(true);
  };

  const handleDelete = (e: React.MouseEvent, templateId: string) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this template?")) {
      deleteMutation.mutate(templateId);
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex h-full items-center justify-center text-red-500">
        Error loading templates.
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-black text-white mb-2">Meal Templates</h1>
          <p className="text-gray-400">Combine foods and recipes into reusable templates.</p>
        </div>
        <button
          onClick={handleCreateNew}
          className="bg-amber-500 hover:bg-amber-400 text-black font-bold px-6 py-3 rounded-xl transition-all shadow-[0_0_20px_rgba(245,158,11,0.2)] hover:shadow-[0_0_30px_rgba(245,158,11,0.4)]"
        >
          + Create Template
        </button>
      </div>

      {!templates || templates.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-12 bg-[#1A1A1A] border border-[#2A2A2A] rounded-2xl text-center">
          <div className="w-16 h-16 bg-[#2A2A2A] rounded-full flex items-center justify-center mb-4">
            <span className="text-2xl">📋</span>
          </div>
          <h3 className="text-xl font-bold text-white mb-2">No templates yet</h3>
          <p className="text-gray-400 mb-6 max-w-md">
            Create a template to quickly log your frequent meals. Templates can contain both individual foods and full recipes.
          </p>
          <button
            onClick={handleCreateNew}
            className="text-amber-500 font-bold hover:text-amber-400 transition-colors"
          >
            Create your first template →
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {templates.map(template => (
            <TemplateCard
              key={template.id}
              template={template}
              onClick={() => handleEdit(template)}
              onDeleteClick={(e) => handleDelete(e, template.id)}
            />
          ))}
        </div>
      )}

      <TemplateFormDialog
        isOpen={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        templateToEdit={templateToEdit}
      />
    </div>
  );
};
