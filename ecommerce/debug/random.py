## TOOLS ##
from core.models import Order, Address, Payment, Refund

def get_random_instance(model, *args, **kwargs):

    if model == Address:
        choice = kwargs.get('choice', None)
        objs = model.objects.filter(address_type=choice)

    elif model == Payment and kwargs.get('relation', None) == 'Order':
        # OnetoOne relation between Order and Payment
        orders =  Order.objects.filter(payment__isnull=False)
        pks = [o.payment.pk for o in orders]
        objs = Payment.objects.exclude(pk__in=pks)

    elif model == Order and kwargs.get('relation', None) == 'Refund':
        # OnetoOne relation between Order and Refund
        refunds = Refund.objects.filter(order__isnull=False)
        pks = [r.order.pk for r in refunds]
        objs = Order.objects.exclude(pk__in=pks)

    else:
        objs = model.objects.all()
    

    if objs.count() == 0:
        return
    index = random.randint(0, objs.count()-1)
    keys = [m.pk for m in objs]

    return objs.filter(pk=keys[index]).first()


def random_text(text, max_length=None):
    res = ""
    if text == "t":
        res = lorem.text()
        res = re.sub("\.", "", res)

    if text == "uniq":
        # some text begins the same
        letters = string.ascii_lowercase
        res = ''.join(random.choice(letters) for i in range(max_length))
        res = re.sub("\.", "", res)        

    elif text == 'n' and max_length:
        res = str([random.randint(1, 9) for i in range(0, max_length)])
        res = re.sub("\[|\]|\,|\s", "", res)

    if max_length:
        return res[:max_length]
    return res