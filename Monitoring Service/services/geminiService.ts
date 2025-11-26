import { GoogleGenAI } from "@google/genai";
import { STR, Transaction, Customer } from '../types';

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });

export const analyzeSTR = async (str: STR, transaction: Transaction, customer: Customer): Promise<string> => {
  if (!process.env.API_KEY) {
    return "AI Analysis Unavailable: Missing API Key.";
  }

  try {
    const prompt = `
      You are a senior financial crime analyst. Analyze the following Suspicious Transaction Report (STR).
      
      Customer Context:
      - ID: ${customer.id}
      - Occupation: ${customer.occupation}
      - Risk Level: ${customer.riskLevel}
      - Region: ${customer.region}
      - Tags: ${customer.tags.join(', ')}

      Transaction Details:
      - Amount: ${transaction.amount} ${transaction.currency}
      - Type: ${transaction.type}
      - Destination: ${transaction.destinationCountry}
      - Flags Triggered: ${transaction.flags.join(', ')}
      
      Task:
      Provide a concise 3-sentence risk narrative explaining why this activity is suspicious based on the triggered flags (e.g., Benford's Law, Round Numbers, Structuring) and customer profile. Recommend an immediate action (e.g., Freeze, RFI, Dismiss).
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });

    return response.text || "Analysis generated no text.";
  } catch (error) {
    console.error("Gemini Analysis Error:", error);
    return "Error generating analysis. Please check system logs.";
  }
};