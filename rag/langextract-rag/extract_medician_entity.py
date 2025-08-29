import langextract as lx

# Text with a medication mention
input_text = "Patient took 400 mg PO Ibuprofen q4h for two days."

# Define extraction prompt
prompt_description = "Extract medication information including medication name, dosage, route, frequency, and duration in the order they appear in the text."

# Define example data with entities in order of appearance
examples = [
    lx.data.ExampleData(
        text="Patient was given 250 mg IV Cefazolin TID for one week.",
        extractions=[
            lx.data.Extraction(extraction_class="dosage", extraction_text="250 mg"),
            lx.data.Extraction(extraction_class="route", extraction_text="IV"),
            lx.data.Extraction(extraction_class="medication", extraction_text="Cefazolin"),
            lx.data.Extraction(extraction_class="frequency", extraction_text="TID"),  # TID = three times a day
            lx.data.Extraction(extraction_class="duration", extraction_text="for one week")
        ]
    )
]

# result = lx.extract(
#     text_or_documents=input_text,
#     prompt_description=prompt_description,
#     examples=examples,
#     model_id="gemini-2.5-pro",
#     api_key="your-api-key-here"  # Optional if LANGEXTRACT_API_KEY environment variable is set
# )

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt_description,
    examples=examples,
    model_id="llama3:latest",  # Automatically selects Ollama provider
    model_url="http://localhost:11434",
    fence_output=False,
    use_schema_constraints=False
)

# Display entities with positions
print(f"Input: {input_text}\n")
print("Extracted entities:")
for entity in result.extractions:
    position_info = ""
    if entity.char_interval:
        start, end = entity.char_interval.start_pos, entity.char_interval.end_pos
        position_info = f" (pos: {start}-{end})"
    print(f"• {entity.extraction_class.capitalize()}: {entity.extraction_text}{position_info}")

# Save and visualize the results
lx.io.save_annotated_documents([result], output_name="medical_ner_extraction.jsonl", output_dir=".")

# Generate the interactive visualization
html_content = lx.visualize("medical_ner_extraction.jsonl")
with open("medical_ner_visualization.html", "w") as f:
    if hasattr(html_content, 'data'):
        f.write(html_content.data)  # For Jupyter/Colab
    else:
        f.write(html_content)

print("Interactive visualization saved to medical_ner_visualization.html")