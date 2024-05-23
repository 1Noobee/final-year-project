import { OpenAI } from "@langchain/openai";
import {  } from "@langchain/core/outputs";

// Define callback functions
const callbacks = [
  {
    handleLLMStart: async (llm, prompts) => {
      console.log(JSON.stringify(llm, null, 2));
      console.log(JSON.stringify(prompts, null, 2));
    },
    handleLLMEnd: async (output) => {
      console.log(JSON.stringify(output, null, 2));
    },
    handleLLMError: async (err) => {
      console.error(err);
    },
  },
];

// Create a new instance of OpenAI with callbacks
const model = new OpenAI({ callbacks });

// Invoke the model with a prompt
model.invoke(
  "What would be a good company name for a company that makes colorful socks?"
).then((response) => {
  console.log(JSON.stringify(response, null, 2));
}).catch((error) => {
  console.error(error);
});
