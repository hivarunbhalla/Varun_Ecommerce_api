from django.dispatch import receiver   
from store.signals import order_created


# recevier( signal {for which signal this function should execute}, sender{from where this signal should be received})
@receiver(order_created)
def on_order_created(seders, **kwargs):
    # understanding how to connect multiple modules using signals
    # Here we are connecting 2 modules store and core
    print(kwargs['order'])