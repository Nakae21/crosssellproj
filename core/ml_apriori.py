import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from core.models import Order

def train_apriori_model():
    orders = Order.objects.all()
    transactions = []

    for order in orders:
        product_names = [p.name for p in order.products.all()]
        transactions.append(product_names)

    df = pd.DataFrame(transactions).fillna('')

    # One-hot encoding
    oht = pd.get_dummies(df.apply(pd.Series).stack()).sum(level=0)

    frequent_itemsets = apriori(oht, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    # Save rules or return them
    return rules
