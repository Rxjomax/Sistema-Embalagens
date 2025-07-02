# Ficheiro: core/forms.py

from django import forms

class RequiredFieldsMixin:
    """
    Este Mixin percorre todos os campos de um formulário
    e adiciona um asterisco (*) ao label se o campo for obrigatório.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                # Adiciona o asterisco ao final do label existente
                field.label = f"{field.label} *"