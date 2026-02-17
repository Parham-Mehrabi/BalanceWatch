from django import forms


from ledger.models import Transaction



class CreateTransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ["description", 'amount', "action", "occurred_at", "wallet"]


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': "input"
            })
        
        self.fields["amount"].widget.attrs.update({
            "min": 0,
            "step": 1000000
        })
        self.fields['wallet'].queryset = user.wallets.all()
        first_wallet = user.wallets.first()
        if first_wallet:
            self.fields['wallet'].initial = first_wallet

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero")
        return amount
    
