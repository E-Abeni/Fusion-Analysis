import { GoogleGenAI } from "@google/genai";
import { AppState } from '../types';

// Initialize the client. 
// Note: In a real scenario, ensure process.env.API_KEY is set. 
// We assume it is available per instructions.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });

export const auditConfiguration = async (configState: AppState): Promise<string> => {
  try {
    const model = 'gemini-2.5-flash';
    
    const prompt = `
      You are a senior AML/CTF Compliance Officer and Technical Auditor.
      Analyze the following configuration for a financial monitoring engine.
      
      Configuration Data:
      ${JSON.stringify({
        riskListsCount: configState.riskLists.length,
        activeRules: configState.analysisRules.filter(r => r.enabled).map(r => ({ name: r.name, params: r.parameters })),
        dbStatus: configState.dbConfig.status,
        kafkaStatus: configState.kafkaConfig.status
      }, null, 2)}

      Please provide a brief, professional audit report in Markdown format covering:
      1. **Coverage Gaps**: Are critical analysis methods (like Benford or Geo Risk) disabled?
      2. **Threshold Sensitivity**: Are the Z-Score or dormancy parameters standard for a general retail bank? Suggest tighter/looser values if needed.
      3. **Data Integrity**: Note if data sources are disconnected.
      
      Keep the tone professional, concise, and actionable. Limit to 300 words.
    `;

    const response = await ai.models.generateContent({
      model: model,
      contents: prompt,
    });

    return response.text || "Unable to generate audit report.";
  } catch (error) {
    console.error("Gemini Audit Error:", error);
    return "AI Audit service is currently unavailable. Please check your API Key configuration.";
  }
};

export const suggestRuleParameters = async (ruleName: string, description: string): Promise<string> => {
  try {
    const model = 'gemini-2.5-flash';
    const prompt = `
      For an AML transaction monitoring rule named "${ruleName}" (${description}), 
      suggest 3 sets of configuration parameters representing:
      1. Conservative (Low False Positive)
      2. Balanced (Standard)
      3. Aggressive (High Security)

      Return ONLY the suggestions as a bulleted list.
    `;

    const response = await ai.models.generateContent({
      model: model,
      contents: prompt,
    });
    return response.text || "No suggestions available.";
  } catch (e) {
    return "Could not fetch suggestions.";
  }
}
