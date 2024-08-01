# Описание:

TextEvaluator использует модель AI-TQA Basic для оценки текста и определения наличия в нем плохих слов или выражений.

# Установка:

`pip install ai-tqa`

# Использование:

```python
from ai_tqa import TextEvaluator

evaluator = TextEvaluator()

text = "Привет, даун!"

result_with_detail = evaluator.evaluate_text(text, detail=True)
result_without_detail = evaluator.evaluate_text(text, detail=False)

print(f"Результат с деталями: {result_with_detail}, Плохие слова: {result_with_detail[1]}")
print(f"Результат без деталей: {result_without_detail}")
```

# Контрибьюторы:

- KroZen