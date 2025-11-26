import React from 'react';
import { ArrowRight, AlertCircle, CheckCircle2 } from 'lucide-react';
import { REQUIRED_ENGINE_FIELDS } from '../constants';
import { FieldMapping } from '../types';

interface FieldMapperProps {
  availableFields: string[];
  currentMappings: FieldMapping[];
  onMappingChange: (mappings: FieldMapping[]) => void;
}

export const FieldMapper: React.FC<FieldMapperProps> = ({ availableFields, currentMappings, onMappingChange }) => {
  
  const handleMap = (engineField: string, sourceField: string) => {
    const newMappings = [...currentMappings];
    const index = newMappings.findIndex(m => m.engineField === engineField);
    
    if (index >= 0) {
      newMappings[index] = { ...newMappings[index], sourceField };
    } else {
      // Basic type inference mock
      newMappings.push({
        engineField,
        sourceField,
        dataType: 'string',
        isRequired: true
      });
    }
    onMappingChange(newMappings);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
      <h3 className="text-lg font-semibold text-slate-800 mb-4">Field Schema Mapping</h3>
      <p className="text-sm text-slate-500 mb-6">
        Map the incoming data fields from your source to the required fields for the Analytic Engine.
        Green checkmarks indicate valid mappings.
      </p>

      <div className="space-y-4">
        {REQUIRED_ENGINE_FIELDS.map((req) => {
          const mapping = currentMappings.find(m => m.engineField === req.name);
          const isMapped = !!mapping?.sourceField;

          return (
            <div key={req.name} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg border border-slate-100 hover:border-blue-200 transition-colors">
              <div className="flex items-center space-x-4 w-1/3">
                <div className={`p-1.5 rounded-full ${isMapped ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                  {isMapped ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
                </div>
                <div>
                  <p className="font-medium text-slate-700 font-mono text-sm">{req.name}</p>
                  <p className="text-xs text-slate-400 uppercase">{req.type}</p>
                </div>
              </div>

              <ArrowRight className="text-slate-300" size={20} />

              <div className="w-1/3">
                <select
                  className="w-full bg-white border border-slate-300 text-slate-700 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
                  value={mapping?.sourceField || ''}
                  onChange={(e) => handleMap(req.name, e.target.value)}
                >
                  <option value="">Select Source Field...</option>
                  {availableFields.map(f => (
                    <option key={f} value={f}>{f}</option>
                  ))}
                </select>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
